from selenium import webdriver
from  PROJECT.variables import DRIVERS

def send_message(cellphone, contact, message):
    driver = DRIVERS[cellphone]
    try:
        driver.find_element_by_xpath('//*[@title=\"'+ contact +'\"]').click()
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]').send_keys(message)
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[3]/button').click()
        return True
    except:
        return False

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

def find_image(message):
    try:
        image = message.find_element_by_xpath('div/div/div/div/div[2]/img')
        return image.get_attribute('src')
    except:
        return None

def find_response(message):
    try:
        response = message.find_element_by_xpath('div/div/div/div/div/div/div/div[2]/span').text
        return response
    except:
        return None

def get_messages(cellphone, contact):
    driver = DRIVERS[cellphone]
    driver.find_element_by_xpath('//*[@title=\"'+ contact +'\"]').click()
    class_ = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/div[3]/div/div/div[3]/div[2]/div/div').get_attribute("class")
    print(class_)
    class_ = class_.split(" ")[0]
    messages = driver.find_elements_by_css_selector('div.'+class_)
    texts = []
    responses = []
    owner = []
    for message in messages:
        texts.append(None)
        texts[-1] = find_text(message)

        responses.append(None)
        responses[-1] = find_response(message)

        owner.append(message.find_element_by_xpath('span').get_attribute('aria-label'))
    return get_response(texts, responses, owner)

def get_response(text, responses,owner):
    id=1
    answer=[]
    for i in range(len(text)):
        if owner[i] is not None:
            name = ["start", "green"]
        if owner[i] == "Tú:":
            name = ["end", "blue"]
        answer.append({"id": id, "name":name[0], "message":text[i], "response": responses[i], "color": name[1]})
        id+=1
    return {"code":1, "messages":answer, "owner":owner}