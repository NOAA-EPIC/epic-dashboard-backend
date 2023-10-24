from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


UPP = "Unified Post Processor - Earth Prediction Innovation Center"
GETTING_STARTED = "Getting Started - Earth Prediction Innovation Center"
TECHNICAL_FAQ = "Technical FAQs - Earth Prediction Innovation Center"

TABLES = {
    UPP : ['11.0.0', '10.1.0'],
    GETTING_STARTED : ['Continuing Monthly Costs', 'Image builder', 'SRW Run', 'Total Monthly Single Run'],
    TECHNICAL_FAQ : ['Short-Range Weather Application', 'UFS Weather Model', 'UFS_UTILS', 'CCPP-physics']
}


def test_tables(driver, element):
    status_code = 200
    table_elements = driver.find_elements(By.XPATH, "//table")
    table_titles = []

    for table in table_elements:
        table_rows = table.find_elements(By.XPATH, ".//tr")
        for row in table_rows:
            try:
                first_column = row.find_element(By.XPATH, "./td[1]")
                title = first_column.text.strip()
                
                if not title:
                    title_element = first_column.find_element(By.XPATH, "./p/a/span")
                    title = title_element.get_attribute("textContent").strip()
                
                if title:
                    table_titles.append(title)
                    
            except NoSuchElementException:
                continue
            except Exception as e:
                return 404, f'There was an error {e}',

    if element in TABLES.keys() and table_titles == TABLES[element]:
        message = f'Found all elements of the table for {element}'
    else: 
        message = f'There was an error with the table for {element}'
        status_code = 404
    
    return status_code, message
