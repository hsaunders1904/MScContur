# -*- Makefile -*- (for emacs)
# Models/Feynrules/python/Makefile-FR.  Generated from Makefile-FR.in by configure.
#
# Herwig 7.0.1
#
# This Makefile is intended for compiling Herwig plugins
# You can find example plugins in the Contrib directory
#
# This Makefile received very little testing, 
# any bug reports are very welcome!
#

#
# C++ flags
# 
.PRECIOUS: %.o
.PHONY: all clean

CXX = g++

CXXFLAGS = -Wall -Wextra -pedantic -O3

# add additional package header directories here
CPPFLAGS = -I/unix/cedar/software/sl6/Herwig-7.0.0/./include -I/unix/cedar/software/sl6/Herwig-7.0.0/./include -I/unix/cedar/software/sl6/Herwig-7.0.0/./include

# add additional libraries here
LDFLAGS = 

ALLCCFILES=$(shell echo *.cc)
all : FRModel.so 
ALLOBJFILES=$(ALLCCFILES:.cc=.o)

%.so : $(ALLOBJFILES)
	$(CXX) -shared -fPIC $(CXXFLAGS) $(LDFLAGS) $^ -o $@  

%.o : %.cc
	$(CXX) -fPIC $(CPPFLAGS) $(CXXFLAGS) -c $< -o $@

clean:
	@echo "Removing all generated files"
	@rm -f FRModel.so $(ALLOBJFILES) $(ALLCCFILES) *.h
	@rm -f *.run *.log *.out *.tex *.dot *.svg 
	@rm -f *.model *.spc *.in *.template Makefile
