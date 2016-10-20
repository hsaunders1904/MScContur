.PHONY : test

test : dbtest StaticDB.py StaticData.py analyses.db 
	./dbtest	

analyses.db : analyses.sql
	sqlite3 $@ < $<
