PRAGMA foreign_keys=ON;
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

INSERT INTO analysis_pool VALUES('ATLAS_8_JETS');  
INSERT INTO analysis_pool VALUES('CMS_8_JETS');  

INSERT INTO analysis_pool VALUES('ATLAS_8_GAMMA');
INSERT INTO analysis_pool VALUES('CMS_8_GAMMA');

INSERT INTO analysis_pool VALUES('ATLAS_8_HMDY');

INSERT INTO analysis_pool VALUES('ATLAS_8_Zjj');  
INSERT INTO analysis_pool VALUES('ATLAS_8_Wjj');
INSERT INTO analysis_pool VALUES('CMS_8_Wjj');

INSERT INTO analysis_pool VALUES('ATLAS_8_ZZ');
INSERT INTO analysis_pool VALUES('ATLAS_8_WW');
INSERT INTO analysis_pool VALUES('ATLAS_8_Z_GAMMA');
INSERT INTO analysis_pool VALUES('ATLAS_8_GAMMA_MET');

INSERT INTO analysis_pool VALUES('ATLAS_13_JETS');
INSERT INTO analysis_pool VALUES('CMS_13_JETS');
INSERT INTO analysis_pool VALUES('ATLAS_13_Zjj');

CREATE TABLE analysis (
    id      TEXT NOT NULL UNIQUE,
    lumi    REAL NOT NULL,
    pool    TEXT,
    PRIMARY KEY(id),
    FOREIGN KEY(pool) REFERENCES analysis_pool(pool)
);
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
INSERT INTO analysis VALUES('CMS_2014_I1273574',5000.0,'CMS_7_JETS');

-- 7 TeV photons
INSERT INTO analysis VALUES('ATLAS_2012_I1093738',37.0,'ATLAS_7_GAMMA');
INSERT INTO analysis VALUES('ATLAS_2013_I1244522',37.0,'ATLAS_7_GAMMA');
INSERT INTO analysis VALUES('ATLAS_2013_I1263495',4600.0,'ATLAS_7_GAMMA');
INSERT INTO analysis VALUES('ATLAS_2012_I1199269',4900.0,'ATLAS_7_GAMMA');
INSERT INTO analysis VALUES('CMS_2014_I1266056',4500.0,'CMS_7_GAMMA');

-- 7 TeV leptons/MET
INSERT INTO analysis VALUES('ATLAS_2013_I1230812_EL',4600.0,'ATLAS_7_Zjj_EL');
INSERT INTO analysis VALUES('ATLAS_2013_I1230812_MU',4600.0,'ATLAS_7_Zjj_MU');
INSERT INTO analysis VALUES('ATLAS_2014_I1306294_EL',4600.0,'ATLAS_7_Zjj_EL');
INSERT INTO analysis VALUES('ATLAS_2014_I1306294_MU',4600.0,'ATLAS_7_Zjj_MU');
INSERT INTO analysis VALUES('CMS_2015_I1310737_HF',4900.0,'CMS_7_Zjj');
INSERT INTO analysis VALUES('ATLAS_2015_I1345452',4600.0,'ATLAS_7_Wjj');
-- 7 TeV Low mass DY
INSERT INTO analysis VALUES('ATLAS_2014_I1288706',1600.0,'ATLAS_7_LMDY');
-- 7 TeV single jet masses
INSERT INTO analysis VALUES('CMS_2013_I1224539_WJET',5000.0,'CMS_7_Wjj');
INSERT INTO analysis VALUES('CMS_2013_I1224539_ZJET',5000.0,'CMS_7_Zjj');

INSERT INTO analysis VALUES('CMS_2014_I1303894_HF',5000.0,'CMS_7_Wjj');
INSERT INTO analysis VALUES('CMS_2014_I1303894',5000.0,'CMS_7_Wjj');
INSERT INTO analysis VALUES('ATLAS_2014_I1319490_MU',4600.0,'ATLAS_7_Wjj_MU');
INSERT INTO analysis VALUES('ATLAS_2014_I1319490_EL',4600.0,'ATLAS_7_Wjj_EL');

INSERT INTO analysis VALUES('ATLAS_2013_I1217863_Z',4.6,'ATLAS_7_Z_GAMMA');
INSERT INTO analysis VALUES('ATLAS_2013_I1217863_W_MU',4.6,'ATLAS_7_W_GAMMA_MU');
INSERT INTO analysis VALUES('ATLAS_2013_I1217863_W_EL',4.6,'ATLAS_7_W_GAMMA_EL');
INSERT INTO analysis VALUES('ATLAS_2012_I1203852_HF',4.6,'ATLAS_7_ZZ');

-- 8 TeV fully hadronic
INSERT INTO analysis VALUES('ATLAS_2015_I1394679',20300,'ATLAS_8_JETS');
-- normalised, no total xsec yet INSERT INTO analysis VALUES('CMS_2016_I1421646',19700,'CMS_8_JETS');

-- 8 TeV photons
INSERT INTO analysis VALUES('ATLAS_2016_I1457605',20200.0,'ATLAS_8_GAMMA');
INSERT INTO analysis VALUES('ATLAS_2017_I1591327',20300.0,'ATLAS_8_GAMMA');
INSERT INTO analysis VALUES('ATLAS_2014_I1306615',20300.0,'ATLAS_8_GAMMA');

-- 8 TeV High mass DY
INSERT INTO analysis VALUES('ATLAS_2016_I1467454',20300.0,'ATLAS_8_HMDY');

-- 8 TeV leptons+MET
INSERT INTO analysis VALUES('ATLAS_2014_I1279489',20300.0,'ATLAS_8_Zjj');
INSERT INTO analysis VALUES('ATLAS_2015_I1408516',20300.0,'ATLAS_8_Zjj');
INSERT INTO analysis VALUES('ATLAS_2017_I1589844',20200.0,'ATLAS_8_Zjj');

INSERT INTO analysis VALUES('CMS_2016_I1454211',19700.0,'CMS_8_Wjj');
INSERT INTO analysis VALUES('ATLAS_2015_I1397637',20300.0,'ATLAS_8_Wjj');
INSERT INTO analysis VALUES('CMS_2017_I1518399',19700.0,'CMS_8_Wjj');
 
INSERT INTO analysis VALUES('ATLAS_2016_I1426515',20300.0,'ATLAS_8_WW');

INSERT INTO analysis VALUES('ATLAS_2015_I1394865',20300.0,'ATLAS_8_ZZ');

INSERT INTO analysis VALUES('ATLAS_2016_I1448301_EL',20300.0,'ATLAS_8_Z_GAMMA');
INSERT INTO analysis VALUES('ATLAS_2016_I1448301_MU',20300.0,'ATLAS_8_Z_GAMMA');

INSERT INTO analysis VALUES('ATLAS_2016_I1448301_NU',20300.0,'ATLAS_8_GAMMA_MET');

-- 13 TeV fully hadronic
INSERT INTO analysis VALUES('CMS_2016_I1459051',71.0,'CMS_13_JETS');
INSERT INTO analysis VALUES('CMS_2017_I1519995',2600,'CMS_13_JETS');

-- 13 TeV photons

-- 13 TeV leptons+MET
INSERT INTO analysis VALUES('ATLAS_2017_I1514251_EL',3160.0,'ATLAS_13_Zjj');
INSERT INTO analysis VALUES('ATLAS_2017_I1514251_MU',3160.0,'ATLAS_13_Zjj');

-- CMS_2016_I1421646 – Dijet azimuthal decorrelations in $pp$ collisions at $\sqrt{s} = 8$ TeV
-- commented out in python 'CMS_2013_I1224539_WJET',5000.0,CMS_7_Wjj
-- commented out in python 'CMS_2013_I1224539_ZJET',5000.0,CMS_7_Zjj
-- commented out in python 'CMS_2013_I1256943',5200.0   CMS Z+b



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
INSERT INTO blacklist VALUES('ATLAS_2012_I1203852_HF','d03');
INSERT INTO blacklist VALUES('ATLAS_2012_I1203852_HF','d04');
INSERT INTO blacklist VALUES('ATLAS_2012_I1203852_HF','d05');
INSERT INTO blacklist VALUES('ATLAS_2012_I1203852_HF','d06');
INSERT INTO blacklist VALUES('ATLAS_2012_I1203852_HF','d07');
INSERT INTO blacklist VALUES('ATLAS_2012_I1203852_HF','d08');
INSERT INTO blacklist VALUES('ATLAS_2012_I1199269','d04');
INSERT INTO blacklist VALUES('ATLAS_2016_I1426515','d10-x01-y02');
INSERT INTO blacklist VALUES('ATLAS_2016_I1426515','d11-x01-y02');
INSERT INTO blacklist VALUES('ATLAS_2016_I1426515','d12-x01-y02');
INSERT INTO blacklist VALUES('ATLAS_2016_I1426515','d13-x01-y02');
INSERT INTO blacklist VALUES('ATLAS_2016_I1426515','d14-x01-y02');
INSERT INTO blacklist VALUES('ATLAS_2016_I1426515','d15-x01-y02');
INSERT INTO blacklist VALUES('ATLAS_2014_I1306615','d29');
INSERT INTO blacklist VALUES('ATLAS_2017_I1514251_EL','d01-x02-y01');
INSERT INTO blacklist VALUES('ATLAS_2017_I1514251_MU','d01-x02-y01');
INSERT INTO blacklist VALUES('ATLAS_2017_I1514251_EL','d01-x02-y02');
INSERT INTO blacklist VALUES('ATLAS_2017_I1514251_MU','d01-x02-y02');
INSERT INTO blacklist VALUES('ATLAS_2017_I1514251_EL','d01-x02-y03');
INSERT INTO blacklist VALUES('ATLAS_2017_I1514251_MU','d01-x02-y03');
INSERT INTO blacklist VALUES('CMS_2017_I1518399','d02');


CREATE TABLE whitelist (
    id      TEXT NOT NULL,
    pattern TEXT NOT NULL,
    UNIQUE(id,pattern),
    FOREIGN KEY(id) REFERENCES analysis(id)
);
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d01-x01-y01');
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d01-x02-y01');
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d02-x01-y01');
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d03-x01-y01');
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d03-x02-y01');
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d04-x01-y01');
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d04-x02-y01');
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d05-x03-y01');
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d05-x04-y01');
INSERT INTO whitelist VALUES('ATLAS_2014_I1279489','d05-x05-y01');
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
INSERT INTO whitelist VALUES('CMS_2016_I1454211','d10');
INSERT INTO whitelist VALUES('CMS_2016_I1454211','d12');

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


INSERT INTO subpool VALUES('ATLAS_2016_I1457605','.',0);

CREATE TABLE normalization (
    id      TEXT NOT NULL,
    pattern TEXT NOT NULL,
    norm    REAL NOT NULL,
    UNIQUE(id,pattern),
    FOREIGN KEY(id) REFERENCES analysis(id)
);
INSERT INTO normalization VALUES('ATLAS_2014_I1279489','d01',5.88);
INSERT INTO normalization VALUES('ATLAS_2014_I1279489','d02',1.82);
INSERT INTO normalization VALUES('ATLAS_2014_I1279489','d05',0.066);
INSERT INTO normalization VALUES('ATLAS_2014_I1279489','d03',1.10);
INSERT INTO normalization VALUES('ATLAS_2014_I1279489','d04',0.447);
--
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d23',1.45);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d24',1.03);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d25',0.97);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d02',14.96);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d03',14.96);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d04',14.96);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d14',14.96);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d26',14.96);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d05',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d06',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d07',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d08',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d09',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d10',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d15',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d17',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d18',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d19',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d20',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d21',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d22',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d27',537.10);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d11',5.59);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d12',5.59);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d13',5.59);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d16',5.59);
INSERT INTO normalization VALUES('ATLAS_2015_I1408516','d28',5.59);

--
COMMIT;
