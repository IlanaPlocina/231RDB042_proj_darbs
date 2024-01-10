import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import re
from selenium.webdriver.support import expected_conditions as EC

# Darbs ar tīmekli

service = Service()
option = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=option)

driver.maximize_window()

url = "https://www.cvmarket.lv/"
driver.get(url)
time.sleep(1)

atr_vieta=driver.find_element(By.ID, "search[locations][]_Button")
atr_vieta.click()
time.sleep(1)

vieta=driver.find_element(By.ID, "search[locations][]_1")
vieta.click()
time.sleep(1)

meklesana=driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
meklesana.click()
time.sleep(1)

publicesana=driver.find_element(By.CSS_SELECTOR, '[data-sort="activation_date"]')
publicesana.click()
time.sleep(1)

# Darba nosaukuma meklēšana
darba_nosaukumi=[]
info_par_darbu=[]
teksta_sakums_alga="Bruto alga"
teksta_beigums_alga="Darba laiks"
h2_nosaukumi=driver.find_elements(By.TAG_NAME,'h2')
for h2 in h2_nosaukumi:
    darba_nosaukumi.append(h2.text)
for i in darba_nosaukumi:
    try:
        konkrets_d_v = driver.find_element(By.XPATH, f'//h2[text()="{i}"]')
        current_window = driver.current_window_handle 

        konkrets_d_v.click()

        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

        new_window = [window for window in driver.window_handles if window != current_window][0]
        driver.switch_to.window(new_window)

        salary_elements = driver.find_elements(By.XPATH, '//div[@class="bg-white shadow lg:rounded-xl px-6 py-7.5"]//div[@class="font-semibold"]')
        salary_texts = [element.text for element in salary_elements]
        info_par_darbu.extend(salary_texts)

        driver.close()

        driver.switch_to.window(current_window)
        
        time.sleep(1)
    except Exception:
        pass
# print(darba_nosaukumi)
# print(info_par_darbu)
    
lap_skaitlis=30
univer_lap='?op=search&search%5Bjob_salary%5D=3&search%5Blocations%5D%5B0%5D=129&search%5Bkeyword%5D=&ga_track=homepage&dir=1&sort=activation_date&start='
while True:
    page = f"{univer_lap}{lap_skaitlis}"
    print(page)

    try:
        nak_lapa = driver.find_element(By.CSS_SELECTOR, f'a[href="{page}"]')
        nak_lapa.click()

        h2_nosaukumi = driver.find_elements(By.TAG_NAME, 'h2')
        for h2 in h2_nosaukumi:
            darba_nosaukumi.append(h2.text)

            try:
                konkrets_d_v = driver.find_element(By.XPATH, f'//h2[text()="{h2.text}"]')
                current_window = driver.current_window_handle 

                konkrets_d_v.click()

                WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

                new_window = [window for window in driver.window_handles if window != current_window][0]
                driver.switch_to.window(new_window)

                salary_elements = driver.find_elements(By.XPATH, '//div[@class="bg-white shadow lg:rounded-xl px-6 py-7.5"]//div[@class="font-semibold"]')
                salary_texts = [element.text for element in salary_elements]
                info_par_darbu.extend(salary_texts)

                driver.close()

                driver.switch_to.window(current_window)

                time.sleep(1)
            except Exception as e:
                print(f"Ошибка во внутреннем цикле: {e}")
    except Exception as e:
        print(f"Ошибка во внешнем цикле: {e}")
        break

    lap_skaitlis += 30
    time.sleep(1)

# print(darba_nosaukumi)
# print(info_par_darbu)








