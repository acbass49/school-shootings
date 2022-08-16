from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from functools import reduce
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def make_test_responses(usr, pswrd, SID, sessions=6, headless = False, button_clicks_per_group=12, delete_previous = False, url_variables = ['TEST=1']):

    check_if_list = ['1','2','3']
    if type(url_variables) == type(check_if_list):
        url_vars = url_variables
    else:
        url_vars = [url_variables]

    total_count = len(url_vars) * int(button_clicks_per_group)

    link = 'https://research.insights-today.com/survey-builder/'+SID+'/edit?SurveyID='+SID
    s = Service(ChromeDriverManager().install())

    if headless:
        options = Options()
        options.headless = headless
        driver = webdriver.Chrome(service=s, options=options)
    else:
        driver = webdriver.Chrome(service=s)

    print('Browser successfully launched!')
    print('Now logging in...')

    driver.get(link)
    driver.implicitly_wait(30)
    time.sleep(5)
    driver.find_elements(By.ID, 'as-template')[1].click()
    time.sleep(2)
    driver.find_element(By.ID, 'UserName').send_keys(usr)
    time.sleep(2)
    driver.find_element(By.ID, 'UserPassword').send_keys(pswrd)
    time.sleep(2)
    driver.find_element(By.ID, 'loginButton').click()
    time.sleep(10)

    print('Successfully logged in')

    if delete_previous:

        # opening data and analysis tab
        print('Opening data and analysis tab')
        driver.get('https://research.insights-today.com/responses/#/surveys/' + SID)

        # Filtering data to test responses
        driver.find_element(By.CSS_SELECTOR, 'button[data-testid="filter-btn"]').click()
        time.sleep(2)
        driver.find_element(By.ID, 'd5e52d3d-bbfe-448d-b27e-a52982a59940').click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'nested-menu._1yNSB._3nT2G').click()
        time.sleep(2)
        driver.find_elements(By.CLASS_NAME, '_ft4rj')[1].find_elements(By.CSS_SELECTOR, 'div[value]')[2].click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'filter-fragment.flex-grow.filter-dropdown._1Fhey._3DUPa._1mVlA').click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'filter-dropdown._3nT2G').click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'filter-fragment.flex-grow.filter-dropdown._1Fhey._3DUPa._1mVlA').click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, '_rfCWW._3DUPa._IatK9._1Dady').send_keys('Survey Test')
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, '_ft4rj').click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, '_MT_vr.modalFooter').find_element(By.CLASS_NAME, '_2cZss._3BX8E').click()
        time.sleep(2)
        print('Filtered data to test responses')

        try:
            # Selecting and deleting all test responses
            driver.find_element(By.CLASS_NAME, 'table-header.active-background._2POdI').find_element(By.CLASS_NAME, '_3R4pJ').click()
            time.sleep(2)
            driver.find_element(By.CLASS_NAME, 'select-all-link._91hw9').click()
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR, 'svg[data-icontype="Trash"]').click()
            time.sleep(2)

            #Confirming deleting all test responses
            driver.find_element(By.CLASS_NAME, '_3q4Mh._aayzW').find_elements(By.CSS_SELECTOR, 'input[class="_3R4pJ"]')[0].click()
            time.sleep(2)
            driver.find_element(By.CLASS_NAME, '_3q4Mh._aayzW').find_elements(By.CSS_SELECTOR, 'input[class="_3R4pJ"]')[1].click()
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR, 'button[data-testid="submit-warning-modal-btn"]').click()
            time.sleep(2)
            print('initiated deleting test responses')

            #Checking deleting progress
            time.sleep(5)
            zero_text = str(driver.find_element(By.CLASS_NAME, '_2mKqe._og_dy').text)
            count = 0
            while zero_text!= "Recorded responses (0)":
                count += 1
                driver.refresh()
                time.sleep(15)
                zero_text = str(driver.find_element(By.CLASS_NAME, '_2mKqe._og_dy').text)
                if count % 6 == 0:
                    print(zero_text)
            print("Finished deleting previous test responses!")
        except NoSuchElementException:
            zero_text = str(driver.find_element(By.CLASS_NAME, '_2mKqe._og_dy').text)
            if zero_text == "Recorded responses (0)":
                print("It appears test responses are already deleted. Generating new responses.")
            else:
                print("There was an error deleting previous test responses. You may have to delete manually. No new test responses generated. Ending process.")
                driver.quit()

    print(f'Setting up {sessions} tabs in browser for generating new test responses')
    
    if delete_previous:
        driver.get(link)
        time.sleep(5)
    
    for i in range(sessions):
        if i != 0:
            driver.execute_script("window.open('"+link+"');")
            time.sleep(6)
            driver.switch_to.window(driver.window_handles[i])
        time.sleep(3)
        driver.find_element(By.ID, 'builder-tools-menu').click()
        time.sleep(2)
        driver.find_element(By.ID, 'test-responses-tool').click()
        time.sleep(2)
        driver.find_element(By.ID,'TestIterationCount').send_keys('1000')
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'Options').click()
        time.sleep(2)
        driver.find_element(By.ID, 'AdditionalParameters').send_keys(url_vars[0])
        time.sleep(2)
        driver.find_element(By.ID, 'SurveyTesterStartButton').click()
        time.sleep(3)

    running_total_count = int(sessions)
    current_count = int(sessions)
    print(f'Count is {current_count}/{total_count} test button presses for new responses!')
    while current_count < int(button_clicks_per_group):
        a = driver.find_element(By.CLASS_NAME, 'WaitingImage').get_attribute('style')
        while a == '':
            time.sleep(3)
            a = driver.find_element(By.CLASS_NAME, 'WaitingImage').get_attribute('style')
            time.sleep(2)
        for j in range(sessions):
            driver.switch_to.window(driver.window_handles[j])
            time.sleep(2)
            driver.find_element(By.ID, 'SurveyTesterStartButton').click()
            time.sleep(2)
        current_count += int(sessions)
        running_total_count += int(sessions)
        print(f'Count is {running_total_count}/{total_count} test button presses for new responses!')  
    
    a = driver.find_element(By.CLASS_NAME, 'WaitingImage').get_attribute('style')
    while a == '':
        time.sleep(3)
        a = driver.find_element(By.CLASS_NAME, 'WaitingImage').get_attribute('style')
        time.sleep(2)
    print(f'Finished with {url_vars[0]}! Pressed test button {running_total_count} times for {url_vars[0]}.')

    if len(url_vars) >= 1:
        for i in range(1, len(url_vars)):
            for j in range(sessions):
                driver.switch_to.window(driver.window_handles[j])
                time.sleep(2)
                driver.find_element(By.ID, 'AdditionalParameters').clear()
                time.sleep(2)
                driver.find_element(By.ID, 'AdditionalParameters').send_keys(url_vars[i])
                time.sleep(2)
                driver.find_element(By.ID, 'SurveyTesterStartButton').click()
                time.sleep(3)
            
            running_total_count += int(sessions)
            current_count = int(sessions)
            print(f'Count is {running_total_count}/{total_count} test button presses!')
            
            while current_count < int(button_clicks_per_group):
                a = driver.find_element(By.CLASS_NAME, 'WaitingImage').get_attribute('style')
                while a == '':
                    time.sleep(3)
                    a = driver.find_element(By.CLASS_NAME, 'WaitingImage').get_attribute('style')
                    time.sleep(2)
                for j in range(sessions):
                    driver.switch_to.window(driver.window_handles[j])
                    time.sleep(2)
                    driver.find_element(By.ID, 'SurveyTesterStartButton').click()
                    time.sleep(2)
                current_count += int(sessions)
                running_total_count += int(sessions) 
            
            a = driver.find_element(By.CLASS_NAME, 'WaitingImage').get_attribute('style')
            while a == '':
                time.sleep(3)
                a = driver.find_element(By.CLASS_NAME, 'WaitingImage').get_attribute('style')
                time.sleep(2)
            print(f'Finished {url_vars[i]}! Pressed test button {current_count} times for {url_vars[i]}.')

    print(f'The final count is {running_total_count}/{total_count} on these URL vars: {url_vars}. Closing chrome driver now.')
    driver.quit()
