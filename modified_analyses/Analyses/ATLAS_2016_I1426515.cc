// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/IdentifiedFinalState.hh"
#include "Rivet/Projections/PromptFinalState.hh"
#include "Rivet/Projections/DressedLeptons.hh"
#include "Rivet/Projections/VetoedFinalState.hh"
#include "Rivet/Projections/VisibleFinalState.hh"

namespace Rivet {


  class ATLAS_2016_I1426515 : public Analysis {
  public:

    /// Constructor
    DEFAULT_RIVET_ANALYSIS_CTOR(ATLAS_2016_I1426515);


 public:

    /// Book histograms and initialise projections before the run
    void init() {

      const FinalState FS(Cuts::abseta < 4.5);

      /// @todo Initialise and register projections here
      // Project photons for dressing
      IdentifiedFinalState photon_id(FS);
      photon_id.acceptIdPair(PID::PHOTON);

      // Project dressed electrons with pT > 15 GeV and |eta| < 2.47
      PromptFinalState el_bare(FinalState(Cuts::abspid == PID::ELECTRON));
      Cut cuts = (Cuts::abseta < 2.47) && ( (Cuts::abseta <= 1.37) || (Cuts::abseta >= 1.52) ) && (Cuts::pT > 10*GeV);
      DressedLeptons el_dressed_FS(photon_id, el_bare, 0.1, cuts, true, true);
      declare(el_dressed_FS, "EL_DRESSED_FS");

      // Project dressed muons with pT > 15 GeV and |eta| < 2.5
      PromptFinalState mu_bare(FinalState(Cuts::abspid == PID::MUON));
      DressedLeptons mu_dressed_FS(photon_id, mu_bare, 0.1, Cuts::abseta < 2.4 && Cuts::pT > 15*GeV, true, true);
      declare(mu_dressed_FS, "MU_DRESSED_FS");

      Cut cuts_WW = (Cuts::abseta < 2.5) && (Cuts::pT > 20*GeV);
      IdentifiedFinalState lep_id(FS);
      lep_id.acceptIdPair(PID::MUON);
      lep_id.acceptIdPair(PID::ELECTRON);
      PromptFinalState lep_bare(lep_id);
      DressedLeptons leptons(photon_id, lep_bare, 0.1, cuts_WW, true, true);
      declare(leptons,"leptons");
     
      declare(FinalState(Cuts::abspid == PID::TAU || Cuts::abspid == PID::NU_TAU), "tau_id");
 
      // get MET from generic invisibles
      VetoedFinalState ivfs(FS);
      ivfs.addVetoOnThisFinalState(VisibleFinalState(FS));
      addProjection(ivfs, "InvisibleFS");

      // Project jets
      FastJets jets(FS, FastJets::ANTIKT, 0.4, JetAlg::NO_MUONS, JetAlg::NO_INVISIBLES);
      addProjection(jets, "jets");
       
      // integrated cross sections
      //d01 ee/mm fiducial integrated cross sections
      _hist_mm_fid_intxsec = bookHisto1D(1, 1, 1);
      _hist_ee_fid_intxsec = bookHisto1D(1, 1, 2);
      
      //d02 emme fiducial integrated cross sections
      _hist_emme_fid_intxsec = bookHisto1D(2, 1, 1);
      
      //d10  emme fiducial differential cross section (leading lepton ptlead + ptlead normalized)
      _hist_emme_fid_ptlead = bookHisto1D(10, 1, 1);
      _hist_emme_fid_ptleadnorm = bookHisto1D(10, 1, 2);

      //d11  emme fiducial differential cross section (dilepton-system ptll + ptll normalized)
      _hist_emme_fid_ptll = bookHisto1D(11, 1, 1);
      _hist_emme_fid_ptllnorm = bookHisto1D(11, 1, 2);
  
      //d12  emme fiducial differential cross section (dilepton-system mll + mll normalized)
      _hist_emme_fid_mll = bookHisto1D(12, 1, 1);
      _hist_emme_fid_mllnorm = bookHisto1D(12, 1, 2);
  
      //d13  emme fiducial differential cross section (dilepton-system delta_phi_ll + dphill normalized)
      _hist_emme_fid_dphill = bookHisto1D(13, 1, 1);
      _hist_emme_fid_dphillnorm = bookHisto1D(13, 1, 2);
  
      //d14  emme fiducial differential cross section (absolute rapidity of dilepton-system y_ll + y_ll normalized)
      _hist_emme_fid_yll = bookHisto1D(14, 1, 1);
      _hist_emme_fid_yllnorm = bookHisto1D(14, 1, 2);

      //d15  emme fiducial differential cross section (absolute costheta* of dilepton-system costhetastar_ll + costhetastar_ll normalized)
      _hist_emme_fid_costhetastarll = bookHisto1D(15, 1, 1);
      _hist_emme_fid_costhetastarllnorm = bookHisto1D(15, 1, 2);
       
    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      const double weight = event.weight();

      /// Find leptons
      const FinalState& ifs = apply<VetoedFinalState>(event, "InvisibleFS");
      const vector<DressedLepton>& leptons = apply<DressedLeptons>(event, "leptons").dressedLeptons();
      const vector<DressedLepton>& good_mu = apply<DressedLeptons>(event, "MU_DRESSED_FS").dressedLeptons();
      const vector<DressedLepton>& good_el = apply<DressedLeptons>(event, "EL_DRESSED_FS").dressedLeptons();
      const Jets& jets = applyProjection<FastJets>(event, "jets").jetsByPt(Cuts::pT>25*GeV && Cuts::abseta < 4.5);

      //taus are excluded from the fiducial cross section
      const Particles taus = applyProjection<FinalState>(event, "tau_id").particlesByPt(Cuts::pT>12.*GeV && Cuts::abseta < 3.0);
      if (taus.size())  vetoEvent;
      
      // remove events that do not contain 2 good leptons (either muons or electrons)
      if ((leptons.size() != 2) and ((good_el.size() != 1) or (good_mu.size() != 1)))  vetoEvent;

      // splitting in channels
      int channel = -1; // 1=mm, 2=ee;  3=emu; 4=mue
      if (good_mu.size() == 2)  channel = 1; //mm
      else if (good_el.size() == 2)  channel = 2; //ee
      else if (good_mu.size() == 1 && good_el.size() == 1 && good_el[0].pT() > good_mu[0].pT())  channel = 3; //emu
      else if (good_mu.size() == 1 && good_el.size() == 1 && good_el[0].pT() < good_mu[0].pT())  channel = 4; //mue

      const DressedLepton *lep1;
      const DressedLepton *lep2;

      // assign leptons
      if (channel==1) {
        if (good_mu[0].pT() > good_mu[1].pT()) {
          lep1 = &good_mu[0];
          lep2 = &good_mu[1];
        }
        else {
          lep1 = &good_mu[1];
          lep2 = &good_mu[0];
        }
      }
      else if (channel==2) {
        if (good_el[0].pT() > good_el[1].pT()) {
          lep1 = &good_el[0];
          lep2 = &good_el[1];
        }
        else {
          lep1 = &good_el[1];
          lep2 = &good_el[0];
        }
      }
      else if (channel==3 || channel==4) { //emu
        if (channel==3) {
          lep1 = &good_el[0];
          lep2 = &good_mu[0];
        } 
        else {	
          lep1 = &good_mu[0];
          lep2 = &good_el[0];
        }
      }
      else vetoEvent;

      if (lep1->pT() < 25*GeV || lep2->pT() < 20*GeV)  vetoEvent;
        
      Jets jets_selected;
      foreach (const Jet &j, jets) {
        if (j.abseta() > 4.5 && j.pT() <= 25*GeV )  continue;
        bool keep = true;
        foreach(DressedLepton el, good_el)  keep &= deltaR(j, el) >= 0.3;
        if (keep)  jets_selected += j;
      }
    
      /// define variables	
      FourMomentum met;
      foreach (const Particle& p, ifs.particles())  met += p.momentum();

      FourMomentum dilep =  (*lep1).momentum() + (*lep2).momentum();
      double ptll = dilep.pT()/GeV;
      double Mll = dilep.mass()/GeV;
      double Yll = dilep.absrap();    
      double DPhill = fabs(deltaPhi(*lep1, *lep2));
      double costhetastar = fabs(tanh((lep1->eta() - lep2->eta()) / 2));

      double DPhi_met = fabs(deltaPhi((*lep1), met));
      if (fabs(deltaPhi( (*lep2) , met)) < DPhi_met)  DPhi_met = fabs(deltaPhi((*lep2), met));
      if (DPhi_met > M_PI/2)  DPhi_met = 1.;
      else  DPhi_met = fabs(sin(DPhi_met));
 
      // Apply selections
      // mll lower cut (reject quarkonia)
      if ((channel == 1 || channel == 2) && Mll < 15.)  vetoEvent;
      else if (Mll < 10.)  vetoEvent;
    
      // Z veto (reject Z -- only dilepton channels)
      if ((channel == 1 || channel == 2) && abs(Mll - 91.1876) < 15.)  vetoEvent;       
    
      // Met rel cut
      if ((channel == 1 || channel == 2) && met.pT()*DPhi_met < 45*GeV)  vetoEvent;
      else if (met.pT()*DPhi_met < 15*GeV)  vetoEvent;

      // MET (pt-MET) cut
      if ((channel == 1 || channel == 2) && met.pT() <= 45*GeV)  vetoEvent; // begin MET cut
      else if (met.pT() <= 20*GeV)  vetoEvent; 

      if (jets_selected.empty()) { // 0 jets

        if (channel == 1)  _hist_mm_fid_intxsec->fill(1.0, weight);
        else if (channel == 2)  _hist_ee_fid_intxsec->fill(1.0, weight);
        else if (channel == 3 || channel == 4) {


          _hist_emme_fid_intxsec->fill(1.0, weight);

          _hist_emme_fid_ptlead->fill(lep1->pT()/GeV, weight);
          _hist_emme_fid_ptleadnorm->fill(lep1->pT()/GeV, weight);
             
          _hist_emme_fid_ptll->fill(ptll, weight);
          _hist_emme_fid_ptllnorm->fill(ptll, weight);
             
          _hist_emme_fid_mll->fill(Mll, weight);
          _hist_emme_fid_mllnorm->fill(Mll, weight);
             
          _hist_emme_fid_dphill->fill(DPhill, weight);
          _hist_emme_fid_dphillnorm->fill(DPhill, weight);
       
          _hist_emme_fid_yll->fill(Yll, weight);
          _hist_emme_fid_yllnorm->fill(Yll, weight);
         
          _hist_emme_fid_costhetastarll->fill(costhetastar, weight);
          _hist_emme_fid_costhetastarllnorm->fill(costhetastar, weight);
        }
      }
    }


    /// Normalise histograms etc., after the run
    void finalize() {

      /// @todo Normalise, scale and otherwise manipulate histograms here
      const double sf(crossSection()/femtobarn/sumOfWeights());

      scale(_hist_mm_fid_intxsec, sf);
      scale(_hist_ee_fid_intxsec, sf);
      scale(_hist_emme_fid_intxsec, sf);

      scale(_hist_emme_fid_ptlead, sf); 
      scale(_hist_emme_fid_ptll, sf); 
      scale(_hist_emme_fid_mll, sf); 
      scale(_hist_emme_fid_dphill, sf); 
      scale(_hist_emme_fid_yll, sf); 
      scale(_hist_emme_fid_costhetastarll, sf); 
      
      normalize(_hist_emme_fid_ptleadnorm);
      normalize(_hist_emme_fid_ptllnorm);
      normalize(_hist_emme_fid_mllnorm);
      normalize(_hist_emme_fid_dphillnorm);
      normalize(_hist_emme_fid_yllnorm);
      normalize(_hist_emme_fid_costhetastarllnorm);
    }


  private:

    //d01 ee/mm fiducial integrated cross sections
    Histo1DPtr _hist_mm_fid_intxsec;
    Histo1DPtr _hist_ee_fid_intxsec;

    //d02 emme fiducial integrated cross sections
    Histo1DPtr _hist_emme_fid_intxsec;
      
    //d10  emme fiducial differential cross section (leading lepton ptlead + ptlead normalized)
    Histo1DPtr _hist_emme_fid_ptlead;
    Histo1DPtr _hist_emme_fid_ptleadnorm;

    //d11  emme fiducial differential cross section (dilepton-system ptll + ptll normalized)
    Histo1DPtr _hist_emme_fid_ptll;
    Histo1DPtr _hist_emme_fid_ptllnorm;
  
    //d12  emme fiducial differential cross section (dilepton-system mll + mll normalized)
    Histo1DPtr _hist_emme_fid_mll;
    Histo1DPtr _hist_emme_fid_mllnorm;
  
    //d13  emme fiducial differential cross section (dilepton-system delta_phi_ll + dphill normalized)
    Histo1DPtr _hist_emme_fid_dphill;
    Histo1DPtr _hist_emme_fid_dphillnorm;
  
    //d14  emme fiducial differential cross section (absolute rapidity of dilepton-system y_ll + y_ll normalized)
    Histo1DPtr _hist_emme_fid_yll;
    Histo1DPtr _hist_emme_fid_yllnorm;

    //d15  emme fiducial differential cross section (absolute costheta* of dilepton-system costhetastar_ll + costhetastar_ll normalized)
    Histo1DPtr _hist_emme_fid_costhetastarll;
    Histo1DPtr _hist_emme_fid_costhetastarllnorm;
    //@}

  };

  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(ATLAS_2016_I1426515);

}
