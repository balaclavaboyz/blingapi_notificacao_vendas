import requests
from dotenv import load_dotenv
from pathlib import Path
import os
import json
import smtplib
from email.message import EmailMessage

STATUS='Pendentes'

def update_current_nfs():
    load_dotenv()
    env_path = Path('.')/'.env'
    load_dotenv(dotenv_path=env_path)

    key=os.getenv("APIKEY")

    url=("https://bling.com.br/Api/v2/notasfiscais/json/&apikey="+key)

    res=requests.get(url)
    with open('nfs.json','w') as f:
        json.dump(res.json(),f)

    return res.json()

def filter_nfs_list(updated_nfs):
    list_checked=[]
    if updated_nfs==True:
        input_dict=json.loads(updated_nfs)
        input_dict=input_dict['retorno']['notasfiscais']
        filtered=[x for x in input_dict if (x['notafiscal']['situacao'] == STATUS)]
        for i in filtered:
            list_checked.append(i['notafiscal']['chaveAcesso'])
        return list_checked
    else:
        with open('nfs.json','r',encoding='utf-8') as f:
            input_dict=json.load(f)
            input_dict=input_dict['retorno']['notasfiscais']
            filtered=[x for x in input_dict if (x['notafiscal']['situacao'] == STATUS)]
            for i in filtered:
                list_checked.append(i['notafiscal']['chaveAcesso'])
        return list_checked


def create_checked_list():
    list_checked=filter_nfs_list(update_current_nfs())
    with open('checked.json','w') as f:
        f.write(json.dumps(list_checked))

def check_current_list():
    updated_nfs=update_current_nfs()
    filtered_nfs_list=filter_nfs_list(updated_nfs)

    with open('checked.json','r') as f:
        checked_list=json.load(f)
        if filtered_nfs_list==checked_list:
            print('nada mudou')
        else:
            print('mudou algo')
            send_email_notif()
            create_checked_list()

def check_file_exists():
    Thefile = Path('checked.json')
    if Thefile.exists()==False:
        Thefile.touch(exist_ok=True)
        with open('checked.json','a') as f:
            f.write('[]')
    Thefile = Path('nfs.json')
    Thefile.touch(exist_ok=True)

def send_email_notif():
    msg = EmailMessage()
    msg['Subject'] = "Bling Venda"
    msg['From'] = os.getenv("MEUEMAIL")
    msg['To'] = os.getenv("MEUEMAIL")
    password = os.getenv("MINHASENHA")
    msg.add_header('Content-Type', 'text/html')

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')

if __name__=="__main__":
    check_file_exists() 
    check_current_list()