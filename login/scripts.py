from selenium import webdriver
from PIL import Image
from io import BytesIO

import time
from PROJECT.variables import DRIVERS, PROCESS, WAIT

from.models import Pedido, Sucursal
from django.http import HttpResponse

from datetime import datetime, timedelta

import base64
import _thread

from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 800))
display.start()

def createSucursal(form):
    Sucursal.objects.create(user=form['user'], cellphone=form['cellphone'], sucursal=form['sucursal'], password=form['password'])

def checkLog(user, password):
    user = Sucursal.objects.filter(user=user, password=password).last()
    if user is None:
        return {'state':False}
    return {'state':True, 'cellphone':user.cellphone, 'sucursal':user.sucursal}

def checkNumber(cellphone):
    user = Sucursal.objects.filter(cellphone=cellphone).last()
    if user is None:
        return {'state':False}
    return {'state':True}

def replace(contact):
    temp = list(contact)
    temp[0]="+"
    return "".join(temp)

def send_message(cellphone, contact, message):
    driver = DRIVERS[cellphone]
    driver.find_element_by_xpath('//*[@title=\"'+ contact +'\"]').click()
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]').send_keys(message)
    try:
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[3]/button').click()
    except:
        pass

def get_new_messages(cellphone):
    driver = DRIVERS[cellphone]

    class_ = driver.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div[1]').get_attribute("class")
    class_ = class_.split(" ")[0]
    contacts = driver.find_elements_by_css_selector('div.'+class_)
    list_contacts =[]
    for contact in contacts:
        try:
            contact.find_element_by_xpath('div/div/div[2]/div[2]/div[2]/span/div')
            name = contact.find_element_by_xpath('div/div/div[2]/div[1]/div/span/span').text
            list_contacts.append(name)
        except:
            pass
    try:
        name=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[1]/div/span').text
        if name in PROCESS[cellphone].keys():
            if not name in list_contacts:
                list_contacts.append(name)
        else:
            list_contacts.remove(name)
    except:
        pass
    return list_contacts

def find_text(message):
    try:
        text =  message.find_element_by_xpath('div/div/div/span/span')
        return text.text
    except:
        try:
            text =  message.find_element_by_xpath('div/div/div/div/span/span')
            return text.text
        except:
            return None

def get_contacts(cellphone):
    contacts=[]
    index=0
    for contact in WAIT[cellphone]:
        contacts.append({'id':index, 'name':contact})
    return {'contacts':contacts}

def get_messages(cellphone, contact):
    driver = DRIVERS[cellphone]
    driver.find_element_by_xpath('//*[@title=\"'+ contact +'\"]').click()
    class_ = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/div[3]/div/div/div[3]/div[2]/div/div').get_attribute("class")
    class_ = class_.split(" ")[0]
    messages = driver.find_elements_by_css_selector('div.'+class_)
    result=[]
    last_owner=''
    index = 0
    for message in messages:
        text=find_text(message)
        owner=message.find_element_by_xpath('span').get_attribute('aria-label')
        if owner is None:
            owner=last_owner
        last_owner=owner
        if owner=="Tú:":
            result.append({'id':index,'text':text, 'align':'right', 'color':'black', 'background':'white'})
        else:
            result.append({'id':index,'text':text, 'align':'left', 'color':'white', 'background':'purple'})
        index+=1
    return ({'messages':result})

def get_last_message(cellphone, contact):
    driver = DRIVERS[cellphone]
    driver.find_element_by_xpath('//*[@title=\"'+ contact +'\"]').click()
    class_ = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/div[3]/div/div/div[3]/div[2]/div/div').get_attribute("class")
    class_ = class_.split(" ")[0]
    messages = driver.find_elements_by_css_selector('div.'+class_)
    return find_text(messages[-1])

def states(cellphone, contact, message):
    cell= get_cellphone(cellphone,contact)
    delivery = Pedido.objects.filter(cellphone=cell).last()
    if PROCESS[cellphone][contact] == 0:
        if message == 1:
            cellphone = get_cellphone(cell,contact)
            delivery = Pedido.objects.filter(cellphone=cellphone).last()
            if delivery is None:
                WAIT[cell].append(contact)
                del PROCESS[cellphone][contact]
            else:
                send_message(cell, contact, "Su dirección es")
                send_message(cell, contact, delivery.direction + "\n1) Si\n2) No")
                PROCESS[cell][contact]=1
        if message == 2:
            send_message(cellphone, contact, "")
    elif PROCESS[cellphone][contact] == 1:
        if message == 1:
            PROCESS[cellphone][contact]=2
            send_message(cellphone,contact, "Su pedido anterior fue:\n")
            send_message(cellphone, contact, delivery.delivery)
            send_message(cellphone,contact,"1) Si desea repetir su pedido \n2) Si desea hacer cambios")
        if message == 2:
            WAIT[cellphone].append(contact)
            del PROCESS[cellphone][contact]
    elif PROCESS[cellphone][contact] == 2:
        if message == 1:
            PROCESS[cellphone][contact]=3
            send_message(cellphone,contact,"Usted va a pedir " +delivery.delivery)
            send_message(cellphone,contact,"Con un costo de $" + str(delivery.value))
            send_message(cellphone,contact,"1) Confirmar pedido\n2) Hablar con un agente")
        if message == 2:
            WAIT[cellphone].append(contact)
            del PROCESS[cellphone][contact]
    elif PROCESS[cellphone][contact] == 3:
        if message == 1:
            Pedido.objects.create(restaurant=cellphone ,cellphone=delivery.cellphone, value=delivery.value, name=delivery.name, sucursal=delivery.sucursal, delivery=delivery.delivery, direction=delivery.direction)
            send_message(cellphone, contact, "Su pedido ha sido realizado")
        if message == 2:
            WAIT[cellphone].append(contact)
        del PROCESS[cellphone][contact]

def create_delivery(form,cellphone):
    Pedido.objects.create(restaurant=cellphone, delivery=form['delivery'],cellphone=form['cellphone'], value=form['value'], name=form['client'], sucursal=form['sucursal'], direction=form['direction'])
    try:
        WAIT[cellphone].remove(form['cellphone'])
        send_message(cellphone, form['cellphone'], "El pedido ha sido creado")
    except:
        WAIT[cellphone].remove(form['client'])
        send_message(cellphone, form['client'], "El pedido ha sido creado")

def get_cellphone(cellphone, contact):
    driver = DRIVERS[cellphone]
    driver.find_element_by_xpath('//*[@title=\"'+ contact +'\"]').click()
    driver.find_element_by_xpath('//*[@id="main"]/header/div[1]').click()
    time.sleep(2)
    return driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/div[1]/div[4]/div[3]/div/div/span/span').text

def get_pedidos(sucursal, restaurant):
    deliverys=Pedido.objects.filter(sucursal=sucursal,restaurant=restaurant, state=False)
    pedidos=[]
    for delivery in deliverys:
        pedidos.append({"id":delivery.pk, "name":delivery.name, "direction":delivery.direction, "cellphone":delivery.cellphone, "delivery":delivery.delivery})
    return {'pedidos':pedidos}

def dispatch(pk, contact, cellphone):
    delivery = Pedido.objects.filter(pk=pk).first()
    delivery.state = True
    delivery.save()
    send_message(cellphone, contact, "Su pedido ha sido despachado\n")


def get_last_pedido(cell, contact):
    cellphone = get_cellphone(cell,contact)
    delivery=Pedido.objects.filter(cellphone=cellphone, restaurant=cell).last()
    if delivery is None:
        delivery=Pedido.objects.filter(cellphone=contact).last()
        if delivery is None:
            return {'form':{'client':'','direction':'','sucursal':'','cellphone':get_cellphone(cell,contact), 'delivery':''}}
    return {'form':{'client':delivery.name, 'direction':delivery.direction, 'sucursal':delivery.sucursal, 'cellphone':delivery.cellphone, 'delivery':delivery.delivery, 'value':delivery.value}}

def bot(cell, wait):
    while True:
        try:
            contacts = get_new_messages(cell)
            for contact in contacts:
                if contact in PROCESS[cell].keys():
                    message=get_last_message(cell, contact)
                    if message.isnumeric():
                        states(cell, contact, int(message))
                    else:
                        pass
                        #send_message(cell, contact, "Su mensaje no es valido")
                elif not contact in WAIT[cell]:
                    cellphone = get_cellphone(cell,contact)
                    delivery = Pedido.objects.filter(cellphone=cellphone).last()
                    if delivery is None:
                        WAIT[cell].append(contact)
                        del PROCESS[cellphone][contact]
                    else:
                        send_message(cell, contact, "Su dirección es")
                        send_message(cell, contact, delivery.direction + "\n1) Si\n2) No")
                        PROCESS[cell][contact]=1
        except:
            pass

def create_new_connection(cellphone):
    try:
        DRIVERS[cellphone].close()
    except:
        if cellphone=='':
            return {"Qr":''}
    driver = webdriver.Firefox()
    driver.get("https://web.whatsapp.com/")
    DRIVERS[cellphone] = driver
    if not cellphone in PROCESS.keys():
        PROCESS[cellphone]={}
        WAIT[cellphone]=[]
        _thread.start_new_thread(bot,(cellphone, 'wait message'))
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
            with open(cellphone+'.png', "rb") as f:
                return {'state':True, "Qr":base64.b64encode(f.read())}
        except:
            pass