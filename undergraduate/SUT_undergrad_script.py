"""Description:
    * author: Magdy Abdelkader
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 02-11-20
    * description:This script extracts the corresponding undergraduate courses details and tabulate it.
"""

import csv
import re
import time
from pathlib import Path
from selenium import webdriver
import bs4 as bs4
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
import copy
from CustomMethods import TemplateData
from CustomMethods import DurationConverter as dura

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/SUT_undergrad_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/SUT_undergrad.csv'

course_data = {'Level_Code': '', 'University': 'Swinburne University of Technology', 'City': '', 'Country': 'Australia',
               'Course': '', 'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD', 'Currency_Time': 'year',
               'Duration': '', 'Duration_Time': '', 'Full_Time': '', 'Part_Time': '', 'Prerequisite_1': '',
               'Prerequisite_2': 'IELTS', 'Prerequisite_3': '', 'Prerequisite_1_grade': '', 'Prerequisite_2_grade': '6.0',
               'Prerequisite_3_grade': '', 'Website': '', 'Course_Lang': '', 'Availability': '', 'Description': '',
               'Career_Outcomes': '', 'Online': '', 'Offline': '', 'Distance': '', 'Face_to_Face': '',
               'Blended': '', 'Remarks': ''}

possible_cities = {'rockhampton': 'Rockhampton', 'cairns': 'Cairns', 'bundaberg': 'Bundaberg', 'townsville': 'Townsville',
                   'online': 'Online', 'gladstone': 'Gladstone', 'mackay': 'Mackay', 'mixed': 'Online', 'yeppoon': 'Yeppoon',
                   'brisbane': 'Brisbane', 'sydney': 'Sydney', 'queensland': 'Queensland', 'melbourne': 'Melbourne',
                   'albany': 'Albany', 'perth': 'Perth', 'adelaide': 'Adelaide', 'noosa': 'Noosa', 'emerald': 'Emerald'}

possible_languages = {'Japanese': 'Japanese', 'French': 'French', 'Italian': 'Italian', 'Korean': 'Korean',
                      'Indonesian': 'Indonesian', 'Chinese': 'Chinese', 'Spanish': 'Spanish'}

course_data_all = []
level_key = TemplateData.level_key  # dictionary of course levels
faculty_key = TemplateData.faculty_key  # dictionary of course levels

# GET EACH COURSE LINK
for each_url in course_links_file:
    actual_cities = []
    remarks_list = []
    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(1)

    # SAVE COURSE URL
    course_data['Website'] = pure_url

    # SAVE COURSE TITLE
    title = soup.find('h1', id='course-title')
    if title:
        course_data['Course'] = title.get_text().strip()
        print('COURSE TITLE: ', title.get_text().strip())

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i
    print('COURSE LEVEL CODE: ', course_data['Level_Code'])

    # DECIDE THE FACULTY
    for i in faculty_key:
        for j in faculty_key[i]:
            if j.lower() in course_data['Course'].lower():
                course_data['Faculty'] = i
    print('COURSE FACULTY: ', course_data['Faculty'])

    # COURSE DESCRIPTION
    description_tag = soup.find('div', class_='')
    if description_tag:
        description_list = []
        description_tag_1 = description_tag.find_next('div', class_='with-margins general-content')
        if description_tag_1:
            description = description_tag_1.find_all('p')
            for p in description:
                description_list.append(p.get_text().strip())
            description_list = ' '.join(description_list)
            course_data['Description'] = description_list
            print('COURSE DESCRIPTION: ', description_list)

    # COURSE LANGUAGE
    for language in possible_languages:
        if language in course_data['Course']:
            course_data['Course_Lang'] = language
        else:
            course_data['Course_Lang'] = 'English'
    print('COURSE LANGUAGE: ', course_data['Course_Lang'])

    # DURATION & DURATION_TIME / PART-TIME & FULL-TIME
    list_of_course_info_tags = soup.find_all('div', class_='course-info l-span-3')
    if list_of_course_info_tags:
        for index, duration_container in enumerate(list_of_course_info_tags):
            if index == 1:
                duration_tag = duration_container.find('h3')
                if duration_tag:
                    duration = duration_tag.find_next_sibling('p')
                    if duration:
                        part_full_time = duration.find_next_sibling('p')
                        if part_full_time:
                            if 'full-time' in part_full_time.get_text().lower().strip():
                                course_data['Full_Time'] = 'yes'
                            else:
                                course_data['Full_Time'] = 'no'
                            if 'part-time' in part_full_time.get_text().lower().strip():
                                course_data['Part_Time'] = 'yes'
                            else:
                                course_data['Part_Time'] = 'no'
                            print('FULL-TIME/PART-TIME: ',  course_data['Full_Time'] + ' / ' + course_data['Part_Time'])
                        converted_duration = dura.convert_duration(duration.get_text().strip())
                        if converted_duration is not None:
                            duration_list = list(converted_duration)
                            if duration_list[0] == 1 and 'Years' in duration_list[1]:
                                duration_list[1] = 'Year'
                            elif duration_list[0] == 1 and 'Months' in duration_list[1]:
                                duration_list[1] = 'Month'
                            course_data['Duration'] = duration_list[0]
                            course_data['Duration_Time'] = duration_list[1]
                            print('DURATION/DURATION-TIME', str(course_data['Duration']) + ' / ' + course_data['Duration_Time'])

    # DELIVERY
    delivery_tag = soup.find('h2', id='course-subtitle')
    if delivery_tag:
        delivery_text = delivery_tag.get_text().lower().strip()
        if 'blended' in delivery_text:
            course_data['Blended'] = 'yes'
        else:
            course_data['Blended'] = 'no'
        if 'digital' in delivery_text:
            course_data['Distance'] = 'yes'
        else:
            course_data['Distance'] = 'no'
        if 'on-campus' in delivery_text:
            course_data['Offline'] = 'yes'
            course_data['Face_to_Face'] = 'yes'
        else:
            course_data['Offline'] = 'no'
            course_data['Face_to_Face'] = 'no'
        if 'oua' in delivery_text:
            course_data['Online'] = 'yes'
        else:
            course_data['Online'] = 'no'
        print('DELIVERY: online: ' + course_data['Online'] + ' offline: ' + course_data['Offline'] + ' face to face: ' +
              course_data['Face_to_Face'] + ' blended: ' + course_data['Blended'] + ' distance: ' +
              course_data['Distance'])




