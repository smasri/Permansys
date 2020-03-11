# import gc
# import hashlib
# import json
import os
from Lib.functools import wraps
import pymysql
# from random import seed, randint
# import random
# import re
# import string
# import uuid
# #from testGmail import emailwithfile
# #from models import *
# from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template, request, flash, send_file, g, redirect, session, url_for
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
# #from flask_admin.model import BaseModelView as ModelView
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import text
# #from wtforms_sqlalchemy.orm import model_form
# from wtforms_alchemy import ModelForm
# import pyAesCrypt
# from werkzeug.datastructures import MultiDict
# #import nfname
from calendar import HTMLCalendar
from datetime import date
from flask_admin.model import typefmt
#from wtforms_alchemy import ModelForm
from flask_wtf import FlaskForm
from pmsdb import *
from flask_wtf.csrf import CSRFProtect
from flask import Blueprint
from flask_login import current_user
from flask import current_app as app
#from .assets import compile_auth_assets
from flask_login import login_required
from flask_table import Table, Col, LinkCol
from ISO import *

def date_format(view, value):
    return value.strftime('%d.%m.%Y')

MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
        type(None): typefmt.null_formatter,
        date: date_format
    })

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://dev_apps:dev_apps!@#@192.168.196.100:3306/pms"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root22011963@localhost:3308/pms"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///suku2.db3"
app.config['ED_FOLDER'] = "C:/UED"
app.secret_key = os.urandom(24)
# app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=9)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DB_SERVER'] = 'localhost'
app.config['UPLOAD_FOLDER'] = "C:/upload"
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024
app.config['WTF_CSRF_CHECK_DEFAULT'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 100
db = SQLAlchemy(app)

pms_bp = Blueprint('pms_bp', __name__,
                    template_folder='templates',
                    static_folder='static')
def get_db():
    if 'db' not in g:
        #g.db = sqlite3.connect("SUKU2.db3")
        g.db = pymysql.connect(host='localhost', port=3308, user='root', password='root22011963', db='pms', cursorclass=pymysql.cursors.DictCursor)
        #g.db = pymysql.connect(host='192.168.196.100',port=3306,user='dev_apps',password='dev_apps!@#',db='suk',cursorclass=pymysql.cursors.DictCursor)
    return g.db
def get_cur():
    if 'cur' not in g:
        g.dbx = get_db()
       #g.dbx.row_factory = sqlite3.Row
        g.cur =g.dbx.cursor()
    return g.cur

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:

            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            session.pop('logged_in',None)
            session['stat_log'] = "Status: Logged-Out"
            session['ng'] = "No Group Selected"
            return redirect(('/login'))
    return wrap


def makemydir(d):
    # d is a directory need to appended to c:\upload\
    d = app.config['UPLOAD_FOLDER'] + "/" + d
    if not os.path.exists(d):
        os.makedirs(d)

def makeEDdir(d):
    # d is a directory need to appended to c:\upload\
    d = app.config['ED_FOLDER'] + "/" + d
    if not os.path.exists(d):
        os.makedirs(d)

@pms_bp.route("/test_table")
def test_table():
    class RiskResponds(Table):

        mitigation = LinkCol("MitigationPlan",'pms_bp.selectrisk',attr='mitigation', url_kwargs=dict(id='id', jobtype='jobtype', jobid="jobid"))
        description =Col("Description")
        staff_responsible = Col("Staff ID")
        jobtype = Col("Job Type")
        jobid = Col("Job ID")
        classes = ["'display compact'"]
        html_attrs = {"id":"filetest"}

    riskresp = Risk_respond.query.all()
    session.remove()
    table = RiskResponds(items=riskresp)

    return render_template("test_table.html", table=table)

# updated for assign new Profile

@pms_bp.route("/nanti")
def nanti():
    return render_template("test_tab.html")

@pms_bp.route("/downloadpms")
def downloadpms():
    return render_template("test_tab.html")

@pms_bp.route("/editit")
def editit():
    return render_template("test_tab.html")
## to list risk and show detail/Add detail/add mitigation

@pms_bp.route("/list_risk")
def list_risk():
    #List all the risks and add mitigation in respond file.
    data = Risk_register.query.all()
    dbpms.session.remove()
    col = Risk_register.__table__.columns.keys()
    return render_template("list_risk.html", data = data, col = col)

@pms_bp.route('/testtablelogin', methods=('GET', 'POST'))
def testtablelogin():
    log = Login()
    logdata = log.query.all()
    dbpms.session.remove()
    logref = LoginTable
    logtable = logref(logdata)
    emailpri = session["ID_Login"]
    job = "Risk"
    sql = "Select * from Login where ID in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = LoginTable2
    jobsel = logref2(logsel)
    return render_template("myfirsttable.html", table = logtable, jobsel=jobsel, jobtype=job)

@pms_bp.route('/selectrisk', methods=('GET', 'POST'))
@login_required
def selectrisk():
    log = Risk_register()
    logdata = log.query.all()
    dbpms.session.remove()
    logref = Risk_table
    logtable = logref(logdata)
    emailpri = session["ID_Login"]
    job = "RISK"
    sql = "Select * from riskregister where ID in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = Risk_table2
    jobsel = logref2(logsel)
    job_head = "Risk Management - List of Core Risks"
    profile="Main"
    return render_template("myfirsttable.html", table = logtable, jobsel=jobsel, jobtype=job, job_head=job_head, profile=profile)

@pms_bp.route('/selectplans', methods=('GET', 'POST'))
@login_required
def selectplans():
    log = Risk_respond()
    if request.method == "GET":
        fn = request.args.get("id")
        job = request.args.get("jobtype")
        logdata = log.query.filter_by(jobid=fn,jobtype=job).all()
    else:
        logdata = log.query.all()

    logtable = Risk_respondtable(logdata)
    dbpms.session.remove()
    emailpri = session["ID_Login"]
    sql = "Select * from riskrespond where id in (select PlanID from planprofile where (EmailPri=%s and PlanType=%s and MainID=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job, fn))
    logsel = cur.fetchall()
    logref2 = Risk_respondtable2
    jobsel = logref2(logsel)
    job_head = "List of Controlled Plan"
    profile = "Plan"
    return render_template("myfirsttable.html", table = logtable, jobsel=jobsel, jobtype=job, job_head=job_head, profile=profile, fn = fn)

@pms_bp.route("/add_into_list", methods=["POST"])
@login_required
def add_into_list():
    # Process data from AJAX
    data ={}
    data = request.get_json()
    # data in the form of ID number
    if data:
        #  convert data to [xx@ccc, yyy@ccc]
        #mydata = re.findall(r'[\w\.-]+@[\w\.-]+', data["Email"])
        mdata = data["Selection"].split(',')
        group_use = data['GroupUsed']
        order = data['Order']
        admin1 = data["Ladmin"]
        job = data["Job"]
        fn = data["fn"]
        emailpri=session['ID_Login']
        #emailpri = 'Sukkuriya@gmail.com'

        # staffid = 'xxx'
        dbc = get_db()
        cur = dbc.cursor()
        if order == "Main":
            sqc = "select EmailPri from workprofile where EmailPri=%s and WorkProfile =%s and ProfileID=%s"
            sql = "Insert into `workprofile` (`EmailPri`, `WorkProfile`, `ProfileID`) values (%s,%s,%s)"
        else:
            sqc = "Select EmailPri from planprofile where EmailPri=%s and PlanType = %s and PlanID=%s"
            sql = "Insert into `planprofile` (`EmailPri`, `PlanType`, `PlanID`, `MainID`) values (%s,%s,%s,%s)"
        for i in mdata:
            cur.execute(sqc, (emailpri, job, i))
            data = cur.fetchone()
            if data is None:
                if order == "Plan":
                    cur.execute(sql, (emailpri, job, i, fn))
                else:
                    cur.execute(sql, (emailpri, job, i))
                dbc.commit()

        return jsonify({'data': 'New selection added/updated successfully'})

# updated for assign new Profile
@pms_bp.route("/del_from_list", methods=["POST"])
@login_required
def del_from_list():
    # Process data from AJAX
    data ={}
    data = request.get_json()
    # data in the form of ID number
    if data:
        #  convert data to [xx@ccc, yyy@ccc]
        #mydata = re.findall(r'[\w\.-]+@[\w\.-]+', data["Email"])
        mdata = data["Selection"].split(',')
        group_use = data['GroupUsed']
        order = data['Order']
        admin1 = data["Ladmin"]
        job = data["Job"]
        fn = data["fn"]
        emailpri=session['ID_Login']
        #emailpri = 'Sukkuriya@gmail.com'

        # staffid = 'xxx'
        dbc = get_db()
        cur = dbc.cursor()
        if order == "Main":
            sqc = "Delete From workprofile where EmailPri=%s and WorkProfile =%s and ProfileID=%s"
        else:
            sqc =  "Delete From planprofile where EmailPri=%s and PlanType =%s and PlanID=%s and MainID=%s"
        for i in mdata:
            if order == "Main":
                cur.execute(sqc, (emailpri, job, i))
            else:
                cur.execute(sqc, (emailpri, job, i, fn))
            dbc.commit()
        return jsonify({'data': 'Selection deleted successfully'})

@pms_bp.route('/selectKPI', methods=('GET', 'POST'))
@login_required
def selectKPI():
    log = Keykpi_register()
    logdata = log.query.all()
    dbpms.session.remove()
    logref = Keykpi_Table
    logtable = logref(logdata)
    emailpri = session["ID_Login"]
    job = "KPI"
    sql = "Select * from keykpi where id in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = Keykpi_Table2
    jobsel = logref2(logsel)

    job_head = "Key KPI - List of Key KPI"
    profile="Main"
    return render_template("myfirsttable.html", table = logtable, jobsel=jobsel, jobtype=job, job_head=job_head, profile=profile)

@pms_bp.route('/selectAudit', methods=('GET', 'POST'))
@login_required
def selectAudit():
    log = Audit_register()
    logdata = log.query.all()
    dbpms.session.remove()
    logref = Audit_Table
    logtable = logref(logdata)
    emailpri = session["ID_Login"]
    job = "AUDIT"
    sql = "Select * from auditregister where id in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = Audit_Table2
    jobsel = logref2(logsel)

    job_head = "Audit Findings-List"
    profile="Main"
    return render_template("myfirsttable.html", table = logtable, jobsel=jobsel, jobtype=job, job_head=job_head, profile=profile)

@pms_bp.route('/selectISO', methods=('GET', 'POST'))
@login_required
def selectISO():
    log = ISO_register()
    logdata = log.query.all()
    dbpms.session.remove()
    logref = ISO_Table
    logtable = logref(logdata)
    emailpri = session["ID_Login"]
    job = "ISO"
    sql = "Select * from isoregister where id in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = ISO_Table2
    jobsel = logref2(logsel)

    job_head = "ISO27001-Details"
    profile="Main"
    return render_template("myfirsttable.html", table = logtable, jobsel=jobsel, jobtype=job, job_head=job_head, profile=profile)

@pms_bp.route('/selectInstruction', methods=('GET', 'POST'))
@login_required
def selectInstruction():
    log = Instruction_register()
    logdata = log.query.all()
    dbpms.session.remove()
    logref = Instruction_Table
    logtable = logref(logdata)
    emailpri = session["ID_Login"]
    job = "INSTRUCT"
    sql = "Select * from instruction where id in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = Instruction_Table2
    jobsel = logref2(logsel)

    job_head = "Instructions-Details"
    profile="Main"
    return render_template("myfirsttable.html", table = logtable, jobsel=jobsel, jobtype=job, job_head=job_head, profile=profile)

@pms_bp.route('/selectTraining', methods=('GET', 'POST'))
@login_required
def selectTraining():
    log = Training_register()
    logdata = log.query.all()
    dbpms.session.remove()
    logref = Training_Table
    logtable = logref(logdata)
    emailpri = session["ID_Login"]
    job = "TRAIN"
    sql = "Select * from trainingregister where id in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = Training_Table2
    jobsel = logref2(logsel)

    job_head = "TRAINING-Details"
    profile="Main"
    return render_template("myfirsttable.html", table = logtable, jobsel=jobsel, jobtype=job, job_head=job_head, profile=profile)

@pms_bp.route('/selectTrainingSchedule', methods=('GET', 'POST'))
@login_required
def selectTrainingSchedule():
    log = Training_schedule()
    logdata = log.query.all()
    dbpms.session.remove()
    logref = Training_Schedule_Table
    logtable = logref(logdata)
    emailpri = session["ID_Login"]
    job = "TRAINSC"
    sql = "Select * from trainingschedule where id in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = Training_Schedule_Table2
    jobsel = logref2(logsel)

    job_head = "TRAINING SCHEDULE-Details"
    profile="Main"
    return render_template("myfirsttable.html", table = logtable, jobsel=jobsel, jobtype=job, job_head=job_head, profile=profile)

@pms_bp.route('/selectCompetency', methods=('GET', 'POST'))
@login_required
def selectCompetency():
    log = Competency_register()
    logdata = log.query.all()
    dbpms.session.remove()
    logref = Competency_Table
    logtable = logref(logdata)
    emailpri = session["ID_Login"]
    job = "COMT"
    sql = "Select * from competencyregister where id in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = Competency_Table2
    jobsel = logref2(logsel)

    job_head = "COMPETENCY CHOICES"
    profile="Main"
    return render_template("myfirsttable.html", table = logtable, jobsel=jobsel, jobtype=job, job_head=job_head, profile=profile)

@pms_bp.route('/selectPost', methods=('GET', 'POST')) # todo how to transfer topic to all HTML subs
@login_required
def selectPost():
    log = Post_register()
    logdata = log.query.all()
    dbpms.session.remove()
    logref = Post_Table
    logtable = logref(logdata)
    emailpri = session["ID_Login"]
    job = "POST"
    sql = "Select * from postregister where id in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = Post_Table2
    jobsel = logref2(logsel)

    job_head = "POST REGISTER Details"
    profile="Main"
    return render_template("myfirsttable.html", table = logtable, jobsel=jobsel, jobtype=job, job_head=job_head, profile=profile)

@pms_bp.route('/selectJob', methods=('GET', 'POST'))
@login_required
def selectJob():
    log = Job_description()
    logdata = log.query.all()
    dbpms.session.remove()
    logref = Job_Table
    logtable = logref(logdata)
    emailpri = session["ID_Login"]
    job = "JOBD"
    sql = "Select * from jobdescription where id in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = Job_Table2
    jobsel = logref2(logsel)

    job_head = "JOB REGISTERED Details"
    profile="Main"


    return render_template("myfirsttable.html", table = logtable, jobsel=jobsel, jobtype=job, job_head=job_head, profile=profile)

@pms_bp.route('/SummaryJob', methods=('GET', 'POST'))
@login_required
def SummaryJob():
    # log = Job_description()
    # logdata = log.query.all()
    # dbpms.session.remove()
    # logref = Job_Table
    # logtable = logref(logdata)
    emailpri = session["ID_Login"]
    job = "JOBD"
    sql = "Select * from jobdescription where id in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    jobsel = Job_Table(logsel,classes=['table table-striped'])
    # Search for plans detail
    ix = []
    if logsel:
        y = 0
        for x in logsel:
            ix.insert(y, x['id'])
            y = y + 1

        sq = 'SELECT A.EmailPri, A.PlanType, A.MainID, B.* \
            FROM riskrespond AS B INNER JOIN planprofile AS A ON B.id = A.ID \
            WHERE ((A.EmailPri)=%s) AND ((A.PlanType)=%s) AND ((A.MainID) In (' + ','.join((str(n) for n in ix)) + '))'
        cur.execute(sq, (emailpri, job))
        logsel = cur.fetchall()
        logref = Risk_respondtable3
        jobresp = logref(logsel)

    job_head = "Summary of Selection Details"
    profile="Main"

    job = "POST"
    sql = "Select * from postregister where id in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = Post_Table
    postsel = logref2(logsel,classes=['table table-striped'])
    # Search for plans detail
    ix = []
    if logsel:
        y = 0
        for x in logsel:
            ix.insert(y, x['id'])
            y = y + 1

        sq = 'SELECT A.EmailPri, A.PlanType, A.MainID, B.* \
            FROM riskrespond AS B INNER JOIN planprofile AS A ON B.id = A.ID \
            WHERE ((A.EmailPri)=%s) AND ((A.PlanType)=%s) AND ((A.MainID) In (' + ','.join((str(n) for n in ix)) + '))'
        cur.execute(sq, (emailpri, job))
        logsel = cur.fetchall()
        logref = Risk_respondtable3
        postresp = logref(logsel)

    job = "COMT"
    sql = "Select * from competencyregister where id in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = Competency_Table
    comtsel = logref2(logsel,classes=['table table-striped'])
    # Search for plans detail
    ix = []
    if logsel:
        y = 0
        for x in logsel:
            ix.insert(y, x['id'])
            y = y + 1

        sq = 'SELECT A.EmailPri, A.PlanType, A.MainID, B.* \
            FROM riskrespond AS B INNER JOIN planprofile AS A ON B.id = A.ID \
            WHERE ((A.EmailPri)=%s) AND ((A.PlanType)=%s) AND ((A.MainID) In (' + ','.join((str(n) for n in ix)) + '))'
        cur.execute(sq, (emailpri, job))
        logsel = cur.fetchall()
        logref = Risk_respondtable3
        comtresp = logref(logsel)

    job = "TRAINSC"
    sql = "Select * from trainingschedule where id in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = Training_Schedule_Table
    trainscsel = logref2(logsel,classes=['table table-striped'])
    # Search for plans detail
    ix = []
    if logsel:
        y = 0
        for x in logsel:
            ix.insert(y, x['id'])
            y = y + 1

        sq = 'SELECT A.EmailPri, A.PlanType, A.MainID, B.* \
            FROM riskrespond AS B INNER JOIN planprofile AS A ON B.id = A.ID \
            WHERE ((A.EmailPri)=%s) AND ((A.PlanType)=%s) AND ((A.MainID) In (' + ','.join((str(n) for n in ix)) + '))'
        cur.execute(sq, (emailpri, job))
        logsel = cur.fetchall()
        logref = Risk_respondtable3
        trainscresp = logref(logsel)
    else:
        trainscresp = ""

    job = "TRAIN"
    sql = "Select * from trainingregister where id in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = Training_Table
    trainsel = logref2(logsel,classes=['table table-striped'])
    # Search for plans detail
    ix = []
    if logsel:
        y = 0
        for x in logsel:
            ix.insert(y, x['id'])
            y = y + 1

        sq = 'SELECT A.EmailPri, A.PlanType, A.MainID, B.* \
            FROM riskrespond AS B INNER JOIN planprofile AS A ON B.id = A.ID \
            WHERE ((A.EmailPri)=%s) AND ((A.PlanType)=%s) AND ((A.MainID) In (' + ','.join((str(n) for n in ix)) + '))'
        cur.execute(sq, (emailpri, job))
        logsel = cur.fetchall()
        logref = Risk_respondtable3
        trainresp = logref(logsel)

    job = "INSTRUCT"
    sql = "Select * from instruction where id in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = Instruction_Table
    instructsel = logref2(logsel,classes=['table table-striped'])
    # Search for plans detail
    ix = []
    if logsel:
        y = 0
        for x in logsel:
            ix.insert(y, x['id'])
            y = y + 1

        sq = 'SELECT A.EmailPri, A.PlanType, A.MainID, B.* \
            FROM riskrespond AS B INNER JOIN planprofile AS A ON B.id = A.ID \
            WHERE ((A.EmailPri)=%s) AND ((A.PlanType)=%s) AND ((A.MainID) In (' + ','.join((str(n) for n in ix)) + '))'
        cur.execute(sq, (emailpri, job))
        logsel = cur.fetchall()
        logref = Risk_respondtable3
        instructresp = logref(logsel)
    else:
        instructresp = ''

    job = "ISO"
    sql = "Select * from isoregister where id in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = ISO_Table
    isosel = logref2(logsel,classes=['table table-striped'])
    # Search for plans detail
    ix = []
    if logsel:
        y = 0
        for x in logsel:
            ix.insert(y, x['id'])
            y = y + 1

        sq = 'SELECT A.EmailPri, A.PlanType, A.MainID, B.* \
            FROM riskrespond AS B INNER JOIN planprofile AS A ON B.id = A.ID \
            WHERE ((A.EmailPri)=%s) AND ((A.PlanType)=%s) AND ((A.MainID) In (' + ','.join((str(n) for n in ix)) + '))'
        cur.execute(sq, (emailpri, job))
        logsel = cur.fetchall()
        logref = Risk_respondtable3
        isoresp = logref(logsel)

    job = "AUDIT"
    sql = "Select * from auditregister where id in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = Audit_Table
    auditsel = logref2(logsel,classes=['table table-striped'])
    # Search for plans detail
    ix = []
    if logsel:
        y = 0
        for x in logsel:
            ix.insert(y, x['id'])
            y = y + 1

        sq = 'SELECT A.EmailPri, A.PlanType, A.MainID, B.* \
            FROM riskrespond AS B INNER JOIN planprofile AS A ON B.id = A.ID \
            WHERE ((A.EmailPri)=%s) AND ((A.PlanType)=%s) AND ((A.MainID) In (' + ','.join((str(n) for n in ix)) + '))'
        cur.execute(sq, (emailpri, job))
        logsel = cur.fetchall()
        logref = Risk_respondtable3
        auditresp = logref(logsel)
    else:
        auditresp = ''

    job = "KPI"
    sql = "Select * from keykpi where id in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = Keykpi_Table
    kpisel = logref2(logsel,classes=['table table-striped'])
    # Search for plans detail
    ix = []
    if logsel:
        y = 0
        for x in logsel:
            ix.insert(y, x['id'])
            y = y + 1

        sq = 'SELECT A.EmailPri, A.PlanType, A.MainID, B.* \
            FROM riskrespond AS B INNER JOIN planprofile AS A ON B.id = A.ID \
            WHERE ((A.EmailPri)=%s) AND ((A.PlanType)=%s) AND ((A.MainID) In (' + ','.join((str(n) for n in ix)) + '))'
        cur.execute(sq, (emailpri, job))
        logsel = cur.fetchall()
        logref = Risk_respondtable3
        kpiresp = logref(logsel)

    job = "RISK"
    sql = "Select * from riskregister where ID in (select ProfileID from workprofile where (EmailPri=%s and WorkProfile=%s)) "
    cur = get_cur()
    cur.execute(sql, (emailpri, job))
    logsel = cur.fetchall()
    logref2 = Risk_table
    risksel = logref2(logsel, classes=['table table-striped'])
    # Search for plans detail
    ix = []
    if logsel:
        y = 0
        for x in logsel:
            ix.insert(y,x['id'])
            y = y + 1

        sq = 'SELECT A.EmailPri, A.PlanType, A.MainID, B.* \
        FROM riskrespond AS B INNER JOIN planprofile AS A ON B.id = A.ID \
        WHERE ((A.EmailPri)=%s) AND ((A.PlanType)=%s) AND ((A.MainID) In (' + ','.join((str(n) for n in ix)) + '))'
        cur.execute(sq,(emailpri,job))
        logsel=cur.fetchall()
        logref = Risk_respondtable3
        riskresp = logref(logsel)

    return render_template("summarytable.html", kpisel=kpisel,kpiresp=kpiresp, auditsel=auditsel, auditresp=auditresp, \
                           instructsel=instructsel, instructresp=instructresp, trainsel=trainsel, trainresp=trainresp,\
                           trainscsel=trainscsel, trainscresp=trainscresp, comtsel=comtsel, comtresp=comtresp,\
                           isosel=isosel, isoresp=isoresp, postsel=postsel,postresp=postresp, jobsel=jobsel, jobresp=jobresp,\
                           risksel=risksel, riskresp=riskresp)


# todo: for contract management : Done 80% - to link to summary
# todo: Change of Staff and Handing Over the Jobs also History
# todo: Topics for all the HTML prompts
# todo: Comments and list of comments for each Table list
# todo: File upload/download for each Jobs and Plans - to check Jquery Mobile
# todo: Rationalise all tables fields
# todo: Summary of Login Jobs - 90%, next- todo Confirmation
# todo: Confirmation from Login after Selection of Jobs
# todo: Confirmation from Supervisor after received Login Submission Confirmation
# todo: Ability from login to look into each jobs and plans in a form format and upload or download files
# todo: email summary of the jobs
# todo: Convert from Primary or General Templates to Personal or Specific Templates to suit each person job
# todo: History of transactions
# todo: Improve the ADMIN parts so that Admin can manage all changes directly
# todo: save job for the year contracting, retrieve the year contracting
# todo: For Document submission, include -Jobtype, JobID, MainID, Group, EmailPri
# todo: Completion date for jobs.


if __name__ == "__main__":
    app.run(debug=True)