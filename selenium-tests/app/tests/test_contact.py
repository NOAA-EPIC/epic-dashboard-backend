import json
import app.util.utility as ut
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


CONTACT_PAGE = '/html/body/div/section[4]/div/div/div/section/div/div[2]/div/div[2]/div/p[1]/a'
PAGE_TITLE = 'Contact Epic - Earth Prediction Innovation Center'


def test_contact(driver):
    status_code = 200
    result_list = []
    body = ''

    if ut.click_hidden_link(driver, CONTACT_PAGE):
        if str(driver.title) == PAGE_TITLE:
            result_list.append(f"Found {PAGE_TITLE}")
            
            submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
             
            error_elements = driver.find_elements(By.XPATH, "//div[@class='error-message']")
            if error_elements:
                error_messages = [error.text for error in error_elements]
                result_list.append(f"Errors occurred after clicking the contact button: {', '.join(error_messages)}")
                status_code = 404
                body = 'Errors with Contact Page occurred'

            else:
                result_list.append("Submit button clicked successfully")
        else:
            result_list.append(f'{PAGE_TITLE} did not match the expected title.')
            status_code = 404
            body = 'Errors with Contact Page occurred'

    else:
        result_list.append(list_entry = f'Selenium failed to find the page for {PAGE_TITLE}.')
        status_code = 404
        body = 'Errors with Contact Page occurred'

    return {
        "status_code": status_code,
        "body": json.dumps(body),
        "contact_results": result_list,
    }
