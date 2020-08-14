import os
import re
import base64
import time
import PIL
from selenium import webdriver
from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 600))
display.start()
driver = webdriver.Firefox()
driver.get("https://online-barcode-reader.inliteresearch.com/")

def getstring(img_data):
    from django.conf import settings
    start_time = time.time()
    with open(settings.BASE_DIR + "imageToSave.png", "wb") as fh:
        fh.write(base64.b64decode(img_data))
    driver.find_element_by_id("MainContent_chkPdf417").click()
    driver.find_element_by_id("MainContent_FileUpload1").send_keys(settings.BASE_DIR +"imageToSave.png")
    driver.find_element_by_id("MainContent_cmdReadBarcodesRed").click()
    while True:
        try:
            a = driver.find_element_by_id("MainContent_DataList1_Label5_0").text
            driver.get("https://online-barcode-reader.inliteresearch.com/")
            return a
        except:
            pass

def getdata(img_data):
    start_time = time.time()
    decode = getstring(img_data)
    cc=findcc(decode[287:307])
    lastname1 = findlastname(decode[287:307],decode[364:384])
    lastname2 = findlastname(decode[441:461],'')
    name1 = findname(decode[518:538], decode[595:605])
    name2 = findname(decode[606:615], decode[672:692])
    date = finddate(decode[749:769])
    gender = getgender(decode[749:769][-11])
    blood = decode[826:846][8:11]
    return {"time":time.time() - start_time,"cc":cc,"name":[name1,name2], "last":[lastname1,lastname2], 'date':date, 'gender':gender, 'blood':blood}

def finddate(line):
    return {"day":line[-4:-2],"month":line[-6:-4], "year":line[-10:-6]}

def getgender(word):
    if word=='F':
        return 'Femenino'
    return 'Masculino'

def findcc(line):
    cc=re.sub('[^0-9]','', line)
    for i in range(len(cc)):
        if cc[i] != '0':
            return cc[i:]
    return '0'

def findlastname(line1,line2):
    line=line1+line2
    return re.sub('[^A-Z]','', line)

def findname(semiline1,semiline2):
    line=semiline1+semiline2
    return re.sub('[^A-Z]','', line)