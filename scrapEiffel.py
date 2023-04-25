from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Configurez votre navigateur web pour le contrôle à distance avec Selenium
driver = webdriver.Chrome(options=options)


# Accédez à la page de réservation de la tour Eiffel
driver.get("https://ticket.toureiffel.paris/fr")

wait = WebDriverWait(driver, 10)
button_denied = wait.until(EC.visibility_of_element_located((By.ID, "tarteaucitronAllDenied2")))
button_denied.click()

# Attendez 2 secondes
time.sleep(1)

# Attendez que le bouton i avec l'id d-next soit visible, puis cliquez dessus
next_button = wait.until(EC.visibility_of_element_located((By.ID, "d-next")))
next_button.click()

# Attendez 2 secondes
time.sleep(1)

input_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[@for='1-0-d-day-1']"))) #changer ici la date du jour par rapport au mois au niveau du for
input_element.click()

# Attendez 2 secondes
time.sleep(1)

button_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//li[@class='jeune_item']//button[@class='minus_more more']")))
button_element.click()
button_element.click()
# Attendez 2 secondes
time.sleep(1)

# Attendez que le bouton i avec l'id d-next soit visible, puis cliquez dessus
next_button = wait.until(EC.visibility_of_element_located((By.ID, "edit-submit")))
next_button.click()

# Attendez 5 secondes
time.sleep(6)

ul_element = driver.find_element(By.CSS_SELECTOR, "ul.destination_list")
li_elements = ul_element.find_elements(By.TAG_NAME, "li")
if "not-available" in li_elements[0].get_attribute("class"):
    # ne rien faire, pas de place au troisieme etage
    print("oui")
else:
    print("non")
    li_elements[0].click() 
    time.sleep(1)
    div_ascenseur = driver.find_element(By.CSS_SELECTOR, ".item.billet_sommet_par_ascenseur")
    div_ascenseur.click()

    time.sleep(1)

    ul_schedule = driver.find_element(By.CSS_SELECTOR, "ul.schedule_list")
    li_schedule = ul_schedule.find_elements(By.TAG_NAME, "li")

    if "disabled" in li_schedule[22].get_attribute("class"):
        print("Oui disabled")
    else:
        print("Non pas disabled")


# Attendez 5 secondes
time.sleep(3)

# Fermez le navigateur
driver.quit()
