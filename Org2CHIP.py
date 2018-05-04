# This script reads the Org2CHIP in CSV format and
#  stores it in memory
import sys
import os
import csv
import collections
import datetime
import pprint
import logging
logging.basicConfig(level=logging.WARNING)
# NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL 
# Set up input and output variables for the script
now = datetime.date.today()
Directory = "C:\\Users\\IBM_ADMIN\\Documents\\SO\\Temp\\"
Log1File = "C:\\Users\\IBM_ADMIN\\Downloads\\Active IPC OrgID List for Changes.csv"
Log2File = "C:\\Users\\IBM_ADMIN\\Downloads\\Active IPC OrgID List for Tickets.csv"
BlueIDFile = Directory+"BlueID_Accounts.csv"
DPFile = Directory+"Data Privacy 19MAY2017.csv"
OutputFile = Directory+"map_org2chip_"+ str(now)+ "-00.00.00.000000.csv"
CDIFile = Directory+"CDI Changes "+ str(now)+ ".csv"
MsgFile = Directory+"Org2CHIP"+str(now)+".log"
# define functions
def mapiot(iot):
    mpiot = {'Middle East & Africa IOT':'MEA', 'Japan IOT':'JP', 'Asia Pacific IOT':'AP', \
    'Greater China Group IOT':'CHN', 'Europe IOT':'EUR', 'North America IOT':'USA', \
    'Latin America IOT':'LA', '':''}
    stdiot = mpiot[iot]
    return stdiot

def mapimt(imt):
    mpimt = {'Italy IMT':'Italy','US IMT':'','Spain, Portugal, Greece, Israel IMT':'SPGI',\
    'United Kingdom and Ireland IMT':'UKI','Belgium, Netherlands, Luxembourg IMT':'Benelux',\
    'Latin America':'','France IMT':'France','Middle East & Africa':'MEA','DACH IMT':'DACH',\
    'Japan IMT':'','India-South Asia IMT':'','Central and Eastern Europe IMT':'CEE',\
    'Australia/New Zealand IMT':'','ASEAN IMT':'','Korea IMT':'','Canada IMT':'',\
    'Nordic IMT':'Nordic','Greater China':'', '':''}
    stdimt = mpimt[imt]
    return stdimt

def dpallow(dp, bac):
    dpok = '1-','3-'
    if bac !='' & dp.startswith(dpok) :
        return "YES"
    else :
        return "NO"

def selectDP(cd):
    DPList = DP[cd]
    DPOpt = {'Country':[], 'IPC':[], 'L1 Country':[], 'L2 Country':[]}
    DPFilter = {'Country': '', 'IPC': '', 'L1 Country':'', 'L2 Country':''}
    len = DPList.__len__()
    ans = 0
    if len > 1:
        while ans not in list(range(1, len+1)) :
            print(">> "+keylog+": Multiple choices for DP")
            for i in range(len):
                DPRow = DPList[i]
                L1C = DPRow[L1CountryIndex].split(',')
                L2C = DPRow[L2CountryIndex].split(',')
                if  (DPFilter['Country'] != '') & (DPRow[CountryIndex] not in DPFilter['Country']) : continue
                if  (DPFilter['IPC'] != '') & (DPRow[IPCIndex] not in DPFilter['IPC']) : continue
                if  (DPFilter['L1 Country'] != '') & (DPFilter['L1 Country'] not in DPRow[L1CountryIndex].split(',')) : continue
                if  (DPFilter['L2 Country'] != '') & (DPFilter['L2 Country'] not in DPRow[L2CountryIndex].split(',')) : continue
                print(">>    " + str(i+1) +" - " + "Client: "+DPRow[ClientIndex]\
                +", Country: "+DPRow[CountryIndex]+", L1 Country: "+DPRow[L1CountryIndex]+", L2 Country: "+DPRow[L2CountryIndex]\
                +", IPC Tool: "+DPRow[IPCIndex]+", Last modif: "+DPRow[ModifIndex]+", Status: "+DPRow[DPIndex])
                if  DPRow[CountryIndex] not in DPOpt['Country'] : DPOpt['Country'].append(DPRow[CountryIndex])
                if  DPRow[IPCIndex] not in DPOpt['IPC'] : DPOpt['IPC'].append(DPRow[IPCIndex])
                for j in L1C :
                    if  j not in DPOpt['L1 Country'] : DPOpt['L1 Country'].append(j)
                for j in L2C :
                    if  j not in DPOpt['L2 Country'] : DPOpt['L2 Country'].append(j)
            try:
                ans = int(input(">>  Please indicate your choice (or 0 to filter) for :"+keylog+"  \n"))
            except: 
                sys.exit("Illegal input")
            if ans == 0 :
                # select a filter
                print(">>    Please select a filter from : \n")
                Opt = list(DPOpt.keys())
                ans1 = 0
                for j in range(Opt.__len__()) :
                    print(">>    " + str(j+1) +" - " + Opt[j])
                while ans1 not in range(1, Opt.__len__()+1) :
                    try:
                        ans1 = int(input(">>  Please select a filter :\n"))
                    except: 
                        sys.exit("Illegal input")
                # select a filter value
                print(">>    Please select a filter value from (or 0 the clear the filter): \n")
                Filter= DPOpt[Opt[ans1-1]]
                ans2 = -1
                for j in range(Filter.__len__()) :
                    print(">>    " + str(j+1) +" - " + Filter[j])
                while ans2 not in range(0, Filter.__len__()+1) :
                    try:
                        ans2 = int(input(">>  Please select a filter value :\n"))
                    except: 
                       sys.exit("Illegal input")
                if ans2 != 0 :
                    DPFilter[Opt[ans1-1]] = Filter[ans2-1]                               
                else :
                    DPFilter[Opt[ans1-1]] = ''
        return DPList[ans-1]
    else :
        return DPList[0]    

def selectBAC(cd):
    BIdList = BId[cd]
    BIdOpt = {'Country':[], 'Type':[], 'Status':[], 'Phase': [], 'Focus':[]}
    BIdFilter = {'Country': '', 'Type': '', 'Status': '', 'Phase':'', 'Focus':''}
    len = BIdList.__len__()
    ans = 0
    if len > 1:
        while ans not in list(range(1, len+1)) :
            print(">> "+keylog+": Multiple choices for BlueId")
            for i in range(len):
                BIdRow = BIdList[i]
                if  (BIdFilter['Country'] != '') & (BIdRow[BIdCountryIndex] not in BIdFilter['Country']) : continue
                if  (BIdFilter['Type'] != '') & (BIdRow[TypeIndex] not in BIdFilter['Type']) : continue
                if  (BIdFilter['Status'] != '') & (BIdRow[StatusIndex] not in BIdFilter['Status']) : continue
                if  (BIdFilter['Phase'] != '') & (BIdRow[PhaseIndex] not in BIdFilter['Phase']) : continue
                if  (BIdFilter['Focus'] != '') & (BIdRow[FocusIndex] not in BIdFilter['Focus']) : continue
                print(">>    " + str(i+1) +" - " + "Client: "+BIdRow[NameIndex]+", Country: "+BIdRow[BIdCountryIndex]\
                +", Type: "+BIdRow[TypeIndex]+", Phase: "+BIdRow[PhaseIndex]\
                +", Status :"+BIdRow[StatusIndex]+", Focus: "+BIdRow[FocusIndex])
                if  BIdRow[BIdCountryIndex] not in BIdOpt['Country'] : BIdOpt['Country'].append(BIdRow[BIdCountryIndex])
                if  BIdRow[TypeIndex] not in BIdOpt['Type'] : BIdOpt['Type'].append(BIdRow[TypeIndex])
                if  BIdRow[StatusIndex] not in BIdOpt['Status'] : BIdOpt['Status'].append(BIdRow[StatusIndex])
                if  BIdRow[PhaseIndex] not in BIdOpt['Phase'] : BIdOpt['Phase'].append(BIdRow[PhaseIndex])
                if  BIdRow[FocusIndex] not in BIdOpt['Focus'] : BIdOpt['Focus'].append(BIdRow[FocusIndex])
            try:
                ans = int(input(">>  Please indicate your choice (or 0 to filter) for :"+keylog+" \n"))
            except: 
                sys.exit("Illegal input")
            if ans == 0 :
                # select a filter
                print(">>    Please select a filter from : \n")
                Opt = list(BIdOpt.keys())
                ans1 = 0
                for j in range(Opt.__len__()) :
                    print(">>    " + str(j+1) +" - " + Opt[j])
                while ans1 not in range(1, Opt.__len__()+1) :
                    try:
                        ans1 = int(input(">>  Please select a filter :\n"))
                    except: 
                        sys.exit("Illegal input")
                # select a filter value
                print(">>    Please select a filter value from : \n")
                Filter= BIdOpt[Opt[ans1-1]]
                ans2 = -1
                for j in range(Filter.__len__()) :
                    print(">>    " + str(j+1) +" - " + Filter[j])
                while ans2 not in range(0, Filter.__len__()+1) :
                    try:
                        ans2 = int(input(">>  Please select a filter value (or 0 the clear the filter) :\n"))
                    except: 
                        sys.exit("Illegal input")
                if ans2 != 0 :
                    BIdFilter[Opt[ans1-1]] = Filter[ans2-1]                               
                else :
                    BIdFilter[Opt[ans1-1]] = ''
        return BIdList[ans-1]
    else :
        return BIdList[0]

def active(yyyymm):
    nbmonths = 6
    if yyyymm == "" : return "NO"
    year = int(yyyymm[0 : 4])
    month = int(yyyymm[4 : 6])
    mm = ((int(now.year) -year) * 12) + (int(now.month) - month)
    if mm <= nbmonths :
        return "YES"
    else :
        return "NO"
    if mm <= nbmonths :
        return "YES"
    else :
        return "NO"
# Open the message log file
# Log = open(MsgFile, 'w')
# logging.info(">> Log file opened : " + MsgFile)
# Select the reference Org2CHIP file
files =  []
ls = os.listdir(path=Directory)
ls.sort(reverse=True)
for f in ls :
    if (f.startswith("map_org2chip_") & f.endswith("-00.00.00.000000.csv")) :
        files.append(f)
print (">>   List of available Org2CHIP files (limited to 15): ")
for i in range(1, min(15, len(files)+1)) :
    print (str(i) + " - "+files[i-1])
ans = 0
try:
    while ans not in range(1, min(15, len(files)+1)) :
        ans = int(input(">>   Please select the reference Org2CHIP file: \n"))
except:
    sys.exit("Illegal input")
InputFile = Directory+files[ans-1]
# Read the original Org2CHIP file
# encoding='utf8', 
try:
    print(">>   Reading the "+InputFile+" file....")
    with open(InputFile, "r", encoding='utf8', newline='') as Org2Chip:
        # Set up CSV reader and process the header
        csvReader = csv.DictReader(Org2Chip)
        # Create an empty dictionary that will hold the Org2CHIP data
        O2C = {}
        # Loop through the lines and store in the dictionary
        for row in csvReader:
            rowd = collections.OrderedDict(row)
            key = rowd["KEY"]
            O2C [key] = rowd
    O2CHeader = rowd.keys()
    logging.info(">> Original Org2CHIP File red")
except:
    sys.exit("Reference Org2CHIP file couldn't be red")
# Read the BlueId file
try:
    with open(BlueIDFile, "r", newline='') as BlueId:
        # Set up CSV reader and process the header
        csvReader = csv.reader(BlueId)
        header = csvReader.__next__()
        KeyIndex = header.index("CDIR ID")
        BACIndex = header.index("BlueID Account ID")
        LegacyIndex = header.index("Legacy Account ID")
        NameIndex = header.index("Account Name")
        TypeIndex = header.index("Account Type")
        PhaseIndex = header.index("Account Phase")
        StatusIndex = header.index("Account Status")
        BIdCountryIndex = header.index("Country")
        IMTIndex = header.index("IMT")
        IOTIndex = header.index("IOT")
        GeoIndex = header.index("Geo")
        FocusIndex = header.index("Is CHIP enabled")
        emptyRow = []
        for i in range(len(header)) : emptyRow.append('')
        # Create an empty dictionary that will hold the BlueId data
        BId = {}
        # Loop through the lines and store in the dictionary
        for row in csvReader:
            key = row[KeyIndex]
            if key in BId:
                BId[key].append(row)
            else:
                BId[key] = [row]
    logging.info(">> BlueId File red")
except: 
    sys.exit("BlueId file couldn't be red")
# Read the Data Privacy file
try:
    with open(DPFile, "r",  newline='') as DPf:
        # Set up CSV reader and process the header
        csvReader = csv.reader(DPf)
        header = csvReader.__next__()
        KeyIndex = header.index("CDIR")
        DPIndex = header.index("Status")
        IPCIndex = header.index("IPC Tools")
        ClientIndex = header.index("Client")
        CountryIndex = header.index("Country")
        ModifIndex = header.index("Last Modified")
        IPCIndex= header.index("IPC Tools")
        L1CountryIndex = header.index("Lvl1_Sup_Location")
        L2CountryIndex = header.index("Lvl2_Sup_Location")
        # Create an empty dictionary that will hold the Org2CHIP data
        DP = {}
        # Loop through the lines and store in the dictionary
        for row in csvReader:
            key = row[KeyIndex]
            if key in DP:
                DP [key].append(row)
            else:
                DP[key] = [row]
    logging.info(">> Data Privacy File red")
except: 
    sys.exit("DP file couldn't be red")
# Process the log files
LogFiles = [Log1File, Log2File]
rec = collections.OrderedDict()
# opens the CDI log file and write the header
CDIHeader = O2CHeader  #temporarily - same structure of files
with open(CDIFile, "w", encoding='utf8', newline='') as CDI :
    csvWriter = csv.DictWriter(CDI, CDIHeader)
    # write the header row
    csvWriter.writeheader()
for LogFile in LogFiles:
    # open  the log file
    try:
        with open(LogFile, "r", encoding='utf16',  newline='') as f:
            fcsv = csv.DictReader(f,  delimiter = '\t')
            logging.info(">> Opening the Audit File :" + LogFile)
            # read the log file line by line
            for line in fcsv:
                keylog = line["IPC"]+"+"+line["Organization"]
                chg = 0
                SDIchg = 0
                if keylog in O2C:
                    # check consistency of information between O2C and the log file
                    rec = O2C[keylog].copy()
                    # update the last update date, if needed
                    td = now.strftime('%Y%m')
                    if line["Open Month ID"] > td : 
                        op = ""
                    else :
                        op = line["Open Month ID"]
                    if line["Closed Month ID"] > td : 
                        cl = ""
                    else :
                        cl = line["Closed Month ID"]
                    latestact = max(op, cl)
                    if (rec["Latest Activity"] < latestact) or (rec["Latest Activity"] > td) :
                         rec["Latest Activity"] = latestact
                         # rec["Update Date"] = now.strftime('%d-%b-%y')
                         rec["Activity"] = active(latestact)                         #update the activity indicator
                         chg = 1
                         #logging.info(">> Updated reccord " + keylog + " with Latest Activity = " + rec["Latest Activity"])
                    #check the DP status (if changed)]
                    key = rec["CDIR ID"]
                    if key in DP :
                        DPList = []
                        for i in iter(DP[key]):
                            DPList.append(i[DPIndex])
                        if rec["Data Privacy"] not in DPList : 
                            DPRow = selectDP(key)
                            DPStatus= DPRow[DPIndex]
                            rec["Data Privacy"] = DPStatus
                            print(">>  Data Privacy for " + keylog + "have changed \n")
                            SDIScope = dpallow(DPStatus)
                            if rec["SDI Scope"] != SDIScope :  
                                print(">>  CDI Scope for " + keylog + "have changed \n")
                                SDIchg = 1
                            rec["SDI Scope"] = SDIScope 
                            pass
                    pass
                else:
                    # prepare the record to add to O2C
                    # Log.write(">> New entry found for " + pprint.pformat(line))
                    # map the new feed to a BlueID entry
                    cdir = line["Custom Directory Identifier"]
                    rec = {}
                    if cdir in BId :
                        BIdRow = selectBAC(cdir)
                        logging.info(">> BlueID information selected : " + pprint.pformat(BIdRow, compact='true'))
                    else :
                        BIdRow = emptyRow
                        print(">>   No BlueID reference found for " + cdir)
                    # find the DP information and copy it
                    # try to find an entry in the DP Database
                    if cdir in DP :
                        DPRow = selectDP(cdir)
                        logging.info(">> Data Privacy information selected : " + pprint.pformat(DPRow))
                        DPStatus = DPRow[DPIndex]    #to be updated with the best value
                    else :
                        DPStatus = ""
                    # copy fields from the log file,  the BlueId file or the DP file
                    rec["KEY"] = keylog
                    rec["Account Name"] = line["Account Name"]
                    rec["IPC"] = line["IPC"]
                    rec["OrgID"] = line["Organization"]
                    rec["CDIR ID"] = cdir
                    rec["IMT Name"] = line["IMT Name"]
                    rec["Leading Country"] = line["Leading Country"]
                    rec["CHIP ID"] = BIdRow[LegacyIndex]
                    rec["CHIP IOT"] = mapiot(BIdRow[IOTIndex])
                    rec["CHIP IMT"] = mapimt(BIdRow[IMTIndex])  
                    rec["CHIP Country"] = BIdRow[BIdCountryIndex]
                    bacId = BIdRow[BACIndex]
                    rec["InScope"] = dpallow(DPStatus,  bacId)
                    rec ["Active"] = "YES"
                    rec["PriSM ID"] = line["Organization ID"]
                    rec["BlueID"] = bacId
                    rec["BlueID Country"] = BIdRow[BIdCountryIndex]                
                    # try to find another entry in O2C with the same BAC and propose to copy its SDI Scope
                    if (BIdRow != emptyRow) & (BIdRow[TypeIndex] != 'Internal') :
                        for k in iter(O2C) :
                            if (O2C[k]['BlueID'] == BIdRow[BACIndex]) &  (O2C[k]['SDI Scope'] == 'YES'):
                                rec["SDI Scope"] = 'YES'
                                logging.info(">> CDI allowed by copy of " + k + "for the next record" )
                                break 
                        rec["SDI Scope"] = dpallow(DPStatus,  bacId) 
                    else :
                        rec["SDI Scope"] = dpallow(DPStatus,  bacId)
                    if rec["SDI Scope"] == 'YES' :  SDIchg = 1
                    rec["Creation Date"] = now.strftime('%d-%b-%y')
                    rec["Update Date"] = ""
                    rec["CHIP Active"] = ""
                    rec["Data Privacy"] = DPStatus    #to be determined from the DP status
                    rec["Latest Activity"] = max(line["Open Month ID"], line["Closed Month ID"])
                    rec["Activity"] = "YES" 
                    chg = 1
                    logging.info(">> New reccord " + pprint.pformat(rec, compact='true'))
                    # prepare the remaining fields
                    # write the record to O2C
                if chg == 1 :
                    O2C[keylog]= rec
                    if SDIchg == 1 : 
                        with open(CDIFile, "a", encoding='utf8', newline='') as CDI :
                            csvWriter = csv.DictWriter(CDI, CDIHeader)
                            csvWriter.writerow(rec)
            pass
    except: 
        sys.exit( LogFile + " Audit file couldn't be red")
# Create the updated Org2CHIP file
try:
    with open(OutputFile, "w", encoding='utf8', newline='') as Org2Chip:
        csvWriter = csv.DictWriter(Org2Chip, O2CHeader)
        # write the header row
        csvWriter.writeheader()
        # write all the Org2CHIP rows
        for row in iter(O2C):
            csvWriter.writerow(O2C[row])
            pass
        pass
except:
    sys.exit("Output file could not be written")
#
#Log.close()

# the end
