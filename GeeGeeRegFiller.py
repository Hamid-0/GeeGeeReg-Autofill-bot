from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import re



loginID = "username"
loginPIN = "pin"




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



web.get('https://geegeereg.uottawa.ca/geegeereg/Activities/ActivitiesDetails.asp?aid=316')

try:
    web.implicitly_wait(2)
    login = web.find_element(by=By.XPATH, value='//*[@id="toolbar-login"]/a')
    login.click()

    

    loginField = web.find_element(by=By.XPATH, value='//*[@id="ClientBarcode"]')
    loginField.send_keys(loginID)

    logjnPINField = web.find_element(by=By.XPATH, value='//*[@id="AccountPIN"]')
    logjnPINField.send_keys(loginPIN)

    loginFinal = web.find_element(by=By.XPATH, value='//*[@id="Enter"]')
    loginFinal.click()

    timesTable = web.find_element(by=By.XPATH, value='//*[@id="activity-detail-table"]')

    nextButton = web.find_element(by=By.XPATH, value='//*[@id="activity-detail-table_next"]')
    nextButtonClass = nextButton.get_attribute('class')


    # allows us to check if the next button is disabled
    nL = nextButtonClass.split(' ')
    allSlots = []

    while (not search(nL,'ui-state-disabled')): #while the next button is not disabled
            for row in timesTable.find_elements(by=By.CSS_SELECTOR,value='tr'):
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
            

            
    
except(Exception):
    print("\nAn Error has occured please launch the program again!\n")
    print()
    web.quit()
    exit()
finally:
    web.quit()




chosen =False
while(not chosen):
    print("Choose from the following times:")
    i= 0
    for slot in allSlots:
        i+=1
        print(i,"-",slot[0],"@ "+slot[1])
    choice = input("")

    if(i <10):
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
    else:
        if re.match("^(1[1-"+str(i%10)+"])$", choice) or re.match("^([1-9])$", choice) or choice == '10':
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
web2 = webdriver.Chrome()

web2.get('https://geegeereg.uottawa.ca/geegeereg/Activities/ActivitiesDetails.asp?aid=316')

try:
    web2.implicitly_wait(2)
    login = web2.find_element(by=By.XPATH, value='//*[@id="toolbar-login"]/a')
    login.click()

    

    loginField = web2.find_element(by=By.XPATH, value='//*[@id="ClientBarcode"]')
    loginField.send_keys(loginID)

    logjnPINField = web2.find_element(by=By.XPATH, value='//*[@id="AccountPIN"]')
    logjnPINField.send_keys(loginPIN)

    loginFinal = web2.find_element(by=By.XPATH, value='//*[@id="Enter"]')
    loginFinal.click()

    timesTable = web2.find_element(by=By.XPATH, value='//*[@id="activity-detail-table"]')

    nextButton = web2.find_element(by=By.XPATH, value='//*[@id="activity-detail-table_next"]')
    nextButtonClass = nextButton.get_attribute('class')
                
    nL = nextButtonClass.split(' ')
    availableSlots = []
    allSlots = []
    found = False

    while (not search(nL,'ui-state-disabled') and not found): #while the next button is not disabled
            for row in timesTable.find_elements(by=By.CSS_SELECTOR,value='tr'):
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
                        for col in row.find_elements(by=By.CSS_SELECTOR,value='td'):
                            for row2 in col.find_elements(by=By.CSS_SELECTOR,value='tr'):
                                for col2 in row2.find_elements(by=By.CSS_SELECTOR,value='td'):
                                    span = col2.find_element(by=By.TAG_NAME, value='span')
                                    if(col2.text == 'Add' and span.text == 'Add'):
                                        span.click()
                                        
            if(not found):   
                nextButtonClass = nextButton.get_attribute('class') #get the class of the next button to check if it is disabled
                nL = nextButtonClass.split(' ') #split the class into a list of words to check if it is disabled
                nextButton.click()
                

            

    if found:
        

        checkoutBtn = web2.find_elements(by=By.XPATH, value='//*[@id="RegistrationDetails"]/div[3]/div/span/span[1]/input')

        for btn in checkoutBtn:
            if btn.is_displayed():
                btn.click()
                break
        

        detailBtn = web2.find_element(by=By.XPATH, value='//*[@id="regist-detail-info-btn-show"]')
        detailBtn.click()
    else:
        print('Sorry this slot was just taken. Please try again')
        web2.quit()
except(Exception):
    print("\nAn Error has occured please launch the program again!\n")
    web2.quit()
    exit()
    

