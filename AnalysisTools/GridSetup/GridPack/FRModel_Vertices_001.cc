// -*- C++ -*-
//
// FRModelV_V_25.cc is a part of Herwig - A multi-purpose Monte Carlo event generator
// Copyright (C) 2002-2007 The Herwig Collaboration
//
// Herwig is licenced under version 2 of the GPL, see COPYING for details.
// Please respect the MCnet academic guidelines, see GUIDELINES for details.

#include "FRModel.h"
#include "ThePEG/Helicity/Vertex/Scalar/SSSVertex.h"
#include "ThePEG/Helicity/Vertex/Scalar/SSSSVertex.h"
#include "ThePEG/Helicity/Vertex/Vector/FFVVertex.h"
#include "ThePEG/Helicity/Vertex/Vector/VVVVVertex.h"
#include "ThePEG/Helicity/Vertex/Vector/VVVVertex.h"
#include "ThePEG/Helicity/Vertex/Scalar/VVSSVertex.h"
#include "ThePEG/Helicity/Vertex/Scalar/VVSVertex.h"
#include "ThePEG/Helicity/Vertex/Scalar/FFSVertex.h"

#include "ThePEG/Utilities/DescribeClass.h"
#include "ThePEG/Persistency/PersistentOStream.h"
#include "ThePEG/Persistency/PersistentIStream.h"

namespace Herwig 
{
  using namespace ThePEG;
  using namespace ThePEG::Helicity;
  using ThePEG::Constants::pi;

  class FRModelV_V_1: public SSSSVertex {
 public:
  FRModelV_V_1() {
    addToList(25,25,25,25);
  }
  void setCoupling(Energy2 ,tcPDPtr,tcPDPtr,tcPDPtr,tcPDPtr) {
    double lam = model_->lam();
    //    getParams(q2);
    norm((((1.0*(-ii))*1.0)*((-6.0*ii)*lam)));
    
    
    
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
    
    
    orderInGem(2);
    orderInGs(0);
    SSSSVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_1 & operator=(const FRModelV_V_1 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_1,Helicity::SSSSVertex>
describeHerwigFRModelV_V_1("Herwig::FRModelV_V_1",
				       "FRModel.so");
// void FRModelV_V_1::getParams(Energy2 ) {
// }

class FRModelV_V_2: public SSSVertex {
 public:
  FRModelV_V_2() {
    addToList(25,25,25);
  }
  void setCoupling(Energy2 ,tcPDPtr,tcPDPtr,tcPDPtr) {
    double vev = model_->vev();
    double lam = model_->lam();
    //    getParams(q2);
    norm(((((1.0*(-ii))*1.0)*(((-6.0*ii)*lam)*vev))) * GeV / UnitRemoval::E);
    
    
    
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
    SSSVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_2 & operator=(const FRModelV_V_2 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_2,Helicity::SSSVertex>
describeHerwigFRModelV_V_2("Herwig::FRModelV_V_2",
				       "FRModel.so");
// void FRModelV_V_2::getParams(Energy2 ) {
// }

class FRModelV_V_4: public VVVVertex {
 public:
  FRModelV_V_4() {
    addToList(21,21,21);
  }
  void setCoupling(Energy2 ,tcPDPtr,tcPDPtr,tcPDPtr) {
    double G = model_->G();
    //    getParams(q2);
    norm((((1.0*ii)*(-ii))*(-G)));
    
    
    
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
    VVVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_4 & operator=(const FRModelV_V_4 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_4,Helicity::VVVVertex>
describeHerwigFRModelV_V_4("Herwig::FRModelV_V_4",
				       "FRModel.so");
// void FRModelV_V_4::getParams(Energy2 ) {
// }

class FRModelV_V_5: public VVVVVertex {
 public:
  FRModelV_V_5() {
    addToList(21,21,21,21);
  }
  void setCoupling(Energy2 ,tcPDPtr,tcPDPtr,tcPDPtr,tcPDPtr) {
    double G = model_->G();
    //    getParams(q2);
    norm((((((1.0*ii)*(-1.0/3.0))*(ii*sqr(G)))+(((1.0*ii)*(-1.0/3.0))*(ii*sqr(G))))+(((1.0*ii)*(-1.0/3.0))*(ii*sqr(G)))));
    
    
    setType(1);
setOrder(0,1,2,3);
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
    orderInGs(2);
    VVVVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_5 & operator=(const FRModelV_V_5 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_5,Helicity::VVVVVertex>
describeHerwigFRModelV_V_5("Herwig::FRModelV_V_5",
				       "FRModel.so");
// void FRModelV_V_5::getParams(Energy2 ) {
// }

class FRModelV_V_6: public FFSVertex {
 public:
  FRModelV_V_6() {
    addToList(-5,5,25);
  }
  void setCoupling(Energy2 ,tcPDPtr,tcPDPtr,tcPDPtr) {
    double yb = model_->yb();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*(-((ii*yb)/sqrt(2.0)))));
    right(((((1.0*(-ii))*1.0)*1.0)*(-((ii*yb)/sqrt(2.0)))));
    
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
    FFSVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_6 & operator=(const FRModelV_V_6 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_6,Helicity::FFSVertex>
describeHerwigFRModelV_V_6("Herwig::FRModelV_V_6",
				       "FRModel.so");
// void FRModelV_V_6::getParams(Energy2 ) {
// }

class FRModelV_V_7: public FFSVertex {
 public:
  FRModelV_V_7() {
    addToList(-15,15,25);
  }
  void setCoupling(Energy2 ,tcPDPtr,tcPDPtr,tcPDPtr) {
    double ytau = model_->ytau();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*(-((ii*ytau)/sqrt(2.0)))));
    right(((((1.0*(-ii))*1.0)*1.0)*(-((ii*ytau)/sqrt(2.0)))));
    
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
    FFSVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_7 & operator=(const FRModelV_V_7 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_7,Helicity::FFSVertex>
describeHerwigFRModelV_V_7("Herwig::FRModelV_V_7",
				       "FRModel.so");
// void FRModelV_V_7::getParams(Energy2 ) {
// }

class FRModelV_V_8: public FFSVertex {
 public:
  FRModelV_V_8() {
    addToList(-6,6,25);
  }
  void setCoupling(Energy2 ,tcPDPtr,tcPDPtr,tcPDPtr) {
    double yt = model_->yt();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*(-((ii*yt)/sqrt(2.0)))));
    right(((((1.0*(-ii))*1.0)*1.0)*(-((ii*yt)/sqrt(2.0)))));
    
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
    FFSVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_8 & operator=(const FRModelV_V_8 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_8,Helicity::FFSVertex>
describeHerwigFRModelV_V_8("Herwig::FRModelV_V_8",
				       "FRModel.so");
// void FRModelV_V_8::getParams(Energy2 ) {
// }

class FRModelV_V_9: public VVVVertex {
 public:
  FRModelV_V_9() {
    addToList(22,-24,24);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr p2,tcPDPtr p3) {
    double ee = model_->ee();
    //    getParams(q2);
    norm((((1.0*ii)*1.0)*(ee*ii)));
    
    
    if((p1->id()==-24&&p2->id()==22&&p3->id()==24)||(p1->id()==22&&p2->id()==24&&p3->id()==-24)||(p1->id()==24&&p2->id()==-24&&p3->id()==22)) {norm(-norm());}
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
    VVVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_9 & operator=(const FRModelV_V_9 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_9,Helicity::VVVVertex>
describeHerwigFRModelV_V_9("Herwig::FRModelV_V_9",
				       "FRModel.so");
// void FRModelV_V_9::getParams(Energy2 ) {
// }

class FRModelV_V_10: public VVSSVertex {
 public:
  FRModelV_V_10() {
    addToList(-24,24,25,25);
  }
  void setCoupling(Energy2 ,tcPDPtr,tcPDPtr,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    //    getParams(q2);
    norm((((1.0*(-ii))*1.0)*((sqr(ee)*ii)/(2.0*sqr(sw)))));
    
    
    
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
    
    
    orderInGem(2);
    orderInGs(0);
    VVSSVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_10 & operator=(const FRModelV_V_10 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_10,Helicity::VVSSVertex>
describeHerwigFRModelV_V_10("Herwig::FRModelV_V_10",
				       "FRModel.so");
// void FRModelV_V_10::getParams(Energy2 ) {
// }

class FRModelV_V_11: public VVSVertex {
 public:
  FRModelV_V_11() {
    addToList(-24,24,25);
  }
  void setCoupling(Energy2 ,tcPDPtr,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double vev = model_->vev();
    double sw = model_->sw();
    //    getParams(q2);
    norm(((((1.0*(-ii))*1.0)*(((sqr(ee)*ii)*vev)/(2.0*sqr(sw))))) * GeV / UnitRemoval::E);
    
    
    
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
    VVSVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_11 & operator=(const FRModelV_V_11 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_11,Helicity::VVSVertex>
describeHerwigFRModelV_V_11("Herwig::FRModelV_V_11",
				       "FRModel.so");
// void FRModelV_V_11::getParams(Energy2 ) {
// }

class FRModelV_V_12: public VVVVVertex {
 public:
  FRModelV_V_12() {
    addToList(22,22,-24,24);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr p2,tcPDPtr p3,tcPDPtr p4) {
    double ee = model_->ee();
    //    getParams(q2);
    norm(((((1.0*ii)*1.0)*-1.0)*(sqr(ee)*ii)));
    
    
    bool done[4]={false,false,false,false};
    tcPDPtr part[4]={p1,p2,p3,p4};
    unsigned int iorder[4]={0,0,0,0};
    for(unsigned int ix=0;ix<4;++ix) {
       if(!done[0] && part[ix]->id()==22) {done[0]=true; iorder[0] = ix; continue;}
       if(!done[1] && part[ix]->id()==22) {done[1]=true; iorder[1] = ix; continue;}
       if(!done[2] && part[ix]->id()==-24) {done[2]=true; iorder[2] = ix; continue;}
       if(!done[3] && part[ix]->id()==24) {done[3]=true; iorder[3] = ix; continue;}
    }
    setType(2);
    setOrder(iorder[0],iorder[1],iorder[2],iorder[3]);
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
    
    
    orderInGem(2);
    orderInGs(0);
    VVVVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_12 & operator=(const FRModelV_V_12 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_12,Helicity::VVVVVertex>
describeHerwigFRModelV_V_12("Herwig::FRModelV_V_12",
				       "FRModel.so");
// void FRModelV_V_12::getParams(Energy2 ) {
// }

class FRModelV_V_13: public VVVVertex {
 public:
  FRModelV_V_13() {
    addToList(-24,24,23);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr p2,tcPDPtr p3) {
    double ee = model_->ee();
    double cw = model_->cw();
    double sw = model_->sw();
    //    getParams(q2);
    norm((((1.0*ii)*1.0)*(((cw*ee)*ii)/sw)));
    
    
    if((p1->id()==24&&p2->id()==-24&&p3->id()==23)||(p1->id()==-24&&p2->id()==23&&p3->id()==24)||(p1->id()==23&&p2->id()==24&&p3->id()==-24)) {norm(-norm());}
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
    VVVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_13 & operator=(const FRModelV_V_13 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_13,Helicity::VVVVertex>
describeHerwigFRModelV_V_13("Herwig::FRModelV_V_13",
				       "FRModel.so");
// void FRModelV_V_13::getParams(Energy2 ) {
// }

class FRModelV_V_14: public VVVVVertex {
 public:
  FRModelV_V_14() {
    addToList(-24,-24,24,24);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr p2,tcPDPtr p3,tcPDPtr p4) {
    double ee = model_->ee();
    double sw = model_->sw();
    //    getParams(q2);
    norm(((((1.0*ii)*1.0)*-1.0)*(-((sqr(ee)*ii)/sqr(sw)))));
    
    
    bool done[4]={false,false,false,false};
    tcPDPtr part[4]={p1,p2,p3,p4};
    unsigned int iorder[4]={0,0,0,0};
    for(unsigned int ix=0;ix<4;++ix) {
       if(!done[0] && part[ix]->id()==-24) {done[0]=true; iorder[0] = ix; continue;}
       if(!done[1] && part[ix]->id()==-24) {done[1]=true; iorder[1] = ix; continue;}
       if(!done[2] && part[ix]->id()==24) {done[2]=true; iorder[2] = ix; continue;}
       if(!done[3] && part[ix]->id()==24) {done[3]=true; iorder[3] = ix; continue;}
    }
    setType(2);
    setOrder(iorder[0],iorder[1],iorder[2],iorder[3]);
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
    
    
    orderInGem(2);
    orderInGs(0);
    VVVVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_14 & operator=(const FRModelV_V_14 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_14,Helicity::VVVVVertex>
describeHerwigFRModelV_V_14("Herwig::FRModelV_V_14",
				       "FRModel.so");
// void FRModelV_V_14::getParams(Energy2 ) {
// }

class FRModelV_V_15: public VVVVVertex {
 public:
  FRModelV_V_15() {
    addToList(22,-24,24,23);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr p2,tcPDPtr p3,tcPDPtr p4) {
    double ee = model_->ee();
    double cw = model_->cw();
    double sw = model_->sw();
    //    getParams(q2);
    norm(((((1.0*ii)*1.0)*0.5)*((((-2.0*cw)*sqr(ee))*ii)/sw)));
    
    
    bool done[4]={false,false,false,false};
    tcPDPtr part[4]={p1,p2,p3,p4};
    unsigned int iorder[4]={0,0,0,0};
    for(unsigned int ix=0;ix<4;++ix) {
       if(!done[0] && part[ix]->id()==22) {done[0]=true; iorder[0] = ix; continue;}
       if(!done[1] && part[ix]->id()==-24) {done[1]=true; iorder[3] = ix; continue;}
       if(!done[2] && part[ix]->id()==24) {done[2]=true; iorder[1] = ix; continue;}
       if(!done[3] && part[ix]->id()==23) {done[3]=true; iorder[2] = ix; continue;}
    }
    setType(2);
    setOrder(iorder[0],iorder[1],iorder[2],iorder[3]);
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
    
    
    orderInGem(2);
    orderInGs(0);
    VVVVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_15 & operator=(const FRModelV_V_15 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_15,Helicity::VVVVVertex>
describeHerwigFRModelV_V_15("Herwig::FRModelV_V_15",
				       "FRModel.so");
// void FRModelV_V_15::getParams(Energy2 ) {
// }

class FRModelV_V_16: public VVSSVertex {
 public:
  FRModelV_V_16() {
    addToList(23,23,25,25);
  }
  void setCoupling(Energy2 ,tcPDPtr,tcPDPtr,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double cw = model_->cw();
    double sw = model_->sw();
    //    getParams(q2);
    norm((((1.0*(-ii))*1.0)*(((sqr(ee)*ii)+(((sqr(cw)*sqr(ee))*ii)/(2.0*sqr(sw))))+(((sqr(ee)*ii)*sqr(sw))/(2.0*sqr(cw))))));
    
    
    
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
    
    
    orderInGem(2);
    orderInGs(0);
    VVSSVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_16 & operator=(const FRModelV_V_16 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_16,Helicity::VVSSVertex>
describeHerwigFRModelV_V_16("Herwig::FRModelV_V_16",
				       "FRModel.so");
// void FRModelV_V_16::getParams(Energy2 ) {
// }

class FRModelV_V_17: public VVSVertex {
 public:
  FRModelV_V_17() {
    addToList(23,23,25);
  }
  void setCoupling(Energy2 ,tcPDPtr,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double vev = model_->vev();
    double cw = model_->cw();
    double sw = model_->sw();
    //    getParams(q2);
    norm(((((1.0*(-ii))*1.0)*((((sqr(ee)*ii)*vev)+((((sqr(cw)*sqr(ee))*ii)*vev)/(2.0*sqr(sw))))+((((sqr(ee)*ii)*sqr(sw))*vev)/(2.0*sqr(cw)))))) * GeV / UnitRemoval::E);
    
    
    
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
    VVSVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_17 & operator=(const FRModelV_V_17 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_17,Helicity::VVSVertex>
describeHerwigFRModelV_V_17("Herwig::FRModelV_V_17",
				       "FRModel.so");
// void FRModelV_V_17::getParams(Energy2 ) {
// }

class FRModelV_V_18: public VVVVVertex {
 public:
  FRModelV_V_18() {
    addToList(-24,24,23,23);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr p2,tcPDPtr p3,tcPDPtr p4) {
    double ee = model_->ee();
    double cw = model_->cw();
    double sw = model_->sw();
    //    getParams(q2);
    norm(((((1.0*ii)*1.0)*-1.0)*(((sqr(cw)*sqr(ee))*ii)/sqr(sw))));
    
    
    bool done[4]={false,false,false,false};
    tcPDPtr part[4]={p1,p2,p3,p4};
    unsigned int iorder[4]={0,0,0,0};
    for(unsigned int ix=0;ix<4;++ix) {
       if(!done[0] && part[ix]->id()==-24) {done[0]=true; iorder[0] = ix; continue;}
       if(!done[1] && part[ix]->id()==24) {done[1]=true; iorder[1] = ix; continue;}
       if(!done[2] && part[ix]->id()==23) {done[2]=true; iorder[2] = ix; continue;}
       if(!done[3] && part[ix]->id()==23) {done[3]=true; iorder[3] = ix; continue;}
    }
    setType(2);
    setOrder(iorder[0],iorder[1],iorder[2],iorder[3]);
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
    
    
    orderInGem(2);
    orderInGs(0);
    VVVVVertex::doinit();
  }
  //    void getParams(Energy2);
 private:
  FRModelV_V_18 & operator=(const FRModelV_V_18 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_18,Helicity::VVVVVertex>
describeHerwigFRModelV_V_18("Herwig::FRModelV_V_18",
				       "FRModel.so");
// void FRModelV_V_18::getParams(Energy2 ) {
// }

class FRModelV_V_19: public FFVVertex {
 public:
  FRModelV_V_19() {
    addToList(-11,12,-24);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((ee*ii)/(sw*sqrt(2.0)))));
    right(0.0);
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
  FRModelV_V_19 & operator=(const FRModelV_V_19 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_19,Helicity::FFVVertex>
describeHerwigFRModelV_V_19("Herwig::FRModelV_V_19",
				       "FRModel.so");
// void FRModelV_V_19::getParams(Energy2 ) {
// }

class FRModelV_V_20: public FFVVertex {
 public:
  FRModelV_V_20() {
    addToList(-13,14,-24);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((ee*ii)/(sw*sqrt(2.0)))));
    right(0.0);
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
  FRModelV_V_20 & operator=(const FRModelV_V_20 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_20,Helicity::FFVVertex>
describeHerwigFRModelV_V_20("Herwig::FRModelV_V_20",
				       "FRModel.so");
// void FRModelV_V_20::getParams(Energy2 ) {
// }

class FRModelV_V_21: public FFVVertex {
 public:
  FRModelV_V_21() {
    addToList(-15,16,-24);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double sw = model_->sw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((ee*ii)/(sw*sqrt(2.0)))));
    right(0.0);
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
  FRModelV_V_21 & operator=(const FRModelV_V_21 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_21,Helicity::FFVVertex>
describeHerwigFRModelV_V_21("Herwig::FRModelV_V_21",
				       "FRModel.so");
// void FRModelV_V_21::getParams(Energy2 ) {
// }

class FRModelV_V_22: public FFVVertex {
 public:
  FRModelV_V_22() {
    addToList(-12,12,23);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double cw = model_->cw();
    double sw = model_->sw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((((cw*ee)*ii)/(2.0*sw))+(((ee*ii)*sw)/(2.0*cw)))));
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
  FRModelV_V_22 & operator=(const FRModelV_V_22 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_22,Helicity::FFVVertex>
describeHerwigFRModelV_V_22("Herwig::FRModelV_V_22",
				       "FRModel.so");
// void FRModelV_V_22::getParams(Energy2 ) {
// }

class FRModelV_V_23: public FFVVertex {
 public:
  FRModelV_V_23() {
    addToList(-14,14,23);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double cw = model_->cw();
    double sw = model_->sw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((((cw*ee)*ii)/(2.0*sw))+(((ee*ii)*sw)/(2.0*cw)))));
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
  FRModelV_V_23 & operator=(const FRModelV_V_23 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_23,Helicity::FFVVertex>
describeHerwigFRModelV_V_23("Herwig::FRModelV_V_23",
				       "FRModel.so");
// void FRModelV_V_23::getParams(Energy2 ) {
// }

class FRModelV_V_24: public FFVVertex {
 public:
  FRModelV_V_24() {
    addToList(-16,16,23);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    double cw = model_->cw();
    double sw = model_->sw();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*((((cw*ee)*ii)/(2.0*sw))+(((ee*ii)*sw)/(2.0*cw)))));
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
  FRModelV_V_24 & operator=(const FRModelV_V_24 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_24,Helicity::FFVVertex>
describeHerwigFRModelV_V_24("Herwig::FRModelV_V_24",
				       "FRModel.so");
// void FRModelV_V_24::getParams(Energy2 ) {
// }

class FRModelV_V_25: public FFVVertex {
 public:
  FRModelV_V_25() {
    addToList(-11,11,22);
  }
  void setCoupling(Energy2 ,tcPDPtr p1,tcPDPtr,tcPDPtr) {
    double ee = model_->ee();
    //    getParams(q2);
    norm(1.0);
    left(((((1.0*(-ii))*1.0)*1.0)*(-(ee*ii))));
    right(((((1.0*(-ii))*1.0)*1.0)*(-(ee*ii))));
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
  FRModelV_V_25 & operator=(const FRModelV_V_25 &);
  //    Complex leftval, rightval, normval;
  tcHwFRModelPtr model_;
};
DescribeClass<FRModelV_V_25,Helicity::FFVVertex>
describeHerwigFRModelV_V_25("Herwig::FRModelV_V_25",
				       "FRModel.so");
// void FRModelV_V_25::getParams(Energy2 ) {
// }

}
