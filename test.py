import requests
import hashlib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Api
api = 'xxx'
secret = 'xxx'

#Fetch session
session = requests.post("https://api.etilbudsavis.dk/v2/sessions", data={'api_key': api}).json()

#Set token + signature
token = session['token']
signature = hashlib.sha256((secret+token).encode('utf-8')).hexdigest()

#Setup email
def sendMail(content):
    #Build mail content
    sent_from = 'dennis@dandersen.dk'
    send_to = 'dennisa@hotmail.dk'

    msg = MIMEText("Godmorgen!\n\nHer er en liste over dagens energidrikke, som er på tilbud:\n\n" + content)
    msg['From'] = 'rootsiedan@gmail.com'
    msg['To'] = 'dennisa@hotmail.dk'
    msg['Subject'] = 'Automatisk daglig energidrikke'

    #Init server and send
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login("rootsiedan@gmail.com", "xxx")
        server.sendmail(sent_from, send_to, msg.as_string())
        server.close()
    except:
        print("Something went wrong..")


#Find energydrinks json
def searchEnergyDrinks(token, signature):
    #Init output
    output = ""

    #Set lat, lng and radius
    lat = "55.944128"
    lng = "8.500266"
    radius = "6000"

    #Do search for energy drinks
    search = requests.get("https://api.etilbudsavis.dk/v2/offers/search?_token=" + token + "&_signature=" + signature + "&query=Energidrik&r_lat=" + lat + "&r_lng=" + lng + "&r_radius=" + radius).json()

    #Build list
    for offer in search:
        output += offer['branding']['name'] + " - " + offer['heading'] + " - [" + str(offer['pricing']['price']) + " " + offer['pricing']['currency'] + "]\n"
        output += offer['description'] + "\n\n"

    return output


#Run app
sendMail(searchEnergyDrinks(token, signature))
