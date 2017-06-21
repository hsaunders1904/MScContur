LOCATION = AnalysisTools/contur/contur/TestingFunctions

$(LOCATION)/analyses.db : $(LOCATION)/analyses.sql
	rm -f $@
	sqlite3 $@ < $<
