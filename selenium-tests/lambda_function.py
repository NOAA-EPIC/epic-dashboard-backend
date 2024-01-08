import os
from app.tests.test_main import test_main
import json
import app.util.utility as ut
# from app.tests.test_contact import test_contact
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import boto3
import datetime
import requests

def lambda_handler(event, context):
    status_code = 200
    url = os.getenv('URL')
    
    # Options
    options = Options()
    options.binary_location = '/opt/chromedriver/headless-chromium'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')

    # Capabilities
    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    capabilities['acceptInsecureCerts'] = True
    
    # webdriver 
    driver =\
        webdriver.Chrome('/opt/chromedriver/chromedriver',chrome_options=options,desired_capabilities=capabilities)

    driver.get(url)
    print("Main title: ", driver.title)
    
    result_dict = test_main(driver)
    status_code = ut.check_status_code(result_dict['status_code'], status_code)
    title_result = result_dict['title_result']

    # contact_results = test_contact(driver)
    # status_code = ut.check_status_code(contact_results['status_code'], status_code)
    
    driver.close()
    driver.quit()
        
    iso_date_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    
    response_data = {
        "title_response": title_result,
        # "table_response" : result_dict['table_list'],
        # "contact_response" : contact_results['contact_results'],
        # "video_response" : result_dict['video_results']
    }
    
    full_response = {
        'status_code': status_code,
        'body' : response_data,
        'time_ran': str(iso_date_time)
    }
    
    s3 = boto3.client('s3')
    
    # Write the JSON string to S3
    response = s3.put_object(
        Bucket='epic-health-dashboard-artifacts',
        Key='selenium-data.json',
        Body=json.dumps(full_response).encode('utf-8'),
        ACL='public-read'
    )

    return {
        "status_code": status_code,
        "response": response
    }
