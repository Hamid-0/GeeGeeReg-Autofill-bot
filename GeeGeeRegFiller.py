from numpy import true_divide
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re



loginID = "username"
loginPIN = "pin"

loginID='29003008039142'
loginPIN='630877'


user = False
if(loginID == "username" or loginPIN == "pin"):
    print("Welcome to the GeeGeeRegFiller!")
    time.sleep(1)
    while not user:
        loginID = input("Enter your login ID: ")
        if re.match("^290030080[0-9]{5}$", loginID):
            loginPIN = input("Enter your login PIN: ")
            if re.match("^[0-9]{6}$", loginPIN):
                user = True
            else:
                print("Invalid PIN\nPlease try again.")
        else:
            print("Invalid UserID\nPlease try again.")



# Auxuliary Functions
def search(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False
    

web = webdriver.Chrome()
    # Enters text "qwerty" with keyDown SHIFT key and after keyUp SHIFT key (QWERTYqwerty)

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




# allows us to check if the next button is disabled
allSlots = []
finalPage = False
while (not finalPage): #while the next button is not disabled
        try:
            time.sleep(0.25)
            nextButton = web.find_element(By.ID, value='activity-detail-table_next')
            nextButtonClass = nextButton.get_attribute('class')
            # allows us to check if the next button is disabled
            nL = nextButtonClass.split(' ')
            timesTable = web.find_element(By.ID, value='activity-detail-table')
            pageNums = web.find_elements(By.ID, 'activity-detail-table_paginate')
            nums = pageNums[0].find_elements(By.CSS_SELECTOR, 'span')
        except:
            time.sleep(4)
            nextButton = web.find_element(By.ID, value='activity-detail-table_next')
            nextButtonClass = nextButton.get_attribute('class')
            # allows us to check if the next button is disabled
            nL = nextButtonClass.split(' ')
            timesTable = web.find_element(By.ID, value='activity-detail-table')
            pageNums = web.find_elements(By.ID, 'activity-detail-table_paginate')
            nums = pageNums[0].find_elements(By.CSS_SELECTOR, 'span')
        if nums[0].text == '23456':
                finalPage = True
        else:
                
            
            for row in timesTable.find_elements(By.CSS_SELECTOR, 'tr'):
                
                rL = row.text.split('\n')
                if (len(rL) > 2 and (rL[0] == 'WORKOUT SESSION' or rL[0] == 'EXPRESS (1 hour) WORKOUT SESSION')):
                    if(len(rL)>=6 and rL[5]=='Add'):
                        infoDump = rL[2] + rL[3]
                        infoDump = re.sub('[-]', '', infoDump)
                        infoDumpL = infoDump.split(' ')
                        slot = [infoDumpL[1], infoDumpL[2]]
                        allSlots.append(slot)
                
        
        nextButtonClass = nextButton.get_attribute('class') #get the class of the next button to check if it is disabled
        nL = nextButtonClass.split(' ') #split the class into a list of words to check if it is disabled
        nextButton.click()
            

            
chosen =False
while(not chosen):
    print("Choose from the following times:")
    i= 0
    for slot in allSlots:
        i+=1
        print(i,"-",slot[0],"@ "+slot[1])
        
    choice = input("")

    if(i < 10):
        if re.match("^([1-9])$", choice):
                print("You have chosen:", allSlots[int(choice)-1][0],"@",allSlots[int(choice)-1][1])
                print("Confirm? (y/n)")
                confirm = input("")
                if confirm == 'y':
                    chosen = True
                    day = allSlots[int(choice)-1][0]
                    chooseTime = allSlots[int(choice)-1][1]
        else:
            print("\nPlease enter a valid option \n")
    elif(i > 10):
        if re.match("^(1[1-"+str(i%10)+"])$", choice) or re.match("^([1-9])$", choice) or choice == '10':
                print("You have chosen:", allSlots[int(choice)-1][0],"@",allSlots[int(choice)-1][1])
                print("Confirm? (y/n)")
                confirm = input("")
                if confirm == 'y':
                    chosen = True
                    day = allSlots[int(choice)-1][0]
                    chooseTime = allSlots[int(choice)-1][1]
    else:
        if re.match("^(10)$", choice) or re.match("^([1-9])$", choice) or choice == '10':
                print("You have chosen:", allSlots[int(choice)-1][0],"@",allSlots[int(choice)-1][1])
                print("Confirm? (y/n)")
                confirm = input("")
                if confirm == 'y':
                    chosen = True
                    day = allSlots[int(choice)-1][0]
                    chooseTime = allSlots[int(choice)-1][1]
        else:
            print("\nPlease enter a valid option \n")
        

# ------------After Choice----------------------------------------------------------------------------------------------------
# create a second chrome instance to fill the form
first = web.find_element(By.ID, value='activity-detail-table_first')
first.click()


availableSlots = []

found = False

while (not found): 
        try:
            time.sleep(0.25)
            nextButton = web.find_element(By.ID, value='activity-detail-table_next')
            nextButtonClass = nextButton.get_attribute('class')
            # allows us to check if the next button is disabled
            nL = nextButtonClass.split(' ')
            timesTable2 = web.find_element(By.ID, value='activity-detail-table')
        except:
            time.sleep(4)
            nextButton = web.find_element(By.ID, value='activity-detail-table_next')
            nextButtonClass = nextButton.get_attribute('class')
            # allows us to check if the next button is disabled
            nL = nextButtonClass.split(' ')
            timesTable2 = web.find_element(By.ID, value='activity-detail-table')  
        
        
        for row in timesTable2.find_elements(By.CSS_SELECTOR, 'tr'):

            try:

                rL = row.text.split('\n')
            except:
                time.sleep(1)
                rL = row.text.split('\n')


            if (len(rL) > 2 and (rL[0] == 'WORKOUT SESSION' or rL[0] == 'EXPRESS (1 hour) WORKOUT SESSION')):
                if(len(rL)>=6 and rL[5]=='Add'):
                    infoDump = rL[2] + rL[3]
                    infoDump = re.sub('[-]', '', infoDump)
                    infoDumpL = infoDump.split(' ')
                    slot = [infoDumpL[1], infoDumpL[2]]
                    allSlots.append(slot)
                if infoDumpL[1] == day and infoDumpL[2] == chooseTime:
                    
                    availableSlots.append(slot)
                    found = True
                    for col in row.find_elements(By.CSS_SELECTOR,value='td'):
                        for row2 in col.find_elements(By.CSS_SELECTOR,value='tr'):
                            for col2 in row2.find_elements(By.CSS_SELECTOR,value='td'):
                                span = col2.find_element(By.TAG_NAME, value='span')
                                if(col2.text == 'Add' and span.text == 'Add'):
                                    span.click()
                                    
        if(not found):   
            nextButtonClass = nextButton.get_attribute('class') #get the class of the next button to check if it is disabled
            nL = nextButtonClass.split(' ') #split the class into a list of words to check if it is disabled
            nextButton.click()
            

        

if found:
    try:
        time.sleep(0.25)
        checkoutBtn = web.find_elements(By.XPATH, value='//*[@id="RegistrationDetails"]/div[3]/div/span/span[1]/input')
    except:
        time.sleep(2)
        checkoutBtn = web.find_elements(By.XPATH, value='//*[@id="RegistrationDetails"]/div[3]/div/span/span[1]/input')
    if(len(checkoutBtn) >= 0):
        checkoutBtn[0].click()
    else:
        checkoutBtn.Key.ENTER
    
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
            
    
    
else:
    print('Sorry this slot was just taken. Please try again')
    web.quit()


