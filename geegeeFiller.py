from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import re


# web = webdriver.Chrome()
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')





# Information for the form
loginID= '29003008097637'
loginPIN= '352428'


web = webdriver.Chrome()




web.get('https://geegeereg.uottawa.ca/geegeereg/Activities/ActivitiesDetails.asp?aid=316')

print(web.title)

login = web.find_element(by=By.XPATH, value='//*[@id="toolbar-login"]/a')
print(login)
login.click()

time.sleep(0.25)

loginField = web.find_element(by=By.XPATH, value='//*[@id="ClientBarcode"]')
loginField.send_keys(loginID)

logjnPINField = web.find_element(by=By.XPATH, value='//*[@id="AccountPIN"]')
logjnPINField.send_keys(loginPIN)

loginFinal = web.find_element(by=By.XPATH, value='//*[@id="Enter"]')
loginFinal.click()

timesTable = web.find_element(by=By.XPATH, value='//*[@id="activity-detail-table"]')

nextButton = web.find_element(by=By.XPATH, value='//*[@id="activity-detail-table_next"]')
nextButtonClass = nextButton.get_attribute('class')

def search(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False
    
i = 0
# allows us to check if the next button is disabled
nL = nextButtonClass.split(' ')
availableSlots = []
allSlots = []

while (not search(nL,'ui-state-disabled')): #while the next button is not disabled
        for row in timesTable.find_elements(by=By.CSS_SELECTOR,value='tr'):
            rL = row.text.split('\n')
            if search(rL,'Add') and (search(rL,'WORKOUT SESSION') or search(rL,'EXPRESS (1 hour) WORKOUT SESSION')):
                infoDump = rL[2] + rL[3]
                infoDump = re.sub('[-]', '', infoDump)
                infoDumpL = infoDump.split(' ')
                slot = [infoDumpL[1], infoDumpL[2]]
                allSlots.append(slot)
                
         
        nextButtonClass = nextButton.get_attribute('class') #get the class of the next button to check if it is disabled
        nL = nextButtonClass.split(' ') #split the class into a list of words to check if it is disabled
        nextButton.click()
        time.sleep(0.25)
        
web.quit()

chosen =False
while(not chosen):
    print("Choose from the following times:")
    i= 0
    for slot in allSlots:
        i+=1
        print(i,"-",slot[0],"@ "+slot[1])
    choice = input("")
    if int(choice) <= i:
            print("You have chosen:", allSlots[int(choice)-1][0],"@",allSlots[int(choice)-1][1])
            print("Confirm? (y/n)")
            confirm = input("")
            if confirm == 'y':
                chosen = True
                day = allSlots[int(choice)-1][0]
                chooseTime = allSlots[int(choice)-1][1]
            else:
                chosen = False
    else:
        print("\nPlease enter a valid option \n")
        continue

# ------------After Choice----------------------------------------------------------------------------------------------------
# create a second chrome instance to fill the form
web2 = webdriver.Chrome()

web2.get('https://geegeereg.uottawa.ca/geegeereg/Activities/ActivitiesDetails.asp?aid=316')


login = web2.find_element(by=By.XPATH, value='//*[@id="toolbar-login"]/a')
print(login)
login.click()

time.sleep(1)

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
            if search(rL,'Add') and (search(rL,'WORKOUT SESSION') or search(rL,'EXPRESS (1 hour) WORKOUT SESSION')):
                infoDump = rL[2] + rL[3]
                infoDump = re.sub('[-]', '', infoDump)
                infoDumpL = infoDump.split(' ')
                slot = [infoDumpL[1], infoDumpL[2]]
                allSlots.append(slot)
                if infoDumpL[1] == day and infoDumpL[2] == chooseTime:
                    print(infoDumpL)
                    availableSlots.append(slot)
                    i= i+1
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
            time.sleep(0.25)
        

if found:
    print('found')
    time.sleep(0.25)

    checkoutBtn = web2.find_elements(by=By.XPATH, value='//*[@id="RegistrationDetails"]/div[3]/div/span/span[1]/input')

    for btn in checkoutBtn:
        if btn.is_displayed():
            btn.click()
            break
    time.sleep(1)
    detailBtn = web2.find_element(by=By.XPATH, value='//*[@id="regist-detail-info-btn-show"]')
    detailBtn.click()
else:
    print('Sorry this slot was just taken. Please try again')
    web2.quit()

