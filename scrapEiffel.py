from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import smtplib #lib pour la partie email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER =  "smtp.gmail.com" #Serveur email
SMTP_PORT = 587 #Port du serveur
GMAIL_USERNAME  = "BotHdws@gmail.com" #Votre adresse  email
GMAIL_PASSWORD = "zakfmsrmlyzokdaf" #Votre  mot de passe
receiverAddress = "hidaouse.hedws@gmail.com" #Adresse mail destinataire

emailSubject = "Rapport du bot tour Eiffel" #Objet du email 
emailBase = "C'est le moment d'acheter :\n\n" #Début du corps du email
emailContent = "" #Contenu du mail
emailSignature = "\n Cordialement,\n Le bot" #Signature du mail
sendEmail = False #Variable de contrôle permettant de savoir s'il faut envoyer l'email


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

    if "disabled" in li_schedule[26].get_attribute("class"):
        print("Oui disabled")
        sendEmail = True
    else:
        print("Non pas disabled")

# Attendez 5 secondes
time.sleep(3)
# Fermez le navigateur
driver.quit()


#Envoi de l'email
if(sendEmail == True):
    #Le corps du mail est composé de la phrase de base, des noms des jeux à acheter et de la signature
    emailBody = emailBase + emailContent + emailSignature

    #Creation de  l'email
    message = MIMEMultipart()
    message['From'] = GMAIL_USERNAME
    message['To'] = receiverAddress
    message['Subject'] = emailSubject
    message.attach(MIMEText(emailBody, 'plain'))

    #Connexion  au serveur Gmail
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()
 
    #Authentification
    session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

    #Envoi de l'email
    session.sendmail(GMAIL_USERNAME, receiverAddress, message.as_string())
    session.quit
    
    #Le mail vient d'être envoyé, on remet la variable de controle à False
    sendEmail = False

else:
    print("rien de nouveau")

