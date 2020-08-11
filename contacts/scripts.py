from selenium import webdriver
from selenium.webdriver import ActionChains

from PROJECT.variables import DRIVERS
import time

def wait_connection(cellphone):
    driver = DRIVERS[cellphone]
    tried = 0
    while True:
        time.sleep(1)
        try:
            driver.find_element_by_xpath('//*[@id="side"]/header')
            return True
        except:
            tried += 1
            if tried == 30:
                driver.close()
                return False

def get_new_messages(cellphone):
    driver = DRIVERS[cellphone]
    new_messages = []
    class_ = driver.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div[1]').get_attribute("class")
    class_ = class_.split(" ")[0]
    contacts = driver.find_elements_by_css_selector('div.'+class_)
    for contact in contacts:
        try:
            contact.find_element_by_xpath('div/div/div[2]/div[2]/div[2]/span/div')
            name = contact.find_element_by_xpath('div/div/div[2]/div[1]/div/span/span').text
            new_messages.append(name)
        except:
            pass
    contacts = []
    id = 1
    for contact in new_messages:
        contacts.append({"id":id, "name": contact, "image": "https://www.tuexperto.com/wp-content/uploads/2015/07/perfil_01.jpg"})
        id+=1

    return {"code": 1, "results":contacts}

def end_conversation(cellphone, contact):
    driver = DRIVERS[cellphone]
    actionChains = ActionChains(driver)
    element = driver.find_element_by_xpath('//*[@title=\"'+ contact +'\"]')
    actionChains.context_click(element).perform()
    driver.find_element_by_xpath('//*[@title=\"'+ 'Archivar chat' +'\"]').click()
    return True