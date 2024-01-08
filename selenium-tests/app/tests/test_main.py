import json
import app.util.utility as ut
from app.tests.test_tables import test_tables
from app.tests.test_videos import test_videos
from selenium import webdriver
from selenium.webdriver.common.by import By


HOME = "Earth Prediction Innovation Center - Site for EPIC, the Earth Prediction Innovation Center Earth Prediction Innovation Center"
SRWA = "Short Range Weather Application - Earth Prediction Innovation Center"
MRWA = "Medium Range Weather Application - Earth Prediction Innovation Center"
UFS = "UFS Weather Model - Earth Prediction Innovation Center"
LDAS = "Land Data Assimilation (DA) System - Earth Prediction Innovation Center"
UPP = "Unified Post Processor - Earth Prediction Innovation Center"
GET_SUPPORT = "Get Support - Earth Prediction Innovation Center"
GETTING_STARTED = "Getting Started - Earth Prediction Innovation Center"
TUTORIALS = "Tutorials - Earth Prediction Innovation Center"
TECHNICAL_FAQ = "Technical FAQs - Earth Prediction Innovation Center"
NEWS = "News - Earth Prediction Innovation Center"
APP_TRAINING = "Application Training - Earth Prediction Innovation Center"
CODEFESTS = "CodeFests - Earth Prediction Innovation Center"
UPCOMING_EVENTS = "Upcoming Events - Earth Prediction Innovation Center"
PAST_EVENTS = "Past Events - Earth Prediction Innovation Center"
ABOUT = "About EPIC - Earth Prediction Innovation Center"
WHO_WE_ARE = "Who We Are - Earth Prediction Innovation Center"
PROGRAM_TEAM = "EPIC Program Team - Earth Prediction Innovation Center"
CONTRACT_TEAM = "EPIC Contract Team - Earth Prediction Innovation Center"
PROGRAM_DETAILS = "EPIC Program Details - Earth Prediction Innovation Center"
INVESTMENT_AREAS = "EPIC’s 7 Investment Areas - Earth Prediction Innovation Center"
GOVERNANCE = "EPIC Governance - Earth Prediction Innovation Center"
COMMUNITY_MODELING = "Community Modeling - Earth Prediction Innovation Center"
GOVERNANCE_DOCS = "Key Governance Documents - Earth Prediction Innovation Center"
PROJECTS = "EPIC Projects - Earth Prediction Innovation Center"
FAQ = "Frequently Asked Questions (FAQ) - Earth Prediction Innovation Center"


PAGES = {
    HOME : '/html/body/header/section[1]/div/div[2]/div/div/div/h5/a',
    }

# PAGES = {
#     HOME : '/html/body/header/section[1]/div/div[2]/div/div/div/h5/a',
#     SRWA : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[1]/ul/li[2]/a',
#     MRWA: '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[1]/ul/li[3]/a',
#     UFS : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[1]/ul/li[4]/a',
#     LDAS : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[1]/ul/li[5]/a',
#     UPP : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[1]/ul/li[6]/a',
#     GET_SUPPORT : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[2]/a',
#     GETTING_STARTED : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[2]/ul/li[1]/a',
#     TUTORIALS : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[2]/ul/li[3]/a',
#     TECHNICAL_FAQ : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[2]/ul/li[5]/a',
#     NEWS : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[3]/ul/li[1]/a',
#     APP_TRAINING : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[3]/ul/li[2]/ul/li[1]/a',
#     CODEFESTS : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[3]/ul/li[2]/ul/li[2]/a',
#     UPCOMING_EVENTS : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[3]/ul/li[2]/ul/li[3]/a',
#     PAST_EVENTS : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[3]/ul/li[2]/ul/li[4]/a',
#     ABOUT : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[4]/a',
#     WHO_WE_ARE: '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[4]/ul/li[1]/a',
#     PROGRAM_TEAM : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[4]/ul/li[1]/ul/li[1]/a',
#     CONTRACT_TEAM : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[4]/ul/li[1]/ul/li[2]/a',
#     PROGRAM_DETAILS : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[4]/ul/li[2]/a',
#     INVESTMENT_AREAS : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[4]/ul/li[3]/a',
#     GOVERNANCE : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[4]/ul/li[4]/a',
#     COMMUNITY_MODELING : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[4]/ul/li[4]/ul/li[1]/a',
#     GOVERNANCE_DOCS: '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[4]/ul/li[4]/ul/li[2]/a',
#     PROJECTS : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[4]/ul/li[4]/ul/li[3]/a',
#     FAQ : '/html/body/header/section[1]/div/div[3]/div/div/div/nav[1]/ul/li[4]/ul/li[4]/ul/li[4]/a',
# }



def test_main(driver):
    status_code = 200
    result_list = []
    body  = ''
    
    # Lists for the results from sub tests of pages
    table_results = []
    video_results = []
    # Click on each page and check the title
    for element in PAGES:
        if ut.click_hidden_link(driver, PAGES[element]):
            if str(driver.title) == element: 
                list_entry = f'Found {element}.'
                
                # if len(driver.find_elements(By.TAG_NAME, "table")) > 0:
                #     new_status_code, results = test_tables(driver, element)
                #     table_results.append(results)
                #     status_code = ut.check_status_code(new_status_code, status_code)
                # if element == TUTORIALS:
                #     new_status_code, results = test_videos(driver)
                #     video_results.extend(results)
                #     status_code = ut.check_status_code(new_status_code, status_code)
            else:
                list_entry = f'{element} did not match the expected title.'
                body = 'Some element(s) failed. See result_list.'
                status_code = ut.check_status_code(404, status_code)
                
        else:
            list_entry = f'Selenium failed to find the page for {element}.'
            body = 'Some element(s) failed. See result_list.'
            status_code = ut.check_status_code(404, status_code)

        print(list_entry)
        result_list.append(list_entry)
    
    return {
        "status_code": status_code,
        "body": json.dumps(body),
        "title_result": result_list,
        "table_list" : table_results,
        "video_results" : video_results
    }
