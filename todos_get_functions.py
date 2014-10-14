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
##in case the user does not write a Run of a cabling file or a semi-url, this function takes the latest cabling file in the url below, and let this script to use it
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

##this function takes the run introduced by the user and search for the file belonging to that run, and lets this script to use it
def filenameF(name):
    suffix='CablingInfo_Run'
    filenameX=suffix+name+'.txt'
    url="https://test-stripdbmonitor.web.cern.ch/test-stripdbmonitor/CondDBMonitoring/cms_orcoff_prod/CMS_COND_31X_STRIP/DBTagCollection/SiStripFedCabling/SiStripFedCabling_GR10_v1_hlt/CablingLog/"
    urllib.urlretrieve(url+filenameX,filenameX)
    return filenameX
###this functions takes the semi-url introduced by the user and looks for it trough the url below to get the cabling file and lets this script to use it 
def semilinkF(namelink):

    pattern=re.split('/',namelink)
    filelink=pattern[-1]

    url="https://test-stripdbmonitor.web.cern.ch/test-stripdbmonitor/CondDBMonitoring/cms_orcoff_prod/CMS_COND_31X_STRIP/DBTagCollection/SiStripFedCabling/"
    urllib.urlretrieve(url+namelink,filelink)

    return filelink

###this function takes the cabling file (regardless the way the user choosed), makes a dictionary of Detids(with pairnumber as secondkey) and a dictionary of FEDs (with FecCH as second key)
def DictionaryCab(filenameC):
    """This function takes a filename as input and looks for it in the URL, then makes a dictionary with DetId as key and pairnumber as key2 or FEDid as key1 and FedCh as key2"""
    FiletxtFEDs = open(filenameC,'r')

    Fd = "FedCrate/FedSlot/FedId/FeUnit/FeChan/FedCh"
    Fc = "FecCrate/FecSlot/FecRing/CcuAddr/CcuChan"
    D = "DcuId/DetId"
    Ll = "LldChan/APV0/APV1"
    pair = "pairNumber/nPairs/nStrips"
    DC = "DCU/MUX/PLL/LLD"
 
    DictionaryCab.CabDict={}		
    DictionaryCab.CabDictF={}
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

        if detid in DictionaryCab.CabDict.keys(): 
            DictionaryCab.CabDict[detid].update({pairnumber:{"FedCrate": fedcrate,"FedSlot":fedslot,"FedId":fedid,"FeUnit":feunit,"FeChan":fechan,"FedCh":fedch,"FecCrate":feccrate,"FecSlot":fecslot,"FecRing":fecring,"CcuAddr":ccuaddr,"CcuChan":ccuchan,"DcuId":dcuid,"DetId":detid,"pairNumber":pairnumber,"LldChan":lldchan,"APV0":apv0,"APV1":apv1,"nPairs":npairs,"nStrips":nstrips,"DCU":dcu,"MUX":mux,"PLL":pll,"LLD":lld}})
		
        else:
            DictionaryCab.CabDict.update({detid:{pairnumber:{"FedCrate": fedcrate,"FedSlot":fedslot,"FedId":fedid,"FeUnit":feunit,"FeChan":fechan,"FedCh":fedch,"FecCrate":feccrate,"FecSlot":fecslot,"FecRing":fecring,"CcuAddr":ccuaddr,"CcuChan":ccuchan,"DcuId":dcuid,"DetId":detid,"pairNumber":pairnumber,"LldChan":lldchan,"APV0":apv0,"APV1":apv1,"nPairs":npairs,"nStrips":nstrips,"DCU":dcu,"MUX":mux,"PLL":pll,"LLD":lld}}})


    for fedcrate, fedslot, fedid, feunit, fechan, fedch, feccrate, fecslot, fecring, ccuaddr, ccuchan, dcuid, detid, lldchan, apv0, apv1, pairnumber, npairs, nstrips, dcu, mux, pll, lld in zip(FedCrateList, FedSlotList, FedIdList, FeUnitList, FeChanList, FedChList, FecCrateList, FecSlotList, FecRingList, CcuAddrList, CcuChanList, DcuIdList, DetIdList, LldChanList, APV0List, APV1List, pairNumberList, nPairsList, nStripsList, DCUList, MUXList, PLLList, LLDList): 
  
                        
        if fedid in DictionaryCab.CabDictF.keys(): 
            DictionaryCab.CabDictF[fedid].update({fedch:{"FedCrate": fedcrate,"FedSlot":fedslot,"FedId":fedid,"FeUnit":feunit,"FeChan":fechan,"FedCh":fedch,"FecCrate":feccrate,"FecSlot":fecslot,"FecRing":fecring,"CcuAddr":ccuaddr,"CcuChan":ccuchan,"DcuId":dcuid,"DetId":detid,"pairNumber":pairnumber,"LldChan":lldchan,"APV0":apv0,"APV1":apv1,"nPairs":npairs,"nStrips":nstrips,"DCU":dcu,"MUX":mux,"PLL":pll,"LLD":lld}})
               
        else:
            DictionaryCab.CabDictF.update({fedid:{fedch:{"FedCrate": fedcrate,"FedSlot":fedslot,"FedId":fedid,"FeUnit":feunit,"FeChan":fechan,"FedCh":fedch,"FecCrate":feccrate,"FecSlot":fecslot,"FecRing":fecring,"CcuAddr":ccuaddr,"CcuChan":ccuchan,"DcuId":dcuid,"DetId":detid,"pairNumber":pairnumber,"LldChan":lldchan,"APV0":apv0,"APV1":apv1,"nPairs":npairs,"nStrips":nstrips,"DCU":dcu,"MUX":mux,"PLL":pll,"LLD":lld}}})



############THESE INSTRUCTIONS ARE FOR GETTING THE INFO OF THE DICTIONARY FOR THE CABLING FILE#############################3
    
#takes the detids from the DictionaryCab  and dumps them in a txt file
def cabdet(filename,cabdict):
    archi=open(filename,'w')
    for p in cabdict:
        archi.write(p+"\n")
    archi.close
    print "A file named %r has been created" %filename


#this function, from the DictionaryCab  makes a txt file with the detids and a code from the rgb scale, and then runs the print_TrackerMap code to make a trackermap of the modules to locate them in the detector

def trmcab(pngname,cabdict):
    archi=open('trackermapdetids.txt','w')
    for p in cabdict:
        archi.write(p)
        archi.write(" "+"255"+" "+ "0"+" "+"0"+"\n")
        archi.close
        os.system(('print_TrackerMap trackermapdetids.txt TrackerMap %r 2400 False True 999 -999')%pngname)
        print "A file named trackermapdetids.txt and a tracker map named %r have been created" %pngname
   
#This function gets the fedids introduced by the user and search in the Fed's dictionary created in the function DictionaryCab for those modules connected to those feds and dumbs the information in a txt file	
def fdetfed(li,fnafe,cabdictf):
        archi1=open(fnafe,'w')
        visited=set()
        for p in li1:
            archi1.write("The modules associated to FED %s are:\n" %p)
            for r in cabdictf[p]:
                if cabdictF[str(int(p))][r]["DetId"]:
                    visited |={cabdictf[str(int(p))][r]["DetId"]}
                    archi1.write(cabdictf[str(int(p))][r]["DetId"]+"\n")
        

# This function gets the Fedids introduced by the user, makes a txt file with the detids associated to those feds and assigns a color, and runs the print_trackerMap to create a Trackermap of the detids associated to a (some) Fed(s) to locate them in the detector 
def trmdetfed(li1,pngname,cabdictf):
        archi=open('ModulestoFeds.txt','w')
        color_list=[" 0 255 0"," 0 0 255"," 255 0 0"," 255 0 255"," 0 255 247"," 255 69 0"," 51 0 51"," 250 128 114"," 47 79 79"]
        for p,j in (li1,color_list):
                for q in cabdictf[p].keys():
                    archi.write(cabdictf[p][q]["DetId"])
                    print j,p
        
        archi.close()
        variable =""

        color_list1=["green","blue","red","pink","cyan","orange","purple","salmon","dark slate gray"]
        for i,j in zip (li1,color_list1):
            variable+='%s=%s  ' % (i,j)
        os.system('print_TrackerMap ModulestoFeds.txt "FEDs: %s for file %s" %r  2400 False True 999 -999' % (variable,filenameC,pngname))


#this function takes the modules and the information wanted by the user (like FedCrate, APV0 etc) introduced by the user and makes a txt file with the cabling Info about those module(s)
def cabinfodet(li1,li2,li3,cabdict):
        for i in li1:
            for j in li2:
                print "For DetID : %r with pairNumber: %r "%(i,j)
                for k in li3:
                    print " %r is:%r "%(k,cabdict[i][j][k])
               

#this function takes the Fedids and cabling words  introduced by the user and creates a txt file with the info of those feds by looking inthe cabling dictionary 
def cabinfofed(li1,li2,li3,cabdicts):
        for l,m in zip(li1,li2):
            print "For FedId : %r with FedCh : %r "%(l,m)
            for n in li3:
                print " %r is:%r "%(n,cabdictf[l][m][n])

#this function gets the cabling info (like FedCrate 23, CcuAddr 123, etc) provided by the user and looks in the cabling dictionary to find the modules associated to those  associated to such cabling info, and dumps the information in a txt file
def cabtodet(li1,li2,cabdict):
        li1=options.infomod2
        li2=options.infomod3
        txt1=open('ModofCab.txt','w')
        listx=[set() for x in range(len(li1))]
        for k,i,y in zip(li1,li2,listx):
            for l in cabdict.keys():
                for m in cabdict[l]:
                    if cabdict[l][m][k]==i:
                        y |={l}
                         
        
        for k,i,x in zip(li1,li2,listx):
            txt1.write("The modules with %s:%s are:\n"%(k,i))
            for y in x:
                txt1.write(y+"\n")



        print "A file named ModofCab.txt with the modules with the info written has been created"
                     
        txt1.close() 
   
##This function get the cabling info provided by the user and dumps in a txt file the modules that thoose properties have in common 

def cabcomdet(li1,li2,cabdict):
    txt_2 = open("CabinCommon.txt",'w')
    objectives = []
    for l in cabdict.keys():
        flag = True
        for m in cabdict[l].keys(): 
            for proper in range(len(li1)):
                if cabdict[l][m][li1[proper]] != li2[proper]:
                    flag = False
        if flag:
            objectives.append(l)
    print "A file named CabinCommon.txt has been created"
    
    return objectives
        


####################3THESE INSTRUCTIONS ARE FOR GETTING THE INFO OF THE ALIAS ######################

#This function gets from the cabling file the detids and the complete alias dictionary (that one with all 15148 detids and its respective alias) and makes and alias dictionary just for those detids of the cabling file choosen by the user
def AliasFun(filenameC,AliasDict):
    FileAliasD=open(filenameC,'r')
    D="DcuId/DetId"
    DetIdAlList=[]
    for line1 in FileAliasD:
        if D in line1:
            pattern1 = re.split('\W+',line1)
            if (int(pattern1[4],16)) not in DetIdAlList:
                DetIdAlList.append(int(pattern1[4],16))
    AliasFun.SiAliasDict={}
    for detID in DetIdAlList:
        beta1 = (AliasDict[int(detID)]) 
        AliasFun.SiAliasDict.update({int(detID):beta1})

#This function makes a file with the alias of the detids of the cabling file, the user provides just the name of the file   
def alscabdet(name,aliasdict):
        beta1=""
        txt_1=open(options.fialc,'w')
        for l in aliasdict:
            beta1 = str(aliasdict[int(l)])
            txt_1.write("%s  %s\n"  %(l,beta1.split("'")[1]))
        print "A file named %r has been created" %name
   
#this function takes the detids provided by the user and makes a txt file with the alias of such a (set of) module(s)     
def alsinfodet(li1,aliasdict):
    for i in li1:
        beta2= str(aliasdict[int(i)])
        print "for module with DetId %s, Alias is %s" %(i,beta2.split("'")[1])
        print "A file named AliasModules.txt has been created"

#This function takes the alias provided by the user, searchs in the alias dictionary and makes a txt file with the modules associated to such Alias(es)
def alstodet(filename,li,aliasdict):
        txt = open (filename,'w')       
        beta3=""
        for j in li:
            txt.write("For Alias %r, the DetIds associated are:\n" % j)
            for l in aliasdict.keys():
                beta3 = str(aliasdict[l])
                if j in beta3:
                    txt.write("%r \n" %l)
        print "A file named %s has been created"%filename
#this function takes the alias provided by the user and search in the alias dictionary the modules with those alias and runs the print_tackermap code to make A tracker map of the modules associated to such alias
def trmdetals(pngname,li1,aliasdict):

        txt=open('faliastkm.txt','w')
        beta4=""
        color_list=["0 255 0","0 0 255","255 0 0","255 0 255","0 255 247","255 69 0","51 0 51","250 128 114","47 79 79"]
        for k in li4:
                for detid in  aliasdict.keys():
                    beta4=str(aliasdict[detid])
                    if k in beta4:
                        txt.write("%r"%detid+" "+"0"+" "+ "255"+" "+"0"+"\n")
        archi.close() 
        color_list1=["green","blue","red","pink","cyan","orange","purple","salmon","dark slate gray"]
        variable=""
        for i,j in zip (li1,color_list):
            variable+='%s=%s  ' % (i,j)
        os.system('print_TrackerMap faliastkm.txt "value: %r for Run  %r" %r 2400 False True 999 -999' % (variable,filenameC,pngname))                      
##This function takes the modules and alias info provided by the user and search in the alias dictionary To know if such modules are or are not in such detector or subdetector
def tfalsdet(li1,li2,aliasdict):
        txt=("trufalsesub.txt",'w')
        for k in li1:
            for l in li2:
                beta6= str(aliasdict[int(k)])
                if l in beta6:
          
                    txt.write("For DetId %r True % r \n" %(k,l))

                if l not in beta6:
                    txt.write("For DetId %r false %r \n" %(k,l))
        print "A file named TrueFalseAlias.txt has been created"



####THE NEXT FUNCTIONS ARE FOR GETTING THE INFO OF THE HV#########


#This function extracts from the cabling file the detids and dump them in  a txt file
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
    
    return DetIdCabList
#this function takes the file created in function DetIdCabL and the file with the hv information of all 15148 modules to  make an hv file for just those detids of the cabling file

def CabHVFiles(fileCab,fileHV,verbose=True):
    sep = " "
    d = {}
    for line in  open(fileHV, "r"):
        key, val = line.strip().split(sep)
        d[key] = val
    detIDs=[line.strip() for line in open(fileCab, "r")] 
    OutFile=open('file.txt','w')
    for detID in detIDs:
        OutFile.write("%s %s\n" % (detID,d[detID]))

#this function takes the file created in function CabHVFiles to create an hv dictionary of the detids of the cabling file

def HVInfoDictF(filename):
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
#this function takes the modules and hv words given by the user and provides the information of such modules by looking in the hv dictionary
def hvtodet(li1,li2,hvdict): 
    txt=open('hvinfodet.txt','w')
    for i in li1:
        print "For DetId %r:" %i
        for j in li2: 
            txt.write(" %r is: %r" % (j,hvdict[i][j]))

#this function takes the hv information provided by the user and looks in the hv dictionary the detids associated to those values
def hvmodva(li1,filenameh,hvdict): 
     
    txt_1=open(filenameh,'w')
        #visited=set([])
    for k in li1:
        txt_1.write("The modules with property %r are:\n" % k)
        for l in hvdict:
            for m in hvdict[l]:
                if hvdict[l][m]==k:
                    #visited |={str(l)}
                   txt_1.write("\n %s" % l)
        print "A file named %r has been created"%filenameh
#this function gets the hv information given by the user and runs the print_trackermap code to make a tracker map of the modules associated to such hv info
def trmdethv(li1,pngname,hvdict):
        txt_1=open('filevamod.txt','w')
        for k in li1:
            if j==1: 
                for l in hvdict:
                    for m in hvdict[l]:
                        if hvdict[l][m]==k:
                            txt_1.write("%s"%l+" "+"0"+" "+ "255"+" "+"0"+"\n")
        
        txt_1.close()
        color_list = ["green","blue","red","yellow","magenta","light blue","dark green","purple","black"]
        variable =""


        for i,j in zip (li1,color_list):
            variable+='%s=%s  ' % (i,j)
        os.system('print_TrackerMap filevamod.txt "value: %r for run %r" %r 2400 False True 999 -999' % (variable,filenameC,pngname))       
       
#this function gets the hv information provided by the user and searchs in the hv dictionary to get the modules that those hv values have in common, dumps the information in a txt file
 
def hvcomdet(filenamet,li1,hvdict):
    txt = open(filenamet,'w')
    li1=options.read_and
    objectivehv=[]
    txt.write("The modules in common for values: ")
    [txt.write("%s, "%x) for x in li1]
    keys=set([])
    for j in HVInfoDictF.HVInfoDict.keys():
        for k in HVInfoDictF.HVInfoDict[j].keys():
            for proper in range(len(li1)):
                if HVInfoDictF.HVInfoDict[j][k]== li1[proper]:
                    keys |={k}
            
    for j in HVInfoDictF.HVInfoDict.keys():
        flag=True
        for proper in range(len(li1)):
            if HVInfoDictF.HVInfoDict[j][(list(keys))[proper]] not in li1[proper]:
                flag=False
        if flag:
            txt.write("\n"+j)
            objectivehv.append(j)
    print "A file named %r options has been created",filenamet
    txt.close  
        
 ##########to get info between sources##################3 
#####the user provides cabling info and the hv info that needs, and this function looks in the cabling file the modules belonging to  those values, and then looks in the hv dictionary to provided the hv info asked by the user, dumps the information in a txt file
def cabtohv(li1, li2, li3, hvofcab, cablinfo,hvdict):#victor
   txt = open(hvofcab, 'w')
   list1 = []
   for i,j in zip(li1,li2):
      for k in li3:
         txt.write("The hv property: %s for modulues with Cabling info: %s:%s is:\n" %(k,i,j))
         for l in cablinfo:
            for m in cablinfo[str(l)]:
               if cablinfo[str(l)][m][i] == j and l not in list1:
                  list1.append(l)
                  txt.write("%s %s\n"%(l,hvdict[str(l)][k]))
   print "A file named" + hvofcab + "has been created"
###the user provides aliases and the hv info that needs and this function looks in the alias dictionary the modules belonging to such alias information and then looks in the hv dictionary the hv info of such modules

def alstohv(li1,li2,aliasdict,hvinfodict):
        txt=open('hvofalias.txt','w') 
        beta=""
        for i,j in zip(li1,li2):
            txt.write("The %r for modulues with Alias %r is:\n" %(j,i))
            for k in aliasdict:
                beta = str(aliasdict[k])
                if i in beta:
                    txt.write("%s %s\n"%(str(k),hvdict[str(k)][j]))
        print "A file named" + hvofcab + "has been created"

########the user provides hv information ant this functions looks in the hv dictionary the modules belonging to such info and dumps in txt file the alias of such modules
def hvtoal(li1,hvdict,aliasdict):
        txt=open('aliastohv.txt','w')
        for j in li1:  
            txt.write("The Alias of modules with %s are: \n"%j)
            for k in hvdict:
                for m in hvdict[k]:
                    if  hvdict[k][m]==j:
                        beta="" 
                        beta=str(aliasdict[int(k)]) 
                        txt.write( "%s  %s \n " %(k,beta.split("'")[1]))
        print "A file named aliastohv.txt with the alias of modules with property %s has been created" %j

#########the user provides cabling info and some aliases and this functions looks for the modules with such cabling info in the cabling dictionary and then looks in the alias dictionary To know if such modules are in such certain subdetector
def tfcabtoals(li1,li2,li3,cabdict,aliasdict): 
    txt2=open('CabinSubdector.txt','w')
    for k,i in zip(li1,li2):  
        for j in cabdict.items():
            for m in cabdict[j]:
                if cabdict[j][m][k]==i:
                    for o in li3:
                        beta6= str(aliasdict[int(j)]) 
                        if o in beta6:
                            txt2.write("For DetId %r True % r \n" %(j, beta6.split("'")[1].split("_")[0]))
                        if o not in beta6:
                            txt2.write("For DetId %r false %r \n " %(j, beta6.split("'")[1].split("_")[0]))


######the user provides hv information and cabling info that wants to know, and this function looks in the hv dictionary the modules with such hv info and then looks in the cabling dictionary the cabling info asked by the user, dumps the information in a txt file
def hvtocab(li1,li2,hvdict,cabdict):

        txt=open('Cabofhv.txt','w')
        list1=set()
        for i in li1:
            for j in li2:
                txt.write("The cabling info:%r for modulues with hv info:%r is:\n" %(j,i))
                for k in hvdict:
                    for l in hvdict[k]:
                        if hvdict[k][l]==i:
                            for l in hvdict[str(k)]:                                     
                                txt.write("%s %s\n"%(k,cabdict[str(k)][l][j]))
 
                                    
        print ("A txt file Cabofhv.txt with the modules and cabling info has been created")
################the user provides alias information and cabling info needed and this function looks in the alias dictionary the modules associated to such alias info and then looks in the cabling dictionary the cabling info asked for those modules
def aliastocab(li1,li2,aliasdict,cablinfo):
        txt=open('CabofAlias.txt','w') 
        beta3=""
        visited = set([])
        for j in li1:
            for l in li2:
                txt.write("The %r for modulues with Alias %r is:\n" %(l,j))
                for k in aliasdict.keys():
                    beta3 = str(aliasdict[k])
                    if str(k) not in visited and (j in beta3 and str(k) in cabdict.keys()):
                        for m in cabdict[str(k)].keys():
                            #visited |={str(k)}
                            print "\n"+str(k)+"  "+str(int(cabdict[str(k)][str(m)][l],16))
                            txt.write( "\n"+str(k)+"  "+str(int(cabdict[str(k)][str(m)][l],16)))
        print ("A txt file CabofAlias.txt with the modules and cabling info has been created")
#######AND NOW INFORMATION FROM TWO SOURCES TO ONE#########

#this function takes the cabling and hv information provided by the user search for the modules of each property in the respective dictionary, intersects the modules of cabling info and hv info provided and then provides the alias info of such modules in a txt file
def cabhvals(li1,li2,li3,cabdict,alsdict,hvdict):
    cab=set([])
    hv=set([])
    valhv=set([])
    txt=open('cabhvtoals.txt','w')
    txt.write('The alias of Modules with cab and hv values:\n')
    for i,j in zip(li1,li2):
        txt.write(i+" "+j+",")
    for h in li3:
        txt.write(","+h+":\n")
    cabpr=[]
    for proper in range(len(li2)):
        cabpr.append(li2[proper])
    print cabpr
    for x in li1:
        for k in cabdict.keys():
            flag = True
            for l in cabdict[k].keys():
                if cabdict[k][l][x] not in cabpr:
                    flag = False
            if flag:
                cab |= {k}
                
    for j in hvdict.keys():
        for k in hvdict[j].keys():
            for proper in range(len(li3)):
                if hvdict[j][k] in li3[proper]:
                    valhv |= {k}
                    
    lispr=[]
    for proper in range(len(li3)):
        lispr.append(li3[proper])
    for x in valhv:
        for j in hvdict.keys():
            flag=True
            if hvdict[j][x] not in lispr:
                flag=False
            if flag:
                hv |= {j}
               
    u=cab & hv
    for i in u:
        beta=str(alsdict[int(i)])
        txt.write("%s  %s\n" %(i,beta.split("'")[1]))
    print "A file named cabhvtoals.txt has been created"
#this function takes the alias and hv information provided by the user, searchs for the modules of each property in the respective dictionary, intersects the modules of alias and hv info provided and then provides the cabling info of such modules in a txt file
def hvalscab(li1,li2,li3,hvdict,alsdict,cabdict):
   
    als=set([])
    hv=set([])
    valhv=set([])
    txt=open('hvalscab.txt','w')
    txt.write('The cabling info of Modules with hv  and alias values:  ')
       
    for j in hvdict.keys():
        for k in hvdict[j].keys():
            for proper in range(len(li1)):
                if hvdict[j][k]== li1[proper]:
                    valhv |={k}
                    
        
    lispr=[]       
    for proper in range(len(li1)):
       lispr.append(li1[proper])
    for x in valhv:
        for j in hvdict.keys():
            flag=True
            if hvdict[j][x] in lispr: 
                flag=False
            if flag:
                hv|={j}
                
 
    for j in li2:
        for detid in alsdict.keys():
            beta3 = str(alsdict[detid])
            if j in beta3:
                als|={str(detid)}
                              

    u=als & hv


    for i in li1:
        txt.write(i+",")
    for j in li2:
        txt.write(","+j)
    for l in li3:
        txt.write("\n\t"+l+" is: \n")
        for m in u:
            for n in cabdict[m]:
                txt.write(m+" "+cabdict[m][n][l]+"\n")
    print "A file named hvalscab.txt has been created"               


#this function takes the alias and cabling information provided by the user, searchs for the modules of each property in the respective dictionary, intersects the modules of alias and cabling info provided and then provides the hv info of such modules in a txt file
def cabalshv(li1,li2,li3,li4,cabdict,alsdict,hvdict):
    
    als=set([])
    hv=set([])
    cab=set([])
    txt=open('cabalshv.txt','w')
    txt.write('The hv info of Modules with cabling  and alias values:  ')

    for j in li1:
        for detid in alsdict.keys():
            beta3 = str(alsdict[detid])
            if j in beta3:
                als |={str(detid)} 
                
    liscab=[]
    for proper in range(len(li3)):
        liscab.append(li3[proper])
    
    for x in li2:
        for k in cabdict.keys():
            flag = True
            for l in cabdict[k].keys():
                    if cabdict[k][l][x] not in liscab:
                        flag = False
            if flag:
                cab |={k}        
                
    u=als & cab
    for i in li1:
        txt.write(i+",")
    for j,k in (li2,li3):
        txt.write(","+j+k)
    for l in li4:
        txt.write("\n\t"+l+" is: \n")
        for m in u:   
            txt.write(m+" "+hvdict[m][l]+"\n")        
    print "A file named cabalshv.txt has been created"
        



##########HERE WE INTRODUCE THE OPTIONS FOR THE INFO#######################
if __name__ == "__main__":
    verbose = True
    usage = "useage: %prog [options] "
    parser = OptionParser(usage)
    parser.set_defaults(mode="advanced")
    parser.add_option("-f", "--file", type="string", dest="filenameC", help="Get the run of the cabling file")
    parser.add_option("--fu", "--fileu", type="string", dest="fileurl", help="Get the url of another cabling file")

    #############these options are fot getting the info of the cabling file####################################
    parser.add_option("-a","--imod2",type="string", dest="cabdet", help="List of DetIds of the cabling file in a txt, write the name of the file")

    parser.add_option("--at","--imod",type="string", dest="trmcab", help="trackermap, write the name of the image(.png)")

    parser.add_option("-z","--lisf",action="callback", callback = cb, dest="detfed1", help="Modules associated to a(some) Fed(s),write the Feds  whereof you want to know the modules associated")
    parser.add_option("--zi","--fnaf",type="string",dest="detfed2",help="Write the name of the file with the modules associated to a(some) Fed(s)")


    parser.add_option("-b","--data",action="callback", callback=cb, dest="trmdetfed1", help="Tracker map of DetIds connected to some FEDs to locate them in the detector, write -b followed by the FedIds")
    parser.add_option("--bf","--dataf",type="string", dest="trmdetfed2", help="name of the trackermap (name.png)")

    parser.add_option("-c","--modul",action="callback", callback=cb, dest="detcab1", help="Information about a(some) module(s),write the modules")
    parser.add_option("--cp","--pairs",action="callback",callback=cb,dest="detcab2",help="write the pairnumber of the module(s) selected, write the pair number 0,1 or 3, or the three of them")
    parser.add_option("--ci","--infom",action="callback",callback=cb, dest="detcab3", help="write what you want to know about the modules introduced,FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD")

    parser.add_option("-g","--feds",action="callback", callback=cb, dest="fedcab1", help="Information about a(some) Fed(s),write the FedIds")
    parser.add_option("--gf","--fedch",action="callback",callback=cb,dest="fedcab2",help="write the FedCh of the Fed(s) selected")
    parser.add_option("--gi","--infof",action="callback",callback=cb, dest="fedcab3", help="write what you want to know about the Fed(s) introduced,FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD")
     
    parser.add_option("-d","--infom2",action="callback",callback=cb, dest="cabdet1", help="info  you want to know the modules associated to, like:FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD")
    parser.add_option("--di","--infom3",action="callback",callback=cb, dest="cabdet2", help="write the number belonging to the info given in -d, like FedCrate 23 or CcuAddr 123 (just write the number)")

    parser.add_option("-n","--cabc1",action="callback",callback=cb, dest="cabcom1", help="if you want to know the modules in common for several info of the cabling,FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD")
    parser.add_option("--ni","--cabc2",action="callback",callback=cb, dest="cabcom2", help="here goes the number of the property")

 

    ########these options are for the alias#############################################

    parser.add_option("-k","--fila",type="string", dest="alscab", help="Dump the Alias of the DetIds of the Cabling file in a txt file, write the name of the file")
    parser.add_option("-l","--alim",action="callback", callback=cb, dest="detals", help="Know the Alias of a (set of) module(s),write the modules")
    
    parser.add_option("-m","--moda",action="callback", callback=cb, dest="alsdet1", help="Know the modules associated to some Alias,write the Alias or something like: from TEC, TECmi, TECminus_7,TECminus_7_5 etc")
    parser.add_option("--mf","--filn",type="string",dest="alsdet2",help="write the name of the file with the modules associated to some alias")
   
    parser.add_option("-y","--altk",action="callback",callback=cb,dest="alitkm1",help="write the alias where of you want a trackermap of detids associated to those alias")
    parser.add_option("--yf","--fnma",type="string",dest="alitkm2",help="write the name of the image(name.png) ")


    parser.add_option("-o","--modi",action="callback",callback=cb,dest="tfalsub1",help="write the modules to know if they are located on certain subdetector")
    parser.add_option("--os","--subi",action="callback",callback=cb, dest="tfalsub", help="write the subdetector in order to know if the module is located there")

    ################these options are for the hv#######################
    
    parser.add_option("-r","--inmod",action="callback", callback = cb, dest="dethv1", help="write the modules in order to get some info")
    parser.add_option("--ri","--datas",action="callback", callback = cb, dest="dethv2", help="write the options of the Info about a (set of) module(s),like PSUName,Cmstrk,Crate,Board,Branch,TrackerSY,Channel")

    parser.add_option("-t","--values",action="callback", callback = cb, dest="hvdet1", help="Modules associated to a(some) value(s),write the values whereof you want to know the modules associated,like cms_trk_dcs_05:CAEN (from 02 to 05), CMS_TRACKER_SY1527_8 (from 1 to 9),branchController05 (from 02 to 05),easyCrate3 (from 1 to 5), easyBoard06 (from 01 to 17), channel002 (002 or 003)")
    parser.add_option("--tf","--names",type="string",dest="hvdet1",help="Write the name of the file with the modules associated to some values")
   
    parser.add_option("-v","--trvac",action="callback",callback=cb,dest="trmhvdet1",help="Trackermap of the modules of certain values (those in option t)")
    parser.add_option("--vf","--fnmv",type="string",dest="trmhvdet2",help="name of the Tracker map image  for modules associated to some hv (.png)")

    parser.add_option("-w","--common", action="callback",callback=cb, dest="hvcom1", help="Values with modules in common, those in option -t")
    parser.add_option("--wf","--common2", type="string", dest="hvcom2", help="Name of file for Values with modules in common")
  
    #################other info#################

    parser.add_option("-e","--alcab1", action="callback",callback=cb, dest="cabals1", help="write the cabling info to know the alias of the detids:value of the cabling,FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD")
    parser.add_option("--en","--alcab2", action="callback",callback=cb, dest="cabals2", help="here goes the number of the property")

    parser.add_option("-i","--alcab3", action="callback",callback=cb, dest="tfcabals1", help="write the cabling info: FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD")
    parser.add_option("--in","--alcab4", action="callback",callback=cb, dest="tfcabals2", help="here goes the number of the property")
    parser.add_option("--ia","--alcab5", action="callback",callback=cb, dest="tfcabals3", help="here goes the subdetector whereof you want to know if the module with the property chosen is there")

    parser.add_option("-j","--cabalj", action="callback",callback=cb, dest="alscab1", help="here goes the alias whereof you want to know the info cabling")
    parser.add_option("--ja","--cabalj2", action="callback",callback=cb, dest="alscab2", help="here goes the info you want to know like:FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD ")

    parser.add_option("-p","--alhv", action="callback",callback=cb, dest="hvals", help="to know the alias of the modules with hv -p property, write the hv property, like those in option -t ")


    parser.add_option("-q","--hval1", action="callback",callback=cb, dest="alshv1", help="to know the hv info detids  with certain property of alias, write the alias you want to know ")
    parser.add_option("--qi","--hval2", action="callback",callback=cb, dest="alshv2", help="write the hv property,PSUName,Cmstrk,Crate,Board,Branch,TrackerSY,Channel")


    parser.add_option("-s","--hvca1", action="callback",callback=cb, dest="cabhv1", help="write the cabling info you know, like: FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD ")
    parser.add_option("--sc","--hvca2", action="callback",callback=cb, dest="cabhv2", help="write the number of the cabling info like: FecRing 34 FedCrate 23(just write the number, on option s you write the number of the property ")
    parser.add_option("--sh","--hvca3", action="callback",callback=cb, dest="cabhv3", help="write the hv info you want to know, like:,PSUName,Cmstrk,Crate,Board,Branch,TrackerSY,Channel" )

    parser.add_option("-u","--cahv1", action="callback",callback=cb, dest="hvcab1", help="write the hv property you know , like:cms_trk_dcs_05:CAEN (from 02 to 05), CMS_TRACKER_SY1527_8 (from 1 to 9),branchController05 (from 02 to 05),easyCrate3 (from 1 to 5), easyBoard06 (from 01 to 17), channel002 (002 or 003)")  
    parser.add_option("--uc","--cahv2", action="callback",callback=cb, dest="hvcab2", help="to know cabling info of modules with certain property of HV, write the cabling info you want to know, like: FedCrate,FedSlot,FedId,FeUnit,FeChan,FedCh,FecCrate,FecSlot,FecRing,CcuAddr,CcuChan,DcuId,DetId,LldChan,APV0,APV1,pairNumber,nPairs,nStrips,DCU,MUX,PLL,LLD")


"""
    (options, args) = parser.parse_args()
    if (options.filenameC is None and options.fileurl is None):
        url = "https://test-stripdbmonitor.web.cern.ch/"
        path = "test-stripdbmonitor/CondDBMonitoring/cms_orcoff_prod/CMS_COND_31X_STRIP/DBTagCollection/SiStripFedCabling/SiStripFedCabling_GR10_v1_hlt/CablingLog/"
        cablingfile = getLatestCabling()
        urllib.urlretrieve(url+path+cablingfile,cablingfile)
        
        ourdictionary=DictionaryCab(cablingfile)
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
    
    #for the alias
        StripDetIDAliasDict=pickle.load(open(os.getenv("CMSSW_RELEASE_BASE")+"/src/CalibTracker/SiStripDCS/data/StripDetIDAlias.pkl"))

        MyAlias=AliasFun(MyFilename,options,StripDetIDAliasDict)

  
    #for the dictionary of the cabling file
        ourdictionary=DictionaryCab(MyFilename)
    #for the HV
        MyCabList=DetIdCabL(MyFilename)
        fileCab1= 'DetIdCab.txt'
        fileHV1='/afs/cern.ch/cms/slc5_amd64_gcc481/cms/cmssw/CMSSW_7_0_4/src/CalibTracker/SiStripDCS/data/StripPSUDetIDMap_BeforeJan132010.dat' 
        MyCabHV=CabHVFiles(fileCab1,fileHV1)
        input5='file.txt'
        MyHVDict = HVInfoDictF(input5, options)
      

#################333
    if options.fileurl:

        Mylink=semilinkF(options.fileurl)
    
    ## for the alias
        StripDetIDAliasDict=pickle.load(open(os.getenv("CMSSW_RELEASE_BASE")+"/src/CalibTracker/SiStripDCS/data/StripDetIDAlias.pkl"))

        MyAlias=AliasFun(Mylink,options,StripDetIDAliasDict)

  
    ##for the dictionary of the cabling file
        ourdictionary=DictionaryCab(Mylink)
     ##for the HV
        MyCabList=DetIdCabL(Mylink)
        fileCab1= 'DetIdCab.txt'
        fileHV1='/afs/cern.ch/cms/slc5_amd64_gcc481/cms/cmssw/CMSSW_7_0_4/src/CalibTracker/SiStripDCS/data/StripPSUDetIDMap_BeforeJan132010.dat' 
        MyCabHV=CabHVFiles(fileCab1,fileHV1)
        input5='file.txt'
        MyHVDict = HVInfoDictF(input5, options)
"""
  
"""
this scripts provides information about the DetIds of the modules based on three kind of files, a cabling file which is a txt file with info of just a certain quantity of DetIDs, a dictionary wich is a .pkl file with the alias of the 15148 DetIDs and an hv txt file with also information about the 15148 DetIds of the detector.
this scripts makes a dictionary with the information contained in the cabling file with DetId as key1 and pairnumber of such DetId as key2,and cabling words like FedCrate,APV0,FedCh,FedId,DcuId,etc as values, together with this DetIds dictionary theres a FedIds dictionary with FedCh as key2 (and FedId as key1) two. 
A second dictionary of the DetIds of the cabling file but with the alias of the DetIds. Based on the alias .pkl file with the alias of all 15148 modules, this script estracts the alias and DetIds of just the cabling file choosen by the user

And A third dictionary of the DetIds of the cabling file but with hv (high voltage) information of those DetIds. Based on a hv .txt file with information of all 15148 modules, this scripts makes a txt file with hv information for just those DetIds of the Cabling file choosen by the user

To get a Cabling file this scripts can: 1) get a Run number introduced by the user and search the file belonging to such Run in a url page written above, 2) if the user chooses not to write a Run this scripts searchs on the same url mentioned in 1) the last cabling file and 3) the user is able to write a part of the url mentioned and this scripts gets the semi-url (which must contain a cabling file at the end) introduced and search such cabling file 

Optparse has been implemented so as to the user has the less interaction with this script, by getting the info provided by the user this scripts searches in the dictionaries mentioned above to return information, it can provide information about keys trough values or provide information about values trough keys in any of such dictionaries, it can also give information from one dictionary to another through keys and/or values. It also runs a code in order to obtain a tracker map of the detids to locate them in the detector, or locate those modules with certain information of any of the dictionaries.
 
"""
