# imports:
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


#driver function:
def get_driver():
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument("--no-sandbox")  
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Step 2: Get a driver
    #driver = webdriver.Chrome(executable_path= 'C:/Users/Owner/Downloads/chrome-win64/chrome-win64/chromedriver.exe', options=chrome_options)

    return driver

# create empty dataframe
def create_dataframe():
    lincenses_df = pd.DataFrame(columns=['Name', 'Board', 'License/Endorsement #', 'Type', 'Status',
       'Sub Status', 'Sub Category', 'Board Action?', 'City', 'State',
       'County', 'Zip Code', 'Compact/Multi-State Eligible', 'Unnamed: 13', 'issue_date', 'expiration_date'])
    return lincenses_df

# # read in list of licenses
# licenses = pd.read_csv('Licenses.csv')

# # start driver, find search key
# driver = get_driver()
# driver.get('https://elicense.ohio.gov/oh_verifylicense')
# input = driver.find_element(By.ID, 'j_id0:j_id110:licenseNumber')

# for each license, search details(including extra info), and add to the license dataframe
def get_license_info(license_list):
    for license in license_list['License #']:
        
        waiter = WebDriverWait(driver, 10)
        waiter.until(EC.element_to_be_clickable((By.CLASS_NAME, 'searchButton')))
        input.send_keys(license)
        search_btn = driver.find_element(By.CLASS_NAME, 'searchButton').click()
        #get basic info from table, save as dataframe
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table', {'id' : 'results'})
        result = pd.read_html(str(table))[0]
        try:
            #get extra info from the expanded view, and add to dataframe 
            waiter.until(EC.element_to_be_clickable((By.XPATH, '//td//div[@class="expand"]')))
            expand_btn = driver.find_element(By.XPATH, '//td//div[@class="expand"]').click()
            additional_info = driver.find_elements(By.XPATH , "//tr[@class ='expanded-detail']//div")
            result['Issue_date'] =additional_info[0].text.split(':')[1]
            result['exp_date'] =additional_info[2].text.split(':')[1]
            # save screenshot of info
            driver.save_screenshot(f'screenshots/{license}.png')
            # add all info to license dataframe
            input.clear()
        except:
            #license not found
            input.clear()
            #lincenses_df['License/Endorsement #'] = license
            #incenses_df['Name'] = lincenses_df['Name'].str.replace('Your search return 0 records', np.nan)

        lincenses_df = pd.concat([result, pd.DataFrame(lincenses_df)])

        return lincenses_df


def drop_reanme_df(lincenses_df):
    # drop unnecessary columns
    lincenses_df = lincenses_df.drop(columns = ['Board', 'Sub Category', 'Zip Code', 'Compact/Multi-State Eligible', 'Unnamed: 13', 'Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16'])

    # rename columns
    lincenses_df = lincenses_df.rename(columns={"Name": "name", "License/Endorsement #": "License number", 'Type':'type', 'Status':'status',
        'Sub Status':'sub status', 'Board Action?':'board action','City':'city', 'State':'state',
        'County':'county'})
    return lincenses_df

# save license dataframe to a csv
def save_to_csv(lincenses_df):
    lincenses_df.to_csv(f'lincences_info.csv', index=False)

create_dataframe()