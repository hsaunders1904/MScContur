#!usr/bin/env python

#############################################################################################
### Here store aditional static data we dont get from rivet, this can be improved greatly..
global anapool, subpools
anapool=['ATLAS_7_JETS','ATLAS_7_Zjj_EL','ATLAS_7_Wjj_mu','CMS_7_JETS','CMS_7_Wjj','CMS_7_Zjj','ATLAS_8_JETS','ATLAS_7_Wjj_EL','ATLAS_7_GAMMA','ATLAS_7_Z_GAMMA','ATLAS_7_W_GAMMA_MU','ATLAS_7_W_GAMMA_EL','ATLAS_7_ZZ','ATLAS_7_GAMMAGAMMA','CMS_GAMMA_JET','ATLAS_7_Zjj_MU','ATLAS_8_Zjj','ATLAS_8_GAMMA']
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
    elif 'ATLAS_2013_I1230812_EL' in h:
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
        anatype=anapool[8]
    elif 'ATLAS_2014_I1306294_EL' in h:
        lumi = 4600
        anatype=anapool[1]
    #elif 'CMS_2013_I1256943' in h:
        #lumi = 5200
        ###this one is normalised in a completely stupid way, possible to undo this
        ###CMS Z+bb
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
    elif 'ATLAS_2014_I1306294_MU' in h:
        lumi = 4600
        anatype=anapool[15]
    elif 'ATLAS_2013_I1230812_MU' in h:
                #Z+jets        blacklist=['d02','d04','d06','d08']
        lumi = 4600
        anatype=anapool[15]
        for plotkey in blacklist:
            if plotkey in h:
                lumi = -1
   # elif 'CMS_2013_I1224539_WJET' in h:
   #     lumi=5000
   #     anatype=anapool[4]
   # elif 'CMS_2013_I1224539_ZJET' in h:
   #     lumi=5000
   #     anatype=anapool[5]
    elif 'ATLAS_2014_I1279489' in h:
        #lumi=20300
        anatype=anapool[16]
        whitelist=['d01-x01-y01','d01-x02-y01','d02-x01-y01','d03-x01-y01','d03-x02-y01','d04-x01-y01','d04-x02-y01','d05-x03-y01','d05-x04-y01','d05-x05-y01']
        #whitelist=['d03-x01-y01','d03-x02-y01']
        for plotkey in whitelist:
            if plotkey in h:
                lumi = 20300
    elif 'ATLAS_2015_I1408516' in h:
        #if 'EL' in h:
        #    continue
        #    subpool = subpools[0]

        #    subpool = subpools[1]
        anatype=anapool[16]
        lumi=20300
        #if 'MU' in h:
        #    lumi=-1
        #if 'd41' in h:
        #    lumi=-1
    elif 'ATLAS_2016_I1457605' in h:
        anatype=anapool[17]
        lumi=20200
        subpool = subpools[0]
        
    return lumi,anatype,subpool

#############################################################################################
### Special function to help with plots normalised to total xs
def isNorm(h):
    isNorm=False
    normFac=1.0
    if 'CMS_2013_I1224539' in h:
        isNorm=True
        normFac = 1.0/1000.0
    if 'ATLAS_2014_I1279489' in h:
        isNorm=True
        #normFac = 1.
        if 'd01' in h:
            normFac = 5.88
        if 'd02' in h:
            normFac = 1.82
        if 'd05' in h:
            normFac = 0.066
        if 'd03' in h:
            normFac = 1.10
        if 'd04' in h:
            normFac = 0.447
    if 'ATLAS_2015_I1408516' in h:
        #normFac=1.0
        _12_20 = ['d23']
        _20_30 = ['d24']
        _30_46 = ['d25']
        _46_66 = ['d02','d03','d04','d14','d26']
        _66_116 = ['d05','d06','d07','d08','d09','d10','d15','d17','d18','d19','d20','d21','d22','d27']
        _116_150 = ['d11','d12','d13','d16','d28']
        for plotkey in _12_20:
            if plotkey in h:
                normFac = 1.45
                isNorm=True
        for plotkey in _20_30:
            if plotkey in h:
                normFac = 1.03
                isNorm=True
        for plotkey in _30_46:
            if plotkey in h:
                normFac = 0.97
                isNorm=True
        for plotkey in _46_66:
            if plotkey in h:
                normFac = 14.96
                isNorm=True
        for plotkey in _66_116:
            if plotkey in h:
                normFac = 537.10
                isNorm=True
        for plotkey in _116_150:
            if plotkey in h:
                normFac = 5.59
                isNorm=True
    return isNorm, normFac
