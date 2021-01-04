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
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException, \
    StaleElementReferenceException, JavascriptException, ElementClickInterceptedException
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
course_links_file_path = course_links_file_path.__str__() + '/SUT_master_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/SUT_master.csv'

course_data = {'Level_Code': '', 'University': 'Swinburne University of Technology', 'City': '', 'Country': 'Australia',
               'Course': '', 'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD', 'Currency_Time': 'year',
               'Duration': '', 'Duration_Time': '', 'Full_Time': '', 'Part_Time': '', 'Prerequisite_1': 'IELTS',
               'Prerequisite_2': '', 'Prerequisite_3': '', 'Prerequisite_1_grade': '6.5', 'Prerequisite_2_grade': '',
               'Prerequisite_3_grade': '', 'Website': '', 'Course_Lang': '', 'Availability': '', 'Description': '',
               'Career_Outcomes': '', 'Online': '', 'Offline': '', 'Distance': '', 'Face_to_Face': '',
               'Blended': '', 'Remarks': '', 'Subject_or_Unit_1': '',
               'Subject_Objective_1': '', 'Subject_Description_1': '',
               'Subject_or_Unit_2': '', 'Subject_Objective_2': '', 'Subject_Description_2': '',
               'Subject_or_Unit_3': '', 'Subject_Objective_3': '', 'Subject_Description_3': '',
               'Subject_or_Unit_4': '', 'Subject_Objective_4': '', 'Subject_Description_4': '',
               'Subject_or_Unit_5': '', 'Subject_Objective_5': '', 'Subject_Description_5': '',
               'Subject_or_Unit_6': '', 'Subject_Objective_6': '', 'Subject_Description_6': '',
               'Subject_or_Unit_7': '', 'Subject_Objective_7': '', 'Subject_Description_7': '',
               'Subject_or_Unit_8': '', 'Subject_Objective_8': '', 'Subject_Description_8': '',
               'Subject_or_Unit_9': '', 'Subject_Objective_9': '', 'Subject_Description_9': '',
               'Subject_or_Unit_10': '', 'Subject_Objective_10': '', 'Subject_Description_10': '',
               'Subject_or_Unit_11': '', 'Subject_Objective_11': '', 'Subject_Description_11': '',
               'Subject_or_Unit_12': '', 'Subject_Objective_12': '', 'Subject_Description_12': '',
               'Subject_or_Unit_13': '', 'Subject_Objective_13': '', 'Subject_Description_13': '',
               'Subject_or_Unit_14': '', 'Subject_Objective_14': '', 'Subject_Description_14': '',
               'Subject_or_Unit_15': '', 'Subject_Objective_15': '', 'Subject_Description_15': '',
               'Subject_or_Unit_16': '', 'Subject_Objective_16': '', 'Subject_Description_16': '',
               'Subject_or_Unit_17': '', 'Subject_Objective_17': '', 'Subject_Description_17': '',
               'Subject_or_Unit_18': '', 'Subject_Objective_18': '', 'Subject_Description_18': '',
               'Subject_or_Unit_19': '', 'Subject_Objective_19': '', 'Subject_Description_19': '',
               'Subject_or_Unit_20': '', 'Subject_Objective_20': '', 'Subject_Description_20': '',
               'Subject_or_Unit_21': '', 'Subject_Objective_21': '', 'Subject_Description_21': '',
               'Subject_or_Unit_22': '', 'Subject_Objective_22': '', 'Subject_Description_22': '',
               'Subject_or_Unit_23': '', 'Subject_Objective_23': '', 'Subject_Description_23': '',
               'Subject_or_Unit_24': '', 'Subject_Objective_24': '', 'Subject_Description_24': '',
               'Subject_or_Unit_25': '', 'Subject_Objective_25': '', 'Subject_Description_25': '',
               'Subject_or_Unit_26': '', 'Subject_Objective_26': '', 'Subject_Description_26': '',
               'Subject_or_Unit_27': '', 'Subject_Objective_27': '', 'Subject_Description_27': '',
               'Subject_or_Unit_28': '', 'Subject_Objective_28': '', 'Subject_Description_28': '',
               'Subject_or_Unit_29': '', 'Subject_Objective_29': '', 'Subject_Description_29': '',
               'Subject_or_Unit_30': '', 'Subject_Objective_30': '', 'Subject_Description_30': '',
               'Subject_or_Unit_31': '', 'Subject_Objective_31': '', 'Subject_Description_31': '',
               'Subject_or_Unit_32': '', 'Subject_Objective_32': '', 'Subject_Description_32': '',
               'Subject_or_Unit_33': '', 'Subject_Objective_33': '', 'Subject_Description_33': '',
               'Subject_or_Unit_34': '', 'Subject_Objective_34': '', 'Subject_Description_34': '',
               'Subject_or_Unit_35': '', 'Subject_Objective_35': '', 'Subject_Description_35': '',
               'Subject_or_Unit_36': '', 'Subject_Objective_36': '', 'Subject_Description_36': '',
               'Subject_or_Unit_37': '', 'Subject_Objective_37': '', 'Subject_Description_37': '',
               'Subject_or_Unit_38': '', 'Subject_Objective_38': '', 'Subject_Description_38': '',
               'Subject_or_Unit_39': '', 'Subject_Objective_39': '', 'Subject_Description_39': '',
               'Subject_or_Unit_40': '', 'Subject_Objective_40': '', 'Subject_Description_40': ''}

possible_cities = {'rockhampton': 'Rockhampton', 'cairns': 'Cairns', 'bundaberg': 'Bundaberg', 'townsville': 'Townsville',
                   'online': 'Online', 'gladstone': 'Gladstone', 'mackay': 'Mackay', 'mixed': 'Online', 'yeppoon': 'Yeppoon',
                   'brisbane': 'Brisbane', 'sydney': 'Sydney', 'queensland': 'Queensland', 'melbourne': 'Melbourne',
                   'albany': 'Albany', 'perth': 'Perth', 'adelaide': 'Adelaide', 'noosa': 'Noosa', 'emerald': 'Emerald',
                   'hawthorn': 'Hawthorn', 'wantirna': 'Wantirna', 'prahran': 'Prahran'}

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
    title_tag = soup.find('div', class_='title-block')
    if title_tag:
        title = title_tag.find('h1')
        delivery_ = title_tag.find('h2')
        if title:
            course_data['Course'] = title.get_text().strip()
            print('COURSE TITLE: ', title.get_text().strip())
        # DELIVERY
        if delivery_:
            delivery_text = delivery_.get_text().lower().strip()
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
            print('DELIVERY: online: ' + course_data['Online'] + ' offline: ' + course_data[
                'Offline'] + ' face to face: ' +
                  course_data['Face_to_Face'] + ' blended: ' + course_data['Blended'] + ' distance: ' +
                  course_data['Distance'])


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

    # AVAILABILITY
    ave_local_tab = soup.find('a', id='tab-local')
    ave_international_tab = soup.find('a', id='tab-international')
    if ave_local_tab:
        course_data['Availability'] = 'D'
    if ave_international_tab:
        course_data['Availability'] = 'I'
    if ave_local_tab and ave_international_tab:
        course_data['Availability'] = 'A'
    print('AVAILABILITY: ' + course_data['Availability'])

    # CAREER OUTCOMES
    career_title = soup.find('h3', text=re.compile('Career opportunities', re.IGNORECASE))
    if career_title:
        career_list = []
        career_div = career_title.find_next('div', id='cs-aims-objectives')
        if career_div:
            career_row = career_div.find('div', class_='row')
            if career_row:
                career_st_column = career_row.find('div', class_='l-two-column')
                career_nd_column = career_row.find('div', class_='l-two-column l-two-column--last')
                if career_st_column:
                    career_ul = career_st_column.find('ul')
                    if career_ul:
                        career_li = career_ul.find_all('li')
                        for li in career_li:
                            career_list.append(li.get_text().strip())
                if career_nd_column:
                    career_ul = career_nd_column.find('ul')
                    if career_ul:
                        career_li = career_ul.find_all('li')
                        for li in career_li:
                            career_list.append(li.get_text().strip())
                career_list = ' '.join(career_list)
                course_data['Career_Outcomes'] = career_list
                print('CAREER OUTCOMES: ', course_data['Career_Outcomes'])

    # CITY
    location = soup.find('span', class_='course-location')
    if location:
        location_text = location.get_text().lower().strip()
        if 'hawthorn' in location_text:
            actual_cities.append('hawthorn')
        if 'wantirna' in location_text:
            actual_cities.append('wantirna')
        if 'prahran' in location_text:
            actual_cities.append('prahran')
        if location_text == '':
            actual_cities.append('hawthorn')
    else:
        actual_cities.append('online')
    print('CITY: ', actual_cities)

    # FEES
    # for local
    fees_div = soup.find('div', id='fees')
    if fees_div:
        fees_table = fees_div.find('table', class_='table table--blocked-th')
        if fees_table:
            t_body = fees_table.find('tbody')
            if t_body:
                tr = t_body.find('tr')
                if tr:
                    elements = tr.find_all('td')
                    if elements:
                        if len(elements) == 4:
                            for index, element in enumerate(elements):
                                if index == 2:
                                    d_fee = element.get_text().strip().replace('$', '')
                                    course_data['Local_Fees'] = d_fee
                                    print('LOCAL FEE: ', course_data['Local_Fees'])
    # for international
    # navigate to international tab
    if soup.find('a', id='tab-international'):
        try:
            browser.execute_script("arguments[0].click();", WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-international"]'))))
        except TimeoutException:
            pass
        time.sleep(2)
        # grab the data
        # fee_title = soup.find_all('div', class_='course-info l-span-4 l-span-last')
        # if fee_title:
        #     for fee_tag in fee_title:
        #         fee = fee_tag.find('h3', text=re.compile('Fees', re.IGNORECASE))
        #         if fee:
        #             fee_p = fee.find_next_sibling('p')
        #             if fee_p:
        #                 print(fee_p.get_text())
        try:
            fee = browser.find_element_by_xpath('//*[@id="main-content-area"]/div[6]/div[2]/p')
        except NoSuchElementException:
            fee = None
            pass
        if fee:
            fee_text = fee.text
            fee_n = re.search(r"\d+(?:,\d+)|\d+", fee_text.__str__())
            if fee_n:
                fee_number = fee_n.group()
                course_data['Int_Fees'] = fee_number
                print('INTERNATIONAL FEE: ', course_data['Int_Fees'])

    course_data['Remarks'] = remarks_list
    del remarks_list

    # UNITES
    subjects_link = []
    try:
        THE_XPATH = '//*[@id="cs-field-units"]/descendant::a'
        units_list = browser.find_elements_by_xpath(f"{THE_XPATH}")
        for i, a in enumerate(units_list):
            if i < 20:
                link = a.get_attribute('href')
                subjects_link.append(link)
            if len(subjects_link) == 20:
                break
        # print('links list: ', subjects_link)
        i = 1
        for s in subjects_link:
            browser.get(s)
            # subject name
            try:
                THE_XPATH = '//*[@id="content"]/main/section[1]/header/div/h1'
                WebDriverWait(browser, 3).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, f'{THE_XPATH}'))
                )
                value = browser.find_element_by_xpath(f'{THE_XPATH}').text
                print('UNIT NAME: ', value)
                course_data[f'Subject_or_Unit_{i}'] = value
            except(AttributeError, TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
                print(f'cant extract subject name {i}')

            # subject objective
            try:
                THE_XPATH = "//h3[contains(text(), 'Aims and objectives')]/following-sibling::div[@class='with-margins general-content']"
                WebDriverWait(browser, 3).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, f'{THE_XPATH}'))
                )
                value = browser.find_element_by_xpath(f'{THE_XPATH}').text
                print('UNIT OBJECTIVES: ', value)
                course_data[f'Subject_Objective_{i}'] = value
            except(AttributeError, TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
                print(f'cant extract subject objective {i}')
            i += 1
    except (AttributeError, TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
        print(f'something went wrong here:  {e}')

    # duplicating entries with multiple cities for each city
    for i in actual_cities:
        course_data['City'] = possible_cities[i]
        course_data_all.append(copy.deepcopy(course_data))
    del actual_cities

    # TABULATE THE DATA
    desired_order_list = ['Level_Code', 'University', 'City', 'Course', 'Faculty', 'Int_Fees', 'Local_Fees',
                          'Currency', 'Currency_Time', 'Duration', 'Duration_Time', 'Full_Time', 'Part_Time',
                          'Prerequisite_1', 'Prerequisite_2', 'Prerequisite_3', 'Prerequisite_1_grade',
                          'Prerequisite_2_grade', 'Prerequisite_3_grade', 'Website', 'Course_Lang', 'Availability',
                          'Description', 'Career_Outcomes', 'Country', 'Online', 'Offline', 'Distance', 'Face_to_Face',
                          'Blended', 'Remarks', 'Subject_or_Unit_1', 'Subject_Objective_1',
                          'Subject_Description_1',
                          'Subject_or_Unit_2', 'Subject_Objective_2', 'Subject_Description_2',
                          'Subject_or_Unit_3', 'Subject_Objective_3', 'Subject_Description_3',
                          'Subject_or_Unit_4', 'Subject_Objective_4', 'Subject_Description_4',
                          'Subject_or_Unit_5', 'Subject_Objective_5', 'Subject_Description_5',
                          'Subject_or_Unit_6', 'Subject_Objective_6', 'Subject_Description_6',
                          'Subject_or_Unit_7', 'Subject_Objective_7', 'Subject_Description_7',
                          'Subject_or_Unit_8', 'Subject_Objective_8', 'Subject_Description_8',
                          'Subject_or_Unit_9', 'Subject_Objective_9', 'Subject_Description_9',
                          'Subject_or_Unit_10', 'Subject_Objective_10', 'Subject_Description_10',
                          'Subject_or_Unit_11', 'Subject_Objective_11', 'Subject_Description_11',
                          'Subject_or_Unit_12', 'Subject_Objective_12', 'Subject_Description_12',
                          'Subject_or_Unit_13', 'Subject_Objective_13', 'Subject_Description_13',
                          'Subject_or_Unit_14', 'Subject_Objective_14', 'Subject_Description_14',
                          'Subject_or_Unit_15', 'Subject_Objective_15', 'Subject_Description_15',
                          'Subject_or_Unit_16', 'Subject_Objective_16', 'Subject_Description_16',
                          'Subject_or_Unit_17', 'Subject_Objective_17', 'Subject_Description_17',
                          'Subject_or_Unit_18', 'Subject_Objective_18', 'Subject_Description_18',
                          'Subject_or_Unit_19', 'Subject_Objective_19', 'Subject_Description_19',
                          'Subject_or_Unit_20', 'Subject_Objective_20', 'Subject_Description_20',
                          'Subject_or_Unit_21', 'Subject_Objective_21', 'Subject_Description_21',
                          'Subject_or_Unit_22', 'Subject_Objective_22', 'Subject_Description_22',
                          'Subject_or_Unit_23', 'Subject_Objective_23', 'Subject_Description_23',
                          'Subject_or_Unit_24', 'Subject_Objective_24', 'Subject_Description_24',
                          'Subject_or_Unit_25', 'Subject_Objective_25', 'Subject_Description_25',
                          'Subject_or_Unit_26', 'Subject_Objective_26', 'Subject_Description_26',
                          'Subject_or_Unit_27', 'Subject_Objective_27', 'Subject_Description_27',
                          'Subject_or_Unit_28', 'Subject_Objective_28', 'Subject_Description_28',
                          'Subject_or_Unit_29', 'Subject_Objective_29', 'Subject_Description_29',
                          'Subject_or_Unit_30', 'Subject_Objective_30', 'Subject_Description_30',
                          'Subject_or_Unit_31', 'Subject_Objective_31', 'Subject_Description_31',
                          'Subject_or_Unit_32', 'Subject_Objective_32', 'Subject_Description_32',
                          'Subject_or_Unit_33', 'Subject_Objective_33', 'Subject_Description_33',
                          'Subject_or_Unit_34', 'Subject_Objective_34', 'Subject_Description_34',
                          'Subject_or_Unit_35', 'Subject_Objective_35', 'Subject_Description_35',
                          'Subject_or_Unit_36', 'Subject_Objective_36', 'Subject_Description_36',
                          'Subject_or_Unit_37', 'Subject_Objective_37', 'Subject_Description_37',
                          'Subject_or_Unit_38', 'Subject_Objective_38', 'Subject_Description_38',
                          'Subject_or_Unit_39', 'Subject_Objective_39', 'Subject_Description_39',
                          'Subject_or_Unit_40', 'Subject_Objective_40', 'Subject_Description_40']

    course_dict_keys = set().union(*(d.keys() for d in course_data_all))

    with open(csv_file, 'w', encoding='utf-8', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, course_dict_keys)
        dict_writer.writeheader()
        dict_writer.writerows(course_data_all)

    with open(csv_file, 'r', encoding='utf-8') as infile, open('SUT_master_ordered.csv', 'w', encoding='utf-8',
                                                               newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
        # reorder the header first
        writer.writeheader()
        for row in csv.DictReader(infile):
            # writes the reordered rows to the new file
            writer.writerow(row)


