import os
import json
import subprocess
import time
import re
import math
import platform
from datetime import datetime
from tkinter import *
from tkinter import ttk
# To do
# Fix cmds
# add hddsize
# send to mongo db using the tech as collection cats
# then work on DB AutoFill to grab from mongo DB
# Work on a base for auto posting
# gather all info needed for an informative posting
systemOS = str(platform.system())

CMD_NAME = [
    'Serial',
    'Manufacturer',
    'Model',
    'Processor',
    'HDD_Size',
    'HDD_S/N',
    'Ram',
    'Video',

    ]
CMD_Linux = [
    'sudo dmidecode -s system-serial-number',
    'cat /sys/class/dmi/id/board_vendor',
    'sudo dmidecode -s system-product-name',
    "cat /proc/cpuinfo | grep 'model name' | uniq",
    'lsblk --output SIZE -n -d /dev/sda',
    'lsblk --nodeps -no serial /dev/sda',
    'sudo dmidecode -t 17 | grep "Size.*MB"',
    'sudo lshw -C display | grep product',
    ]
CMD_Windows = [
    'wmic bios get serialnumber',
    'wmic computersystem get manufacturer',
    'wmic computersystem get model',
    'wmic cpu get name',
    'fsutil volume diskfree c:', #create  divide function USE A DIFFRENT CMD
    'wmic diskdrive get serialnumber', # USE A DIFFRENT CMD 
    'systeminfo | findstr /C:"Total Physical Memory', # divide function
    'wmic path win32_VideoController get name',
    ]

def unparsed_info():
    unparsed_filename = str(systemOS) + '_UNPARSED' +'.txt'
    DB = open(unparsed_filename, "w")
    x = 0
    if systemOS == 'Linux':
        CMD = CMD_Linux
    else:
        CMD = CMD_Windows
    while x < len(CMD_NAME):
        if systemOS == 'Linux':
            cm_main = subprocess.getoutput(CMD[x])
            DB.write('\n' + CMD_NAME[x] + '\n' +  str(cm_main.replace("           "," "))  + '\n')
        else:
            cm_main = subprocess.getoutput(CMD[x].replace("\n", ""))
            DB.write(CMD_NAME[x] + '\n' +  str(cm_main.replace("           "," "))  + '\n')

        x += 1
    DB.write('\n' + '""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""' + '\n')
    DB.close()
    return
unparsed_info()
COMPUTER = []
def regex_parse():

    Windows_regex = (r"SerialNumber.*\n\n(.*)|Manufacturer.*\n\n(.*)|Model.*\n\n(.*)|Processor\nName.*\n\n(.*)|HDD_Size\n.*\n(.*)|\n"
	      r"HDD_S.*\nSerialNumber.*\n\n(.*)|Ram\nTotal.*:(.*)|Video\nName.*\n\n(.*)|Optical_Drive:(.*)|USB:(.*)|OS(.*)|\n"
	      r"Windows_LIC:(.*)|Productivity:(.*)|Office License:(.*)|OTHER:(.*)|Tech:(.*)")
    Linux_regex = (r"Serial\n(.*)|Manufacturer\n(.*)|Model\n(.*)|Processor\n.*:(.*)|HDD_Size\n(.*)|HDD_S.*\n(.*)|Ram\n.*:(.*)|Video\n.*:(.*)|Optical_Drive:(.*)|USB:(.*)|OS(.*)|Windows_LIC:(.*)|Productivity:(.*)|Office License:(.*)|OTHER:(.*)|Tech:(.*)")
    unparsed_filename = str(systemOS) + '_UNPARSED' +'.txt'
    with open(unparsed_filename) as Unparsed_File:
        output_name = ['NULL', 'SerialNumber', 'Manufacturer', 'Model',  'Processor',  'HDD_Size',  'HDD_S/N', 'Ram','Video','Optical_Drive','USB','OS','Windows_LIC','Productivity', 'Office License', 'OTHER', 'Tech']
        Unparsed_File = Unparsed_File.read()

        if systemOS == 'Linux':
            matches = re.finditer(Linux_regex, Unparsed_File, re.MULTILINE)
        else:
            matches = re.finditer(Windows_regex, Unparsed_File, re.MULTILINE)

        for match in matches:
            x = 1
            while x < 17:
                if match[x] == None:
                    null = 'null'
                else:
                    str_match = str(match[x])
                    if systemOS == 'Windows':
                        #WINDOWS ONLY
                        if x == 5:
                            HDD_REG = (r"\((.*)\)")
                            hdd_match = re.finditer(HDD_REG, str_match, re.MULTILINE)
                            for hdd in hdd_match:
                                parsed_hdd = hdd[1]
                                NO_WHITE_SPACE = parsed_hdd.replace(" ", "")
                                JSON_DICT = {output_name[x]: NO_WHITE_SPACE}
                                COMPUTER.append(JSON_DICT)
                        elif x == 7:
                            s = ''.join(x for x in str_match if x.isdigit())
                            num = int(s)
                            div = num/1024
                            ram = math.ceil(div)
                            parsed_ram = str(ram) + " GB"
                            NO_WHITE_SPACE = parsed_ram.replace(" ", "")
                            JSON_DICT = {output_name[x]: NO_WHITE_SPACE}
                            COMPUTER.append(JSON_DICT)
                        elif x ==4:
                            Intel_REG = (r"TM\)(.*)")
                            cpu_arc = 'intel'
                            AMD_REG = (r"AMD(.*)")
                            
                            if cpu_arc == 'intel':
                                
                                i_cpu_reg = Intel_REG
                                i_cpu_match = re.finditer(i_cpu_reg, str_match, re.MULTILINE)
                                for cpu_i in i_cpu_match:
                                    new_cpu = re.finditer(i_cpu_reg, str_match, re.MULTILINE)
                                a_cpu_reg = AMD_REG
                                a_cpu_match = re.finditer(a_cpu_reg, Unparsed_File, re.MULTILINE)
                                for cpu_a in a_cpu_match:
                                    new_cpu = re.finditer(a_cpu_reg, str_match, re.MULTILINE)

                            else:
                                null = 'NULL'
    
                               
                            for cpu in new_cpu:
                                parsed_cpu = cpu[1]
                                NO_WHITE_SPACE = parsed_cpu.replace(" ", "")
                                
                                JSON_DICT = {output_name[x]: NO_WHITE_SPACE}
                                COMPUTER.append(JSON_DICT)
                        else:
                            NO_WHITE_SPACE = str_match.replace(" ", "")
                            JSON_DICT = {output_name[x]: NO_WHITE_SPACE}
                            COMPUTER.append(JSON_DICT)
                    else:
                        NO_WHITE_SPACE = str_match.replace(" ", "")
                        JSON_DICT = {output_name[x]: NO_WHITE_SPACE}
                        COMPUTER.append(JSON_DICT)

                x+=1
    return
regex_parse()
INPUT = []

def input(defType, defOpt, defUsb, defOs, defWinlic, defProd, defOfficelic, defOther, defTech):

    global optVar
    global USBent
    global osVar
    global WINDLICent
    global PRODent
    global OFFICEent
    global OTHERent
    global techVar
    global typeVar
    win= Tk()
    win.title("")
    win.geometry("400x600")
    def ent():
        list = ["Optical Drice",USBent,"OS", WINDLICent,PRODent,OFFICEent,OTHERent, "Tech", "Type"]
        nameList = ['Optical Drive', 'USB', 'OS', 'Windows License', 'Productivity', 'Office License', 'OTHER', 'Tech', 'Type']
        x = 0
        while x < len(nameList):
            if x == 0:
                #Optical Drive
                if optVar.get() == 1:
                    DICT = {nameList[x]: "DVD/RW"}
                    INPUT.append(DICT)
                else:
                    DICT = {nameList[x]: "NA"}
                    INPUT.append(DICT)
            elif x == 2:
                #OS
                if osVar.get() == 1:
                    DICT = {nameList[x]: "Windows 10 Pro"}
                    INPUT.append(DICT)
                else:
                    DICT = {nameList[x]: "Linux Mint"}
                    INPUT.append(DICT)
            elif x ==7:
                # Tech
                DICT = {nameList[x]: techVar.get()}
                INPUT.append(DICT)
            elif x ==8:
                DICT = {nameList[x]: typeVar.get()}
                INPUT.append(DICT)
            else:
                Entry = list[x].get()
                if Entry == '':
                    DICT = {nameList[x]: 'N/A'}
                    INPUT.append(DICT)
                else:    
                    DICT = {nameList[x]: Entry}
                    INPUT.append(DICT)
            x+=1
        
        win.destroy()
        def confirm():
            nameList = ['Optical Drive', 'USB', 'OS', 'Windows License', 'Productivity', 'Office License', 'OTHER', 'Tech']
            def EXIT():
                win.destroy()
                for item in INPUT:
                    COMPUTER.append(item)
                json_file = 'systeminfo/' + 'parsed' + '.json'
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(COMPUTER, f, ensure_ascii=False, indent=4)


            Optical = INPUT[0]
            win= Tk()
            win.geometry("400x650")
            def edit():
                win.destroy()
                if INPUT[0]["Optical Drive"] == 'DVD/RW':
                    opt = 1
                else:
                    opt = 0
                if INPUT[2]["OS"] == 'Windows 10 Pro':
                    osin = 1
                else:
                    osin = 0
                input(defType = INPUT[8]["Type"], defOpt = opt,defUsb = INPUT[1]["USB"],defOs = osin,defWinlic = INPUT[3]["Windows License"],defProd = INPUT[4]["Productivity"],defOfficelic = INPUT[5]["Office License"],defOther = INPUT[6]["OTHER"],defTech = INPUT[7]["Tech"])
            label=Label(win, text="System Information", font=("Courier 22 bold"))
            label.pack(pady = 20)

            Type = Label(win, text="Type: " + INPUT[8]["Type"], font=("Courier 14 bold"))
            Type.pack()
            
            Serial = Label(win, text="Serial Number: " + COMPUTER[0]["SerialNumber"], font=("Courier 14 bold"))
            Serial.pack()  

            man = Label(win, text="Manufacturer: " + COMPUTER[1]["Manufacturer"],font=("Courier 14 bold"))
            man.pack()

            mod = Label(win, text="Model: " + COMPUTER[2]["Model"], font=("Courier 14 bold"))
            mod.pack()
            print(COMPUTER)
            Proc = Label(win, text="Processor: " + COMPUTER[3]["Processor"], font=("Courier 14 bold"))
            Proc.pack()
            
            HDDSize = Label(win, text="HDD Size: " + COMPUTER[4]["HDD_Size"], font=("Courier 14 bold"))
            HDDSize.pack()
            
            HDDSer = Label(win, text="HDD Serial Number: " + COMPUTER[5]["HDD_S/N"], font=("Courier 14 bold"))
            HDDSer.pack()

            Ram = Label(win, text="Ram: " + COMPUTER[6]["Ram"], font=("Courier 14 bold"))
            Ram.pack()
    
            Video = Label(win, text="Video: " + COMPUTER[7]["Video"], font=("Courier 14 bold"))
            Video.pack()
            
            OPT = Label(win, text="Optical Drive: " + INPUT[0]["Optical Drive"], font=("Courier 14 bold"))
            OPT.pack()

            USB = Label(win, text="USB : " + INPUT[1]["USB"], font=("Courier 14 bold"))
            USB.pack()
            
            OS = Label(win, text="OS: " + INPUT[2]["OS"], font=("Courier 14 bold"))
            OS.pack()
            
            WinLic = Label(win, text="Windows License: " + INPUT[3]["Windows License"], font=("Courier 14 bold"))
            WinLic.pack()
            
            Prod = Label(win, text="Productivity: " + INPUT[4]["Productivity"], font=("Courier 14 bold"))
            Prod.pack()
            
            OffLic = Label(win, text="Office License: " + INPUT[5]["Office License"], font=("Courier 14 bold"))
            OffLic.pack()
            
            Oth = Label(win, text="Other: " + INPUT[6]["OTHER"], font=("Courier 14 bold"))
            Oth.pack()
            
            tch = Label(win, text="Tech: " + INPUT[7]["Tech"], font=("Courier 14 bold"))
            tch.pack()
            
            #Create a Button to validate Entry Widget
            exbut = ttk.Button(win, text= "Re-Do",width= 20, command= edit).pack(side = BOTTOM, pady = 10)
            confbut = ttk.Button(win, text= "CONFIRM",width= 20, command= EXIT).pack(side = BOTTOM, pady = 10)

            win.mainloop()
            return
        confirm()
        return
    # Defualt Values
    MainLable=Label(win, text="System Information", font=("Courier 22 bold"))
    MainLable.pack()
    #Type
    typev=Label(win, text="System Type", font=("Courier 14 bold"))
    typev.pack()
    typeVar = StringVar(win)
    typeVar.set(defType) # Def Value
    TYPE = OptionMenu(win, typeVar, "Laptop", "Desktop")
    TYPE.pack()
    #Otpical Drive5
    optVar = IntVar(value = defOpt) #value=1 to set to checked by default
    OPT = Checkbutton(win, text='Optical Drive?',font=("Courier 14 bold"), variable=optVar, onvalue=1, offvalue=0)
    OPT.pack()
    #USB
    USB=Label(win, text="USB", font=("Courier 14 bold"))
    USB.pack()
    USBent= Entry(win, width= 2)
    USBent.insert(0, defUsb)
    USBent.focus_set()
    USBent.pack()
    #OS
    osVar = IntVar(value = defOs)
    OS = Checkbutton(win, text='Windows?',font=("Courier 14 bold"), variable=osVar, onvalue=1, offvalue=0)
    OS.pack()
    #WINDOWS_LIC
    WINDLIC=Label(win, text="Windows License", font=("Courier 14 bold"))
    WINDLIC.pack()
    WINDLICent= Entry(win, width= 30)
    WINDLICent.insert(0, defWinlic)
    WINDLICent.focus_set()
    WINDLICent.pack()
    #Productivity
    PROD=Label(win, text="Productivity", font=("Courier 14 bold"))
    PROD.pack()
    PRODent = Entry(win, width= 30)
    PRODent.insert(0, defProd)
    PRODent.focus_set()
    PRODent.pack()
    #Offcie_LIC
    OFFICE=Label(win, text="Office License", font=("Courier 14 bold"))
    OFFICE.pack()
    OFFICEent= Entry(win, width= 10)
    OFFICEent.insert(0, defOfficelic)
    OFFICEent.focus_set()
    OFFICEent.pack()
    #OTHER
    OTHER=Label(win, text="Other", font=("Courier 14 bold"))
    OTHER.pack()
    OTHERent = Entry(win, width= 40)
    OTHERent.insert(0, defOther)
    OTHERent.focus_set()
    OTHERent.pack()
    #TECH
    tech=Label(win, text="Tech Name", font=("Courier 14 bold"))
    tech.pack()
    techVar = StringVar(win)
    techVar.set(defTech) # Def Value
    TECH = OptionMenu(win, techVar, "Troy", "Malachi", "Alexander")
    TECH.pack()
    

    ttk.Button(win, text= "Confirm",width= 20, command= ent).pack(side = BOTTOM, pady = 10)

    win.mainloop()
    return
input(defType = '', defOpt = 0,defUsb = '',defOs = 0,defWinlic = '',defProd = '',defOfficelic = '',defOther = '',defTech = '')


