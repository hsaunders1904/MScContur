PRAGMA foreign_keys=ON;
-- This is a version of the SQL for the DB which contains only the analyses used in the first contur paper arXiv:1606.05296, for backward comarparison.
BEGIN TRANSACTION;
CREATE TABLE analysis_pool (
    pool    TEXT NOT NULL UNIQUE,
    PRIMARY KEY(pool)
);
INSERT INTO analysis_pool VALUES('ATLAS_7_JETS');  
INSERT INTO analysis_pool VALUES('CMS_7_JETS');    

INSERT INTO analysis_pool VALUES('ATLAS_7_GAMMA');  
INSERT INTO analysis_pool VALUES('CMS_7_GAMMA');      

INSERT INTO analysis_pool VALUES('ATLAS_7_LMDY');

INSERT INTO analysis_pool VALUES('ATLAS_7_Zjj_EL');
INSERT INTO analysis_pool VALUES('ATLAS_7_Zjj_MU');
INSERT INTO analysis_pool VALUES('ATLAS_7_Wjj_EL'); 
INSERT INTO analysis_pool VALUES('ATLAS_7_Wjj_MU'); 
INSERT INTO analysis_pool VALUES('ATLAS_7_Wjj'); 
INSERT INTO analysis_pool VALUES('CMS_7_Zjj');  
INSERT INTO analysis_pool VALUES('CMS_7_Wjj');    
INSERT INTO analysis_pool VALUES('ATLAS_7_Z_GAMMA');
INSERT INTO analysis_pool VALUES('ATLAS_7_W_GAMMA_MU'); 
INSERT INTO analysis_pool VALUES('ATLAS_7_W_GAMMA_EL');
INSERT INTO analysis_pool VALUES('ATLAS_7_ZZ');         
INSERT INTO analysis_pool VALUES('ATLAS_7_WW');         

INSERT INTO analysis_pool VALUES('ATLAS_8_JETS');  

CREATE TABLE analysis (
    id      TEXT NOT NULL UNIQUE,
    lumi    REAL NOT NULL,
    pool    TEXT,
    PRIMARY KEY(id),
    FOREIGN KEY(pool) REFERENCES analysis_pool(pool)
);
-- Note, the LUMI value given here should be in units which match the normalisation
-- of the cross section plots. Most in pb, some in fb.

-- Superseded/deprecated analyses
INSERT INTO analysis VALUES('ATLAS_2012_I1083318',36.0,NULL);
INSERT INTO analysis VALUES('ATLAS_2011_I945498',36.0,NULL);
INSERT INTO analysis VALUES('ATLAS_2011_I921594',35.0,NULL);
INSERT INTO analysis VALUES('ATLAS_2011_S9128077',2.4,NULL);

-- 7 TeV fully hadronic
INSERT INTO analysis VALUES('ATLAS_2014_I1325553',4500.0,'ATLAS_7_JETS');
INSERT INTO analysis VALUES('ATLAS_2014_I1268975',4500.0,'ATLAS_7_JETS');
INSERT INTO analysis VALUES('ATLAS_2014_I1326641',4510.0,'ATLAS_7_JETS');
INSERT INTO analysis VALUES('ATLAS_2014_I1307243',4500.0,'ATLAS_7_JETS');
INSERT INTO analysis VALUES('CMS_2014_I1298810',5000.0,'CMS_7_JETS');

-- 7 TeV photons
INSERT INTO analysis VALUES('ATLAS_2012_I1093738',37.0,'ATLAS_7_GAMMA');
INSERT INTO analysis VALUES('ATLAS_2013_I1263495',4600.0,'ATLAS_7_GAMMA');
INSERT INTO analysis VALUES('ATLAS_2012_I1199269',4900.0,'ATLAS_7_GAMMA');
INSERT INTO analysis VALUES('CMS_2014_I1266056',4500.0,'CMS_7_GAMMA');

-- 7 TeV Z+jets
INSERT INTO analysis VALUES('ATLAS_2013_I1230812_EL',4600.0,'ATLAS_7_Zjj_EL');
INSERT INTO analysis VALUES('ATLAS_2013_I1230812_MU',4600.0,'ATLAS_7_Zjj_MU');
INSERT INTO analysis VALUES('CMS_2015_I1310737',4900.0,'CMS_7_Zjj');

-- 7 TeV W+jets. 
INSERT INTO analysis VALUES('ATLAS_2014_I1319490_MU',4600.0,'ATLAS_7_Wjj_MU');
INSERT INTO analysis VALUES('ATLAS_2014_I1319490_EL',4600.0,'ATLAS_7_Wjj_EL');
INSERT INTO analysis VALUES('CMS_2014_I1303894',5000.0,'CMS_7_Wjj');

-- 7 TeV dibosons, plots in fb 
INSERT INTO analysis VALUES('ATLAS_2013_I1217863_Z',4.6,'ATLAS_7_Z_GAMMA');
INSERT INTO analysis VALUES('ATLAS_2013_I1217863_W_MU',4.6,'ATLAS_7_W_GAMMA_MU');
INSERT INTO analysis VALUES('ATLAS_2013_I1217863_W_EL',4.6,'ATLAS_7_W_GAMMA_EL');
INSERT INTO analysis VALUES('ATLAS_2012_I1203852',4.6,'ATLAS_7_ZZ');

-- 8 TeV fully hadronic
-- plots in fb
INSERT INTO analysis VALUES('ATLAS_2015_I1394679',20.3,'ATLAS_8_JETS');


CREATE TABLE blacklist (
    id      TEXT NOT NULL,
    pattern TEXT NOT NULL,
    UNIQUE(id,pattern),
    FOREIGN KEY(id) REFERENCES analysis(id)
);
INSERT INTO blacklist VALUES('ATLAS_2013_I1230812_EL','d02');
INSERT INTO blacklist VALUES('ATLAS_2013_I1230812_EL','d04');
INSERT INTO blacklist VALUES('ATLAS_2013_I1230812_EL','d06');
INSERT INTO blacklist VALUES('ATLAS_2013_I1230812_EL','d08');
INSERT INTO blacklist VALUES('ATLAS_2013_I1230812_MU','d02');
INSERT INTO blacklist VALUES('ATLAS_2013_I1230812_MU','d04');
INSERT INTO blacklist VALUES('ATLAS_2013_I1230812_MU','d06');
INSERT INTO blacklist VALUES('ATLAS_2013_I1230812_MU','d08');

INSERT INTO blacklist VALUES('CMS_2014_I1298810','d13');
INSERT INTO blacklist VALUES('CMS_2014_I1298810','d14');
INSERT INTO blacklist VALUES('CMS_2014_I1298810','d15');
INSERT INTO blacklist VALUES('CMS_2014_I1298810','d16');
INSERT INTO blacklist VALUES('CMS_2014_I1298810','d17');
INSERT INTO blacklist VALUES('CMS_2014_I1298810','d18');
INSERT INTO blacklist VALUES('ATLAS_2013_I1217863_Z','d17');
INSERT INTO blacklist VALUES('ATLAS_2013_I1217863_Z','d18');
INSERT INTO blacklist VALUES('ATLAS_2013_I1217863_Z','d20');
INSERT INTO blacklist VALUES('ATLAS_2013_I1217863_W_MU','d15');
INSERT INTO blacklist VALUES('ATLAS_2013_I1217863_W_MU','d16');
INSERT INTO blacklist VALUES('ATLAS_2013_I1217863_W_MU','d19');
INSERT INTO blacklist VALUES('ATLAS_2013_I1217863_W_EL','d15');
INSERT INTO blacklist VALUES('ATLAS_2013_I1217863_W_EL','d16');
INSERT INTO blacklist VALUES('ATLAS_2013_I1217863_W_EL','d19');
INSERT INTO blacklist VALUES('ATLAS_2012_I1203852','d03');
INSERT INTO blacklist VALUES('ATLAS_2012_I1203852','d04');
INSERT INTO blacklist VALUES('ATLAS_2012_I1203852','d05');
INSERT INTO blacklist VALUES('ATLAS_2012_I1203852','d06');
INSERT INTO blacklist VALUES('ATLAS_2012_I1203852','d07');
INSERT INTO blacklist VALUES('ATLAS_2012_I1203852','d08');
INSERT INTO blacklist VALUES('ATLAS_2012_I1199269','d04');


CREATE TABLE whitelist (
    id      TEXT NOT NULL,
    pattern TEXT NOT NULL,
    UNIQUE(id,pattern),
    FOREIGN KEY(id) REFERENCES analysis(id)
);
--
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d13');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d14');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d15');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d16');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d17');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d18');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d19');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d20');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d21');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d22');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d23');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d24');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d25');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d26');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d27');
INSERT INTO whitelist VALUES('ATLAS_2014_I1307243','d28');

CREATE TABLE subpool (
    id      TEXT NOT NULL,
    pattern TEXT NOT NULL,
    subid   INTEGER NOT NULL,
    UNIQUE(id,pattern),
    FOREIGN KEY(id) REFERENCES analysis(id)
);
INSERT INTO subpool VALUES('ATLAS_2014_I1325553','d01-x01-y0[1-6]',0);
INSERT INTO subpool VALUES('ATLAS_2014_I1325553','d02-x01-y0[1-6]',1);
INSERT INTO subpool VALUES('ATLAS_2014_I1268975','d01-x01-y0[1-6]',0);
INSERT INTO subpool VALUES('ATLAS_2014_I1268975','d02-x01-y0[1-6]',1);
INSERT INTO subpool VALUES('ATLAS_2014_I1326641','d0[1-5]-x01-y01',0);
INSERT INTO subpool VALUES('ATLAS_2014_I1326641','(d10|d0[6-9])-x01-y01',1);
INSERT INTO subpool VALUES('CMS_2014_I1298810','d0[1-6]-x01-y01',0);
-- check this next one, one of the .py entries had y02 listed
INSERT INTO subpool VALUES('CMS_2014_I1298810','(d1[0-2]|d0[7-9])-x01-y01',1);
INSERT INTO subpool VALUES('ATLAS_2014_I1307243','(d20|d1[3-9])-x01-y01',0);
INSERT INTO subpool VALUES('ATLAS_2014_I1307243','d2[1-8]-x01-y01',1);
INSERT INTO subpool VALUES('ATLAS_2013_I1263495','d01-x01-y0[13]',0);



CREATE TABLE normalization (
--  analysis id, plot pattern, norm factor for ref data, was mc plot area normalised by rivet?  (0=no, 1=yes) 
    id      TEXT NOT NULL,
    pattern TEXT NOT NULL,
    norm    REAL NOT NULL,
    scalemc INT NOT NULL,
    UNIQUE(id,pattern),
    FOREIGN KEY(id) REFERENCES analysis(id)
);
-- this is BR to a single charged lepton, needed when the xsec is report as a W 
-- and the generator reports the final state. The bug in the paper!
-- INSERT INTO normalization VALUES('ATLAS_2014_I1319490_MU','d',0.108059,0);
-- INSERT INTO normalization VALUES('ATLAS_2014_I1319490_EL','d',0.108059,0);
-- INSERT INTO normalization VALUES('CMS_2014_I1303894','d',0.108059,0);

--
COMMIT;