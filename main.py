from flask import Flask, render_template
from multiprocessing import Pool
from flask_mail import Mail
import function
from flask import send_file
import time
import full_pipeline
app = Flask(__name__)
pool = Pool(processes=4)

BASE_INPUT_PATH = '/projects/team-1/html/null-project/Input'
BASE_OUTPUT_PATH = '/projects/team-1/html/null-project/Output'
UPLOAD_FOLDER = BASE_INPUT_PATH
DOWNLOAD_FOLDER = BASE_OUTPUT_PATH

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pristine.webapp@gmail.com'
app.config['MAIL_PASSWORD'] = 'Team1-pristine'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

import os
from flask import request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
from random import randint
import subprocess
import email_util
import db_util

db_util.init_db()

with app.app_context():
    email_util.init_email_sender(mail)

ALLOWED_EXTENSIONS = set(['txt','tsv','csv'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_job_id():
    r1 = randint(0, 9)
    r3 = randint(0, 9)
    r2 = datetime.today().strftime('%Y%m%d%H%M%S')
    return "2"+str(r1) + r2 + str(r3)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/index")
def index2():
    return render_template('index.html')

@app.route("/our_technology")
def our_technology():
    return render_template('our_technology.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/explore_infectious_diseases")
def explore_infectious_diseases():
    return render_template('explore_infectious_diseases.html')

@app.route("/chicken_pox")
def chicken_pox():
    return render_template('chicken_pox.html')

@app.route("/cold_sores")
def cold_sores():
    return render_template('cold_sores.html')

@app.route("/bladder_infection")
def bladder_infection():
    return render_template('bladder_infection.html')

@app.route("/childhood_ear_infection")
def childhood_ear_infection():
    return render_template('childhood_ear_infection.html')

@app.route("/chronic_sinus_infection")
def chronic_sinus_infection():
    return render_template('chronic_sinus_infection.html')

@app.route("/common_cold")
def common_cold():
    return render_template('common_cold.html')

@app.route("/covid_19")
def covid_19():
    return render_template('covid_19.html')

@app.route("/gingivitis")
def gingivitis():
    return render_template('gingivitis.html')

@app.route("/hepatitis")
def hepatitis():
    return render_template('hepatitis.html')

@app.route("/intestinal_parasites")
def intestinal_parasites():
    return render_template('intestinal_parasites.html')

@app.route("/measles")
def measles():
    return render_template('measles.html')

@app.route("/mononucleosis")
def mononucleosis():
    return render_template('mononucleosis.html')

@app.route("/mumps")
def mumps():
    return render_template('mumps.html')

@app.route("/myringitis")
def myringitis():
    return render_template('myringitis.html')

@app.route("/penumonia")
def penumonia():
    return render_template('penumonia.html')

@app.route("/plantar_warts")
def plantar_warts():
    return render_template('plantar_warts.html')

@app.route("/rheumatic_fever")
def rheumatic_fever():
    return render_template('rheumatic_fever.html')

@app.route("/rubella")
def rubella():
    return render_template('rubella.html')

@app.route("/scarlet_fever")
def scarlet_fever():
    return render_template('scarlet_fever.html')

@app.route("/shingles")
def shingles():
    return render_template('shingles.html')

@app.route("/strep_throat")
def strep_throat():
    return render_template('strep_throat.html')

@app.route("/tonsillitis")
def tonsillitis():
    return render_template('tonsillitis.html')

@app.route("/tuberculosis")
def tuberculosis():
    return render_template('tuberculosis.html')

@app.route("/urinary_tract_infection")
def urinary_tract_infection():
    return render_template('urinary_tract_infection.html')

@app.route("/about_us")
def about_us():
    return render_template('about_us.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # parsing Params
    user_email = str(request.form["email"])
    print("$$$$$$$$$$$$$$$$$$$$$"+user_email+"$$$$$$$$$$$$$$$$$$$$$$$$$")
    ancestry = str(request.form.get('ancestry'))
    print("*********************"+ancestry+"***************************")

    # check if the post request has the file part
    if 'file1' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file1 = request.files['file1']

    if file1.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return render_template('error.html')

    if file1 and (allowed_file(file1.filename)):
        filename1 = secure_filename(file1.filename)
        file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
        resp = jsonify({'message': 'File successfully uploaded'})
        resp.status_code = 201

        new_filename = generate_job_id()

        ###Moving files to job ID folder####
        subprocess.run("mkdir /projects/team-1/html/null-project/Input/" + new_filename, shell=True)
        subprocess.run("mkdir /projects/team-1/html/null-project/Output/" + new_filename, shell=True)
        subprocess.run("mv /projects/team-1/html/null-project/Input/" + file1.filename + " /projects/team-1/html/null-project/Input/" + new_filename + "_report.tsv", shell=True)
        subprocess.run("mv /projects/team-1/html/null-project/Input/" + new_filename + "_report.tsv"+ " /projects/team-1/html/null-project/Input/" + new_filename+"/"+new_filename + "_report.tsv", shell=True)

        ###########async call############

        file1_location = "/projects/team-1/html/null-project/Input/" +new_filename+"/" +new_filename + "_report.tsv"
        output_location = "/projects/team-1/html/null-project/Output/" + new_filename + "/"
        # pool.apply_async(pipeline_ahish_sonali.f, (file1_location,'GP_DOWNLOAD_FOLDER/job_id/'',file2_location,flag,))   # evaluate "f(10)" asynchronously in a single process
        #pool.apply_async(function.f, (10,new_filename))
        pool.apply_async(full_pipeline.f, (file1_location,output_location,ancestry,new_filename))
        #time.sleep(10)
        print("*********here************")
        c1 = db_util.pristine_data(job_id=new_filename, email=user_email, job_submitted=0, email_sent=0)
        db_util.insert(c1)

        #return resp
        return render_template('thankyou.html')
    else:
        resp = jsonify({'message': 'Allowed format is txt'})
        resp.status_code = 400
        return render_template('error.html')


@app.route("/download", methods=['GET'])
def download_processed_files():
    job_id = str(request.args.get("id"))
    subprocess.run("tar -zcvf ./Output/" + str(job_id)+".tar.gz ./Output/" + str(job_id), shell=True)
    file_path = BASE_OUTPUT_PATH + "/" + str(job_id)+".tar.gz"
    #file_path = BASE_OUTPUT_PATH+"/result.zip"
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = "22220")

