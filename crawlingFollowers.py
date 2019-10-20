from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

import pandas
from selenium.webdriver.common.keys import Keys

def callCSS(target):
    waitUntilCSSselector(target, 3)
    return driver.find_element_by_css_selector(target)

def callXPATH(target):
    waitUntil(target, 3)
    return driver.find_element_by_xpath(target)

def waitUntil(xpath, batasWaktu):
    WebDriverWait(driver, batasWaktu).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

def waitUntilName(name, batasWaktu):
    WebDriverWait(driver, batasWaktu).until(
        EC.presence_of_element_located((By.NAME, name))
    )

def waitUntilCSSselector(CSSselector, batasWaktu):
    WebDriverWait(driver, batasWaktu).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, CSSselector))
    )

#konversi jumlah di IG menjadi integer python
def toInteger(String):
    return int(String.replace(",", ""))

#membersihkan karakter non-Ascii, dan mereturn lowercase String
def cleanString(String):
    String = String.lower()
    i = 0
    if "\n" in String :
        String = String.replace("\n", " ")
    
    while i < len(String):
        if(ord(String[i]) < 0 or ord(String[i]) > 127):
            String = String.replace(String[i], "")
        else:
            i += 1
    return String

#return true jika akun tersebut private, return false jika sebaliknya
def isPrivate(username):
    driver.get("https://www.instagram.com/"+username)
    output = False
    try:
        waitUntil("//div[@class = 'v1Nh3 kIKUG  _bz0w']", 5)
    #kalo error berarti akun tersebut private
    except:
        output = True
    #thanks to : https://stackoverflow.com/questions/27626783/python-selenium-browser-driver-back
    return output

#mereturn list yang berisi hashtag
def getTag(String):
    output = list()
    if String == "":
        return output
    
    String = String.split(" ")
    for i in String :
        if len(i) > 1 :
            if(i[0] == "#" and i[1] != "#"):
                output.append(i)
    return output


def waitXPATH(drv, elm, timer = 20):
    element = WebDriverWait(drv, timer).until(
    EC.presence_of_element_located((By.XPATH, elm)))
def waitName(drv, elm, timer =20):
    element = WebDriverWait(drv, timer).until(
    EC.presence_of_element_located((By.NAME, elm)))

######input
inpName = str(input("username : "))
inpPass = str(input("password : "))
inpCycle = int(input("ring : "))
inpTarget = str(input("first visited username : "))
###########

driver = webdriver.Firefox()
driver.get("https://www.instagram.com/")

waitXPATH(driver, "/html/body/span/section/main/article/div[2]/div[2]/p/a")
driver.find_element_by_xpath("/html/body/span/section/main/article/div[2]/div[2]/p/a").click()
search = ""

waitXPATH(driver, "/html/body/span/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input")
login_username = driver.find_element_by_name("username")
login_password = driver.find_element_by_name("password")

login_username.clear()
login_username.send_keys(inpName)
login_password.clear()
login_password.send_keys(inpPass)

login_password.send_keys(Keys.RETURN)

try :
    waitXPATH(driver, "//button[@class = 'aOOlW   HoLwm ']")
    ignore_pop = driver.find_element_by_xpath("//button[@class = 'aOOlW   HoLwm ']")
    ignore_pop.click()
except :
    pass

def Grab(username,mList):
    tFList = []
    yPosition = 0
    if (not isPrivate(username)):
        time.sleep(5)
        driver.get("https://www.instagram.com/"+username)
        waitUntilCSSselector("li.Y8-fY:nth-child(2) > a:nth-child(1)", 5)
        callCSS("li.Y8-fY:nth-child(2) > a:nth-child(1)").click()
        bruh = 0
        #/html/body/div[3]/div/div[2]/ul/div/li[1]/div/div[2]/div[1]/div/div/a
        #/html/body/div[3]/div/div[2]/ul/div/li[2]/div/div[2]/div[1]/div/div/a
        attempt = 0
        while (attempt < 4):
            bruh += 1
            #print(callXPATH("/html/body/div[3]/div/div[2]/ul/div/li["+str(bruh)+"]/div/div[2]/div[1]/div/div/a").text)
            #print(callXPATH("/html/body/div[3]/div/div[2]/ul/div/li["+str(bruh)+"]/div/div[1]/div[2]/div[1]/a").text)
            #print(callXPATH("/html/body/div[3]/div/div[2]/ul/div/li["+str(bruh)+"]/div/div[1]/div[2]/div[1]/a").text)
            ##f13d3639e91c72a > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)
            ##f2b4c24ae992468 > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)
            #li.wo9IH:nth-child(24) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)
            try:
                subject = callXPATH("/html/body/div[3]/div/div[2]/ul/div/li["+str(bruh)+"]/div/div[1]/div[2]/div[1]/a").text
                if not (subject in mList):
                    tFList.append(subject)
                    print(subject)
                    #print(tFList)
                attempt = 0
            except:
                try:
                    subject = callXPATH("/html/body/div[3]/div/div[2]/ul/div/li["+str(bruh)+"]/div/div[2]/div[1]/div/div/a").text
                    if not (subject in mList):
                        tFList.append(subject)
                        print(subject)
                        #print(tFList)
                    attempt = 0
                except:
                    attempt += 1
                    bruh -= 1
                    print(attempt)
                    print(bruh)
                    try:
                        waitUntilCSSselector(".isgrP", 10)
                        #driver.find_element_by_css_selector(".isgrP").send_keys(Keys.PAGE_DOWN)
                        driver.execute_script("arguments[0].scroll("+str(yPosition)+", "+str(yPosition + 450)+")", driver.find_element_by_css_selector(".isgrP"))
                        waitUntil("//a[@class = 'FPmhX notranslate _0imsa ']", 10)
                        yPosition += 450
                    except:
                        print("bruh")
                        return tFList
            
    return tFList
def Cycle(sList, tCycle):
    try:
        #output
        deList = []
        #daftar akun yg udh dikunjungi
        totList = []
        totList.extend(sList)
        deList.append(sList)
        for i in range(tCycle):
            #menyiapkan siklus
            deList.append([])
        for v in range(len(deList)-1):
            for w in deList[v]:
                deList[v+1].extend(Grab(w, totList))
                print(deList)
                totList.extend(deList[v+1])
        return deList
    except:
        return deList

u_ar_ge = []
u_ar_ge.append(inpTarget)
epicBruh = Cycle(u_ar_ge, inpCycle)
            
    
file = open("accounts.txt", "w")
file.write(str(epicBruh).replace("[", "").replace("]", "").replace(" ", "").replace("'", ""))
file.close()
