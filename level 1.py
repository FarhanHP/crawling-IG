from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
import time
import pandas as pd

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
    driver.get("https://www.instagram.com/"+username)
    output = False
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


driver = webdriver.Firefox()

#load data level1
try :
    df = pd.read_csv("level 1.csv")
except:
    data = dict()
    data["ACCOUNTS"] = list()
    data["POSTS"] = list()
    data["TAGS"] = list()
    data["LIKES"] = list()
    data["COMMENTS"] = list()
    df = pd.DataFrame(data)

#list yang berisi daftar akun instagram yang akan dikunjungi
unvisitedAccounts = list()

temp = open("accounts.txt", "r")
unvisitedAccounts = temp.read().split(",")
temp.close()

#list yang berisi daftar akun instagram yang sudah dikunjungi
visitedAccounts = list()
for account in df["ACCOUNTS"]:
    if account not in visitedAccounts:
        visitedAccounts.append(account)

index = len(df["ACCOUNTS"])
print(index)
#mulai crawling
while len(unvisitedAccounts) > 0 :
    #mencari akun selanjutnya
    currentAccount = unvisitedAccounts.pop(0)
    while (currentAccount == "" or currentAccount in visitedAccounts or isPrivate(currentAccount) ) and len(unvisitedAccounts) > 0:
        currentAccount = unvisitedAccounts.pop(0)
    print(currentAccount)

    #mengunjungi halaman akun
    driver.get("https://www.instagram.com/"+currentAccount)
    time.sleep(5)

    try:
        waitUntilCSSselector("button[class = 'dCJp8 afkep xqRnw']", 5)
        driver.find_element_by_css_selector("button[class = 'dCJp8 afkep xqRnw']").click()
    #kalo gaada lewatin
    except:
        pass
    
    #mengambil jumlah postingan
    waitUntilCSSselector("span[class = 'g47SY ']", 5)
    jmlhPosts = toInteger(driver.find_element_by_css_selector("span[class *= 'g47SY ']").text)

    #jumlah postingan maksimal 1000
    if jmlhPosts > 1000 :
        jmlhPosts = 1000

    #klik postingan pertama
    waitUntilCSSselector("div[class = 'v1Nh3 kIKUG  _bz0w']", 5)
    driver.find_element_by_css_selector("div[class = 'v1Nh3 kIKUG  _bz0w']").click()
            
    #crawling semua postingan
    for i in range(jmlhPosts):
        #mengambil jumlah likes
        #kalo foto
        try:
            waitUntilCSSselector("._8A5w5 > span", 5)
            like = toInteger(driver.find_element_by_css_selector("._8A5w5 > span").text)
        #kalo video
        except:
            try :
                waitUntilCSSselector("span[class = 'vcOH2']", 5)
                driver.find_element_by_css_selector("span[class = 'vcOH2']").click()
                like = toInteger(driver.find_element_by_css_selector("div[class = 'vJRqr'] > span").text)
                driver.find_element_by_css_selector("div[class = 'QhbhU']").click()
            #kalo error skip postnya
            except :
                try:
                    print(1)
                    #klik tombol next
                    waitUntilCSSselector("a[class *= 'HBoOv coreSpriteRightPaginationArrow']", 5)
                    driver.find_element_by_css_selector("a[class *= 'HBoOv coreSpriteRightPaginationArrow']").click()
                    continue
                #kalo error crawling postnya berhenti
                except:
                    break
                        
                
        descTemp = str()
        #ngambil caption
        try:
            descTemp = cleanString(driver.find_element_by_css_selector("div[class *= 'C7I1f X7jCj'] > div[class *= 'C4VMK'] > span").text)
        except:
            pass

        #mengambil tag yang ada di caption
        tags = getTag(descTemp)

        #mengambil komentar
        comment = list()
        try:
            waitUntilCSSselector("div.C7I1f > div.C4VMK > span", 5)
            comment = driver.find_elements_by_css_selector("div.C7I1f > div.C4VMK > span")
            if descTemp != 0 :
                comment = comment[1:]
        except:
            pass
        for ii in range(len(comment)):
            comment[ii] = cleanString(comment[ii].text)

        df.loc[index] = [currentAccount, descTemp, tags, like, comment]
        df.to_csv("level 1.csv", index=False)
        index += 1
        print(index)

        if i < jmlhPosts - 1 :
            try:
                #klik tombol next
                waitUntilCSSselector("a[class *= 'HBoOv coreSpriteRightPaginationArrow']", 5)
                driver.find_element_by_css_selector("a[class *= 'HBoOv coreSpriteRightPaginationArrow']").click()
            except:
                break

    #close post
    waitUntilCSSselector("button[class *= 'ckWGn']", 5)
    driver.find_element_by_css_selector("button[class *= 'ckWGn']").click()
        
print("Crawling is done")
