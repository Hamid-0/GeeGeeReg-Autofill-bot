from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re

from selenium.webdriver.chrome.options import Options
chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")

loginID = "username"
loginPIN = "pin"



user = False
if(loginID == "username" or loginPIN == "pin"):
    print("Welcome to the GeeGeeRegFiller!")
    time.sleep(1)
    while not user:
        loginID = input("Enter your login ID: ")
        if re.match("^29003008[0-9]{6}$", loginID):
            loginPIN = input("Enter your login PIN: ")
            if re.match("^[0-9]{6}$", loginPIN):
                user = True
            else:
                print("Invalid PIN\nPlease try again.")
        else:
            print("Invalid UserID\nPlease try again.")



print("Finding Available Slots...")

web = webdriver.Chrome(options=chrome_options)

web.get('https://geegeereg.uottawa.ca/geegeereg/Activities/ActivitiesDetails.asp?aid=316')

try:
    time.sleep(0.25)
    login = web.find_element(By.ID, value='toolbar-login')
    login.click()
except:
    time.sleep(2)
    login = web.find_element(By.ID, value='toolbar-login')
    login.click()


time.sleep(0.25)
try:
    loginField = web.find_element(By.ID, value='ClientBarcode')
    loginField.send_keys(loginID)

    logjnPINField = web.find_element(By.ID, value='AccountPIN')
    logjnPINField.send_keys(loginPIN)

    loginFinal = web.find_element(By.ID, value='Enter')
    loginFinal.click()
except:
    time.sleep(2)
    loginField = web.find_element(By.ID, value='ClientBarcode')
    loginField.send_keys(loginID)

    logjnPINField = web.find_element(By.ID, value='AccountPIN')
    logjnPINField.send_keys(loginPIN)

    loginFinal = web.find_element(By.ID, value='Enter')
    loginFinal.click()

try:
    time.sleep(0.25) 
    popUpNo = web.find_element(By.XPATH,value = '//*[@id="incomplete-transaction"]/form/div[3]/table/tbody/tr/td[2]/a')
    popUpNo.click()
    web.get('https://geegeereg.uottawa.ca/geegeereg/Activities/ActivitiesDetails.asp?aid=316')
except:
    pass




allSlots = []
for i in range(0,4):

    time.sleep(0.5)
    nextButton = web.find_element(By.ID, value='activity-detail-table_next')      
    sessionType = web.find_elements(By.XPATH, value = '//*[@id="activity-course-row"]/td[1]')
    days = web.find_elements(By.XPATH, value = '//*[@id="activity-course-row"]/td[3]')
    times = web.find_elements(By.XPATH, value = '//*[@id="activity-course-row"]/td[4]')
    locations = web.find_elements(By.XPATH, value = '//*[@id="activity-course-row"]/td[6]')
    addOrNot = web.find_elements(By.XPATH, value = '//*[@id="activity-course-row"]/td[9]/table/tbody/tr[1]/td/span')
    for j in range(len(sessionType)):
        sessionTypeF = sessionType[j].text.split('\n')[0]
        timeF= times[j].text.strip(" ").split('-')[0]
        if sessionTypeF =='EXPRESS (1 hour) WORKOUT SESSION' or sessionTypeF =='WORKOUT SESSION':
            if addOrNot[j].text == 'Add':
                allSlots.append([sessionTypeF, days[j].text, timeF, locations[j].text, addOrNot[j].text])

    
    nextButton.click()




first = web.find_element(By.ID, value='activity-detail-table_first')
first.click()

web.minimize_window()            


chosen =False
while(not chosen):
    print("Choose from the following times:")
    i= 0
    for slot in allSlots:
        i+=1
        # print(i,"-",slot[1],"@"+slot[2] + "   in " + slot[3])
        print(f"{i}{' - ':2s}{slot[1]:2s}{' @'+slot[2]:10s}{'in':3s}{slot[3]:30s}")
    choice = input("")

    if(i < 10):
        if re.match("^([1-9])$", choice):
                print(f"{allSlots[int(choice)-1][1]:2s}{' @'+allSlots[int(choice)-1][2]:8s}{'in':3s}{allSlots[int(choice)-1][3]:30s}")
                print("Confirm? (y/n)")
                confirm = input("")
                if confirm == 'y':
                    chosen = True
                    chooseDay = allSlots[int(choice)-1][1]
                    chooseTime = allSlots[int(choice)-1][2]
        else:
            print("\nPlease enter a valid option \n")
    elif(i > 10):
        if re.match("^(1[1-"+str(i%10)+"])$", choice) or re.match("^([1-9])$", choice) or choice == '10':
                print(f"{allSlots[int(choice)-1][1]:2s}{' @'+allSlots[int(choice)-1][2]:8s}{'in':3s}{allSlots[int(choice)-1][3]:30s}")
                print("Confirm? (y/n)")
                confirm = input("")
                if confirm == 'y':
                    chosen = True
                    chooseDay = allSlots[int(choice)-1][1]
                    chooseTime = allSlots[int(choice)-1][2]
    else:
        if re.match("^(10)$", choice) or re.match("^([1-9])$", choice) or choice == '10':
                print(f"{allSlots[int(choice)-1][1]:2s}{' @'+allSlots[int(choice)-1][2]:8s}{'in':3s}{allSlots[int(choice)-1][3]:30s}")
                print("Confirm? (y/n)")
                confirm = input("")
                if confirm == 'y':
                    chosen = True
                    chooseDay = allSlots[int(choice)-1][1]
                    chooseTime = allSlots[int(choice)-1][2]
        else:
            print("\nPlease enter a valid option \n")
        

# ------------After Choice----------------------------------------------------------------------------------------------------
# create a second chrome instance to fill the form
web.maximize_window()

found = False

while(not found):

    time.sleep(0.5)
    nextButton = web.find_element(By.ID, value='activity-detail-table_next')      
    sessionType = web.find_elements(By.XPATH, value = '//*[@id="activity-course-row"]/td[1]')
    days = web.find_elements(By.XPATH, value = '//*[@id="activity-course-row"]/td[3]')
    times = web.find_elements(By.XPATH, value = '//*[@id="activity-course-row"]/td[4]')
    locations = web.find_elements(By.XPATH, value = '//*[@id="activity-course-row"]/td[6]')
    addOrNot = web.find_elements(By.XPATH, value = '//*[@id="activity-course-row"]/td[9]/table/tbody/tr[1]/td/span')
    for j in range(len(sessionType)):
        sessionTypeF = sessionType[j].text.split('\n')[0]
        timeF= times[j].text.strip(" ").split('-')[0]
        if days[j].text == chooseDay and timeF == chooseTime:
            addOrNot[j].click()
            found = True
    
    if not found:
        nextButton.click()



time.sleep(1)
checkoutBtn = web.find_element(By.XPATH, value='//*[@id="RegistrationDetails"]/div[3]/div/span/span[1]/input')

checkoutBtn.click()
    
    

try:
    time.sleep(0.25)
    detail = web.find_element(By.ID, value='regist-detail-info-btn-show')
    detail.click()

except:
    try:
        time.sleep(2)
        detail = web.find_element(By.ID, value='regist-detail-info-btn-show')
        detail.click()
    except:
        print("Click Complete transaction and you are good to go!")
        print("Enjoy Working Out!")
finally:
    print("Click Complete transaction and you are good to go!")
    print("Enjoy Working Out!")
        




