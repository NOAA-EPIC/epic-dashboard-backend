def click_hidden_link(driver, xpath):
    try:
        element =  driver.find_element_by_xpath(xpath)
        driver.execute_script("arguments[0].click();", element)
        return True
    except Exception as e:
        print("Exception in element click:", e)
        return False
        

def check_status_code(new, current):
    if new != current and current == 200:
        return new
    return current
