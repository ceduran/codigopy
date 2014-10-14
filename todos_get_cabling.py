
  #!/usr/bin/env python
import re
import urllib
import urllib2
import pickle
import os
import sys
from optparse import OptionParser



#this function implemets callback to make the optpars able to take several arguments for each option##
def cb(option, opt_str, value, parser):
    args=[]
    for arg in parser.rargs:
        if arg[0] != "-":
            args.append(arg)
        else:
            del parser.rargs[:len(args)]
            break
    if getattr(parser.values, option.dest):
        args.extend(getattr(parser.values, option.dest))
    setattr(parser.values, option.dest, args)

def getLatestCabling():
   cabfile = ""
   url = "https://test-stripdbmonitor.web.cern.ch/"
   path = "test-stripdbmonitor/CondDBMonitoring/cms_orcoff_prod/CMS_COND_31X_STRIP/DBTagCollection/SiStripFedCabling/SiStripFedCabling_GR10_v1_hlt/CablingLog/"
   pattern = '<a href="CablingInfo_Run.*?">(.*?)</a>'
   response = urllib2.urlopen(url+path).read()
   for filename in re.findall(pattern, response):
      cabfile = filename
   print cabfile
   return cabfile


def filenameF(name):
    suffix='CablingInfo_Run'
    filenameX=suffix+name+'.txt'
    url="https://test-stripdbmonitor.web.cern.ch/test-stripdbmonitor/CondDBMonitoring/cms_orcoff_prod/CMS_COND_31X_STRIP/DBTagCollection/SiStripFedCabling/SiStripFedCabling_GR10_v1_hlt/CablingLog/"
    urllib.urlretrieve(url+filenameX,filenameX)
    return filenameX

def semilinkF(namelink):

    pattern=re.split('/',namelink)
    filelink=pattern[-1]

    url="https://test-stripdbmonitor.web.cern.ch/test-stripdbmonitor/CondDBMonitoring/cms_orcoff_prod/CMS_COND_31X_STRIP/DBTagCollection/SiStripFedCabling/"
    urllib.urlretrieve(url+namelink,filelink)

    return filelink

###this function makes a dictionary of Detids(with pairnumber as secondkey) and a dictionary of FEDs (with FecCH as second key) for the cabling file 
def DictionaryCab(filenameC,options):
    """This function takes a filename as input and looks for it in the URL, then makes a dictionary with DetId as key and pairnumber as key2 or FEDid as key1 and FedCh as key2"""
    FiletxtFEDs = open(filenameC,'r')

    Fd = "FedCrate/FedSlot/FedId/FeUnit/FeChan/FedCh"
    Fc = "FecCrate/FecSlot/FecRing/CcuAddr/CcuChan"
    D = "DcuId/DetId"
    Ll = "LldChan/APV0/APV1"
    pair = "pairNumber/nPairs/nStrips"
    DC = "DCU/MUX/PLL/LLD"
 
    DictionaryCab.CablingInfoDict={}		
    CablingInfoDictF={}
    # Creating lists
    FedCrateList = []
    FedSlotList = []
    FedIdList=[]
    FeUnitList=[]
    FeChanList=[]
    FedChList=[]
		
    FecCrateList=[]
    FecSlotList=[]
    FecRingList=[]
    CcuAddrList=[]
    CcuChanList=[]
		
    DcuIdList=[]
    DetIdList=[]
		
    LldChanList=[]
    APV0List=[]
    APV1List=[]
    pairNumberList=[]
    nPairsList=[]
    nStripsList=[]
		
    DCUList=[]
    MUXList=[]
    PLLList=[]
    LLDList=[]


    for line in FiletxtFEDs:
        if Fd in line:
            pattern = re.split('\W+',line)
            FedCrateList.append(pattern[7])
            FedSlotList.append(pattern[8])
            FedIdList.append(pattern[9])
            FeUnitList.append(pattern[10])
            FeChanList.append(pattern[11])
            FedChList.append(pattern[12])
        if Fc in line:
            pattern = re.split('\W+',line)
            FecCrateList.append(pattern[6])
            FecSlotList.append(pattern[7])
            FecRingList.append(pattern[8])
            CcuAddrList.append(pattern[9])
            CcuChanList.append(pattern[10])
        if D in line:
            pattern = re.split('\W+',line)
            DcuIdList.append(str(int(pattern[3],16)))
            DetIdList.append(str(int(pattern[4],16)))
        if Ll in line:
            pattern = re.split('\W+',line)
            LldChanList.append(pattern[4])
            APV0List.append(pattern[5])
            APV1List.append(pattern[6])
        if pair in line:
            pattern = re.split('\W+',line)
            pairNumberList.append(pattern[4])
            nPairsList.append(pattern[5])
            nStripsList.append(pattern[6])
        if DC in line:
            pattern = re.split('\W+',line)
            DCUList.append(pattern[6])
            MUXList.append(pattern[7])
            PLLList.append(pattern[8])
            LLDList.append(pattern[9])
        
		

    for fedcrate,fedslot,fedid,feunit,fechan,fedch,feccrate,fecslot,fecring,ccuaddr,ccuchan,dcuid,detid,lldchan,apv0,apv1,pairnumber,npairs,nstrips,dcu,mux,pll,lld  in zip(FedCrateList,FedSlotList,FedIdList,FeUnitList,FeChanList,FedChList,FecCrateList,FecSlotList,FecRingList,CcuAddrList,CcuChanList,DcuIdList,DetIdList,LldChanList,APV0List,APV1List,pairNumberList,nPairsList,nStripsList,DCUList,MUXList,PLLList,LLDList):

        if detid in DictionaryCab.CablingInfoDict.keys(): 
            DictionaryCab.CablingInfoDict[detid].update({pairnumber:{"FedCrate": fedcrate,"FedSlot":fedslot,"FedId":fedid,"FeUnit":feunit,"FeChan":fechan,"FedCh":fedch,"FecCrate":feccrate,"FecSlot":fecslot,"FecRing":fecring,"CcuAddr":ccuaddr,"CcuChan":ccuchan,"DcuId":dcuid,"DetId":detid,"pairNumber":pairnumber,"LldChan":lldchan,"APV0":apv0,"APV1":apv1,"nPairs":npairs,"nStrips":nstrips,"DCU":dcu,"MUX":mux,"PLL":pll,"LLD":lld}})
		
        else:
            DictionaryCab.CablingInfoDict.update({detid:{pairnumber:{"FedCrate": fedcrate,"FedSlot":fedslot,"FedId":fedid,"FeUnit":feunit,"FeChan":fechan,"FedCh":fedch,"FecCrate":feccrate,"FecSlot":fecslot,"FecRing":fecring,"CcuAddr":ccuaddr,"CcuChan":ccuchan,"DcuId":dcuid,"DetId":detid,"pairNumber":pairnumber,"LldChan":lldchan,"APV0":apv0,"APV1":apv1,"nPairs":npairs,"nStrips":nstrips,"DCU":dcu,"MUX":mux,"PLL":pll,"LLD":lld}}})


    for fedcrate, fedslot, fedid, feunit, fechan, fedch, feccrate, fecslot, fecring, ccuaddr, ccuchan, dcuid, detid, lldchan, apv0, apv1, pairnumber, npairs, nstrips, dcu, mux, pll, lld in zip(FedCrateList, FedSlotList, FedIdList, FeUnitList, FeChanList, FedChList, FecCrateList, FecSlotList, FecRingList, CcuAddrList, CcuChanList, DcuIdList, DetIdList, LldChanList, APV0List, APV1List, pairNumberList, nPairsList, nStripsList, DCUList, MUXList, PLLList, LLDList): 
  
                        
        if fedid in CablingInfoDictF.keys(): 
            CablingInfoDictF[fedid].update({fedch:{"FedCrate": fedcrate,"FedSlot":fedslot,"FedId":fedid,"FeUnit":feunit,"FeChan":fechan,"FedCh":fedch,"FecCrate":feccrate,"FecSlot":fecslot,"FecRing":fecring,"CcuAddr":ccuaddr,"CcuChan":ccuchan,"DcuId":dcuid,"DetId":detid,"pairNumber":pairnumber,"LldChan":lldchan,"APV0":apv0,"APV1":apv1,"nPairs":npairs,"nStrips":nstrips,"DCU":dcu,"MUX":mux,"PLL":pll,"LLD":lld}})
               
        else:
            CablingInfoDictF.update({fedid:{fedch:{"FedCrate": fedcrate,"FedSlot":fedslot,"FedId":fedid,"FeUnit":feunit,"FeChan":fechan,"FedCh":fedch,"FecCrate":feccrate,"FecSlot":fecslot,"FecRing":fecring,"CcuAddr":ccuaddr,"CcuChan":ccuchan,"DcuId":dcuid,"DetId":detid,"pairNumber":pairnumber,"LldChan":lldchan,"APV0":apv0,"APV1":apv1,"nPairs":npairs,"nStrips":nstrips,"DCU":dcu,"MUX":mux,"PLL":pll,"LLD":lld}}})

    


############THESE INSTRUCTIONS ARE FOR GETTING THE INFO OF THE DICTIONARY FOR THE CABLING FILE#############################3
    #dump the detids of the cabling file in a txt file 
    if options.listrc2:
        archi=open(options.listrc2,'w')
        [archi.write("%s\n"%p) for p in DictionaryCab.CablingInfoDict]
        archi.close
        print "A file named %r has been created" %options.listrc2


    #trackermap of the modules of the cabling
    if options.listrc:
        archi=open('trackermapdetids.txt','w')
        [archi.write(p+" "+"255"+" "+ "0"+" "+"0"+"\n") for p in DictionaryCab.CablingInfoDict]

        archi.close
        os.system(('print_TrackerMap trackermapdetids.txt TrackerMap %r 2400 False True 999 -999')%options.listrc)
        print "A file named trackermapdetids.txt and a tracker map named %r have been created" %options.listrc
   
   #A file with the DetIds associated to a(some) FED(s)	
    if options.lisfem and options.fnafe:
        archi1=open(options.fnafe,'w')
        lif1=options.lisfem
        visited=set([])
        listf=[]
        for p in lif1:
            archi1.write("The modules associated to FED %s are:\n" %p)
            for r in CablingInfoDictF[p]:
                if CablingInfoDictF[str(int(p))][r]["DetId"] not in visited:
                    visited.add(CablingInfoDictF[str(int(p))][r]["DetId"])
                    archi1.write(CablingInfoDictF[str(int(p))][r]["DetId"]+"\n")
                    
   # A Trackermap of the detids associated to a (some) Fed(s)
    if options.lisfetrc:
        archi=open('ModulestoFeds.txt','w')
        li1=options.lisfetrc
        color_list=[" 0 255 0"," 0 0 255"," 255 0 0"," 255 255 0"," 255 0  255"," 0 255 255"," 0 102 0"," 102 0 102"," 47 79 79"," 255 140 0"]
        for p in li1:
            for q in CablingInfoDictF[p].keys():
                archi.write(CablingInfoDictF[p][q]["DetId"]+color_list[li1.index(p)]+"\n")

        archi.close()
        variable =""

        color_list = ["green","blue","red","yellow","magenta","light blue","dark green","purple","grey","orange"]
        for i,j in zip (li1,color_list):
            variable+='%s=%s  ' % (i,j)
        os.system('print_TrackerMap ModulestoFeds.txt "FEDs: %s for file %s" %r  2400 False True 999 -999' % (variable,filenameC,options.fnmodtof))
      
    #Info about a (set of) module(s)
    if  options.lismod and options.pairnumb:
        li3=options.lismod
        li4=options.pairnumb
        li5=options.infmod
        txt=open('infomodules.txt','w')
        for i in li3:
            for j in li4:
                txt.write("For DetID : %r with pairNumber: %r\n "%(i,j))
                for k in li5:
                    txt.write(" %r is:%r\n "%(k,DictionaryCab.CablingInfoDict[i][j][k]))
        print("A file named infomodules.txt has been created")
               

    #info about a (set of) Fed(s)
    if options.lisfed and options.fedc:
        
        li3=options.lisfed
        li4=options.fedc
        li5=options.infed
        txt=open('infofeds.txt','w')
        for l,m in zip(li3,li4):
            txt.write( "For FedId : %r with FedCh : %r \n"%(l,m))
            for n in li5:
                txt.write( " %r is:%r \n"%(n,CablingInfoDictF[l][m][n]))
        print("A file named infofeds.txt has been created")

   #modules associated to something
    if options.infomod2 and options.infomod3:
        li1=options.infomod2
        li2=options.infomod3
        txt1=open('ModofCab.txt','w')
        txt2=open('ModofCabtm.txt','w')
        listx=[set() for x in range(len(li1))]
        for k,i,y in zip(li1,li2,listx):
            for l in DictionaryCab.CablingInfoDict.keys():
                for m in DictionaryCab.CablingInfoDict[l]:
                    if DictionaryCab.CablingInfoDict[l][m][k]==i:
                        y.add(l)
                         
        color_list=[" 0 255 0"," 0 0 255"," 255 0 0"," 255 255 0"," 255 0  255"," 0 255 255"," 0 102 0"," 102 0 102"," 47 79 79"," 255 140 0"]
        for k,i,x in zip(li1,li2,listx):
            txt1.write("The modules with %s:%s are:\n"%(k,i))
            for y in x:
                txt1.write(y+"\n")
                txt2.write(y+color_list[li1.index(k)]+"\n")
        
        variable =""
        color_list = ["green","blue","red","yellow","magenta","light blue","dark green","purple","grey","orange"]
        for i,j in zip (li1,color_list):
            variable+='%s=%s  ' % (i,j)
        os.system('print_TrackerMap ModofCabtm.txt "values: %s for file %s" ModofCabtm.png  2400 False True 999 -999' % (variable,filenameC))
      
        print "A file named ModofCab.txt and a trackermap named ModofCabtm.png with the info have been created"
          
        txt1.close() 
   
   ###Properties of cabling with modules in common 

    if options.cabcommon1 and options.cabcommon2:
        txt_2 = open("CabinCommon",'w')
        li1=options.cabcommon1
        li2=options.cabcommon2
        print "li1, li2:"
        print li1,li2
        print type(li2[0])

        objectives = []
        DictionaryCab.CablingInfoDict
        txt=open('Modulescommon.txt','w')
        txt2=open('Modulescommontm.txt','w')
        txt.write("The modules in common for:  ")
        for i,j in zip(li1,li2):
            txt.write("%s %s, "%(i,j))
        for l in DictionaryCab.CablingInfoDict.keys():
            flag = True
            for x in DictionaryCab.CablingInfoDict[l].keys(): 
                for proper in range(len(li1)): 
                    if DictionaryCab.CablingInfoDict[l][x][li1[proper]] != li2[proper]:
                        flag = False
            if flag:
                objectives.append(l)
                txt.write("\n%s"%l)
                txt2.write(l+" "+"0"+" "+"0"+" "+"255"+"\n")

        variable =""
        for i,j in zip (li1,li2):
            variable+='%s:%s  ' % (i,j)
        os.system('print_TrackerMap Modulescommontm.txt "values: %s for file %s" Modulescommon.png  2400 False True 999 -999' % (variable,filenameC))
      

        print("A file named Modulescommon.txt has been created")


    return DictionaryCab
####################3THESE INSTRUCTIONS ARE FOR GETTING THE INFO OF THE ALIAS ######################
def AliasFun(filenameC,options,AliasDict):
    FileAliasD=open(filenameC,'r')
    D="DcuId/DetId"
    DetIdAlList=[]
    for line1 in FileAliasD:
        if D in line1:
            pattern1 = re.split('\W+',line1)
            if (int(pattern1[4],16)) not in DetIdAlList:
                DetIdAlList.append(int(pattern1[4],16))
    AliasFun.SAliasDict={}
    for detID in DetIdAlList:
        beta1 = (AliasDict[int(detID)]) 
        AliasFun.SAliasDict.update({int(detID):beta1})

   #A file with the alias of the detids of the cabling file   
    if options.fialc:
        beta1=""
        txt_1=open(options.fialc,'w')
        for detID in DetIdAlList:
            beta1 = str(AliasDict[int(detID)])
            txt_1.write("%s  %s\n"  %(detID,beta1.split("'")[1]))
        print "A file named %r has been created" %options.fialc
   
    #the alias of a (set of) module(s)     
    if options.alimod:
        txt=open('AliasModules.txt','w')
        for i in options.alimod:
            beta2= str(AliasFun.SAliasDict[int(i)])
            txt.write("for module with DetId %s, Alias is %s\n" %(i,beta2.split("'")[1]))
        print "A file named AliasModules.txt has been created"

   #A file with the modules associated to a certain Alias(es)
    if options.modali and options.filena:
        txt_2 = open (options.filena,'w')       
        beta3=""
        for j in options.modali:
            txt_2.write("For Alias %r, the DetIds associated are:\n" % j)
            for detid in AliasFun.SAliasDict.keys():
                beta3 = str(AliasFun.SAliasDict[detid])
                if j in beta3:
                    txt_2.write("%r \n" %detid)
        print "A file named %s has been created" %options.filena
    #A tracker map of the modules associated to some alias
    if options.alitkm:
        txt=open('faliastkm.txt','w')
        li1=options.alitkm
        color_list=[" 0 255 0"," 0 0 255"," 255 0 0"," 255 255 0"," 255 0  255"," 0 255 255"," 0 102 0"," 102 0 102"," 47 79 79"]
        for k in li1:
            for detid in  AliasFun.SAliasDict.keys():
                beta=str(AliasFun.SAliasDict[detid])
                if k in beta:
                    txt.write(str(detid)+color_list[li1.index(k)]+"\n")
        
        txt.close()
        color_list = ["green","blue","red","yellow","magenta","light blue","dark green","purple","grey"]
        variable =""


        for i,j in zip (li1,color_list):
            variable+='%s=%s  ' % (i,j)
        os.system('print_TrackerMap faliastkm.txt "value: %r for Run  %r" %r 2400 False True 999 -999' % (variable,filenameC,options.fnaltomod))                      
   ##To know if a module is or is not in a detector or subdetector
    if options.modinf and options.subinf:
        txt=open('TrueFalseAlias.txt','w')
        for k in options.modinf:
            for l in options.subinf:
                beta6= str(AliasFun.SAliasDict[int(k)])
                if l in beta6:
                    
                   txt.write("For DetId %s true %s\n"%(k,l))

                if l not in beta6:
                    txt.write("For DetId %s false %s\n"%(k,l))
        print "A file named TrueFalseAlias.txt has been created"

####THE NEXT FUNCTIONS ARE FOR GETTING THE INFO OF THE HV#########


#function to extract the Detids of the cabling file in a txt file
def DetIdCabL(filenameC,verbose=True):                                                 
    """This function takes a filename as input and looks for it in URL ... ,
    it parses all detIDs and dumps them in a local file named detIdCab.txt""" 
    #filenameX=filenameC+'.txt'
    FileCabList = open(filenameC,'r')
    D = "DcuId/DetId" 
    DetIdCabList = []
    for line1 in FileCabList:                                                                                                           
        if D in line1:
            pattern1 = re.split('\W+',line1)
            if (int(pattern1[4],16)) not in DetIdCabList:
                DetIdCabList.append(int(pattern1[4],16))  
    #txtCab=open("DetIdCab.txt",'w')
    #for i in DetIdCabList:
    #    txtCab.write("%r\n" %i)
    
    return DetIdCabList
 
#function to make a PSUName file of the cabling file

def CabHVFiles(fileCab,fileHV,verbose=True):
    sep = " "
    d = {}
    for line in  open(fileHV, "r"):
        key, val = line.strip().split(sep)
        d[key] = val
    #detIDs=[liner for line in fileCab]#open(fileCab, "r")] 
    OutFile=open('file.txt','w')
    for detID in fileCab:
        OutFile.write("%s %s\n" % (detID,d[str(detID)]))

#function to make the dictionary of the psuname file of the cabling file

def HVInfoDictF(filenameC,filename, options):
    FiletxtHV = open(filename,'r')
    HVInfoDictF.HVInfoDict = {}
    DetIdList = []
    PSUList = []
    CmstrkList = []
    TrackerSyList= []
    BranchList = []
    CrateList = []
    BoardList = []
    ChannelList = []
    for line2 in FiletxtHV:
        if "cms_trk" in line2 :
            pattern1 = re.split(' ',line2)
            DetIdList.append(pattern1[0])
            PSUList.append(pattern1[1].split("\n")[0])
            pattern2 = re.split('/',pattern1[1])
            CmstrkList.append(pattern2[0])
            TrackerSyList.append(pattern2[1])
            BranchList.append(pattern2[2])
            CrateList.append(pattern2[3])
            BoardList.append(pattern2[4])
            ChannelList.append(pattern2[5].split("\n")[0])
    for detid,psu,cmstrk,trackersy,branch,crate,board,channel in zip(DetIdList,PSUList,CmstrkList,TrackerSyList,BranchList,CrateList,BoardList,ChannelList):
        HVInfoDictF.HVInfoDict.update({detid:{'PSUName':psu,'Cmstrk':cmstrk,'TrackerSY':trackersy,'Branch':branch,'Crate':crate,'Board':board,'Channel':channel}})
    ###here are the stuff that the code provides
    #info about a module
    if options.search_and and options.look_and: 
        li1=options.search_and
        li2=options.look_and   
        txt=open('InfoModuleHV.txt','w')
        for i in li1:
            txt.write("For DetId %s:\n" %i)
            for j in li2: 
                txt.write(" %s is: %s \n" % (j,HVInfoDictF.HVInfoDict[i][j]))
        print "A file named InfoModuleHV.txt has been created"
    #a file with the modules associated to some values
    if options.see_and and options.filenameva: 
     
        txt_1=open(options.filenameva,'w')
        li3=options.see_and
        for k in li3:
            txt_1.write("The modules with property %r are:\n" % k)
            for l in HVInfoDictF.HVInfoDict:
                for m in HVInfoDictF.HVInfoDict[l]:
                    if HVInfoDictF.HVInfoDict[l][m]==k:
                        txt_1.write("%s\n" % l)
        print "A file named %r has been created"%options.filenameva
   #######tracker map to some modules 
    if options.vatrcm:
        txt=open('filevamod.txt','w')
        li1=options.vatrcm
        color_list=[" 0 255 0"," 0 0 255"," 255 0 0"," 255 255 0"," 255 0  255"," 0 255 255"," 0 102 0"," 102 0 102"," 47 79 79"," 255 140 0"]
        detlist=[]
        for k in li1:
            for l in HVInfoDictF.HVInfoDict:
                for m in HVInfoDictF.HVInfoDict[l]:
                    if HVInfoDictF.HVInfoDict[l][m]==k:
                        detlist.append(l) 
                        u=str(l)+color_list[li1.index(k)]

                        if detlist.count(l)>1:
                            b=u.replace(str(l)+color_list[li1.index(k)],str(l)+color_list[-1])
                            txt.write(b+"\n")
                        else:
                            txt.write(u+"\n")
                        
        txt.close()
        color_list = ["green","blue","red","yellow","magenta","light blue","dark green","purple","grey","orange"]
        variable =""

        for i,j in zip (li1,color_list):
            variable+='%s=%s  ' % (i,j)
        os.system('print_TrackerMap filevamod.txt "value: %r for file %r,orange is for modules in common" %r 2400 False True 999 -999' % (variable,filenameC,options.fnmodtov))       
       
    #a file with the modules associated to some values simmultaneously
 
    if options.read_and and options.filenameco:
        txt = open(options.filenameco,'w')
        li1=options.read_and
        objectives=[]
        txt.write("The modules in common for values: ")
        [txt.write("%s, "%x) for x in li1]
        keys=set([])
        for j in HVInfoDictF.HVInfoDict.keys():
            for k in HVInfoDictF.HVInfoDict[j].keys():
                for proper in range(len(li1)):
                    if HVInfoDictF.HVInfoDict[j][k] in li1[proper]:
                        keys.add(k)
        listk=list(keys)
        lispr=[]
        #for proper in range(len(li1)):
        #    lispr.append(li1[proper])
        for i in HVInfoDictF.HVInfoDict:
            flag=True 
            for j in HVInfoDictF.HVInfoDict[i]:
                for proper in range(len(keys)):
                    
                    if HVInfoDictF.HVInfoDict[i][listk[proper]]!=li1[proper]:
                        flag=False
            if flag:
                        txt.write("\n"+i)
                        objectives.append(j)


        txt.close  
        print "A file named %s has been created"%options.filenameco
  
##########HERE WE INTRODUCE THE OPTIONS FOR THE INFO#######################33
if __name__ == "__main__":
    verbose = True
    usage = "useage: %prog [options] "
    parser = OptionParser(usage)
    parser.set_defaults(mode="advanced")
    parser.add_option("-f", "--file", type="string", dest="filenameC", help="Write the run of the cabling file")
    parser.add_option("--fu", "--fileu", type="string", dest="fileurl", help="write the link to the cabling file beggining with: SiStripFedCabling_...CablingInfoRun_X.txt")

    #############these options are fot getting the info of the cabling file####################################
    parser.add_option("-a","--imod2",type="string", dest="listrc2", help="List of DetIds of the cabling file in a txt, write the name of the file")

    parser.add_option("--at","--imod",type="string", dest="listrc", help="List of DetIds of the cabling file in a txt file and a trackermap, write the name of the image(.png)")

    parser.add_option("-z","--lisf",action="callback", callback = cb, dest="lisfem", help="Modules associated to a(some) Fed(s),write the Feds  whereof you want to know the modules associated")
    parser.add_option("--zi","--fnaf",type="string",dest="fnafe",help="Write the name of the file with the modules associated to a(some) Fed(s)")


    parser.add_option("-b","--data",action="callback", callback=cb, dest="lisfetrc", help="Tracker map of DetIds connected to some FEDs to locate them in the detector, write -b followed by the FedIds")
    parser.add_option("--bf","--dataf",type="string", dest="fnmodtof", help="name of the trackermap (name.png)")

    parser.add_option("-c","--modul",action="callback", callback=cb, dest="lismod", help="Information about a(some) module(s),write the modules")
    parser.add_option("--cp","--pairs",action="callback",callback=cb,dest="pairnumb",help="write the pairnumber of the module(s) selected, write the pair number 0,1 or 3, or the three of them")
    parser.add_option("--ci","--infom",action="callback",callback=cb, dest="infmod", help="write what you want to know about the modules introduced,FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD")

    parser.add_option("-g","--feds",action="callback", callback=cb, dest="lisfed", help="Information about a(some) Fed(s),write the FedIds")
    parser.add_option("--gf","--fedch",action="callback",callback=cb,dest="fedc",help="write the FedCh of the Fed(s) selected")
    parser.add_option("--gi","--infof",action="callback",callback=cb, dest="infed", help="write what you want to know about the Fed(s) introduced,FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD")
     
    parser.add_option("-d","--infom2",action="callback",callback=cb, dest="infomod2", help="info  you want to know the modules associated to, like:FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD")
    parser.add_option("--di","--infom3",action="callback",callback=cb, dest="infomod3", help="write the number belonging to the info given in -d, like FedCrate 23 or CcuAddr 123 (just write the number)")

    parser.add_option("-n","--cabc1",action="callback",callback=cb, dest="cabcommon1", help="if you want to know the modules in common for several info of the cabling,FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD")
    parser.add_option("--ni","--cabc2",action="callback",callback=cb, dest="cabcommon2", help="here goes the number of the property")

 

    ########these options are for the alias#############################################

    parser.add_option("-k","--fila",type="string", dest="fialc", help="Dump the Alias of the DetIds of the Cabling file in a txt file, write the name of the file")
    parser.add_option("-l","--alim",action="callback", callback=cb, dest="alimod", help="Know the Alias of a (set of) module(s),write the modules")
    
    parser.add_option("-m","--moda",action="callback", callback=cb, dest="modali", help="Know the modules associated to some Alias,write the Alias or something like: from TEC, TECmi, TECminus_7,TECminus_7_5 etc")
    parser.add_option("--mf","--filn",type="string",dest="filena",help="write the name of the file with the modules associated to some alias")
   
    parser.add_option("-y","--altk",action="callback",callback=cb,dest="alitkm",help="write the alias where of you want a trackermap of detids associated to those alias")
    parser.add_option("--yf","--fnma",type="string",dest="fnaltomod",help="write the name of the image(name.png) ")


    parser.add_option("-o","--modi",action="callback",callback=cb,dest="modinf",help="write the modules to know if they are located on certain subdetector")
    parser.add_option("--os","--subi",action="callback",callback=cb, dest="subinf", help="write the subdetector in order to know if the module is located there")

    ################these options are for the hv#######################
    
    parser.add_option("-r","--inmod",action="callback", callback = cb, dest="search_and", help="write the modules in order to get some info")
    parser.add_option("--ri","--datas",action="callback", callback = cb, dest="look_and", help="write the options of the Info about a (set of) module(s),like PSUName,Cmstrk,Crate,Board,Branch,TrackerSY,Channel")

    parser.add_option("-t","--values",action="callback", callback = cb, dest="see_and", help="Modules associated to a(some) value(s),write the values whereof you want to know the modules associated,like cms_trk_dcs_05:CAEN (from 02 to 05), CMS_TRACKER_SY1527_8 (from 1 to 9),branchController05 (from 02 to 05),easyCrate3 (from 1 to 5), easyBoard06 (from 01 to 17), channel002 (002 or 003)")
    parser.add_option("--tf","--names",type="string",dest="filenameva",help="Write the name of the file with the modules associated to some values")
   
    parser.add_option("-v","--trvac",action="callback",callback=cb,dest="vatrcm",help="Trackermap of the modules of certain values (those in option t)")
    parser.add_option("--vf","--fnmv",type="string",dest="fnmodtov",help="name of the Tracker map image  for modules associated to some hv (.png)")

    parser.add_option("-w","--common", action="callback",callback=cb, dest="read_and", help="Values with modules in common, those in option -t")
    parser.add_option("--wf","--common2", type="string", dest="filenameco", help="Name of file for Values with modules in common")
  
    #################other info#################

    parser.add_option("-e","--alcab1", action="callback",callback=cb, dest="aliascab1", help="write the property to know the location in the detector:value of the cabling,FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD")
    parser.add_option("--en","--alcab2", action="callback",callback=cb, dest="aliascab2", help="here goes the number of the property")

    parser.add_option("-i","--alcab3", action="callback",callback=cb, dest="aliascab3", help="write the property to know the location in the detector:value of the cabling,FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD")
    parser.add_option("--in","--alcab4", action="callback",callback=cb, dest="aliascab4", help="here goes the number of the property")
    parser.add_option("--ia","--alcab5", action="callback",callback=cb, dest="aliascab5", help="here goes the subdetector whereof you want to know if the module with the property chosen is there")

    parser.add_option("-j","--cabalj", action="callback",callback=cb, dest="cabalias1", help="here goes the alias whereof you want to know the info cabling")
    parser.add_option("--ja","--cabalj2", action="callback",callback=cb, dest="cabalias2", help="here goes the info you want to know like:FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD ")

    parser.add_option("-p","--alhv", action="callback",callback=cb, dest="aliashv", help="to know the alias of the modules with hv -p property, write the hv property, like those in option -t ")


    parser.add_option("-q","--hval1", action="callback",callback=cb, dest="hvalias1", help="to know the alias of modules with certain property of HV, write the alias you want to know ")
    parser.add_option("--qi","--hval2", action="callback",callback=cb, dest="hvalias2", help="write the hv property,PSUName,Cmstrk,Crate,Board,Branch,TrackerSY,Channel")


    parser.add_option("-s","--hvca1", action="callback",callback=cb, dest="hvcab1", help="write the cabling info you know, like: FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD ")
    parser.add_option("--sc","--hvca2", action="callback",callback=cb, dest="hvcab2", help="write the number of the cabling info like: FecRing 34 FedCrate 23(just write the number, on option s you write the number of the property ")
    parser.add_option("--sh","--hvca3", action="callback",callback=cb, dest="hvcab3", help="write the hv info you want to know, like:,PSUName,Cmstrk,Crate,Board,Branch,TrackerSY,Channel" )

    parser.add_option("-u","--cahv1", action="callback",callback=cb, dest="cabhv1", help="write the hv property you know , like:cms_trk_dcs_05:CAEN (from 02 to 05), CMS_TRACKER_SY1527_8 (from 1 to 9),branchController05 (from 02 to 05),easyCrate3 (from 1 to 5), easyBoard06 (from 01 to 17), channel002 (002 or 003)")  
    parser.add_option("--uc","--cahv2", action="callback",callback=cb, dest="cabhv2", help="to know cabling info of modules with certain property of HV, write the cabling info you want to know, like: FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD")
 
    parser.add_option("--cd","--cabha1", action="callback",callback=cb, dest="cabhvals1", help="to know alias info given cabling and hv info, write the cabling info you want to know, like: FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD") 
    parser.add_option("--cn","--cabhv2", action="callback",callback=cb, dest="cabhvals2", help="write the number of cabling info in option -x")
    parser.add_option("--ch","--cabhv3",action="callback",callback=cb,dest="cabhvals3",help="write hv info you know like: cms_trk_dcs_05:CAEN (from 02 to 05), CMS_TRACKER_SY1527_8 (from 1 to 9),branchController05 (from 02 to 05),easyCrate3 (from 1 to 5), easyBoard06 (from 01 to 17), channel002 (002 or 003)")

    parser.add_option("--hd","--hac1", action="callback",callback=cb, dest="hvalscab1", help="Write the hv data you know, like channel002,branchController05,etc")     
    parser.add_option("--ha","--hac2", action="callback",callback=cb, dest="hvalscab2", help="Write the alias you know")
    parser.add_option("--hc","--hac3", action="callback",callback=cb, dest="hvalscab3", help="write the cabling info you want to know, like FeChan,FedCh,FecCrate,FecSlot,etc ")

    parser.add_option("--ad","--ach1", action="callback",callback=cb, dest="cabalshv1", help="Write the alias data you know, like TEC,TECm,TECminus_5_6,etc")     
    parser.add_option("--ac","--ach2", action="callback",callback=cb, dest="cabalshv2", help="Write the cabling info like in option --cd,CcuAddr,CcuChan,DcuId,etc ")
    parser.add_option("--an","--ach3", action="callback",callback=cb, dest="cabalshv3", help="write the numer of the cabling property in option --ac (for example 123 for CcuAddr, 26 for CcuChan, etc ")
    parser.add_option("--ah","--ach4", action="callback",callback=cb, dest="cabalshv4", help="Write the hv  info like in option you want to know --cd,CcuAddr,CcuChan,DcuId,etc ")

    (options, args) = parser.parse_args()
    if (options.filenameC is None and options.fileurl is None):
        url = "https://test-stripdbmonitor.web.cern.ch/"
        path = "test-stripdbmonitor/CondDBMonitoring/cms_orcoff_prod/CMS_COND_31X_STRIP/DBTagCollection/SiStripFedCabling/SiStripFedCabling_GR10_v1_hlt/CablingLog/"
        cablingfile = getLatestCabling()
        urllib.urlretrieve(url+path+cablingfile,cablingfile)
        
        ourdictionary=DictionaryCab(cablingfile,options)
        #options.filenameC = cablingfile

        StripDetIDAliasDict=pickle.load(open(os.getenv("CMSSW_RELEASE_BASE")+"/src/CalibTracker/SiStripDCS/data/StripDetIDAlias.pkl"))

        MyAlias=AliasFun(cablingfile,options,StripDetIDAliasDict)

        MyCabList=DetIdCabL(cablingfile)

        fileCab1= 'DetIdCab.txt'
        fileHV1='/afs/cern.ch/cms/slc5_amd64_gcc481/cms/cmssw/CMSSW_7_0_4/src/CalibTracker/SiStripDCS/data/StripPSUDetIDMap_BeforeJan132010.dat' 
    
        MyCabHV=CabHVFiles(fileCab1,fileHV1)
        input5='file.txt'
        MyHVDict = HVInfoDictF(input5, options)

    

    #########HERE ALL THE FUNCTIONS ARE CALLED 
    if options.filenameC:
        MyFilename=filenameF(options.filenameC)
    
    ## for the alias
        StripDetIDAliasDict=pickle.load(open(os.getenv("CMSSW_RELEASE_BASE")+"/src/CalibTracker/SiStripDCS/data/StripDetIDAlias.pkl"))

        MyAlias=AliasFun(MyFilename,options,StripDetIDAliasDict)

  
    ##for the dictionary of the cabling file
        ourdictionary=DictionaryCab(MyFilename,options)
     ##for the HV
        MyCabList=DetIdCabL(MyFilename)
        fileCab1= 'DetIdCab.txt'
        fileHV1='/afs/cern.ch/cms/slc5_amd64_gcc481/cms/cmssw/CMSSW_7_0_4/src/CalibTracker/SiStripDCS/data/StripPSUDetIDMap_BeforeJan132010.dat' 
        MyCabHV=CabHVFiles(MyCabList,fileHV1)
        input5='file.txt'
        MyHVDict = HVInfoDictF(MyFilename,input5, options)
   

    if options.fileurl:

        Mylink=semilinkF(options.fileurl)
            
    ## for the alias
        StripDetIDAliasDict=pickle.load(open(os.getenv("CMSSW_RELEASE_BASE")+"/src/CalibTracker/SiStripDCS/data/StripDetIDAlias.pkl"))

        MyAlias=AliasFun(Mylink,options,StripDetIDAliasDict)

  
    ##for the dictionary of the cabling file
        ourdictionary=DictionaryCab(Mylink,options)
     ##for the HV
        MyCabList=DetIdCabL(Mylink)
        fileCab1= 'DetIdCab.txt'
        fileHV1='/afs/cern.ch/cms/slc5_amd64_gcc481/cms/cmssw/CMSSW_7_0_4/src/CalibTracker/SiStripDCS/data/StripPSUDetIDMap_BeforeJan132010.dat' 
        MyCabHV=CabHVFiles(fileCab1,fileHV1)
        input5='file.txt'
        MyHVDict = HVInfoDictF(Mylink,input5, options)
   

####These options are to get information from one source to another ###########

           #####To know the alias of modules with certain info of the cabling file  
    if options.aliascab1 and options.aliascab2: 
    
        li1=options.aliascab1
        li2=options.aliascab2
        txt=open('AliasforCabling.txt','w')
        listx=[set() for x in range(len(li1))]
        for k,i,y in zip(li1,li2,listx):
            for j in DictionaryCab.CablingInfoDict:
                for l in DictionaryCab.CablingInfoDict[j]:
                    if DictionaryCab.CablingInfoDict[j][l][k]==i:
                       y.add(l)
        for k,i,y in zip(li1,li2,listx):
            txt.write("The Alias of modules with %s:%s are: \n\n" %(k,i))
            for x in y:
                beta=str(AliasFun.SAliasDict[int(x)]).split("'")[1]
                txt.write(x+"  "+beta+"\n")
                        
        print "A txt file named AliasforCabling.txt has been created"

   ########To know the alias of modulos with certain info of the HV######
    if options.aliashv:
        li1=options.aliashv
        txt=open('aliastohv.txt','w')
        for j in li1:  
            txt.write("The Alias of modules with %s are: \n"%j)
            for k in HVInfoDictF.HVInfoDict:
                for m in HVInfoDictF.HVInfoDict[k]:
                    if  HVInfoDictF.HVInfoDict[k][m]==j:
                        beta="" 
                        beta=str(AliasFun.SAliasDict[int(k)]) 
                        txt.write( "%s  %s \n " %(k,beta.split("'")[1]))
                    
        print "A file named aliastohv.txt with the alias of modules has been created" 

           #########To know if modules with certain cabling info are in certain subdetector
    if options.aliascab3 and options.aliascab4: 
    
        li1=options.aliascab3
        li2=options.aliascab4
        li3=options.aliascab5
        txt=open('CabinSubdector.txt','w')
        listx=[set() for x in range(len(li1))]
        for k,i,x in zip(li1,li2,listx):  
            for j in DictionaryCab.CablingInfoDict:
                for m in DictionaryCab.CablingInfoDict[j]:
                    if DictionaryCab.CablingInfoDict[j][m][k]==i:
                       x.add(j)
                        
        for k,i,x in zip(li1,li2,listx):
            txt.write('For modules with %s:%s\n'%(k,i))
            for y in x:
                beta6= str(AliasFun.SAliasDict[int(y)])
                for o in li3:
                    if o in beta6:
                        txt.write("For DetId %r True % r\n " %(y,o))
                    if o not in beta6:
                        txt.write("For DetId %r false %r\n " %(y,o))
        print "A file named CabinSubdector.txt has been created"
           ################To know the cabling info of modules with certain alias
    if options.cabalias1 and options.cabalias2:
        li1=options.cabalias1
        li2=options.cabalias2
        txt=open('CabofAlias.txt','w') 
        beta3=""
        listx=[set() for x in range(len(li2))]
        listals=set([])
        listcab=set([])
        for i in li1:
            for j in AliasFun.SAliasDict:
                beta3 = str(AliasFun.SAliasDict[j])
                if i in beta3:
                    listals.add(j)
        for k in li2:
            for l in li1:
                txt.write("The %s for modulues with Alias %s is:\n" %(l,k))
                for j in listals:
                    for m in DictionaryCab.CablingInfoDict[str(j)]:
                        listcab.add(str(int(DictionaryCab.CablingInfoDict[str(j)][str(m)][k],16)))
                    for n in listcab:
                        txt.write("\n"+str(j)+"  "+n)

              
        print "A txt file CabofAlias.txt with the modules and cabling info has been created"
        
         ########### to know hv info of modules with certain alias##########################
    if options.hvalias1 and options.hvalias2:

        li1=options.hvalias1
        li2=options.hvalias2
        txt=open('hvofalias.txt','w') 
        beta=""
        list1=[]
        for i,j in zip(li1,li2):
            txt.write("The %s for modulues with Alias %s is:\n" %(j,i))
            for k in AliasFun.SAliasDict:
                beta = str(AliasFun.SAliasDict[k])
                if i in beta and k not in list1:
                    list1.append(k)
                    txt.write("%s %s\n"%(str(k),HVInfoDictF.HVInfoDict[str(k)][j]))
        print "A txt file hvofalias.txt with the modules and cabling info has been created" 
         ################# to know hv info of modules with certain cabling info
    if options.hvcab1 and options.hvcab2:

        li1=options.hvcab1
        li2=options.hvcab2
        li3=options.hvcab3
        
        txt=open('hvofcab.txt','w') 
        listx=[set() for x in range(len(li1))]
        for i,j,x in zip(li1,li2,listx):
            for l in DictionaryCab.CablingInfoDict:
                for m in DictionaryCab.CablingInfoDict[str(l)]:                            
                    if  DictionaryCab.CablingInfoDict[str(l)][m][i]==j :
                        x.add(l)
                        
        
        for i,j,x in zip(li1,li2,listx):
            txt.write('The hv info for modules with %s:%s \n' %(i,j))
            for k in li3:
                for y in x:
                    txt.write(y+" "+HVInfoDictF.HVInfoDict[str(y)][k]+"\n")

        print "A file named hvofcab.txt with has been created "
       


 ################To know the cabling info of modules with certain hv

    if options.cabhv1 and options.cabhv2:
        li1=options.cabhv1
        li2=options.cabhv2
       
        txt=open('Cabofhv.txt','w')
        listhv=[set() for y in range(len(li1))]
        listx=[set() for x in range(len(li1))]
      
        for i,j in zip(li1,listhv):
            for k in HVInfoDictF.HVInfoDict:
                for l in HVInfoDictF.HVInfoDict[k]:
                    if HVInfoDictF.HVInfoDict[k][l]==i:
                        j.add(k)
        
        for x,z in zip(listhv,listx):
            for l in li2:
                for y in x:
                    for j in DictionaryCab.CablingInfoDict[y]:
                        z.add((y,l+ DictionaryCab.CablingInfoDict[y][j][l]))
        for i,n in zip(listx,li1):
            txt.write("For modules with %s \n"%n)
            for j,k in i:
                    txt.write(j+" "+k+"\n")
                  
 
        print ("A txt file Cabofhv.txt with the modules and cabling info has been created")

####################Now info between two and a third info######################33

#### to know alias given cabling and hv

if options.cabhvals1:       

    li1=options.cabhvals1
    li2=options.cabhvals2
    li3=options.cabhvals3
    cab=set([])
    hv=set([])
    valhv=set([])
    txt=open('cabhvtoals.txt','w')
    txt2=open('cabhv.txt','w')
    txt.write('The alias of Modules with cab and hv values:\n')
    txt2.write('The modules in common for cab and hv values:\n')
    for i,j in zip(li1,li2):
        txt.write(i+" "+j+" ")
        txt2.write(i+" "+j+" ")
    for h in li3:
        txt.write(" "+h+":\n")
    cabpr=[]
    for proper in range(len(li2)):
        cabpr.append(li2[proper])
    
    for x in li1:
        for k in DictionaryCab.CablingInfoDict.keys():
            flag = True
            for l in DictionaryCab.CablingInfoDict[k].keys():
                if DictionaryCab.CablingInfoDict[k][l][x] not in cabpr:
                    flag = False
            if flag:
                cab.add(k)
          
    for j in HVInfoDictF.HVInfoDict.keys():
        for k in HVInfoDictF.HVInfoDict[j].keys():
            for proper in range(len(li3)):
                if HVInfoDictF.HVInfoDict[j][k] in li3[proper]:
                    valhv.add(k)
                
    lispr=[]
    for proper in range(len(li3)):
        lispr.append(li3[proper])
    for x in valhv:
        for j in HVInfoDictF.HVInfoDict.keys():
            flag=True
            if HVInfoDictF.HVInfoDict[j][x] not in lispr:
                flag=False
            if flag:
               hv.add(j)
    print lispr        
    u=cab & hv
    for i in u:
        beta=str(AliasFun.SAliasDict[int(i)])
        txt.write("%s  %s\n" %(i,beta.split("'")[1]))
        txt2.write("\n"+i)
    print "A file named cabhvtoals.txt with the alias of modules and a file named cabhv.txt with the modules in common to cabling and hv introduced have been created"

    #######to know cabling given hv and alias   

if options.hvalscab1 and options.hvalscab2:
    li1=options.hvalscab1 
    li2=options.hvalscab2
    li3=options.hvalscab3
   
    als=set([])
    hv=set([])
    valhv=set([])
    txt=open('hvalscab.txt','w')
    txt2=open('hvals.txt','w')
    txt.write('The cabling info of Modules with hv  and alias values:  ')
    txt2.write('The modules in common for hv and alias values:')   
    for j in HVInfoDictF.HVInfoDict.keys():
        for k in HVInfoDictF.HVInfoDict[j].keys():
            for proper in range(len(li1)):
                if HVInfoDictF.HVInfoDict[j][k]== li1[proper]:
                    valhv.add(k)
                    
        
    lispr=[]       
    for proper in range(len(li1)):
       lispr.append(li1[proper])
    for x in valhv:
        for j in HVInfoDictF.HVInfoDict.keys():
            flag=True
            if HVInfoDictF.HVInfoDict[j][x] in lispr: 
                flag=False
            if flag:
                hv.add(j)
                
 
    for j in li2:
        for detid in AliasFun.SAliasDict.keys():
            beta3 = str(AliasFun.SAliasDict[detid])
            if j in beta3:
                als.add(str(detid))
                              

    u=als & hv


    for i in li1:
        txt.write(i+" ")
        txt2.write(i+" ")
    for j in li2:
        txt.write(" "+j)
        txt2.write(" "+j)
    for l in li3:
        txt.write("\n\t"+l+" is: \n")
        for m in u:
            for n in DictionaryCab.CablingInfoDict[m]:
                txt.write(m+" "+DictionaryCab.CablingInfoDict[m][n][l]+"\n")
            txt2.write("\n"+m)
    print "two files named hvalscab.txt (with cabling info of modules with hv and alias introduced) and hvals.txt (with modules in common for hv and alias values introduced) have been created"               


 ####To know hv known alias and cabling
if options.cabalshv1 and options.cabalshv2:
    
    li1=options.cabalshv1 
    li2=options.cabalshv2
    li3=options.cabalshv3
    li4=options.cabalshv4
    als=set([])
    hv=set([])
    cab=set([])
    txt=open('cabalshv.txt','w')
    txt.write('The hv info of Modules with cabling  and alias values:  ')

    for j in li1:
        for detid in AliasFun.SAliasDict.keys():
            beta3 = str(AliasFun.SAliasDict[detid])
            if j in beta3:
                als.add(str(detid)) 
                
    liscab=[]
    for proper in range(len(li3)):
        liscab.append(li3[proper])
    
    for x in li2:
        for k in DictionaryCab.CablingInfoDict.keys():
            flag = True
            for l in DictionaryCab.CablingInfoDict[k].keys():
                    if DictionaryCab.CablingInfoDict[k][l][x] not in liscab:
                        flag = False
            if flag:
                cab.add(k)        
                
    u=als & cab
    txt2=open('cabals.txt','w')
    txt2.write('The modulos in common for cabling and alias values introduced:')
    for i in li1:
        txt.write(i+" ")
        txt2.write(i+" ")
    for j,k in zip(li2,li3):
        txt.write(" "+j+" "+k)
        txt2.write(" "+j+" "+k)
    for l in li4:
        txt.write("\n\t"+l+" is: \n")
        for m in u:   
            txt.write(m+" "+HVInfoDictF.HVInfoDict[m][l]+"\n")
            txt2.write("\n"+m)
    print "two files named cabalshv.txt and cabals.txt have been created"
    
    
