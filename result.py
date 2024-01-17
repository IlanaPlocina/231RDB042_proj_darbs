import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import pandas
from selenium.webdriver.support import expected_conditions as EC
import openpyxl
from tabulate import tabulate

# Lietotāja prasījumi
liet_pilseta = input("Uzrakstiet pilsētu/novadu/vietu, kur plānojat meklēt darbu: ")
while True:
    liet_students = input("Vai Jūs esat students? (nav iespējas strādāt pilno slodzi): ")
    if liet_students == 'Jā':
        break 
    elif liet_students == 'Nē':
        liet_darba_laiks = input("Kāds darba laiks Jūs interesē? (Pilna / Nepilna slodze): ")
        if liet_darba_laiks in ['Pilna', 'Nepilna']:
            break
        else:
            print("Lūdzu, ievadiet pareizu atbildi ('Pilna' vai 'Nepilna').")
    else:
        print("Lūdzu, ievadiet pareizu atbildi ('Jā' vai 'Nē').")

# Darbs ar tīmekli
service = Service()
option = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=option)

driver.maximize_window()
    
# Darbs ar vietas_exel.xlsx failu
pilsetas_id=""
fails = pandas.read_excel("vietas_exel.xlsx")
info_list = fails.values.tolist()
lines=0
for line in info_list:
    lines+=1
for i in range (lines):
    vieta=info_list[i][0]
    # print(vieta)
    if vieta==liet_pilseta:
        pilsetas_id=info_list[i][1]
# print(pilsetas_id)


url = "https://www.cvmarket.lv/"
driver.get(url)
time.sleep(1)

atr_vieta=driver.find_element(By.ID, "search[locations][]_Button")
atr_vieta.click()
time.sleep(1)

vieta=driver.find_element(By.ID, f"{pilsetas_id}")
vieta.click()
time.sleep(1)

meklesana=driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
meklesana.click()
time.sleep(1)

publicesana=driver.find_element(By.CSS_SELECTOR, '[data-sort="activation_date"]')
publicesana.click()
time.sleep(1)

# Darba nosaukuma meklēšana
# Informarcijas par darbu meklēšana
darba_nosaukumi=[]
info_par_darbu=[]
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
        
        time.sleep(1)

        salary_elements = driver.find_elements(By.XPATH, '//div[@class="bg-white shadow lg:rounded-xl px-6 py-7.5"]//div[@class="font-semibold"]')
        salary_texts = [element.text for element in salary_elements]
        selected_salary_texts = salary_texts[:6]
        info_par_darbu.extend(selected_salary_texts)


        driver.close()

        driver.switch_to.window(current_window)
        
        time.sleep(1)
    except Exception:
        selected_salary_texts = ['-','-','-','-','-','-']
        info_par_darbu.extend(selected_salary_texts)
# print(darba_nosaukumi)
# print(info_par_darbu)
    
lap_skaitlis=30
univer_lap='?op=search&search%5Bjob_salary%5D=3&search%5Blocations%5D%5B0%5D=129&search%5Bkeyword%5D=&ga_track=homepage&dir=1&sort=activation_date&start='
while True:
    page = f"{univer_lap}{lap_skaitlis}"
    # print(page)

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

                time.sleep(1)

                salary_elements = driver.find_elements(By.XPATH, '//div[@class="bg-white shadow lg:rounded-xl px-6 py-7.5"]//div[@class="font-semibold"]')
                salary_texts = [element.text for element in salary_elements]
                selected_salary_texts = salary_texts[:6]
                info_par_darbu.extend(selected_salary_texts)

                driver.close()

                driver.switch_to.window(current_window)

                time.sleep(1)
            except Exception:
                selected_salary_texts = ['-','-','-','-','-','-']
                info_par_darbu.extend(selected_salary_texts)
                
        lap_skaitlis += 30
        time.sleep(1)

    except Exception:
        break



# info par darbu (sadalīšana)
i_p_d = [info_par_darbu[i:i+6] for i in range(0, len(info_par_darbu), 6)]

# ieraksts Exel tabulā
df_vakances_nosaukums = pandas.DataFrame({'Vakances nosaukums': darba_nosaukumi})
df_i_p_d = pandas.DataFrame(i_p_d, columns=['Ievadīts', 'Publicēts līdz', 'Atrašanas vieta', 'Bruto alga', 'Darba laiks', 'Papildus informācija'])
tab = pandas.concat([df_vakances_nosaukums, df_i_p_d.iloc[:, 0:]], axis=1)
tab.to_excel('dati_pd.xlsx', index=False)

# Exel tabulas rediģēšana
fails=openpyxl.load_workbook('dati_pd.xlsx')
lapa=fails.active
col = ['B', 'C', 'D', 'E', 'F']
for c in col:
    lapa.column_dimensions[c].width = 20
lapa.column_dimensions['A'].width = 60
lapa.column_dimensions['G'].width = 50
fails.save('dati_pd.xlsx')

# Nepieciešamas informācijas meklēšana
darbs = []
x=0
visa_info_fails = pandas.read_excel("dati_pd.xlsx")
info_list_viss = visa_info_fails.values.tolist()
k = visa_info_fails.iloc[:, :]

lines_viss = len(info_list_viss)
# Studensts = Jā
if liet_students == 'Jā':
    for i in range(lines_viss):
        sesta_kol = info_list_viss[i][6]
        if isinstance(sesta_kol, str) and "studenti" in sesta_kol:
            darbs.append(info_list_viss[i])
    else:
        if not darbs:
            x = 1
            print("Diemžēl, tādas vakances nav!")

# Students = Nē
if liet_students == 'Nē':
    for i in range(lines_viss):
        piekta_kol = info_list_viss[i][5]
        if liet_darba_laiks == "Pilna" and isinstance(piekta_kol, str) and "pilna" in piekta_kol:
            darbs.append(info_list_viss[i])
        elif liet_darba_laiks == "Nepilna" and isinstance(piekta_kol, str) and "nepilna" in piekta_kol:
            darbs.append(info_list_viss[i])
    else:
        if not darbs:
            x = 1
            print("Diemžēl, tādas vakances nav!")

# informācijas izvadīšana uz ekranu
if (x==0):
    virsraksti=['Vakances nosaukums','Ievadīts', 'Publicēts līdz', 'Atrašanas vieta', 'Bruto alga', 'Darba laiks', 'Papildus informācija']
    tabula=pandas.DataFrame(darbs, columns=virsraksti)
    print(tabula)
        