import app.util.utility as ut
from selenium.webdriver.common.by import By


BASE_PATH = "/html/body/main/div/div[1]/section[2]/div/div/div/div/div/div/div[1]/div[1]/div[2]/div[1]/div"

VIDEO_NAMES = [
    "HPC-Stack Setup on a Mac",
    "Creating a Base Image on Amazon Web Services (AWS)"
    ]

    # "Copying Amazon Machine Image (AMI) onto an EC2 instance",
    # "Creating a HeadNode on Amazon Web Services (AWS)",
    
def test_videos(driver):
    status_code = 200
    result_list = []
    for i in range(1, len(VIDEO_NAMES)+1):
        xpath = f"{BASE_PATH}[{i}]/h4/a"
        elements = driver.find_elements(By.XPATH, xpath)
        
        if elements:
            element = elements[0]
            title = element.get_attribute("text").strip()
            expected_value = VIDEO_NAMES[i - 1] if i <= len(VIDEO_NAMES) else None
            
            if expected_value and title == expected_value:
                result = f'Found video {title}'
            elif expected_value:
                result = f'There was an error with the video {title}'
                status_code = 404

            result_list.append(result)

    return status_code, result_list
