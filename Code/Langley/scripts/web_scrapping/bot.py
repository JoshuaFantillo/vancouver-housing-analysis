from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
from selenium import webdriver


class Bot(webdriver.Chrome):

    def __init__(self, driver_path=r"/Users/jarvis/Desktop/Selenium/Drivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Bot, self).__init__()
        self.implicitly_wait(2)
        self.maximize_window()
        self.wait = WebDriverWait(self, 10)


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()
        else:
            while True:
                pass

    def land_first_page(self):
        self.get("https://services.langleycity.ca/TempestApps/PIP/Pages/Search.aspx")
        element_present = EC.presence_of_element_located((By.XPATH, "//input[@class='form-control']"))
        WebDriverWait(self, 5).until(element_present)
        element_present = EC.presence_of_element_located((By.XPATH, "//select[@class='form-control search-type-control']"))
        WebDriverWait(self, 5).until(element_present)



    def input_folio(self, folio):
        select_element = self.find_element(By.XPATH, "//select[@class='form-control search-type-control']")
        for option in select_element.find_elements(By.TAG_NAME, 'option'):
            if option.text == 'Folio':
                option.click()
                break
        folio_el = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[contains(@placeholder, '12345')]")))
        folio_el.clear()
        folio_el.send_keys(folio)

    def search(self):
        search = self.find_element(By.XPATH, "//span[@class='input-group-addon input-search']")
        search.click()

    def go_to_result(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='list-group-item result-list-item']")))
            res = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='list-group-item result-list-item']")))
            res.click()
            return 0
        except:
            print("not found")
            return 1
    def get_table(self):
        land_values = ['0'] * 5
        improvement_values = ['0'] * 5
        gross_assesment = ['0'] * 5
        try:
            table = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='ctl00_BodyContent_pnl_taxAssessmentBC']")))
        except:
            return land_values,improvement_values, gross_assesment, 1

        content = table.text.split(' ')[14:]
        for i in range(5):
            try:
                land = content[i*10+4].replace(',','')
                improvement = content[i*10+5].replace(',','')
                assessment = content[i*10+6].replace(',','')
                land_values[i] = land
                improvement_values[i] = improvement
                gross_assesment[i] = assessment
            except:
                break


        return land_values,improvement_values, gross_assesment, 0




