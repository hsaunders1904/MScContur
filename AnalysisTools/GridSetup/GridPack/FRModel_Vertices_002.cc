// -*- C++ -*-
//
// FRModelV_V_50.cc is a part of Herwig - A multi-purpose Monte Carlo event generator
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

  class FRModelV_V_26: public FFVVertex {
 public:
  FRModelV_V_26() {
    addToList(-13,13,22);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*(-(ee*ii))));
    right(((((1.0*(-ii))*1.0)*1.0)*(-(ee*ii))));
    if(p1->id()!=-13) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
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
  FRModelV_V_26 & operator=(const FRModelV_V_26 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_26,Helicity::FFVVertex>
describeHerwigFRModelV_V_26("Herwig::FRModelV_V_26",
				       "FRModel.so");
// void FRModelV_V_26::getParams(Energy2 ) {
// }

class FRModelV_V_27: public FFVVertex {
 public:
  FRModelV_V_27() {
    addToList(-15,15,22);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*(-(ee*ii))));
    right(((((1.0*(-ii))*1.0)*1.0)*(-(ee*ii))));
    if(p1->id()!=-15) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
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
  FRModelV_V_27 & operator=(const FRModelV_V_27 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_27,Helicity::FFVVertex>
describeHerwigFRModelV_V_27("Herwig::FRModelV_V_27",
				       "FRModel.so");
// void FRModelV_V_27::getParams(Energy2 ) {
// }

class FRModelV_V_28: public FFVVertex {
 public:
  FRModelV_V_28() {
    addToList(-12,11,24);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((ee*ii)/(sw*sqrt(2.0)))));
    right(0.0);
    if(p1->id()!=-12) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
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
  FRModelV_V_28 & operator=(const FRModelV_V_28 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_28,Helicity::FFVVertex>
describeHerwigFRModelV_V_28("Herwig::FRModelV_V_28",
				       "FRModel.so");
// void FRModelV_V_28::getParams(Energy2 ) {
// }

class FRModelV_V_29: public FFVVertex {
 public:
  FRModelV_V_29() {
    addToList(-14,13,24);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((ee*ii)/(sw*sqrt(2.0)))));
    right(0.0);
    if(p1->id()!=-14) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
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
  FRModelV_V_29 & operator=(const FRModelV_V_29 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_29,Helicity::FFVVertex>
describeHerwigFRModelV_V_29("Herwig::FRModelV_V_29",
				       "FRModel.so");
// void FRModelV_V_29::getParams(Energy2 ) {
// }

class FRModelV_V_30: public FFVVertex {
 public:
  FRModelV_V_30() {
    addToList(-16,15,24);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((ee*ii)/(sw*sqrt(2.0)))));
    right(0.0);
    if(p1->id()!=-16) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
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
  FRModelV_V_30 & operator=(const FRModelV_V_30 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_30,Helicity::FFVVertex>
describeHerwigFRModelV_V_30("Herwig::FRModelV_V_30",
				       "FRModel.so");
// void FRModelV_V_30::getParams(Energy2 ) {
// }

class FRModelV_V_31: public FFVVertex {
 public:
  FRModelV_V_31() {
    addToList(-11,11,23);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double cw = model_->cw();
    double sw = model_->sw();
    //    getParams(q2);
    norm(1.0);
    left((((((1.0*(-ii))*1.0)*1.0)*(((ee*ii)*sw)/(2.0*cw)))+((((1.0*(-ii))*1.0)*1.0)*((-((cw*ee)*ii))/(2.0*sw)))));
    right(((((1.0*(-ii))*1.0)*2.0)*(((ee*ii)*sw)/(2.0*cw))));
    if(p1->id()!=-11) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
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
  FRModelV_V_31 & operator=(const FRModelV_V_31 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_31,Helicity::FFVVertex>
describeHerwigFRModelV_V_31("Herwig::FRModelV_V_31",
				       "FRModel.so");
// void FRModelV_V_31::getParams(Energy2 ) {
// }

class FRModelV_V_32: public FFVVertex {
 public:
  FRModelV_V_32() {
    addToList(-13,13,23);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double cw = model_->cw();
    double sw = model_->sw();
    //    getParams(q2);
    norm(1.0);
    left((((((1.0*(-ii))*1.0)*1.0)*(((ee*ii)*sw)/(2.0*cw)))+((((1.0*(-ii))*1.0)*1.0)*((-((cw*ee)*ii))/(2.0*sw)))));
    right(((((1.0*(-ii))*1.0)*2.0)*(((ee*ii)*sw)/(2.0*cw))));
    if(p1->id()!=-13) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
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
  FRModelV_V_32 & operator=(const FRModelV_V_32 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_32,Helicity::FFVVertex>
describeHerwigFRModelV_V_32("Herwig::FRModelV_V_32",
				       "FRModel.so");
// void FRModelV_V_32::getParams(Energy2 ) {
// }

class FRModelV_V_33: public FFVVertex {
 public:
  FRModelV_V_33() {
    addToList(-15,15,23);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    double cw = model_->cw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*(((-((cw*ee)*ii))/(2.0*sw))+(((ee*ii)*sw)/(2.0*cw)))));
    right(((((1.0*(-ii))*1.0)*1.0)*(((ee*ii)*sw)/cw)));
    if(p1->id()!=-15) {Complex ltemp=left(), rtemp=right(); left(-rtemp); right(-ltemp);}
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
  FRModelV_V_33 & operator=(const FRModelV_V_33 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_33,Helicity::FFVVertex>
describeHerwigFRModelV_V_33("Herwig::FRModelV_V_33",
				       "FRModel.so");
// void FRModelV_V_33::getParams(Energy2 ) {
// }

class FRModelV_V_34: public FFVVertex {
 public:
  FRModelV_V_34() {
    addToList(-2,2,22);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*(((2.0*ee)*ii)/3.0)));
    right(((((1.0*(-ii))*1.0)*1.0)*(((2.0*ee)*ii)/3.0)));
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
  FRModelV_V_34 & operator=(const FRModelV_V_34 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_34,Helicity::FFVVertex>
describeHerwigFRModelV_V_34("Herwig::FRModelV_V_34",
				       "FRModel.so");
// void FRModelV_V_34::getParams(Energy2 ) {
// }

class FRModelV_V_35: public FFVVertex {
 public:
  FRModelV_V_35() {
    addToList(-4,4,22);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*(((2.0*ee)*ii)/3.0)));
    right(((((1.0*(-ii))*1.0)*1.0)*(((2.0*ee)*ii)/3.0)));
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
  FRModelV_V_35 & operator=(const FRModelV_V_35 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_35,Helicity::FFVVertex>
describeHerwigFRModelV_V_35("Herwig::FRModelV_V_35",
				       "FRModel.so");
// void FRModelV_V_35::getParams(Energy2 ) {
// }

class FRModelV_V_36: public FFVVertex {
 public:
  FRModelV_V_36() {
    addToList(-6,6,22);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*(((2.0*ee)*ii)/3.0)));
    right(((((1.0*(-ii))*1.0)*1.0)*(((2.0*ee)*ii)/3.0)));
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
  FRModelV_V_36 & operator=(const FRModelV_V_36 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_36,Helicity::FFVVertex>
describeHerwigFRModelV_V_36("Herwig::FRModelV_V_36",
				       "FRModel.so");
// void FRModelV_V_36::getParams(Energy2 ) {
// }

class FRModelV_V_37: public FFVVertex {
 public:
  FRModelV_V_37() {
    addToList(-2,2,21);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double G = model_->G();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*(ii*G)));
    right(((((1.0*(-ii))*1.0)*1.0)*(ii*G)));
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
    
    
    orderInGem(0);
    orderInGs(1);
    FFVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_37 & operator=(const FRModelV_V_37 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_37,Helicity::FFVVertex>
describeHerwigFRModelV_V_37("Herwig::FRModelV_V_37",
				       "FRModel.so");
// void FRModelV_V_37::getParams(Energy2 ) {
// }

class FRModelV_V_38: public FFVVertex {
 public:
  FRModelV_V_38() {
    addToList(-4,4,21);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double G = model_->G();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*(ii*G)));
    right(((((1.0*(-ii))*1.0)*1.0)*(ii*G)));
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
    
    
    orderInGem(0);
    orderInGs(1);
    FFVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_38 & operator=(const FRModelV_V_38 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_38,Helicity::FFVVertex>
describeHerwigFRModelV_V_38("Herwig::FRModelV_V_38",
				       "FRModel.so");
// void FRModelV_V_38::getParams(Energy2 ) {
// }

class FRModelV_V_39: public FFVVertex {
 public:
  FRModelV_V_39() {
    addToList(-6,6,21);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double G = model_->G();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*(ii*G)));
    right(((((1.0*(-ii))*1.0)*1.0)*(ii*G)));
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
    
    
    orderInGem(0);
    orderInGs(1);
    FFVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_39 & operator=(const FRModelV_V_39 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_39,Helicity::FFVVertex>
describeHerwigFRModelV_V_39("Herwig::FRModelV_V_39",
				       "FRModel.so");
// void FRModelV_V_39::getParams(Energy2 ) {
// }

class FRModelV_V_40: public FFVVertex {
 public:
  FRModelV_V_40() {
    addToList(-1,2,-24);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((ee*ii)/(sw*sqrt(2.0)))));
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
  FRModelV_V_40 & operator=(const FRModelV_V_40 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_40,Helicity::FFVVertex>
describeHerwigFRModelV_V_40("Herwig::FRModelV_V_40",
				       "FRModel.so");
// void FRModelV_V_40::getParams(Energy2 ) {
// }

class FRModelV_V_41: public FFVVertex {
 public:
  FRModelV_V_41() {
    addToList(-3,4,-24);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((ee*ii)/(sw*sqrt(2.0)))));
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
  FRModelV_V_41 & operator=(const FRModelV_V_41 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_41,Helicity::FFVVertex>
describeHerwigFRModelV_V_41("Herwig::FRModelV_V_41",
				       "FRModel.so");
// void FRModelV_V_41::getParams(Energy2 ) {
// }

class FRModelV_V_42: public FFVVertex {
 public:
  FRModelV_V_42() {
    addToList(-5,6,-24);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((ee*ii)/(sw*sqrt(2.0)))));
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
  FRModelV_V_42 & operator=(const FRModelV_V_42 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_42,Helicity::FFVVertex>
describeHerwigFRModelV_V_42("Herwig::FRModelV_V_42",
				       "FRModel.so");
// void FRModelV_V_42::getParams(Energy2 ) {
// }

class FRModelV_V_43: public FFVVertex {
 public:
  FRModelV_V_43() {
    addToList(-2,2,23);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    double cw = model_->cw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((((cw*ee)*ii)/(2.0*sw))-(((ee*ii)*sw)/(6.0*cw)))));
    right(((((1.0*(-ii))*1.0)*1.0)*((((-2.0*ee)*ii)*sw)/(3.0*cw))));
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
  FRModelV_V_43 & operator=(const FRModelV_V_43 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_43,Helicity::FFVVertex>
describeHerwigFRModelV_V_43("Herwig::FRModelV_V_43",
				       "FRModel.so");
// void FRModelV_V_43::getParams(Energy2 ) {
// }

class FRModelV_V_44: public FFVVertex {
 public:
  FRModelV_V_44() {
    addToList(-4,4,23);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    double cw = model_->cw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((((cw*ee)*ii)/(2.0*sw))-(((ee*ii)*sw)/(6.0*cw)))));
    right(((((1.0*(-ii))*1.0)*1.0)*((((-2.0*ee)*ii)*sw)/(3.0*cw))));
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
  FRModelV_V_44 & operator=(const FRModelV_V_44 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_44,Helicity::FFVVertex>
describeHerwigFRModelV_V_44("Herwig::FRModelV_V_44",
				       "FRModel.so");
// void FRModelV_V_44::getParams(Energy2 ) {
// }

class FRModelV_V_45: public FFVVertex {
 public:
  FRModelV_V_45() {
    addToList(-6,6,23);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    double cw = model_->cw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((((cw*ee)*ii)/(2.0*sw))-(((ee*ii)*sw)/(6.0*cw)))));
    right(((((1.0*(-ii))*1.0)*1.0)*((((-2.0*ee)*ii)*sw)/(3.0*cw))));
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
  FRModelV_V_45 & operator=(const FRModelV_V_45 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_45,Helicity::FFVVertex>
describeHerwigFRModelV_V_45("Herwig::FRModelV_V_45",
				       "FRModel.so");
// void FRModelV_V_45::getParams(Energy2 ) {
// }

class FRModelV_V_46: public FFVVertex {
 public:
  FRModelV_V_46() {
    addToList(-2,2,9000006);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double gVq = model_->gVq();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((2.0*ii)*gVq)));
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
  FRModelV_V_46 & operator=(const FRModelV_V_46 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_46,Helicity::FFVVertex>
describeHerwigFRModelV_V_46("Herwig::FRModelV_V_46",
				       "FRModel.so");
// void FRModelV_V_46::getParams(Energy2 ) {
// }

class FRModelV_V_47: public FFVVertex {
 public:
  FRModelV_V_47() {
    addToList(-4,4,9000006);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double gVq = model_->gVq();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((2.0*ii)*gVq)));
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
  FRModelV_V_47 & operator=(const FRModelV_V_47 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_47,Helicity::FFVVertex>
describeHerwigFRModelV_V_47("Herwig::FRModelV_V_47",
				       "FRModel.so");
// void FRModelV_V_47::getParams(Energy2 ) {
// }

class FRModelV_V_48: public FFVVertex {
 public:
  FRModelV_V_48() {
    addToList(-6,6,9000006);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double gVq = model_->gVq();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((2.0*ii)*gVq)));
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
  FRModelV_V_48 & operator=(const FRModelV_V_48 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_48,Helicity::FFVVertex>
describeHerwigFRModelV_V_48("Herwig::FRModelV_V_48",
				       "FRModel.so");
// void FRModelV_V_48::getParams(Energy2 ) {
// }

class FRModelV_V_49: public FFVVertex {
 public:
  FRModelV_V_49() {
    addToList(-1,1,22);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((-(ee*ii))/3.0)));
    right(((((1.0*(-ii))*1.0)*1.0)*((-(ee*ii))/3.0)));
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
  FRModelV_V_49 & operator=(const FRModelV_V_49 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_49,Helicity::FFVVertex>
describeHerwigFRModelV_V_49("Herwig::FRModelV_V_49",
				       "FRModel.so");
// void FRModelV_V_49::getParams(Energy2 ) {
// }

class FRModelV_V_50: public FFVVertex {
 public:
  FRModelV_V_50() {
    addToList(-3,3,22);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((-(ee*ii))/3.0)));
    right(((((1.0*(-ii))*1.0)*1.0)*((-(ee*ii))/3.0)));
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
  FRModelV_V_50 & operator=(const FRModelV_V_50 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_50,Helicity::FFVVertex>
describeHerwigFRModelV_V_50("Herwig::FRModelV_V_50",
				       "FRModel.so");
// void FRModelV_V_50::getParams(Energy2 ) {
// }

}
