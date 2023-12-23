from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

service = Service(executable_path='chromedriver.exe')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--window-size=1920,1080")  # You can adjust the dimensions as needed

driver = webdriver.Chrome(options=chrome_options,service=service)

# go into pracuj
driver.get("https://pracuj.pl")

# accept cookies
WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'size-medium.variant-primary.core_b1fqykql')))

accept_cookie_btn = driver.find_element(By.CLASS_NAME, 'size-medium.variant-primary.core_b1fqykql')
accept_cookie_btn.click()

# input search phrases
WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'core_fhefgxl'))
)
what_search_inputs = driver.find_elements(By.CLASS_NAME, 'core_fhefgxl')

search_phrases = ['Python','', 'Wrocław']
for el_num, zipp in enumerate(zip(what_search_inputs, search_phrases)):
    if el_num ==1:
        continue
    element , phrase = zipp
    element.send_keys(phrase)
    element.click()

# # choose job level
# WebDriverWait(driver,5).until(
#     EC.presence_of_element_located((By.CLASS_NAME, 'focused.size-small.variant-ghost.core_b1fqykql'))
# )
# job_level = driver.find_elements(By.CLASS_NAME, 'focused.size-small.variant-ghost.core_b1fqykql')
# job_level.click()

# search
WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'size-large.variant-primary.core_b1fqykql'))
)
search = driver.find_element(By.CLASS_NAME, 'size-large.variant-primary.core_b1fqykql')
search.click()

# select offerts
WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'tiles_b4e7s16.core_po9665q'))
)

offers_on_page = driver.find_elements(By.CLASS_NAME, 'tiles_b4e7s16.core_po9665q')

offer_descriptrions = {}
for i in range(len(offers_on_page)):
    WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'tiles_b4e7s16.core_po9665q'))
    )
    offer = driver.find_elements(By.CLASS_NAME, 'tiles_b4e7s16.core_po9665q')[i]
    offer.click()
    try:
        WebDriverWait(driver,5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-scroll-id="job-title"]'))
        )
    except Exception:
        continue
    link_to_job_page = driver.current_url
    offer_descriptrions.setdefault(link_to_job_page, {})

    # job title
    job_title = driver.find_element(By.CSS_SELECTOR, '[data-scroll-id="job-title"]')
    offer_descriptrions[link_to_job_page].setdefault('job_title', job_title.text)
    
    # get offer overview
    job_overview_ul = driver.find_element(By.CLASS_NAME, 'offer-vieweLojfZ')
    li_in_job_overview = job_overview_ul.find_elements(By.TAG_NAME, 'li')

    offer_descriptrions[link_to_job_page].setdefault('offer_desc', [])
    for li in li_in_job_overview:
        offer_descriptrions[link_to_job_page]['offer_desc'].append(li.text)

    # get offer requirements
    offer_requirements = driver.find_element(By.CLASS_NAME,'offer-view6lWuAT')
    li_in_job_requirements = driver.find_elements(By.TAG_NAME,'li')
    offer_descriptrions[link_to_job_page].setdefault('offer_requirements', [])
    for li in li_in_job_requirements:
        offer_descriptrions[link_to_job_page]['offer_requirements'].append(li.text)
    

    driver.back()

    
with open('offers.json', 'w') as f:
    json.dump(offer_descriptrions, f)

driver.quit()


