from email.mime.text import MIMEText
import smtplib
from email.mime.multipart import MIMEMultipart
from os import environ
from dotenv import load_dotenv
load_dotenv()

mensaje=MIMEMultipart()
password=environ.get("EMAIL_PASSWORD")
mensaje['From']=environ.get("EMAIL")
mensaje['subject']="Solicitu de olvido de contraseña"

def enviarCorreo(destinatario, nombre, link):
    mensaje['To']=destinatario
    texto=""" Hola {} !, Has solicitado recuperar tu contraseña.
    Para tal efecto te enviaremos el siguiente link 
    al que deberás ingresar para completar el cambio: 
    {} , sino fuiste tu, ignora este mensaje.
    """.format(nombre, link)
    mensaje.attach(MIMEText(texto,'plain'))
    try:
        servidorSMTP=smtplib.SMTP('smtp.gmal.com',587)
        servidorSMTP.starttls()
        servidorSMTP.login(mensaje['From'],
            to_addrs=mensaje['To'],
            msg=mensaje.as_string())
        servidorSMTP.quit()
        return True
    except Exception as e:
        print(e)
        return False
