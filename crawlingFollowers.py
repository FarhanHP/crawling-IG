from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
#from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

#return true jika diblok instagram
def isError():
    try :
        waitUntilCSSselector("div[class = 'main -cx-PRIVATE-Page__main -cx-PRIVATE-Page__main__']", 2)
    except :
        return False
    return True
    

#return true jika suatu element ada
def checkIfCSSselectorExist(CSSselector):
    try:
        waitUntilCSSselector(CSSselector, 2)
    except:
        return False
    return True

#thanks to : https://selenium-python.readthedocs.io/waits.html
#program berhenti sampai element tertentu pada html muncul
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
    time.sleep(5)
    driver.get("https://www.instagram.com/"+username)
    output = False
    if(isError()):
        return output
    try:
        waitUntil("//div[@class = 'v1Nh3 kIKUG  _bz0w']", 5)
    #kalo error berarti akun tersebut private
    except:
        output = True
    #thanks to : https://stackoverflow.com/questions/27626783/python-selenium-browser-driver-back
    driver.execute_script("window.history.go(-1)")
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


url = "https://www.instagram.com/accounts/login/"

usernameIG = input('username : ')
password = input('password : ')
jumlahAkun = int(input('masukkan jumlah akun yang ingin diambil : '))
akunPertama = input('username akun yang ingin dikunjungi pertama kali (harus public) : ')

driver = webdriver.Firefox()
driver.get(url)

unvisitedAccounts2 = [akunPertama]
#output
unvisitedAccounts1 = [akunPertama]
visitedAccounts = []

waitUntilName("username", 20)

#memasukkan username dan password instagram
driver.find_element_by_name("username").send_keys(usernameIG)
driver.find_element_by_name("password").send_keys(password)

waitUntil("/html/body/span/section/main/div/article/div/div[1]/div/form/div[4]/button/div", 20)

#mengklik tombol login instagram
driver.find_element_by_xpath("/html/body/span/section/main/div/article/div/div[1]/div/form/div[4]/button/div").click()

time.sleep(5)

#jika muncul notif untuk menyalakan notifikasi instagram di browser
try:
    waitUntil("//button[@class = 'aOOlW   HoLwm ']", 10)
    driver.find_element_by_xpath("//button[@class = 'aOOlW   HoLwm ']").click()
#kalo gaada lewatin aja
except:
    pass

#mengunjungi akun untuk mengambil followers instagram
while len(unvisitedAccounts1) < jumlahAkun:
    
    #mencari akun selanjutnya
    currentAccount = unvisitedAccounts2.pop(0)
    while isPrivate(currentAccount) and len(unvisitedAccounts2) > 0:
        time.sleep(5)
        currentAccount = unvisitedAccounts2.pop(0)

    #mengunjungi halaman akun
    driver.get("https://www.instagram.com/"+currentAccount)
    visitedAccounts.append(currentAccount)
    time.sleep(5)

    if(isError()):
        break
    
    #mengambil jumlah follower
    try:
        waitUntil("/html/body/span/section/main/div/header/section/ul/li[2]/a/span", 10)
        jmlhFollowers = toInteger(driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title"))
    except:
        continue

    #jumlah followers dibatasi hanya 100 teratas untuk menghindari pembatasan dari instagram
    if jmlhFollowers > 50 :
        jmlhFollowers = 50
            
    #klik list followers
    waitUntil("//a[@class = '-nal3 ']", 10)
    driver.find_element_by_xpath("//a[@class = '-nal3 ']").click()

    #mengambil semua id followers
    acc = list()
    yPosition = 0
    while len(acc) < jmlhFollowers :
        try:
            waitUntilCSSselector(".isgrP", 10)
            #driver.find_element_by_css_selector(".isgrP").send_keys(Keys.PAGE_DOWN)
            driver.execute_script("arguments[0].scroll("+str(yPosition)+", "+str(yPosition + 250)+")", driver.find_element_by_css_selector(".isgrP"))
        
            waitUntil("//a[@class = 'FPmhX notranslate _0imsa ']", 10)
            acc = driver.find_elements_by_xpath("//a[@class = 'FPmhX notranslate _0imsa ']")
            yPosition += 250
        except:
            break

        if checkIfCSSselectorExist("div[class = 'W1Bne   ztp9m ']"):
            time.sleep(5)
            if checkIfCSSselectorExist("div[class = 'W1Bne   ztp9m ']"):
                break

    #memasukkan semua id followers ke unvisitedAccounts
    for i in range(len(acc)):
        if acc[i].text not in visitedAccounts:
            unvisitedAccounts1.append(acc[i].text)
            unvisitedAccounts2.append(acc[i].text)

    #menutup tab list followers
    waitUntilCSSselector("div.WaOAr", 5)
    driver.find_elements_by_css_selector("div.WaOAr")[1].click()

driver.close()

file = open("accounts.txt", "w")
file.write(str(unvisitedAccounts1).replace("[", "").replace("]", "").replace(" ", "").replace("'", ""))
file.close()
