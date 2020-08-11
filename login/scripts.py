from selenium import webdriver
from PIL import Image
from io import BytesIO

import time
from PROJECT.variables import DRIVERS, BOT

from django.http import HttpResponse
from messages.scripts import send_message

import base64
import _thread

def get_new_messages(cellphone):
    driver = DRIVERS[cellphone]

    class_ = driver.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div[1]').get_attribute("class")
    class_ = class_.split(" ")[0]
    contacts = driver.find_elements_by_css_selector('div.'+class_)
    for contact in contacts:
        try:
            contact.find_element_by_xpath('div/div/div[2]/div[2]/div[2]/span/div')
            name = contact.find_element_by_xpath('div/div/div[2]/div[1]/div/span/span').text
            message = contact.find_element_by_xpath('div/div/div[2]/div[2]/div/span/span').text
            for i in BOT[cellphone].keys():
                if i in message.lower():
                    create_message(cellphone, name, BOT[cellphone][i])
        except:
            pass
    return

def create_message(cellphone, name, message):
    message=message.replace(":name:", findname(DRIVERS[cellphone], name))
    print(message)
    send_message(cellphone, name, message)

def findname(driver, name):
    if '+' not in name:
        return name
    try:
        driver.find_element_by_xpath('//*[@title=\"'+ name +'\"]').click()
        driver.find_element_by_xpath('//*[@id="main"]/header/div[2]/div').click()
        name2 = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/div[1]/div[1]/div[2]/span/span').text
        print(name2)
        return name2
    except:
        return ''

def bot(cell, wait):
    while True:
        try:
            get_new_messages(cell)
        except:
            pass


def create_new_connection(cellphone):
    try:
        DRIVERS[cellphone].close()
    except:
        pass
    driver = webdriver.Firefox()
    driver.get("https://web.whatsapp.com/")
    while True:
        try:
            time.sleep(2)
            canvas = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/div/div[2]/div')
            location = canvas.location
            size = canvas.size
            png = driver.get_screenshot_as_png()

            Qr = Image.open(BytesIO(png)) # uses PIL library to open image in memory
            left = location['x']-10
            top = location['y']-10
            right = location['x'] + size['width']+10
            bottom = location['y'] + size['height']+10

            Qr = Qr.crop((left, top, right, bottom)) # defines crop points
            Qr.save(cellphone+'.png') # saves new cropped image
            
            DRIVERS[cellphone] = driver

            _thread.start_new_thread(bot,(cellphone, 'wait message'))
            with open(cellphone+'.png', "rb") as f:
                return {"code":1, "Qr":base64.b64encode(f.read())}
        except:
            pass