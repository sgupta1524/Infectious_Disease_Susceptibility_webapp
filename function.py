#!/usr/bin/env python3

import time
import db_util
from flask import Flask
import db_util
import time
from flask_mail import Mail, Message
from multiprocessing import Pool
import function
import subprocess

DOWNLOAD_URL_PATH = 'http://localhost:5000/download?id=:id:'


def f(mail_instance, job_id):

    for i in range(0,10):
        print(i)
        time.sleep(1)
    
    subprocess.run("pwd", shell = True)
    db_util.update_pipeline_status(job_id)
    """
    while True:
        print("**********************while loop*************************")
        required_id = db_util.get_job_id_for_emails()
        print(required_id)

        for job_id,email in required_id.items():
            download_url = generate_download_url(job_id)
            send_email(download_url,email,mail_instance)
        time.sleep(10)
    """
    
def generate_download_url(job_id):
    print("***************************2")
    download_url = DOWNLOAD_URL_PATH.replace(':id:',str(job_id))

    return download_url

def send_email(download_url, email,mail_instance):
    if is_email_valid(email):
        msg = Message('Result', sender = 'scoliagatech@gmail.com', recipients=[email])
        msg.body = "Please click on the URL to download the results:" + "\n" + "The blue represents your percentile for each infectious disease" + "\n" + "\t"+ download_url
        mail_instance.send(msg)
        db_util.update_email_status(download_url.split('=')[1], 1)
    else:
        db_util.update_email_status(download_url.split('=')[1], -1)

def is_email_valid (email):
    if (email is None) or (not email):
        return False
    if (len(email.split('@')) != 2) or (email.index('@')<1) or (email.index('@')+2>email.rfind('.')) or (email.rfind('.')+2>len(email)):
        return False

    return True
