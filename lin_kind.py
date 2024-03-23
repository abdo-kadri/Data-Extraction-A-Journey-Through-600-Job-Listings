from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import log_info 
import time
import csv

# Constants
LOGIN_URL = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
JOB_SEARCH_URL = 'https://www.linkedin.com/jobs/search/?currentJobId=3803993180&geoId=103644278&keywords=a&location=United%20States&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&start={}'
NUM_PAGES = 1

# Initialize browser with options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-proxy-certificate-handler')
options.add_experimental_option("detach", True) 
browser = webdriver.Chrome(options=options)

# Login
browser.get(LOGIN_URL)
username = browser.find_element(By.CSS_SELECTOR, "#username")  
password = browser.find_element(By.CSS_SELECTOR,'#password')  
username.send_keys(log_info.username)
password.send_keys(log_info.password)
password.send_keys(Keys.RETURN)
time.sleep(1)
print('do a  security check after click ok : ')
input()

# Scrape job data
myItems = []
for i in range(NUM_PAGES):
    try:  
        time.sleep(1) 
        browser.get(JOB_SEARCH_URL.format(i*25))
        time.sleep(1) 
        div_scrole = browser.find_element(By.CSS_SELECTOR, ".jobs-search-results-list")
        scroll_js = "arguments[0].scroll({top: arguments[0].scrollHeight, behavior: 'smooth'})"
        browser.execute_script(scroll_js, div_scrole)
        time.sleep(1) 
        src = browser.page_source
        soup = BeautifulSoup(src , "html.parser")
        cards = soup.select('.scaffold-layout__list-container > li')
        print('cades len' + str(len(cards))) 
        for card in cards:
            try:
                elements = [card.select_one('a strong'),
                            card.select_one('.job-card-container__primary-description '),
                            card.select('.job-card-container__metadata-item')[0] if len(card.select('.job-card-container__metadata-item')) > 0 else None,
                            card.select('.job-card-container__metadata-item')[1] if len(card.select('.job-card-container__metadata-item')) > 1 else None,
                            card.select_one('time')]
                item = [element.text.strip() if element else ' ' for element in elements]
                spaces_count = sum([1 for element in item if element == ' '])
                if spaces_count  != 5 :
                    myItems.append(item)
            except Exception as e:
                print(f"Error in get info: {e}")
    except Exception as e:
        print(f"Error in get pages: {e}")  

print('myitem len :' + str(len(myItems))) 

# Save data to CSV
with open ('D:\Programming\web scraping\linkind\page_2.csv','w',encoding='utf-8-sig') as mydata:
    csvfille = csv.writer(mydata)
    csvfille.writerows(myItems)       
print('SUCCESS')

# Close browser
#browser.quit()
