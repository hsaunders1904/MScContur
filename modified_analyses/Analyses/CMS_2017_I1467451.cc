// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projection.hh"
#include "Rivet/Particle.hh"
#include "Rivet/Event.hh"
#include "Rivet/Projections/ChargedLeptons.hh"
#include "Rivet/Projections/DressedLeptons.hh"
#include "Rivet/Projections/IdentifiedFinalState.hh"
#include "Rivet/Projections/PromptFinalState.hh"
#include "Rivet/Projections/MissingMomentum.hh"

namespace Rivet {


  /// @brief Add a short analysis description here
  class CMS_2017_I1467451 : public Analysis {
  public:

    /// Constructor
    DEFAULT_RIVET_ANALYSIS_CTOR(CMS_2017_I1467451);

    /// Book histograms and initialise projections before the run
    void init() {

      double lepConeSize = 0.1;
      double lepMaxEta = 2.5;

      Cut lepton_cut   = (Cuts::abseta < lepMaxEta);

      // Initialise and register projections
      FinalState fs(-2.5,2.5,0.0*GeV);
      FinalState fsm(-5,5,0.0*GeV);
      addProjection(fs, "FS");
      addProjection(fsm, "FSM");

      ChargedLeptons charged_leptons(fs);
      IdentifiedFinalState photons(fs);
      photons.acceptIdPair(PID::PHOTON);

      PromptFinalState prompt_leptons(charged_leptons);
      prompt_leptons.acceptMuonDecays(true);
      prompt_leptons.acceptTauDecays(false);

      PromptFinalState prompt_photons(photons);
      prompt_photons.acceptMuonDecays(true);
      prompt_photons.acceptTauDecays(false);

      DressedLeptons dressed_leptons = DressedLeptons(prompt_photons, prompt_leptons, lepConeSize, lepton_cut, /*cluster*/ true, /*useDecayPhotons*/ true);
      addProjection(dressed_leptons, "DressedLeptons");

      MissingMomentum Met(fsm);
      addProjection(Met, "MET");

      // Book histograms
      histoPtH=bookHisto1D(1,1,1);
      histoXsec=bookHisto1D(2,1,1);

    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      const double weight = event.weight();

      Particles leptons = applyProjection<DressedLeptons>(event, "DressedLeptons").particlesByPt(10.0*GeV);

      if(leptons.size()<2) vetoEvent;
      if(leptons[0].momentum().pT()<20*GeV || leptons[1].momentum().pT()<10*GeV) vetoEvent;
      if(leptons[0].charge()==leptons[1].charge()) vetoEvent;
      if(abs(leptons[0].pdgId())==abs(leptons[1].pdgId())) vetoEvent;

      FourMomentum LL=(leptons[0].momentum()+leptons[1].momentum());

      if(LL.mass()<12*GeV) vetoEvent;
      if(LL.pT()<30*GeV) vetoEvent;

      FourMomentum EtMiss = applyProjection<MissingMomentum>(event,"MET").missingMomentum();
      FourMomentum P4H = LL+EtMiss;

      double dphi = deltaPhi(LL,EtMiss);

      double mT = sqrt(2*LL.pT()*EtMiss.pT()*(1-cos(dphi)));
      if (mT<50*GeV) vetoEvent;

      histoPtH->fill(min(P4H.pT(),199.),weight);
      histoXsec->fill(8000.,weight);
    }


    /// Normalise histograms etc., after the run
    void finalize() {

      scale(histoPtH,crossSection()/sumOfWeights());
      scale(histoXsec,(histoXsec->xMax()-histoXsec->xMin())*crossSection()/sumOfWeights());

    }


  private:

    Histo1DPtr histoPtH;
    Histo1DPtr histoXsec;   

  };


  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(CMS_2017_I1467451);

}
