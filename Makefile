LOCATION = AnalysisTools/contur/contur/TestingFunctions
ANALYSES = modified_analyses/Analyses

all: $(ANALYSES)/Rivet-ConturOverload.so $(LOCATION)/analyses.db

$(ANALYSES)/Rivet-ConturOverload.so : $(ANALYSES)/*.cc
	$(ANALYSES)/buildrivet.sh 

$(LOCATION)/analyses.db : $(LOCATION)/analyses.sql
	rm -f $@
	sqlite3 $@ < $<

.PHONY :  $(LOCATION)/analyses.db


