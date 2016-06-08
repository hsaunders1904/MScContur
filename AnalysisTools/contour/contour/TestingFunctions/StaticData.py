#!usr/bin/env python

#############################################################################################
### Here store aditional static data we dont get from rivet, this can be improved greatly..
global anapool, subpools
anapool=['ATLAS_7_JETS','ATLAS_7_Zjj','ATLAS_7_Wjj_mu','CMS_7_JETS','CMS_7_Wjj','CMS_7_Zjj','ATLAS_8_JETS','ATLAS_7_Wjj_EL','ATLAS_7_GAMMA','ATLAS_7_Z_GAMMA','ATLAS_7_W_GAMMA_MU','ATLAS_7_W_GAMMA_EL','ATLAS_7_ZZ','ATLAS_7_GAMMAGAMMA','CMS_GAMMA_JET']
##This is really bad, but set up an arbitrary number of subpool tags to iterate over, this should just be done on the fly for each analysis!
subpools=['R1','R2','R3','R4']
def LumiFinder(h):
    #ananame = h.strip("/").split("/")[0]
    lumi = -1
    anatype=''
    subpool=''
    if 'ATLAS_2014_I1325553' in h:
        lumi = 4500
        anatype=anapool[0]
        R1=['d01-x01-y01','d01-x01-y02','d01-x01-y03','d01-x01-y04','d01-x01-y05','d01-x01-y06']
        R2=['d02-x01-y01','d02-x01-y02','d02-x01-y03','d02-x01-y04','d02-x01-y05','d02-x01-y06']
        for poolmember in R1:
            if poolmember in h:
                subpool = subpools[0]
        for poolmember in R2:
            if poolmember in h:
                subpool = subpools[1]
    elif 'ATLAS_2014_I1268975' in h:
        lumi = 4500
        anatype=anapool[0]
        R1=['d01-x01-y01','d01-x01-y02','d01-x01-y03','d01-x01-y04','d01-x01-y05','d01-x01-y06']
        R2=['d02-x01-y01','d02-x01-y02','d02-x01-y03','d02-x01-y04','d02-x01-y05','d02-x01-y06']
        for poolmember in R1:
            if poolmember in h:
                subpool = subpools[0]
        for poolmember in R2:
            if poolmember in h:
                subpool = subpools[1]
    elif 'ATLAS_2014_I1326641' in h:
        lumi = 4510
        anatype=anapool[0]
        R1=['d01-x01-y01','d02-x01-y01','d03-x01-y01','d04-x01-y01','d05-x01-y01']
        R2=['d06-x01-y01','d07-x01-y01','d08-x01-y01','d09-x01-y01','d10-x01-y01']
        for poolmember in R1:
            if poolmember in h:
                subpool = subpools[0]
        for poolmember in R2:
            if poolmember in h:
                subpool = subpools[1]
    elif 'ATLAS_2013_I1230812' in h:
        #Z+jets
        blacklist=['d02','d04','d06','d08']
        lumi = 4600
        anatype=anapool[1]
        for plotkey in blacklist:
            if plotkey in h:
                lumi = -1
#    elif 'ATLAS_2013_I1217863' in h:
#        lumi = 4600
    elif 'ATLAS_2012_I1093738' in h:
        lumi = 37
        anatype=anapool[8]
    elif 'ATLAS_2012_I1083318' in h:
        lumi = 36
    elif 'ATLAS_2011_I945498' in h:
        lumi = 36
    elif 'ATLAS_2011_I921594' in h:
        lumi = 35
    elif 'ATLAS_2011_S9128077' in h:
        lumi = 2.4
    elif 'CMS_2014_I1298810' in h:
        lumi = 5000
        anatype=anapool[3]
        blacklist=['d13','d14','d15','d16','d17','d18']
        for plotkey in blacklist:
            if plotkey in h:
                lumi = -1
        R1=['d01-x01-y01','d02-x01-y01','d03-x01-y01','d04-x01-y01','d05-x01-y01','d06-x01-y01']
        R2=['d07-x01-y01','d08-x01-y02','d09-x01-y01','d10-x01-y01','d11-x01-y01','d12-x01-y01']
        for poolmember in R1:
            if poolmember in h:
                subpool = subpools[0]
        for poolmember in R2:
            if poolmember in h:
                subpool = subpools[1]
    elif 'ATLAS_2013_I1244522' in h:
        lumi = 37
    elif 'ATLAS_2014_I1306294' in h:
        lumi = 4600
    elif 'CMS_2013_I1256943' in h:
        lumi = 5200
    elif 'CMS_2015_I1310737' in h:
        lumi = 4900
        anatype=anapool[5]
    elif 'CMS_2014_I1303894' in h:
        lumi = 5000
        anatype=anapool[4]
    elif 'ATLAS_2014_I1319490_MU' in h:
        lumi = 4600
        anatype=anapool[2]
    elif 'ATLAS_2014_I1319490_EL' in h:
        lumi = 4600
        anatype=anapool[7]
    elif 'ATLAS_2015_I1394679' in h:
        ##this analysis uses y units of fb
        lumi =20.3
        anatype=anapool[6]
    elif 'ATLAS_2014_I1307243' in h:
        lumi = -1
        anatype=anapool[0]
        whitelist=['d13','d14','d15','d16','d17','d18','d19','d20','d21','d22','d23','d24','d25','d26','d27','d28']
        for plotkey in whitelist:
            if plotkey in h:
                lumi = 4500
        R1=['d13-x01-y01','d14-x01-y01','d15-x01-y01','d16-x01-y01','d17-x01-y01','d18-x01-y01','d19-x01-y01','d20-x01-y01']
        R2=['d21-x01-y01','d22-x01-y01','d23-x01-y01','d24-x01-y01','d25-x01-y01','d26-x01-y01','d27-x01-y01','d28-x01-y01']
        for poolmember in R1:
            if poolmember in h:
                subpool = subpools[0]
        for poolmember in R2:
            if poolmember in h:
                subpool = subpools[1]
    elif 'ATLAS_2013_I1263495' in h:
        lumi = 4600
        anatype =anapool[8]
        R1=['d01-x01-y01','d01-x01-y03']
        for poolmember in R1:
            if poolmember in h:
                subpool = subpools[0]
    elif 'ATLAS_2013_I1217863_Z' in h:
        lumi = 4.6
        anatype= anapool[9]
        blacklist=['d17','d18','d20']
        for plotkey in blacklist:
            if plotkey in h:
                lumi = -1
    elif 'ATLAS_2013_I1217863_W_MU' in h:
        lumi = 4.6
        anatype= anapool[10]
        blacklist=['d15','d16','d19']
        for plotkey in blacklist:
            if plotkey in h:
                lumi = -1
    elif 'ATLAS_2013_I1217863_W_EL' in h:
        lumi = 4.6
        anatype= anapool[11]
        blacklist=['d15','d16','d19']
        for plotkey in blacklist:
            if plotkey in h:
                lumi = -1
    elif 'ATLAS_2012_I1203852' in h:
        lumi = 4.600
        anatype= anapool[12]
        blacklist=['d03','d04','d05','d06','d07','d08']
        for plotkey in blacklist:
            if plotkey in h:
                lumi = -1
    elif 'ATLAS_2012_I1199269' in h:
        lumi = 4900
        anatype=anapool[13]
        blacklist=['d04']
        for plotkey in blacklist:
            if plotkey in h:
                lumi = -1
    elif 'CMS_2014_I1266056' in h:
        lumi = 4500
        anatype=anapool[14]
    return lumi,anatype,subpool
