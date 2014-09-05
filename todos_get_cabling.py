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
   return cabfile
       
###this function makes a dictionary of Detids(with pairnumber as secondkey) and a dictionary of FEDs (with FecCH as second key) for the cabling file 
def DictionaryCab(filenameC,options):
    """This function takes a filename as input and looks for it in the URL, then makes a dictionary with DetId as key and pairnumber as key2 or FEDid as key1 and FedCh as key2"""
    url='https://test-stripdbmonitor.web.cern.ch/test-stripdbmonitor/CondDBMonitoring/cms_orcoff_prod/CMS_COND_31X_STRIP/DBTagCollection/SiStripFedCabling/SiStripFedCabling_GR10_v1_hlt/CablingLog/'

    urllib.urlretrieve(url+filenameC, filenameC)
    if verbose:
        print "Will process cabling file at\n%s"%(url+filenameC)
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
            DcuIdList.append(pattern[3])
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
    #dump the detids of the cabling file in a txt file and make a trackermap
    if options.listrc:
        archi=open(options.listrc,'w')
        for p in DictionaryCab.CablingInfoDict.keys():
            archi.write(str(int(p,16)))
            archi.write(" "+"255"+" "+ "0"+" "+"0")
            archi.write('\n')
        archi.close
        os.system('print_TrackerMap options.listrc TrackerMap TrackermapDetIds.png 2400 False True 999 -999')
        print "A file named %r and a tracker map named TrackermapDetIds.png have been created" %options.listrc
   
   #A file with the DetIds associated to a(some) FED(s)	
    if options.lisfem and options.fnafe:
        archi1=open(options.fnafe,'w')
        lif1=options.lisfem
        for p in lif1:
            archi1.write("The modules associated to FED %s are:\n" %p )
            for q in CablingInfoDictF[p].keys():
                archi1.write(str(int(CablingInfoDictF[p][q]["DetId"],16))+"\n")


   # A Trackermap of the detids associated to a (some) Fed(s)
    if options.lisfetrc:
        archi=open('ModulestoFeds.txt','w')
        inputfedid_list=options.lisfetrc
        j=0
        for p in inputfedid_list:
            j+=1
            if j==1: 
                for q in CablingInfoDictF[p].keys():
                    archi.write(str(int(CablingInfoDictF[p][q]["DetId"],16)))
                    archi.write(" "+"0"+" "+ "255"+" "+"0"+"\n")
            if j==2:
                for q in CablingInfoDictF[p].keys():
                    archi.write(str(int(CablingInfoDictF[p][q]["DetId"],16)))
                    archi.write(" "+"0"+" "+ "0"+" "+"255"+"\n")
            if j==3:
                for q in CablingInfoDictF[p].keys():
                    archi.write(str(int(CablingInfoDictF[p][q]["DetId"],16)))
                    archi.write(" "+"255"+" "+ "0"+" "+"0"+"\n")
            if j==4:
                for q in CablingInfoDictF[p].keys():
                    archi.write(str(int(CablingInfoDictF[p][q]["DetId"],16)))
                    archi.write(" "+"255"+" "+ "255"+" "+"0"+"\n")
            if j==5:
                for q in CablingInfoDictF[p].keys():
                    archi.write(str(int(CablingInfoDictF[p][q]["DetId"],16)))
                    archi.write(" "+"255"+" "+ "0"+" "+"255"+"\n")
            if j==6:
                for q in CablingInfoDictF[p].keys():
                    archi.write(str(int(CablingInfoDictF[p][q]["DetId"],16)))
                    archi.write(" "+"0"+" "+ "255"+" "+"255"+"\n")
            if j==7:
                for q in CablingInfoDictF[p].keys():
                    archi.write(str(int(CablingInfoDictF[p][q]["DetId"],16)))
                    archi.write(" "+"0"+" "+ "102"+" "+"0"+"\n")
            if j==8:
                for q in CablingInfoDictF[p].keys():
                    archi.write(str(int(CablingInfoDictF[p][q]["DetId"],16)))
                    archi.write(" "+"102"+" "+ "0"+" "+"102"+"\n")
            if j==9:
                for q in CablingInfoDictF[p].keys():
                    archi.write(str(int(CablingInfoDictF[p][q]["DetId"],16)))
                    archi.write(" "+"0"+" "+ "0"+" "+"0"+"\n")
		
        
        archi.close()
        color_list = ["green","blue","red","yellow","magenta","light blue","dark green","purple","black"]
        variable =""


        for i,j in zip (inputfedid_list,color_list):
            variable+='%s=%s  ' % (i,j)
        os.system('print_TrackerMap ModulestoFeds.txt "FEDs: %s for file %s" %r  2400 False True 999 -999' % (variable,options.filenameC,options.fnmodtof))


    #Info about a (set of) module(s)
    if  options.lismod and options.pairnumb:
        li3=options.lismod
        li4=options.pairnumb
        li5=options.infmod
        for i,j in zip(li3,li4): 
            print "For DetID : %r with pairNumber: %r "%(i,j)
            for k in li5:
                print " %r is:%r "%(k,str(int(DictionaryCab.CablingInfoDict[i][j][k],16)))
               

    #info about a (set of) Fed(s)
    if options.lisfed and options.fedc:
        
        li3=options.lisfed
        li4=options.fedc
        li5=options.infed

        for l,m in zip(li3,li4):
            print "For FedId : %r with FedCh : %r "%(l,m)
            for n in li5:
                print " %r is:%r "%(n,CablingInfoDictF[l][m][n])

   #modules associated to something
    if options.infomod2 and options.infomod3:
      
        li6=options.infomod2
        li7=options.infomod3
        txt1=open('archivo.txt','r+')
        for k,i in zip(li6,li7):
            for j,l in DictionaryCab.CablingInfoDict.items():
                for m,n in l.items():
                    if j not in txt1 and DictionaryCab.CablingInfoDict[j][m][k]==i:
                        print j

####################3THESE INSTRUCTIONS ARE FOR GETTING THE INFO OF THE ALIAS ######################

   #A file with the alias of the detids of the cabling file   
    if options.fialc:
        beta1=""
        txt_1=open(options.fialc,'w')
        for detID in DictionaryCab.CablingInfoDict.keys():
            beta1 = str(StripDetIDAliasDict[int(detID)])
            txt_1.write("%s  %s\n"  %(detID,beta1.split("'")[1]))
   
    #the alias of a (set of) module(s)     
    if options.alimod:

        for i in options.alimod:
            beta2= str(StripDetIDAliasDict[int(i)])
            print "for module with DetId %r, Alias is %r" %(i,beta2.split("'")[1])

   #A file the modules associated to a certain Alias(es)
    if options.modali and options.filena:
        txt_2 = open (options.filena,'w')       
        beta3=""
        for j in options.modali:
            txt_2.write("For Alias %r, the DetIds associated are:\n" % j)
            for detid in StripDetIDAliasDict.keys():
                beta3 = str(StripDetIDAliasDict[detid])
                if j in beta3:
                    txt_2.write("%r \n" %detid)

    #A tracker map of the modules associated to an alias
    if options.alitkm:
        txt_4=open('faliastkm.txt','w')
        li4=options.alitkm
        beta4=""
        j=0
        for k in li4:
            j+=1
            if j==1: 
                for detid in  StripDetIDAliasDict.keys():
                    beta4=str(StripDetIDAliasDict[detid]) 
                    if k in beta4:
                        txt_4.write("%r"%detid+" "+"0"+" "+ "255"+" "+"0"+"\n")
            if j==2:
                for detid in StripDetIDAliasDict.keys():
                    beta4=str(StripDetIDAliasDict[detid])
                    if k in beta4:
                        txt_4.write("%r"%detid+" "+"0"+" "+ "0"+" "+"255"+"\n")
            if j==3:
                for detid in StripDetIDAliasDict.keys():
                    beta4=str(StripDetIDAliasDict[detid])
                    if k in beta4:
                        txt_4.write("%r"%detid+" "+"255"+" "+ "0"+" "+"0"+"\n")
            if j==4:
                for detid in StripDetIDAliasDict.keys():
                    beta4=str(StripDetIDAliasDict[detid])
                    if k in beta4:
                        txt_4.write("%r"%detid+" "+"255"+" "+ "255"+" "+"0"+"\n")
            if j==5:
                for detid in StripDetIDAliasDict.keys():
                    beta4=str(StripDetIDAliasDict[detid])
                    if k in beta4:
                        txt_4.write("%r"%detid+" "+"255"+" "+ "0"+" "+"255"+"\n")
            if j==6:
                for detid in StripDetIDAliasDict.keys():
                    beta4=str(StripDetIDAliasDict[detid])
                    if k in beta4:
                        txt_4.write("%r"%detid+" "+"0"+" "+ "255"+" "+"255"+"\n")
            if j==7:
                for detid in StripDetIDAliasDict.keys():
                    beta4=str(StripDetIDAliasDict[detid])
                    if k in beta4:
                        txt_4.write("%r"%detid+" "+"0"+" "+ "102"+" "+"0"+"\n")
            if j==8:
                for detid in StripDetIDAliasDict.keys():
                    beta4=str(StripDetIDAliasDict[detid])
                    if k in beta4:
                        txt_4.write("%r"%detid+" "+"102"+" "+ "0"+" "+"102"+"\n")
            if j==9:
                for detid in StripDetIDAliasDict.keys():
                    beta4=str(StripDetIDAliasDict[detid])
                    if k in beta4:
                        txt_4.write("%r"%detid+" "+"0"+" "+ "0"+" "+"0"+"\n")
		
        
        txt_4.close()
        color_list = ["green","blue","red","yellow","magenta","light blue","dark green","purple","black"]
        variable =""


        for i,j in zip (li4,color_list):
            variable+='%s=%s  ' % (i,j)
        os.system('print_TrackerMap faliastkm.txt "value: %r for file %r" %r 2400 False True 999 -999' % (variable,options.filenameC,options.fnaltomod))                      
   ##To know if a module is or is not in a detector or subdetector
    if options.modinf and options.subinf:

        for k in options.modinf:
            for l in options.subinf:
                beta6= str(StripDetIDAliasDict[int(k)])
                if l in beta6:
          
                    print "For DetId %r True % r " %(k, beta6.split("'")[1].split("_")[0])

                if l not in beta6:
                    print "For DetId %r false %r " %(k, beta6.split("'")[1].split("_")[0])

    return DictionaryCab



####THE NEXT FUNCTIONS ARE FOR GETTING THE INFO OF THE HV#########


#function to extract the Detids of the cabling file in a txt file
def DetIdCabL(filenameC,verbose=True):                                                 
    """This function takes a filename as input and looks for it in URL ... ,
    it parses all detIDs and dumps them in a local file named detIdCab.txt""" 
    #url1="https://test-stripdbmonitor.web.cern.ch/test-stripdbmonitor/CondDBMonitoring/cms_orcoff_prod/CMS_COND_31X_STRIP/DBTagCollection/SiStripFedCabling/SiStripFedCabling_GR10_v1_hlt/CablingLog/"
    #urllib.urlretrieve(url1+filenameCab,filenameCab)
    #if verbose:
    #     print "Will process cabling file at:\n%s"%(url1+filenameC)
    FileCabList = open(filenameC,'r')
    D = "DcuId/DetId" 
    DetIdCabList = []
    for line1 in FileCabList:                                                                                                           
        if D in line1:
            pattern1 = re.split('\W+',line1)
            if (int(pattern1[4],16)) not in DetIdCabList:
                DetIdCabList.append(int(pattern1[4],16))  
    txtCab=open("DetIdCab.txt",'w')
    for i in DetIdCabList:
        txtCab.write("%r\n" %i)
#function to make a PSUName file of the cabling file

def CabHVFiles(fileCab,fileHV,verbose=True):
    sep = " "
    d = {}
    print "Reading PSUName mapping information from file "
    for line in  open(fileHV, "r"):
        key, val = line.strip().split(sep)
        d[key] = val
    detIDs=[line.strip() for line in open(fileCab, "r")] 
    OutFile=open('file.txt','w')
    for detID in detIDs:
        OutFile.write("%s %s\n" % (detID,d[detID]))

#function to make the dictionary of the psuname file of the cabling file

def HVInfoDictF(filename, options):
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
        for i in li1:
            print "For DetId %r:" %i
            for j in li2: 
                print " %r is: %r" % (j,HVInfoDictF.HVInfoDict[i][j])
    #a file with the modules associated to some values
    if options.see_and and options.filenameva: 
        txt_1=open(options.filenameva,'w')
        li3=options.see_and
        for k in li3:
            txt_1.write("\t\n The modules with property %r are:\n" % k)
            for l,m in HVInfoDictF.HVInfoDict.items():
                if k in m.values():
                    txt_1.write("\n %s" % l)
    #a tracker map of the modules associated to some values
    if options.vatrcm:
        txt_1=open('filevamod.txt','w')
        li1=options.vatrcm
        j=0
        for k in li1:
            j+=1
            if j==1: 
                for l,m in HVInfoDictF.HVInfoDict.items():
                    if k in m.values():
                        txt_1.write(l+" "+"0"+" "+ "255"+" "+"0"+"\n")
            if j==2:
                for l,m in HVInfoDictF.HVInfoDict.items():
                    if k in m.values():
                        txt_1.write(l+" "+"0"+" "+ "0"+" "+"255"+"\n")
            if j==3:
                for l,m in HVInfoDictF.HVInfoDict.items():
                    if k in m.values():
                        txt_1.write(l+" "+"255"+" "+ "0"+" "+"0"+"\n")
            if j==4:
                for l,m in HVInfoDictF.HVInfoDict.items():
                    if k in m.values():
                        txt_1.write(l+" "+"255"+" "+ "255"+" "+"0"+"\n")
            if j==5:
                for l,m in HVInfoDictF.HVInfoDict.items():
                    if k in m.values():
                        txt_1.write(l+" "+"255"+" "+ "0"+" "+"255"+"\n")
            if j==6:
                for l,m in HVInfoDictF.HVInfoDict.items():
                    if k in m.values():
                        txt_1.write(l+" "+"0"+" "+ "255"+" "+"255"+"\n")
            if j==7:
                for l,m in HVInfoDictF.HVInfoDict.items():
                    if k in m.values():
                        txt_1.write(l+" "+"0"+" "+ "102"+" "+"0"+"\n")
            if j==8:
                for l,m in HVInfoDictF.HVInfoDict.items():
                    if k in m.values():
                        txt_1.write(l+" "+"102"+" "+ "0"+" "+"102"+"\n")
            if j==9:
                for l,m in HVInfoDictF.HVInfoDict.items():
                    if k in m.values():
                        txt_1.write(l+" "+"0"+" "+ "0"+" "+"0"+"\n")
		
        
        txt_1.close()
        color_list = ["green","blue","red","yellow","magenta","light blue","dark green","purple","black"]
        variable =""


        for i,j in zip (li1,color_list):
            variable+='%s=%s  ' % (i,j)
        os.system('print_TrackerMap filevamod.txt "value: %r for file %r" %r 2400 False True 999 -999' % (variable,options.filenameC,options.fnmodtov))       
       
    #a file with the modules associated to some values simmultaneously
 
    if options.read_and and options.filenameco:
        txt_2 = open(options.filenameco,'w')
        li4=options.read_and
        for n in HVInfoDictF.HVInfoDict:
            if len(set(li4).intersection(HVInfoDictF.HVInfoDict[n].values())) == len(li4):
                txt_2.write("%s\n" % n)
        txt_2.close  
    return HVInfoDictF.HVInfoDict  

##########HERE WE INTRODUCE THE OPTIONS FOR THE INFO#######################33
if __name__ == "__main__":
    verbose = True
    usage = "useage: %prog [options] "
    parser = OptionParser(usage)
    parser.set_defaults(mode="advanced")
    parser.add_option("-f", "--file", type="string", dest="filenameC", help="Get the name of the cabling file")
    #############these options are fot getting the info of the cabling file####################################
    parser.add_option("-a","--imod",type="string", dest="listrc", help="List of DetIds of the cabling file in a txt file and a trackermap")

    parser.add_option("-z","--lisf",action="callback", callback = cb, dest="lisfem", help="Modules associated to a(some) Fed(s),write the Feds  whereof you want to know the modules associated")
    parser.add_option("--zi","--fnaf",type="string",dest="fnafe",help="Write the name of the file with the modules associated to a(some) Fed(s)")


    parser.add_option("-b","--data",action="callback", callback=cb, dest="lisfetrc", help="Tracker map of DetIds connected to some FEDs to locate them in the detector, write -b followed by the FedIds")
    parser.add_option("--bf","--dataf",type="string", dest="fnmodtof", help="name of the trackermap")

    parser.add_option("-c","--modul",action="callback", callback=cb, dest="lismod", help="Information about a(some) module(s)")
    parser.add_option("--cp","--pairs",action="callback",callback=cb,dest="pairnumb",help="write the pairnumber of the module(s) selected")
    parser.add_option("--ci","--infom",action="callback",callback=cb, dest="infmod", help="Info you want to know about the modules introduced,FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD")

    parser.add_option("-g","--feds",action="callback", callback=cb, dest="lisfed", help="Information about a(some) Fed(s)")
    parser.add_option("--gf","--fedch",action="callback",callback=cb,dest="fedc",help="write the FedCh of the Fed(s) selected")
    parser.add_option("--gi","--infof",action="callback",callback=cb, dest="infed", help="Info you want to know about the Fed(s) introduced")
     
    parser.add_option("-d","--infom2",action="callback",callback=cb, dest="infomod2", help="Info you want to know the modules associated to any value of the cabling,FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD")
    parser.add_option("--di","--infom3",action="callback",callback=cb, dest="infomod3", help="Info you want to know the modules associated to any value of the cabling,FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD")


    ########these options are for the alias#############################################

    parser.add_option("-k","--fila",type="string", dest="fialc", help="Dump the Alias of the DetIds of the Cabling file in a txt file, write the name of the file")
    parser.add_option("-l","--alim",action="callback", callback=cb, dest="alimod", help="Know the Alias of a (set of) module(s),write the modules")
    
    parser.add_option("-m","--moda",action="callback", callback=cb, dest="modali", help="Know the modules associated to some Alias,write the Alias or something like: from TEC, TECmi, TECminus_7,TECminus_7_5 etc")
    parser.add_option("--mf","--filn",type="string",dest="filena",help="write the name of the file with the modules associated to some alias")
   
    parser.add_option("-y","--altk",action="callback",callback=cb,dest="alitkm",help="Tracker map for the alias of some modules")
    parser.add_option("--yf","--fnma",type="string",dest="fnaltomod",help="Tracker map for the alias of some modules")


    parser.add_option("-o","--modi",action="callback",callback=cb,dest="modinf",help="write the modules to know if they are located on certain subdetector")
    parser.add_option("--os","--subi",action="callback",callback=cb, dest="subinf", help="write the subdetector in order to know if the module is located there")

    ################these options are for the hv#######################
    
    parser.add_option("-r","--inmod",action="callback", callback = cb, dest="search_and", help="write the modules in order to get some info")
    parser.add_option("--ri","--datas",action="callback", callback = cb, dest="look_and", help="write the options of the Info about a (set of) module(s)")

    parser.add_option("-t","--values",action="callback", callback = cb, dest="see_and", help="Modules associated to a(some) value(s),write the values whereof you want to know the modules associated,like cms_trk_dcs_05:CAEN (from 02 to 05), CMS_TRACKER_SY1527_8 (from 1 to 9),branchController05 (from 02 to 05),easyCrate3 (from 1 to 5), easyBoard06 (from 01 to 17), channel002 (002 or 003)")
    parser.add_option("--tf","--names",type="string",dest="filenameva",help="Write the name of the file with the modules associated to some values")
   
    parser.add_option("-v","--trvac",action="callback",callback=cb,dest="vatrcm",help="Trackermap of the modules of certain values (those in option t)")
    parser.add_option("--vf","--fnmv",type="string",dest="fnmodtov",help="name of the Tracker map image  for modules associated to some alias")

    parser.add_option("-w","--common", action="callback",callback=cb, dest="read_and", help="Values with modules in common")
    parser.add_option("--wf","--common2", type="string", dest="filenameco", help="Name of file for Values with modules in common")
  
    #################other info#################

    parser.add_option("-e","--alcab1", action="callback",callback=cb, dest="aliascab1", help="write the property to know the location in the detector:value of the cabling,FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD")
    parser.add_option("--en","--alcab2", action="callback",callback=cb, dest="aliascab2", help="here goes the number of the property")

    parser.add_option("-i","--alcab3", action="callback",callback=cb, dest="aliascab3", help="write the property to know the location in the detector:value of the cabling,FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD")
    parser.add_option("--in","--alcab4", action="callback",callback=cb, dest="aliascab4", help="here goes the number of the property")
    parser.add_option("--ia","--alcab5", action="callback",callback=cb, dest="aliascab5", help="here goes the subdetector whereof you want to know if the module with the property chosen is there")

    parser.add_option("-j","--cabalj", action="callback",callback=cb, dest="cabalias1", help="here goes the alias whereof you want to know the info cabling")
    parser.add_option("--ja","--cabalj2", action="callback",callback=cb, dest="cabalias2", help="here goes the info you want to know like:FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD ")




    (options, args) = parser.parse_args()
    if (options.filenameC is None):
        url = "https://test-stripdbmonitor.web.cern.ch/"
        path = "test-stripdbmonitor/CondDBMonitoring/cms_orcoff_prod/CMS_COND_31X_STRIP/DBTagCollection/SiStripFedCabling/SiStripFedCabling_GR10_v1_hlt/CablingLog/"
        cablingfile = getLatestCabling()
        urllib.urlretrieve(url+path+cablingfile,cablingfile)
        ourdictionary=DictionaryCab(cablingfile,options)
        
        fileCab1= 'DetIdCab.txt'
        fileHV1='/afs/cern.ch/cms/slc5_amd64_gcc481/cms/cmssw/CMSSW_7_0_4/src/CalibTracker/SiStripDCS/data/StripPSUDetIDMap_BeforeJan132010.dat' 
    
        MyCabHV=CabHVFiles(fileCab1,fileHV1)
        input5='file.txt'
        MyHVDict = HVInfoDictF(input5, options)

    #########HERE ALL THE FUNCTIONS ARE CALLED  
    ## for the alias
    StripDetIDAliasDict=pickle.load(open(os.getenv("CMSSW_RELEASE_BASE")+"/src/CalibTracker/SiStripDCS/data/StripDetIDAlias.pkl"))
  
    ##for the dictionary of the cabling file

    ourdictionary=DictionaryCab(options.filenameC,options)
     ##for the HV
    MyCabList=DetIdCabL(options.filenameC)
    fileCab1= 'DetIdCab.txt'
    fileHV1='/afs/cern.ch/cms/slc5_amd64_gcc481/cms/cmssw/CMSSW_7_0_4/src/CalibTracker/SiStripDCS/data/StripPSUDetIDMap_BeforeJan132010.dat' 
    MyCabHV=CabHVFiles(fileCab1,fileHV1)
    input5='file.txt'
    MyHVDict = HVInfoDictF(input5, options)

####These options are to get information from one source to another 

    #######from Alias to Cabling and vice versa ######### 
           #####To know the alias of modulos with certain info of the cabling file  
    if options.aliascab1 and options.aliascab2: 
    
        li1=options.aliascab1
        li2=options.aliascab2
        txt=open('AliasforCabling.txt','w')
        for k,i in zip(li1,li2):  
            txt.write("The Alias of modules with %s:%s are: \n" %(k,i))
            for j,l in DictionaryCab.CablingInfoDict.items():
                for m,n in l.items():
                    if DictionaryCab.CablingInfoDict[j][m][k]==i:
                        beta="" 
                        beta=str(StripDetIDAliasDict[int(j)])
                        txt.write( "%s  %s \n " %(j,beta.split("'")[1]))
        print "A txt file named AliasforCabling.txt has been created"
           #########To know if modules with certain info are in certain subdetector
    if options.aliascab3 and options.aliascab4: 
    
        li1=options.aliascab3
        li2=options.aliascab4
        li3=options.aliascab5
        txt2=open('CabinSubdector.txt','w')
        for k,i in zip(li1,li2):  
            for j,l in DictionaryCab.CablingInfoDict.items():
                for m,n in l.items():
                    if DictionaryCab.CablingInfoDict[j][m][k]==i:
                        for o in li3:
                            beta6= str(StripDetIDAliasDict[int(j)]) 
                            if o in beta6:
                                txt2.write("For DetId %r True % r " %(j, beta6.split("'")[1].split("_")[0]))
                            if o not in beta6:
                                txt2.write("For DetId %r false %r " %(j, beta6.split("'")[1].split("_")[0]))
           ################To know the cabling info of modules with certain alias
    if options.cabalias1 and options.cabalias2:

        li1=options.cabalias1
        li2=options.cabalias2
        #txt=open('CabofAlias.txt','w') 
        beta3=""
        for j in li1:
            for k in StripDetIDAliasDict.keys():
                beta3 = str(StripDetIDAliasDict[k])
                print DictionaryCab.CablingInfoDict[k]
                #if j in beta3:
                #    for l,m in zip(li2,DictionaryCab.CablingInfoDict.values()):
                        #print DictionaryCab.CablingInfoDict[k]
                        #print "%r"%(str(int(DictionaryCab.CablingInfoDict[k][m][l],16)))

        #li3=options.lismod
        #li4=options.pairnumb
        #li5=options.infmod
        #for i,j in zip(li3,li4): 
        #    print "For DetID : %r with pairNumber: %r "%(i,j)
        #    for k in li5:
        #        print " %r is:%r "%(k,str(int(DictionaryCab.CablingInfoDict[i][j][k],16)))
               



####################3THESE INSTRUCTIONS A

#a=[detID for detID in ourdictionary.keys() if "23" in [ourdictionary[detID][APVPair]["FedCrate"] for APVPair in ourdictionary[detID].keys()]]
#print a
# b=[ourdictionary[detID][APVPair]["FedCh"] for APVPair in [ detID, ourdictionary[detID].keys() for detID in StripDetIDAliasDict.keys() if list(StripDetIDAliasDict[detID])[0]=="TOBminus_2_4_2_2" ourdictionary[detID].keys() ]]
#CMSSW_RELEASE_BASE/src/CalibTracker/SiStripDCS/data/StripDetIDAlias.pkl
#/afs/cern.ch/cms/slc5_amd64_gcc481/cms/cmssw/CMSSW_7_0_4/src/CalibTracker/SiStripDCS/data/
