from flask import Flask
import db_util
import time
from flask_mail import Mail, Message
from multiprocessing import Pool
import function
import multiprocessing

DOWNLOAD_URL_PATH = 'http://team1.bioapp208803.biosci.gatech.edu/download?id=:id:'


def init_email_sender(mail_instance):
    print("::::::::::::::initialising email sender")

    p = multiprocessing.Process(target=f, args=(mail_instance,))
    p.start()


def f(mail_instance):
    while True:
        required_id = db_util.get_job_id_for_emails()
        #print(required_id)

        for job_id, email in required_id.items():
            download_url = generate_download_url(job_id)
            send_email(download_url, email, mail_instance)
        time.sleep(10)


def generate_download_url(job_id):
    download_url = DOWNLOAD_URL_PATH.replace(':id:', str(job_id))

    return download_url


def send_email(download_url, email, mail_instance):
    if is_email_valid(email):
        msg = Message('Result', sender='pristine.webapp@gmail.com', recipients=[email])
        msg.body = "Please click on the URL to download the results:" + "\n" + "\t" + download_url + "\n" + 'http://team1.bioapp208803.biosci.gatech.edu/explore_infectious_diseases'+"\n"+"Our results are presented in percentiles. " +"\n"+\
                   "A percentile is a number where a certain percentage of scores fall below that number. " +"\n"+"Therefore if you are at a 50th percentile for a given infectious disease, out of 100 normal people of your ancestry 50 will have a lower susceptibility score and 50 will have a higher susceptibility score . " +"\n"+\
                   "The susceptibility score is a genetic calculation that weighs a person’s odds of contracting each infectious disease."
        mail_instance.send(msg)
        db_util.update_email_status(download_url.split('=')[1], 1)
    else:
        db_util.update_email_status(download_url.split('=')[1], -1)


def is_email_valid(email):
    if (email is None) or (not email):
        return False
    if (len(email.split('@')) != 2) or (email.index('@') < 1) or (email.index('@') + 2 > email.rfind('.')) or (
            email.rfind('.') + 2 > len(email)):
        return False

    return True
