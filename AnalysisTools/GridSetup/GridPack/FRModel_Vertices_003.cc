// -*- C++ -*-
//
// FRModelV_V_64.cc is a part of Herwig - A multi-purpose Monte Carlo event generator
// Copyright (C) 2002-2007 The Herwig Collaboration
//
// Herwig is licenced under version 2 of the GPL, see COPYING for details.
// Please respect the MCnet academic guidelines, see GUIDELINES for details.

#include "FRModel.h"
#include "ThePEG/Helicity/Vertex/Vector/FFVVertex.h"

#include "ThePEG/Utilities/DescribeClass.h"
#include "ThePEG/Persistency/PersistentOStream.h"
#include "ThePEG/Persistency/PersistentIStream.h"

namespace Herwig 
{
  using namespace ThePEG;
  using namespace ThePEG::Helicity;
  using ThePEG::Constants::pi;

  class FRModelV_V_51: public FFVVertex {
 public:
  FRModelV_V_51() {
    addToList(-5,5,22);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((-(ee*ii))/3.0)));
    right(((((1.0*(-ii))*1.0)*1.0)*((-(ee*ii))/3.0)));
    if(p1->id()!=-5) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
  }
  void persistentOutput(PersistentOStream & os) const { os << model_; }
  void persistentInput(PersistentIStream & is, int) { is >> model_; }
  //  static void Init();
 protected:
  IBPtr clone() const { return new_ptr(*this); }
  IBPtr fullclone() const { return new_ptr(*this); }
  void doinit() {
    model_ = dynamic_ptr_cast<tcHwFRModelPtr>
	     (generator()->standardModel());
    assert(model_);
    //    getParams(q2);
    
    
    orderInGem(1);
    orderInGs(0);
    FFVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_51 & operator=(const FRModelV_V_51 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_51,Helicity::FFVVertex>
describeHerwigFRModelV_V_51("Herwig::FRModelV_V_51",
				       "FRModel.so");
// void FRModelV_V_51::getParams(Energy2 ) {
// }

class FRModelV_V_52: public FFVVertex {
 public:
  FRModelV_V_52() {
    addToList(-1,1,21);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double G = model_->G();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*(ii*G)));
    right(((((1.0*(-ii))*1.0)*1.0)*(ii*G)));
    if(p1->id()!=-1) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
  }
  void persistentOutput(PersistentOStream & os) const { os << model_; }
  void persistentInput(PersistentIStream & is, int) { is >> model_; }
  //  static void Init();
 protected:
  IBPtr clone() const { return new_ptr(*this); }
  IBPtr fullclone() const { return new_ptr(*this); }
  void doinit() {
    model_ = dynamic_ptr_cast<tcHwFRModelPtr>
	     (generator()->standardModel());
    assert(model_);
    //    getParams(q2);
    
    
    orderInGem(0);
    orderInGs(1);
    FFVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_52 & operator=(const FRModelV_V_52 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_52,Helicity::FFVVertex>
describeHerwigFRModelV_V_52("Herwig::FRModelV_V_52",
				       "FRModel.so");
// void FRModelV_V_52::getParams(Energy2 ) {
// }

class FRModelV_V_53: public FFVVertex {
 public:
  FRModelV_V_53() {
    addToList(-3,3,21);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double G = model_->G();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*(ii*G)));
    right(((((1.0*(-ii))*1.0)*1.0)*(ii*G)));
    if(p1->id()!=-3) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
  }
  void persistentOutput(PersistentOStream & os) const { os << model_; }
  void persistentInput(PersistentIStream & is, int) { is >> model_; }
  //  static void Init();
 protected:
  IBPtr clone() const { return new_ptr(*this); }
  IBPtr fullclone() const { return new_ptr(*this); }
  void doinit() {
    model_ = dynamic_ptr_cast<tcHwFRModelPtr>
	     (generator()->standardModel());
    assert(model_);
    //    getParams(q2);
    
    
    orderInGem(0);
    orderInGs(1);
    FFVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_53 & operator=(const FRModelV_V_53 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_53,Helicity::FFVVertex>
describeHerwigFRModelV_V_53("Herwig::FRModelV_V_53",
				       "FRModel.so");
// void FRModelV_V_53::getParams(Energy2 ) {
// }

class FRModelV_V_54: public FFVVertex {
 public:
  FRModelV_V_54() {
    addToList(-5,5,21);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double G = model_->G();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*(ii*G)));
    right(((((1.0*(-ii))*1.0)*1.0)*(ii*G)));
    if(p1->id()!=-5) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
  }
  void persistentOutput(PersistentOStream & os) const { os << model_; }
  void persistentInput(PersistentIStream & is, int) { is >> model_; }
  //  static void Init();
 protected:
  IBPtr clone() const { return new_ptr(*this); }
  IBPtr fullclone() const { return new_ptr(*this); }
  void doinit() {
    model_ = dynamic_ptr_cast<tcHwFRModelPtr>
	     (generator()->standardModel());
    assert(model_);
    //    getParams(q2);
    
    
    orderInGem(0);
    orderInGs(1);
    FFVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_54 & operator=(const FRModelV_V_54 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_54,Helicity::FFVVertex>
describeHerwigFRModelV_V_54("Herwig::FRModelV_V_54",
				       "FRModel.so");
// void FRModelV_V_54::getParams(Energy2 ) {
// }

class FRModelV_V_55: public FFVVertex {
 public:
  FRModelV_V_55() {
    addToList(-2,1,24);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((ee*ii)/(sw*sqrt(2.0)))));
    right(0.0);
    if(p1->id()!=-2) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
  }
  void persistentOutput(PersistentOStream & os) const { os << model_; }
  void persistentInput(PersistentIStream & is, int) { is >> model_; }
  //  static void Init();
 protected:
  IBPtr clone() const { return new_ptr(*this); }
  IBPtr fullclone() const { return new_ptr(*this); }
  void doinit() {
    model_ = dynamic_ptr_cast<tcHwFRModelPtr>
	     (generator()->standardModel());
    assert(model_);
    //    getParams(q2);
    
    
    orderInGem(1);
    orderInGs(0);
    FFVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_55 & operator=(const FRModelV_V_55 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_55,Helicity::FFVVertex>
describeHerwigFRModelV_V_55("Herwig::FRModelV_V_55",
				       "FRModel.so");
// void FRModelV_V_55::getParams(Energy2 ) {
// }

class FRModelV_V_56: public FFVVertex {
 public:
  FRModelV_V_56() {
    addToList(-4,3,24);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((ee*ii)/(sw*sqrt(2.0)))));
    right(0.0);
    if(p1->id()!=-4) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
  }
  void persistentOutput(PersistentOStream & os) const { os << model_; }
  void persistentInput(PersistentIStream & is, int) { is >> model_; }
  //  static void Init();
 protected:
  IBPtr clone() const { return new_ptr(*this); }
  IBPtr fullclone() const { return new_ptr(*this); }
  void doinit() {
    model_ = dynamic_ptr_cast<tcHwFRModelPtr>
	     (generator()->standardModel());
    assert(model_);
    //    getParams(q2);
    
    
    orderInGem(1);
    orderInGs(0);
    FFVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_56 & operator=(const FRModelV_V_56 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_56,Helicity::FFVVertex>
describeHerwigFRModelV_V_56("Herwig::FRModelV_V_56",
				       "FRModel.so");
// void FRModelV_V_56::getParams(Energy2 ) {
// }

class FRModelV_V_57: public FFVVertex {
 public:
  FRModelV_V_57() {
    addToList(-6,5,24);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((ee*ii)/(sw*sqrt(2.0)))));
    right(0.0);
    if(p1->id()!=-6) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
  }
  void persistentOutput(PersistentOStream & os) const { os << model_; }
  void persistentInput(PersistentIStream & is, int) { is >> model_; }
  //  static void Init();
 protected:
  IBPtr clone() const { return new_ptr(*this); }
  IBPtr fullclone() const { return new_ptr(*this); }
  void doinit() {
    model_ = dynamic_ptr_cast<tcHwFRModelPtr>
	     (generator()->standardModel());
    assert(model_);
    //    getParams(q2);
    
    
    orderInGem(1);
    orderInGs(0);
    FFVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_57 & operator=(const FRModelV_V_57 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_57,Helicity::FFVVertex>
describeHerwigFRModelV_V_57("Herwig::FRModelV_V_57",
				       "FRModel.so");
// void FRModelV_V_57::getParams(Energy2 ) {
// }

class FRModelV_V_58: public FFVVertex {
 public:
  FRModelV_V_58() {
    addToList(-1,1,23);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    double cw = model_->cw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*(((-((cw*ee)*ii))/(2.0*sw))-(((ee*ii)*sw)/(6.0*cw)))));
    right(((((1.0*(-ii))*1.0)*1.0)*(((ee*ii)*sw)/(3.0*cw))));
    if(p1->id()!=-1) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
  }
  void persistentOutput(PersistentOStream & os) const { os << model_; }
  void persistentInput(PersistentIStream & is, int) { is >> model_; }
  //  static void Init();
 protected:
  IBPtr clone() const { return new_ptr(*this); }
  IBPtr fullclone() const { return new_ptr(*this); }
  void doinit() {
    model_ = dynamic_ptr_cast<tcHwFRModelPtr>
	     (generator()->standardModel());
    assert(model_);
    //    getParams(q2);
    
    
    orderInGem(1);
    orderInGs(0);
    FFVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_58 & operator=(const FRModelV_V_58 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_58,Helicity::FFVVertex>
describeHerwigFRModelV_V_58("Herwig::FRModelV_V_58",
				       "FRModel.so");
// void FRModelV_V_58::getParams(Energy2 ) {
// }

class FRModelV_V_59: public FFVVertex {
 public:
  FRModelV_V_59() {
    addToList(-3,3,23);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    double cw = model_->cw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*(((-((cw*ee)*ii))/(2.0*sw))-(((ee*ii)*sw)/(6.0*cw)))));
    right(((((1.0*(-ii))*1.0)*1.0)*(((ee*ii)*sw)/(3.0*cw))));
    if(p1->id()!=-3) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
  }
  void persistentOutput(PersistentOStream & os) const { os << model_; }
  void persistentInput(PersistentIStream & is, int) { is >> model_; }
  //  static void Init();
 protected:
  IBPtr clone() const { return new_ptr(*this); }
  IBPtr fullclone() const { return new_ptr(*this); }
  void doinit() {
    model_ = dynamic_ptr_cast<tcHwFRModelPtr>
	     (generator()->standardModel());
    assert(model_);
    //    getParams(q2);
    
    
    orderInGem(1);
    orderInGs(0);
    FFVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_59 & operator=(const FRModelV_V_59 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_59,Helicity::FFVVertex>
describeHerwigFRModelV_V_59("Herwig::FRModelV_V_59",
				       "FRModel.so");
// void FRModelV_V_59::getParams(Energy2 ) {
// }

class FRModelV_V_60: public FFVVertex {
 public:
  FRModelV_V_60() {
    addToList(-5,5,23);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    double cw = model_->cw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*(((-((cw*ee)*ii))/(2.0*sw))-(((ee*ii)*sw)/(6.0*cw)))));
    right(((((1.0*(-ii))*1.0)*1.0)*(((ee*ii)*sw)/(3.0*cw))));
    if(p1->id()!=-5) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
  }
  void persistentOutput(PersistentOStream & os) const { os << model_; }
  void persistentInput(PersistentIStream & is, int) { is >> model_; }
  //  static void Init();
 protected:
  IBPtr clone() const { return new_ptr(*this); }
  IBPtr fullclone() const { return new_ptr(*this); }
  void doinit() {
    model_ = dynamic_ptr_cast<tcHwFRModelPtr>
	     (generator()->standardModel());
    assert(model_);
    //    getParams(q2);
    
    
    orderInGem(1);
    orderInGs(0);
    FFVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_60 & operator=(const FRModelV_V_60 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_60,Helicity::FFVVertex>
describeHerwigFRModelV_V_60("Herwig::FRModelV_V_60",
				       "FRModel.so");
// void FRModelV_V_60::getParams(Energy2 ) {
// }

class FRModelV_V_61: public FFVVertex {
 public:
  FRModelV_V_61() {
    addToList(-1,1,9000006);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double gVq = model_->gVq();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((2.0*ii)*gVq)));
    right(0.0);
    if(p1->id()!=-1) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
  }
  void persistentOutput(PersistentOStream & os) const { os << model_; }
  void persistentInput(PersistentIStream & is, int) { is >> model_; }
  //  static void Init();
 protected:
  IBPtr clone() const { return new_ptr(*this); }
  IBPtr fullclone() const { return new_ptr(*this); }
  void doinit() {
    model_ = dynamic_ptr_cast<tcHwFRModelPtr>
	     (generator()->standardModel());
    assert(model_);
    //    getParams(q2);
    
    
    orderInGem(1);
    orderInGs(0);
    FFVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_61 & operator=(const FRModelV_V_61 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_61,Helicity::FFVVertex>
describeHerwigFRModelV_V_61("Herwig::FRModelV_V_61",
				       "FRModel.so");
// void FRModelV_V_61::getParams(Energy2 ) {
// }

class FRModelV_V_62: public FFVVertex {
 public:
  FRModelV_V_62() {
    addToList(-3,3,9000006);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double gVq = model_->gVq();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((2.0*ii)*gVq)));
    right(0.0);
    if(p1->id()!=-3) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
  }
  void persistentOutput(PersistentOStream & os) const { os << model_; }
  void persistentInput(PersistentIStream & is, int) { is >> model_; }
  //  static void Init();
 protected:
  IBPtr clone() const { return new_ptr(*this); }
  IBPtr fullclone() const { return new_ptr(*this); }
  void doinit() {
    model_ = dynamic_ptr_cast<tcHwFRModelPtr>
	     (generator()->standardModel());
    assert(model_);
    //    getParams(q2);
    
    
    orderInGem(1);
    orderInGs(0);
    FFVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_62 & operator=(const FRModelV_V_62 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_62,Helicity::FFVVertex>
describeHerwigFRModelV_V_62("Herwig::FRModelV_V_62",
				       "FRModel.so");
// void FRModelV_V_62::getParams(Energy2 ) {
// }

class FRModelV_V_63: public FFVVertex {
 public:
  FRModelV_V_63() {
    addToList(-5,5,9000006);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double gVq = model_->gVq();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((2.0*ii)*gVq)));
    right(0.0);
    if(p1->id()!=-5) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
  }
  void persistentOutput(PersistentOStream & os) const { os << model_; }
  void persistentInput(PersistentIStream & is, int) { is >> model_; }
  //  static void Init();
 protected:
  IBPtr clone() const { return new_ptr(*this); }
  IBPtr fullclone() const { return new_ptr(*this); }
  void doinit() {
    model_ = dynamic_ptr_cast<tcHwFRModelPtr>
	     (generator()->standardModel());
    assert(model_);
    //    getParams(q2);
    
    
    orderInGem(1);
    orderInGs(0);
    FFVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_63 & operator=(const FRModelV_V_63 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_63,Helicity::FFVVertex>
describeHerwigFRModelV_V_63("Herwig::FRModelV_V_63",
				       "FRModel.so");
// void FRModelV_V_63::getParams(Energy2 ) {
// }

class FRModelV_V_64: public FFVVertex {
 public:
  FRModelV_V_64() {
    addToList(18,18,9000006);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double gAXm = model_->gAXm();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*-1.0)*((4.0*ii)*gAXm)));
    right(((((1.0*(-ii))*1.0)*1.0)*((4.0*ii)*gAXm)));
    if(p1->id()!=18) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
  }
  void persistentOutput(PersistentOStream & os) const { os << model_; }
  void persistentInput(PersistentIStream & is, int) { is >> model_; }
  //  static void Init();
 protected:
  IBPtr clone() const { return new_ptr(*this); }
  IBPtr fullclone() const { return new_ptr(*this); }
  void doinit() {
    model_ = dynamic_ptr_cast<tcHwFRModelPtr>
	     (generator()->standardModel());
    assert(model_);
    //    getParams(q2);
    
    
    orderInGem(1);
    orderInGs(0);
    FFVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_64 & operator=(const FRModelV_V_64 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_64,Helicity::FFVVertex>
describeHerwigFRModelV_V_64("Herwig::FRModelV_V_64",
				       "FRModel.so");
// void FRModelV_V_64::getParams(Energy2 ) {
// }

}
