"""Description:
    * author: Magdy Abdelkader
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 02-11-20
    * description:This script extracts all the courses links and save it in txt file.
"""
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os


option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# MAIN ROUTINE
courses_page_url = 'https://www.swinburne.edu.au/courses/study-levels-explained/doctor-of-philosophy/'
list_of_links = []
browser.get(courses_page_url)
delay_ = 5  # seconds

# CLICK THE STUDENT TYPE BUTTON
try:
    browser.execute_script("arguments[0].click();", WebDriverWait(browser, delay_).until(
        EC.element_to_be_clickable((By.XPATH,
                                    '//*[@id="contentblock_236391403_YIA4D8YVR"]/div/div/div/div[2]/div/div/div/div[1]/form/div[1]/button/span'))))
except TimeoutException:
    pass

# SELECT THE LOCAL STUDENT TYPE (INTERNATIONAL IS PRE SELECTED)
try:
    browser.execute_script("arguments[0].click();", WebDriverWait(browser, delay_).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="filters-0-1-label"]'))))
except TimeoutException:
    pass

# CLICK SAVE BUTTON (TO SAVE THE SELECTION)
try:
    browser.execute_script("arguments[0].click();", WebDriverWait(browser, delay_).until(
        EC.element_to_be_clickable((By.XPATH,
                                    '//*[@id="contentblock_236391403_YIA4D8YVR"]/div/div/div/div[2]/div/div/div/div[1]/form/div[1]/div/div[3]/div/button[2]'))))
except TimeoutException:
    pass

# KEEP CLICKING UNTIL THERE IS NO BUTTON
condition = True
while condition:
    try:
        browser.execute_script("arguments[0].click();", WebDriverWait(browser, delay_).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="contentblock_236391403_YIA4D8YVR"]/div/div/div/div[2]/div/div/div/div[2]/footer/button'))))
    except TimeoutException:
        condition = False

# EXTRACT ALL THE LINKS TO LIST
result_elements = browser.find_elements_by_class_name('results-item')
for element in result_elements:
    link = element.get_property('href')
    list_of_links.append(link)

# SAVE TO FILE
course_links_file_path = os.getcwd().replace('\\', '/') + '/SUT_phd_links.txt'
course_links_file = open(course_links_file_path, 'w')
for link in list_of_links:
    if link is not None and link != "" and link != "\n":
        if link == list_of_links[-1]:
            course_links_file.write(link.strip())
        else:
            course_links_file.write(link.strip() + '\n')
course_links_file.close()



