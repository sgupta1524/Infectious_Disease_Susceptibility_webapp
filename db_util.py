from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import subprocess
import shutil
import os

Base = declarative_base()
engine = create_engine('sqlite:///Pristine.db', echo = True)
Session = sessionmaker(bind = engine)
session = Session()

class pristine_data(Base):

     __tablename__ = 'pristine_data'

     job_id = Column(Integer, primary_key=True)
     email = Column(String)
     job_submitted = Column(Integer)
     email_sent = Column(Integer)


def init_db():
    #print("initialising db")
    Base.metadata.create_all(engine)


def insert(obj):
    session.add(obj)
    session.commit()


def update_pipeline_status(JI):
    row = session.query(pristine_data).get(JI)
    row.job_submitted = 1
    session.commit()
	

def get_one(JI):
    row = session.query(pristine_data).get(JI)
    return row


def get_job_id_for_emails():
    results = session.query(pristine_data).filter(pristine_data.job_submitted == 1, pristine_data.email_sent == 0)
    required_ids = {}
    for result in results:
        required_ids[result.job_id] = result.email
    return required_ids


def update_email_status(JI, email_status):
    row=session.query(pristine_data).get(JI)
    row.email_sent = email_status
    session.commit()
    #shutil.rmtree("/projects/team-1/html/null-project/Input/" + JI+"/")
    #subprocess.run("cd "+"/projects/team-1/html/null-project/Input/" + JI+"/")
    #subprocess.run("rm *")
    #subprocess.run("cd ..")
    #subprocess.run("rm -r "+ "/projects/team-1/html/null-project/Input/" + JI, shell = True)
    location = "/projects/team-1/html/null-project/Input/"
    # directory
    dir = JI
    # path
    path = os.path.join(location, dir)
    shutil.rmtree(path, ignore_errors=True)


