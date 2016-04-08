// -*- C++ -*-
//
// FRModel.h is a part of Herwig - A multi-purpose Monte Carlo event generator
// Copyright (C) 2002-2013 The Herwig Collaboration
//
// Herwig is licenced under version 2 of the GPL, see COPYING for details.
// Please respect the MCnet academic guidelines, see GUIDELINES for details.
//
#ifndef HERWIG_FRModel_H
#define HERWIG_FRModel_H

// This is the declaration of the FRModel class.
#include "Herwig/Models/General/BSMModel.h"

namespace Herwig {
using namespace ThePEG;
using ThePEG::Constants::pi;

const Complex ii = Complex(0,1);

/** \ingroup Models
 *  
 *  This is the Herwig FRModel class which inherits from ThePEG 
 *  FeynRules Model class and implements additional FeynRules Model couplings, 
 *  access to vertices for helicity amplitude calculations etc.
 *
 *  @see BSMModel
 */
class FRModel: public BSMModel {

public:
  /// Default constructor
  FRModel();

public:

  /** @name Functions used by the persistent I/O system. */
  //@{
  /**
   * Function used to write out object persistently.
   * @param os the persistent output stream written to.
   */
  void persistentOutput(PersistentOStream & os) const;

  /**
   * Function used to read in object persistently.
   * @param is the persistent input stream read from.
   * @param version the version number of the object when written.
   */
  void persistentInput(PersistentIStream & is, int version);
  //@}

  /**
   * Write out a UFO param_card.dat that matches the configured values
   */
  void writeParamCard() const;

  /**
   * Standard Init function used to initialize the interfaces.
   */
  static void Init();

protected:
  virtual bool registerDefaultVertices() const { return false; }

public:

  /**
   * Pointers to the objects handling the vertices.
   */
  //@{


  double ZERO() const { return ZERO_; }
  double gAXm() const { return gAXm_; }
  double gVq() const { return gVq_; }
  double aEWM1() const { return aEWM1_; }
  double Gf() const { return Gf_; }
  double aS() const { return aS_; }
  double ymb() const { return ymb_; }
  double ymt() const { return ymt_; }
  double ymtau() const { return ymtau_; }
  double MZ() const { return MZ_; }
  double MTA() const { return MTA_; }
  double MT() const { return MT_; }
  double MB() const { return MB_; }
  double MH() const { return MH_; }
  double MXm() const { return MXm_; }
  double MY1() const { return MY1_; }
  double WZ() const { return WZ_; }
  double WW() const { return WW_; }
  double WT() const { return WT_; }
  double WH() const { return WH_; }
  double WY1() const { return WY1_; }
  double aEW() const { return aEW_; }
  double G() const { return G_; }
  double MW() const { return MW_; }
  double ee() const { return ee_; }
  double sw2() const { return sw2_; }
  double cw() const { return cw_; }
  double sw() const { return sw_; }
  double g1() const { return g1_; }
  double gw() const { return gw_; }
  double vev() const { return vev_; }
  double lam() const { return lam_; }
  double yb() const { return yb_; }
  double yt() const { return yt_; }
  double ytau() const { return ytau_; }
  double muH() const { return muH_; }

  //@}  
  
protected:
  
  /** @name Clone Methods. */
  //@{
  /**
   * Make a simple clone of this object.
   * @return a pointer to the new object.
   */
  virtual IBPtr clone() const;

  /** Make a clone of this object, possibly modifying the cloned object
   * to make it sane.
   * @return a pointer to the new object.
   */
  virtual IBPtr fullclone() const;
  //@}
  
protected:

  /**
   * Initialize this object after the setup phase before saving and
   * EventGenerator to disk.
   * @throws InitException if object could not be initialized properly.
   */
  virtual void doinit();

  /**
   * Initialize this object. Called in the run phase just before
   * a run begins.
   */
  virtual void doinitrun();
  //@}

private:
  
  /** 
   * Private and non-existent assignment operator.
   */
  FRModel & operator=(const FRModel &);

private:

  /**
   *  Helper functions for doinit
   */
  //@{


  //@}
  
private:

  /**
   * Pointers to the vertices for FRModel Model helicity amplitude
   * calculations.
   */
  //@{


  double ZERO_;
  double gAXm_;
  double gVq_;
  double aEWM1_;
  double Gf_;
  double aS_;
  double ymb_;
  double ymt_;
  double ymtau_;
  double MZ_;
  double MTA_;
  double MT_;
  double MB_;
  double MH_;
  double MXm_;
  double MY1_;
  double WZ_;
  double WW_;
  double WT_;
  double WH_;
  double WY1_;
  double aEW_;
  double G_;
  double MW_;
  double ee_;
  double sw2_;
  double cw_;
  double sw_;
  double g1_;
  double gw_;
  double vev_;
  double lam_;
  double yb_;
  double yt_;
  double ytau_;
  double muH_;
  //@}
};

}

namespace ThePEG {
  ThePEG_DECLARE_POINTERS(Herwig::FRModel,HwFRModelPtr);
}


#endif /* HERWIG_FRModel_H */
