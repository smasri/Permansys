# import os,smtplib, sqlite3,json, pymysql, gc, hashlib, re, uuid, decimal, random, string
# import sys
# sys.path.append('c:/Program Files/Python373/pyflas/')
# sys.path.append('C:/Program Files/Python373/pyflas/')
import gc
import hashlib
import json
import os
from Lib.functools import wraps
import pymysql
from random import seed, randint
import random
import re
import string
import uuid
from testGmail import emailwithfile
from models import *
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template, request, flash, send_file, g, redirect, session, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
#from flask_admin.model import BaseModelView as ModelView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
#from wtforms_sqlalchemy.orm import model_form
from wtforms_alchemy import ModelForm
import pyAesCrypt
import nfname
from datetime import date
from flask_admin.model import typefmt

def date_format(view, value):
    return value.strftime('%d.%m.%Y')

MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
        type(None): typefmt.null_formatter,
        date: date_format
    })

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://dev_apps:dev_apps!@#@192.168.196.100:3306/suk"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root22011963@localhost:3308/suk"
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///suku2.db3"
app.config['ED_FOLDER'] = "C:/UED"
app.secret_key = os.urandom(24)
#app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=9)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DB_SERVER'] = 'localhost'
app.config['UPLOAD_FOLDER'] = "C:/upload"
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024
dbs=SQLAlchemy(app)


def tapuksaya(fin,pwd):
    bufferSize = 64 * 1024
    pwd=encodepwd(pwd)
    fout = fin + ".aes"
    pyAesCrypt.encryptFile(fin, fout, pwd, bufferSize)

def bukasaya(fin,pwd):
    bufferSize = 64 * 1024
    pwd = encodepwd(pwd)
    pyAesCrypt.decryptFile(fin,fin[:-4],pwd, bufferSize)

def bukagroup(fin,pwd):
    bufferSize = 64 * 1024
    pyAesCrypt.decryptFile(fin,fin[:-4],pwd, bufferSize)

class UserView(ModelView):
    can_delete = False  # disable model deletion
    create_modal = True
    edit_modal = False
    can_export = False
    page_size = 5
    can_set_page_size = True
    column_searchable_list = ['Document_name']
    column_filters = ['Document_Group']
    column_type_formatters = MY_DEFAULT_FORMATTERS
    excluded_list_columns = ['Document_location', 'pwd', 'ec_type', 'Document_Group', 'Size', 'Date_Created', 'Date_Upload','Owner_ID']
    def is_accessible(self):
        if 'master_logged_in' in session:
            return True
        else:
            return False

class myLevelView(ModelView):
    can_delete = True  # disable model deletion
    create_modal = True
    edit_modal = True
    can_export = True
    def is_accessible(self):
        if 'master_logged_in' in session:
            return True
        else:
            return False

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
            return redirect(url_for('login'))
    return wrap

def master_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'master_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to be Super Admin first.")
            #  session['stat_log'] = "Status: Logged-Out"
            #  session['ng'] = "No Group Selected"
            return redirect(url_for('SelectGroup'))

    return wrap
def clearsession():
    session.pop("admin2", None)
    session.pop('user', None)
    session.pop('stat_log', None)
    session.pop('logged_in', None)
    session.pop('ID_Login', None)
    session.pop('PWD', None)
    session.pop('ng', None)

class myModelView(ModelView):
    def is_accessible(self):
        if 'master_logged_in' in session:
            return True
        else:
            return False

admin = Admin(app)
admin.add_view(myModelView(Login,dbs.session))
admin.add_view(UserView(DocumentMaster,dbs.session))
admin.add_view(myModelView(LoginHistory,dbs.session))
admin.add_view(myModelView(DocDialog,dbs.session))
admin.add_view(myModelView(GroupPrimary,dbs.session))
admin.add_view(myLevelView(MembersGroup,dbs.session))
admin.add_view(myLevelView(PostLevel,dbs.session, category='Level'))
admin.add_view(myLevelView(SecurityLevel,dbs.session, category='Level'))
admin.add_view(myLevelView(ActivityLevel,dbs.session, category='Level'))
admin.add_view(myLevelView(DivLevel,dbs.session, category='Level'))

#DocForm = model_form(DocumentMaster, exclude=['Document_location','pwd','ec_type','Document_Group','Size','Date_Created','Date_Upload','Owner_ID'])

class DocForm(ModelForm):
    class Meta:
        model = DocumentMaster
        exclude = ['Document_location', 'pwd', 'ec_type', 'Document_Group', 'Size', 'Date_Created', 'Date_Upload','Owner_ID']

def encodepwd(pwd):
    k1 = hashlib.md5(pwd.encode())
    return k1.hexdigest()

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
def get_dbase():
    db = pymysql.connect(host='localhost:3308',user='root',password='root22011963',db='suk',cursorclass=pymysql.cursors.DictCursor)
    return db
def get_db():
    if 'db' not in g:
        #g.db = sqlite3.connect("SUKU2.db3")
        g.db = pymysql.connect(host='localhost', port=3308, user='root', password='root22011963', db='suk', cursorclass=pymysql.cursors.DictCursor)
        #g.db = pymysql.connect(host='192.168.196.100',port=3306,user='dev_apps',password='dev_apps!@#',db='suk',cursorclass=pymysql.cursors.DictCursor)
    return g.db
def get_cur():
    if 'cur' not in g:
        g.dbx = get_db()
    if 'cur' not in g:
        #g.dbx.row_factory = sqlite3.Row
        g.cur =g.dbx.cursor()
    return g.cur

def check_indb(tbl,fld,vl):
    db = get_db()
    cur = db.cursor()
    cur.execute('select ' + fld + ' from ' + tbl + ' where ' + fld +'= %s', vl)
    return cur.fetchone()

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
 
""" @app.teardown_appcontext
def teardown_db():
    db = g.pop('db', None)

    if db is not None:
        db.close() """
# Take Random ID
def get_randomid():
    ff = uuid.uuid1()
    return("GID" + ff.hex)

# def get_cursor():
#     try:
#         cur = dbconn.cursor()
#         return cur
#     except:
#         print("Unknown Error")

""" 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS """
#
# #  static/data/test_data.json
# filename = os.path.join(app.static_folder, 'data', 'try.json')
#
# with open(filename) as test_file:
#     data = json.load(test_file)

# path = 'c:/upload'
list_of_files = {}
@app.before_request
def before_request():
    g.user = None
    if 'loggged_in' in session:
        g.user=session['logged_in']

@app.route('/getsession')
def getsession():
    if 'logged_in' in session:
        return session['logged_in']
    return "Not Logged In"

@app.route("/logout")
@login_required
def logout():
    act = {}
    act['type'] = "Logout"
    act['doc'] = ""
    activitylog(act)
    session.clear()
    session.pop('logged_in', None)
    flash("You have been logged out!")
    gc.collect()
    session['stat_log'] = "Status: Logged-out"
    session.pop('ng', None)
    return redirect(url_for('login'))

@app.route('/register')
def register():
    # First time registration
    if 'logged_in' in session:
        clearsession()
    dbconn=get_db()
    cur = dbconn.cursor()
    cur.execute("SELECT * from `post_level`")
    pl = cur.fetchall()
    cur.execute("Select * from `div_level`")
    dl= cur.fetchall()
    return render_template("register.html",pl=pl,dl=dl) 

@app.route('/processreg', methods=['POST'])
def processreg():
    fname= request.form.get('FirstName')
    lname= request.form.get('LastName')
    staffid= request.form.get('StaffID')
    division=request.form.get('StaffDiv')
    emailpri= request.form.get('inputEmailPri')
    emailsec= request.form.get('inputEmailSec')
    jobtype= request.form.get('jt')
    telcode= request.form.get('ICode')
    phonenum= request.form.get('phonenumber')
    pwdx= request.form.get('password1')
    ipaddress = request.environ.get('HTTP_X_REAL_IP', request.remote_addr) 
    now=datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    # print("Print {} {} {}:".format(staffid,emailpri,ipaddress))
    dbconn=get_db()
    cur = dbconn.cursor()

    # process password
    k1 = hashlib.md5(pwdx.encode())
    pwd = k1.hexdigest()
    #  Check if EMail already registered
    
    cur.execute("SELECT * from `login` WHERE `EmailPri`=(%s)", emailpri)
    cv = cur.fetchone()

    if not cv:
        # email provided is new and need verification
        res = {}
        # set the token for confirming email
        tokenpri = randomString(32)
        tokensec = randomString(32)
         # add new register
        sql = "INSERT INTO `login` (`Staff_ID`, `Division`,`Firstname`,`Lastname`, \
        `emailpri`,`emailsec`,`jobtype`,`phone`,`phonecode`,`password`, \
        `ipaddress`,`Date`, emailpri_verified,emailsec_verified, tokenpri, tokensec) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # email verification, 10-not verified, everything else is verified.
        cur.execute(sql, (staffid,division,fname,lname,emailpri,emailsec,jobtype,phonenum, \
        telcode, pwd, ipaddress, dt_string, 10,10,tokenpri,tokensec ))
        dbconn.commit()
        #res = "Your Registration is successful. Please use the EMail as a login ID"
        # Set first register to true
        session["FirstRegister"] = True

        # send_email(em)
        subject = "Email Registration into PT Vads Document Management System"
        body = "Dear sir, \n \nYour registration to PT Vads Document Management System is successfull. Please ensure that in order to \
really be able to use the system, and for the purpose of security of the system and documents, you are required to click the URL \
below to register your Email officially. \n\nhttp://127.0.0.1:5000/confirmedemail?token=" + tokenpri + "&email=" + emailpri + "\n\n \
                Your Login ID will be : " + emailpri + "\n\nThank you, \nAdministrator \nPT Vads Documents"
        emailwithfile(emailpri,subject,body)
        lok = "Registration successful: Your Login ID is: " + emailpri + " \n We have send you an Email to verify your email "
        return render_template("RegisterEmail.html",res = emailpri, lok=lok)
    else:
        # email found to be used already. Check if already registered
        cvv = cv['emailpri_verified']
        if  cvv != 20:
            # email need verification
            return render_template("RegisterEmail.html", res=emailpri)
        else:
            res = "The Email you provide had been registered or used. Please use a different Email if you want to register a new one or \
            go to recover password"
            return render_template("register.html",res = res, rok="Registration Fail ! Pse use different Email")


def activitylog(lg):
    lh = LoginHistory()
    lh.Activity_Key = session['ACTIVITYLOG']
    lh.Activity = lg['type']
    lh.FileName = lg['doc']
    lh.login_ID = session['ID_Login']
    dbs.session.add(lh)
    dbs.session.commit()

def activitylogx(lg):
    type_act = lg['type']
    doc = lg['doc']
    db = get_db()
    cur = db.cursor()
    key = session['ACTIVITYLOG']
    login_id = session['ID_Login']
    cur.execute('insert into login_history (activity, Filename, Activity_Key,login_ID) values (%s,%s,%s,%s)',(type_act,doc,key,login_id))
    db.commit()

@app.route('/login')
def login():
    clearsession()
    res = {}
    return render_template("register_2.html", res = res, lok="Please provide Email and Password")

@app.route('/processlogin', methods=["POST","GET"])

def processlogin():
    # Clear all session veriables
    if request.method == "POST":
        emailpri= request.form.get('inputEmailPri')
        pwd= request.form.get('password1')
        k1 = hashlib.md5(pwd.encode())
        pwd = k1.hexdigest()

    else:
        pwd = request.args.get("pwd")
        emailpri = request.args.get("id")

    cur = get_cur()
    cur.execute("SELECT * from `login` WHERE `EmailPri`=%s and `Password`=%s",(emailpri,pwd))
    cv = cur.fetchone()
    # check if email already verified
    if cv:
        if cv['emailpri_verified'] != 20:
            flash("Your Email has not been verified. Please verify accordingly to use the system")
            return render_template("RegisterEmail.html", res = emailpri)

    if not cv:
        return render_template("register_2.html", lok = "Sorry, login and password are not matching. Email: " + format(emailpri))
    else:
        db = get_db()
        cur = db.cursor()
        sql = "Select * from organisation"
        cur.execute(sql)

        app.config['ORGANISATION'] = cur.fetchall()
        sql = "Select * from risklevel"
        cur.execute(sql)

        app.config['RISKLEVEL'] = cur.fetchall()
        sql = "Select * from post_level"
        cur.execute(sql)

        app.config['POSTLEVEL'] = cur.fetchall()
        sql = "Select * from security_level"
        cur.execute(sql)

        app.config['SECURITYLEVEL'] = cur.fetchall()
        session['stat_log'] = "Status: Logged-in"
        session['logged_in'] = True
        session['ID_Login'] = emailpri

        session['PWD'] = pwd
        session['ACTIVITYLOG'] = str(randint(1,1e16))
        session.permanent = True
        act = {}
        act['type'] = "Login"
        act['doc'] = ""
        activitylog(act)
        #session["FirstRegister"] = False
        return redirect(url_for('SelectGroup'))

#  Select group to work with after Login
@app.route("/pwdchange", methods=['POST','GET'])
# @login_required
def pwdchange():
    if request.method == "POST":
        e_mail = request.form.get("E_Mail")

        if not e_mail:
           
            lok = "Enter EMail to send temp password"
        else:
            db = get_db()
            cur = db.cursor()
            cur.execute("SELECT * from `login` WHERE `EmailPri`=(%s)", e_mail)
            cv = cur.fetchall()
            if cv:
                lok = " Pse Check your Email to recover temporary Password"
                # Process Temporary Password
                tempwd = randomString()
                newPwd = encodepwd(tempwd)
                cur.execute("UPDATE `login` SET `Password`=%s where `emailPri`=%s", (newPwd,e_mail ))
                db.commit()
                subject = "PT VADS DMC Password recovery"
                body = "Hi\n\nYou have requested to recover your password.\n\n This is the new password: \n\n "+ tempwd + "\n\nPlease \
use the password to login and change your password. \n\n Thank You. \nAdministrator PTVADS DMS"

                emailwithfile("sukkuriya@gmail.com",subject,body)
                lok = " Pse Check your Email to recover temporary Password: " + tempwd
            else:
                lok = "The email provided is not registered. Please register first"
    else:
        lok = "Enter EMail to send temp password"
    return render_template("RecoverPassword.html", lok = lok)
@app.route("/cp")
# @login_required
def cp():
    return render_template('changePassword.html')

@app.route("/changepassword", methods=['POST','GET'])
# @login_required
def changepassword():
    e_mail = request.form.get('E_Mail')
    passwordold= request.form.get('passwordold')
    passwordnew= request.form.get('passwordnew')
    passwordnewretype = request.form.get('passwordnewretype')
    if passwordnew != passwordnewretype:
        lok = 'new password and retypwe password are missmatched. Pse enter new one'
        return render_template('changePassword.html', lok=lok)
    po= encodepwd(passwordold)
    pn= encodepwd(passwordnew)

    db = get_db()
    cur=db.cursor()
    cur.execute("Select `emailpri` from `login` where `emailpri`=%s and `password`=%s",(e_mail, po))
    
    cr = cur.fetchone()
    if cr:
        # process password change
        cur.execute('Update Login set password=%s where Emailpri=%s',(pn,e_mail))
        db.commit()
        lok="You have successfully change password. Pse login with new password"
        return render_template('register_2.html', lok=lok)
    else:
        lok = "email and password are unmatched. Please reenter"
        return render_template('changePassword.html', lok=lok)

@app.route("/SelectGroup", methods=['POST','GET'])
@login_required
def SelectGroup():
    staff_email = session['ID_Login']
    # new sel_group_name had been confirmed thru ajax call
    Sel_group_name = request.form.get("selgroupname")
    #  set unique ID for group name
    Sel_group_ID = request.form.get("Group_id")
    #  if not Sel_group_ID:
    #      Sel_group_ID = get_randomid()
    dbconn=get_db()
    # cur = dbconn.cursor()
    cur=get_cur()
    if "FirstRegister" in session:
        #  aha, this is first register staff
        #  direct to create new group first or select from existing group (not admin)
        db=get_db()
        #cur =db.cursor()
        cur = get_cur()
        # check if
        cur.execute('Select * from login')
        sel = cur.fetchall()
        return render_template("Create_group.html", cd=sel)

    else:
        # direct to select existing group

        sql = "SELECT A.Group_ID, A.Group_Name, A.Group_Description, 'Admin' as Status, A.Staff_EMail as Staff_Email FROM group_primary A WHERE A.staff_email = %s \
                UNION \
               SELECT B.id as Group_ID, B.Group_Name, B.Group_Description, 'Member' as Status, B.Members_ID as Staff_Email FROM members_group B WHERE B.members_ID = %s"

        cur.execute( sql, (staff_email,staff_email))
        sel = cur.fetchall()
        if not sel:
            #  Create new group
            return redirect(url_for("group"))

        return render_template("Select_group.html", sel = sel)


@app.route("/processdocument", methods=["GET", "POST"])
@login_required
def processdocument():
    # session["ID_group"] = request.args.get("Group_ID")
    # session["ng"] = request.args.get("Group_Name")
    # xa = request.args.get("ladmin")
    # if "Admin" in xa:
    #     session["admin2"] = True
    # else:
    #     session["admin2"] = False
    success = False
    doc = DocumentMaster()
    if request.method == 'POST':

        # form = DocForm(request.form, obj=doc)
        form = DocForm()
        if form.validate():
            form.populate_obj(doc)
            dbs.session.add(doc)
            dbs.session.commit()
            success = True

            flash('All fields are required to be filled')
            return render_template('register_document.html', form=form)
    else:
        form = DocForm(obj=doc)
        return render_template('Reg_Doc.html', form=form, success=success)

@app.route("/ActiveGroup", methods = ["GET","POST"])
@login_required
def ActiveGroup():
    session["ID_group"] = request.args.get("Group_ID")
    session["ng"] = request.args.get("Group_Name")
    xa = request.args.get("ladmin")
    if "Admin" in xa:
        session["admin2"] = True
    else:
        session["admin2"] = False
    
    return redirect("/")

@app.route("/member_list", methods=["GET"])
@login_required
def member_list():
    select_group = request.args.get('Group_Name')
    admin_status = request.args.get('ladmin')

    db = get_db()
    cur = db.cursor()
    sql = "(SELECT B.id, B.EmailPri, B.PhoneCode, B.Staff_ID, A.Group_Name, A.Members_ID, B.FirstName, B.LastName, B.JobType, B.Phone, B.Division, A.Member_status,\
     A.Number_of_transaction FROM members_group as A \
     INNER JOIN login as B ON (A.Members_ID = B.EmailPri) \
     WHERE (A.Group_Name=%s))"
    cur.execute(sql, select_group)
    
    sel = cur.fetchall()
    return render_template('select_member.html', sel = sel, g_name = select_group, am = admin_status, eml = session['ID_Login'])


@app.route("/del_member", methods=["POST"])
@login_required
def del_member():
    data = {}
    data = request.get_json()
    #  print("The Data received is:" + data["Email"] + " group: " + data["Group"])
    if data:
        #  convert data to [xx@ccc, yyy@ccc]
        recdata = re.findall(r'[\w\.-]+@[\w\.-]+', data["Email"])
        workgroup = data['CreateGroup']
        order = data['order']
        admin1 = data["ladmin"]

        if admin1 == 'Admin':
            session["admin2"] = True
        else:
            session["admin2"] = False

        db = get_db()
        cur = db.cursor()
        try:
            for i in recdata:
                sql = "DELETE FROM `members_group` WHERE (`Members_ID`=%s and `Group_Name`=%s);"
                cur.execute(sql, (i, workgroup))
                db.commit()
            return jsonify({'data': 'Selected Emails have been deleted successfully'})
        except:
            return jsonify({'error': 'Error in deleting'})
    else:
        return jsonify({'error': 'Data error!'})

@app.route("/process_member_delete", methods=["POST"])
@login_required
def process_member():
    # Process data from AJAX
    data ={}
    data = request.get_json()
    #  print("The Data received is:" + data["Email"] + " group: " + data["Group"])
    if data:
        #  convert data to [xx@ccc, yyy@ccc]
        mydata = re.findall(r'[\w\.-]+@[\w\.-]+', data["Email"])
        newgroup = data['CreateGroup']
        order = data['order']
        admin1 = data["ladmin"]

        if admin1 == 'Admin':
            session["admin2"] = True
        else:
            session["admin2"] = False

        mastergroup = session['ng']
        staff_email = session['ID_Login']

        #  # * insert into mysql
        dbconn=get_db()
        cur = dbconn.cursor()
        #  check if Group already exist
        sql = "Select max(`group_ID`) from `group_primary`"
        cur.execute(sql)
        dbconn.commit()
        max_id = cur.fetchone()

        if max_id['max(`group_ID`)'] is not None:
            group_id = int(max_id['max(`group_ID`)']) + 1
        else:
            group_id = 1
        ## Check if groupname already exists.

        sql = "SELECT * from `group_primary` where `Group_Name` = %s"
        cur.execute(sql, newgroup)
        sel = cur.fetchone()
        if (not sel):
            #  update Primary Group for new group creation
            if order != "addmember":
                sql = "INSERT into `group_primary` (`group_name`,`staff_email`,`Group_Description`) \
                     values (%s, %s, %s)"
                cur.execute(sql,(mastergroup, staff_email, group_description))
                dbconn.commit()
                session["ID_group"] = mastergroup

            #  Update members selection
            for i in mydata: #i refers to email_address of members
                sql = "INSERT INTO `members_group` (`members_id`, `group_name`) values (%s,%s)"
                cur.execute(sql, (i, newgroup))
                dbconn.commit()
                if order == "newmembers":
                    return jsonify({'data': 'New members added successfully'})
            if 'FirstRegister' in session:
                session.pop('FirstRegister', None)
            return jsonify({'data': 'New group name added successfully'})

        else:
            return jsonify({'error': 'Group Name had already been taken. Please use a different name'})

    else:
        return jsonify({'error': 'missing data!'})

@app.route("/my_group", methods=["POST"])
@login_required
def my_group():
    # Process data from AJAX-Create_Group and Add_member
    data = {}
    data = request.get_json()
    #  print("The Data received is:" + data["Email"] + " group: " + data["Group"])
    if data:
        #  convert data to [xx@ccc, yyy@ccc]
        mydata = re.findall(r'[\w\.-]+@[\w\.-]+', data["Email"])
        newgroup = data['CreateGroup']
        order = data['order']
        admin1 = data["ladmin"]
        group_description = data["GroupDescription"]
        if admin1 == 'Admin':
            session["admin2"] = True
        else:
            session["admin2"] = False

        if 'FirstRegister' in session:
            mastergroup = newgroup
        else:
            if 'ng' in session:
                mastergroup = session['ng']
            else:
                mastergroup = newgroup
        staff_email = session['ID_Login']

        #  # * insert into mysql
        dbconn=get_db()
        cur = dbconn.cursor()
        #  check if Group already exist
        sql = "Select max(`group_ID`) from `group_primary`"
        cur.execute(sql)
        dbconn.commit()
        max_id = cur.fetchone()

        if max_id['max(`group_ID`)'] is not None:
            group_id = int(max_id['max(`group_ID`)']) + 1
        else:
            group_id = 1

        # Lets Deal with creategroup
        if order =='creategroup':
            ## Check if groupname already exists.
            sql = "SELECT * from `group_primary` where `Group_Name` = %s"
            cur.execute(sql, newgroup)
            sel = cur.fetchone()
            if (not sel):
                #  update Primary Group for new group creation
                sql = "INSERT into `group_primary` (`group_name`,`staff_email`,`Group_Description`) \
                     values (%s, %s, %s)"
                cur.execute(sql, (newgroup, staff_email, group_description))
                dbconn.commit()
                #  Update members selection

                for i in mydata:  # i refers to email_address of members
                    sql = "INSERT INTO `members_group` (`members_id`, `group_name`) values (%s,%s)"
                    cur.execute(sql, (i, newgroup))
                    dbconn.commit()

                if 'FirstRegister' in session:
                    session.pop('FirstRegister', None)
                    session['ng'] = mastergroup
                return jsonify({'data': 'New group name added successfully'})
            else:
                return jsonify({'error': 'Group Name had already been taken. Please use a different name'})

        if order=='addmember':
            #  Update members selection
            for i in mydata: #i refers to email_address of members
                sql = "INSERT INTO `members_group` (`members_id`, `group_name`) values (%s,%s)"
                cur.execute(sql, (i, mastergroup))
                dbconn.commit()

            return jsonify({'data': 'New members added successfully'})
    else:
        return jsonify({'error': 'missing data!'})

@app.route("/group")
@login_required
def group():
    #group_Id = session['ng']
    staff_email = session['ID_Login']
    dbconn=get_db()
    cur = dbconn.cursor()
    sql = "Select * from `login` WHERE `EmailPri` not in (%s)"
    cur.execute(sql, staff_email)
    # cur.execute(sql, (group_Id, staff_email))
    cv = cur.fetchall()
    return render_template("Create_group.html", cd = cv)

@app.route('/list', methods=['get', 'post'])
@login_required
#  @master_required
def list():
    
    qid = request.args.get('question_id', default = '*', type = str)
    if qid != '*':
        #  return ('you asked for list {0}'.format(qid))
        with app.app_context():
            dbconn=get_db()
            cur = dbconn.cursor()
            cur.execute("Select * from login where EmailPri in (%s)",qid)
            cv = cur.fetchall()
            return render_template("JSONtoTable.html",cd=cv,content_type='application/json')
    else:
        with app.app_context():
            dbconn=get_db()
            cur = dbconn.cursor()
            cur.execute("Select * from login")
            cv = cur.fetchall()
            return render_template("JSONtoTable.html",cd=cv,content_type='application/json')

@app.route('/lista/<question_id>')
@login_required    
def find_list(question_id):  
    return ('you asked for list :{0}'.format(question_id))

@app.route('/table')
@login_required
def table():
    try:
        dbconn=get_db()
        cur = dbconn.cursor()
        tabledata = cur.execute("Select * from csvjson")

    except Exception as e:
        print(e)
        tabledata = None
    return render_template("Table.html", tabledata=tabledata)

@app.route('/')
@login_required
def home():
    #  for filename in os.listdir(path):
    #      list_of_files[filename] = filename
    dbconn = get_db()
    cur = dbconn.cursor()
    sql = "Select * from `document_master` where `Document_Group`=%s order by `Document_ID` Desc;"
    if 'ng' in session:
        G_id = session["ng"]
        #print("G_ID is ?", G_id)
        cur.execute(sql,G_id)
    else:
        return redirect(url_for("SelectGroup"))    
    data1 = cur.fetchall() 
    #  if not data1:
    #      return jsonify({"data":"You still dont have any Files in this server. Start Uploading."})
    return render_template("main.html", data=data1)


@app.route('/download', methods=['POST','GET'])
@login_required
def download ():
    # For windows you need to use drive name [ex: F:/Example.pdf]
    if request.method == "GET":
        docid = request.args.get("fn")
    else:
        docid = request.form.get("fn")

    dbconn = get_db()
    cur = dbconn.cursor()

    sql = "Select * from Document_Master where Document_ID = %s"
    cur.execute(sql, (docid))
    data = cur.fetchone()
    if  data['Tot_download'] is None:
        tot_download = 0
    else:
        tot_download = data['Tot_download']

    sql = f"update Document_master Set Tot_download={tot_download + 1} where Document_ID = {docid}"
    cur.execute(sql)
    dbconn.commit()

    if data:
        path = data['Document_location']
        gpwd = data['pwd']
        ec_type = data['ec_type']
        gid = data['Document_Group']
    else:
        flash("Document Missing")
        return redirect("/")
    if ec_type == '3':
        # just send directly the file
        act = {}
        act['type'] = "Download"
        act['doc'] = path
        activitylog(act)
        return send_file(path, as_attachment=True)
    if '.aes' in path:
        # os.chdir("c:/upload/" + str(gid) + "/")
        # need to decrypt
        pwd=session['PWD']
        if session['admin2']:
            try:
                bukagroup(path,gpwd)
            except:
                flash("The file is not available")
                return redirect("/")
        else:
            if ec_type == "1":
                flash("You are not authorised to download this file")
                return redirect("/")
            if ec_type == "2":
                try:
                    bukagroup(path, gpwd)
                except:
                    flash("The file is not available")
                    return redirect("/")

        path = path[:-4]
        act = {}
        act['type'] = "Download"
        act['doc'] = path
        activitylog(act)
    return send_file(path, as_attachment=True)

@app.route('/js')
@login_required
def js():
    return render_template("JSONtoHTML.html", data=data)

@app.route('/mod')
@login_required
def mod():
    dbconn = get_db()
    cur = dbconn.cursor
    sql = "Select * from document_primary where Document_group=%s"
    cur.execute(sql,('OCM3'))
    data = cur.fetchall() 
    return render_template("modalex.html", data=data)

@app.route('/savefiletest', methods=["POST"])
def savefiletest():
    if request.method == 'POST':
        fls = request.files.getlist("files[]")
        for f in fls:
            f.save(os.path.join("c:/upload/test/",f.filename))
    return redirect("/")

@app.route('/upload_file')
@login_required
def upload_file():
    if 'ng' in session:
        G_id = session["ng"]
    else:
        return redirect(url_for("SelectGroup"))
    #return render_template('dropfile.html')
    return render_template('Upload_File.html')

@app.route('/processupload', methods=['POST'])
@login_required
def processupload():
    if 'ng' in session:
        G_id = session["ng"]
    else:
        return redirect(url_for("SelectGroup"))
    mymessage=""
    if request.method == "POST":
        files = request.files.getlist("files[]")
        enc_o = request.form.get("rs")
        dbconn = get_db()
        cur = dbconn.cursor()
        sql = "Select max(`Document_ID`) from `Document_master`"
        cur.execute(sql)
        dbconn.commit()
        max_id = cur.fetchone()
        if max_id['max(`Document_ID`)'] is not None:
            group_id = int(max_id['max(`Document_ID`)']) + 1
        else:
            group_id = 1
        now=datetime.now()
        G_id = session['ng']
        makemydir(G_id)
        # general no encryption
        ec_type = '3'
        pwd=""
        for file in files:
            # if (os.path.isfile('c:/upload/' + G_id + "/" + file.filename)):
            #     # filename exist, need to rename the file and save
            fnewname = nfname.nf('c:/upload/' + G_id + "/", file.filename)
            # else:
            #     fnewname = file.filename

            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + G_id, fnewname))
            if enc_o == "1":
                tapuksaya(app.config['UPLOAD_FOLDER'] + "/" + G_id + "/" + fnewname, session['PWD'])
                os.remove(app.config['UPLOAD_FOLDER'] + "/" + G_id + "/" + fnewname)
                pwd = encodepwd(session['PWD'])
                ec_type = '1'
            if enc_o =="2": #group
                tapuksaya(app.config['UPLOAD_FOLDER'] + "/" + G_id +"/"+ fnewname,session['PWD'] + G_id)
                os.remove(app.config['UPLOAD_FOLDER'] + "/" + G_id + "/" + fnewname)
                pwd = encodepwd(session['PWD'] + G_id)
                ec_type = '2'
            mymessage = mymessage + "," + file.filename
            #  flash('File successfully uploaded: ' + file.filename)
            #  towork

            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            sql = "insert into Document_Master (Document_Name, Document_Group, date_Created, Risk_level,\
                    Security_Level, date_Upload , Owner_Id, date_Modified, Document_location, ec_type, pwd, size) Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            # flash('File successfully uploaded: ' + file.filename)
            if enc_o=="1" or enc_o=="2":
                fnew = fnewname + ".aes"
            else:
                fnew = fnewname

            st = os.stat("c:/upload/" + G_id +"/" + fnew)
            fsize = "{:.0f}".format(st.st_size/(1024))
            detail = (fnew, G_id, dt_string, 1, 2, dt_string, session['ID_Login'], dt_string,"c:/upload/" + G_id +"/" + fnew, ec_type, pwd, fsize)

            #  flash('File successfully uploaded: ' + file.filename)
            cur.execute(sql, detail)
            dbconn.commit()
            act = {}
            act['type'] = "Upload"
            act['doc'] = fnew
            activitylog(act)
        flash("Files Uploaded successfully: "+ mymessage)
        return redirect("/")

@app.route("/add_member")
@login_required

def add_member():
    group_Id = session['ng']
    staff_email = session['ID_Login']
    dbconn = get_db()
    cur = dbconn.cursor()
    sql = "SELECT A.Staff_ID, A.EmailPri, A.Division, A.FirstName, A.LastName, A.JobType, B.Members_ID \
            FROM login AS A LEFT JOIN (SELECT A.Members_ID FROM members_group A WHERE (((A.Group_Name)= %s)) \
            GROUP BY A.Members_ID) AS B ON A.EmailPri = B.Members_ID \
            WHERE (((A.EmailPri)<> %s) AND ((B.Members_ID) Is Null))"
    cur.execute(sql, (group_Id, staff_email))
    cv = cur.fetchall()
    return render_template("add_member.html", cv=cv)

@app.route("/utilityencrypdecryp")
@login_required
def utilityencrypdecryp():

    return render_template("Utility_ED.html")
@app.route("/processencrypdecryp", methods=['POST'])
@login_required
def processencrypdecryp():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        job = request.form.get('rs')
        pwd = request.form.get('pwd')
        now = datetime.now()
        G_id = session['ng']
        makeEDdir(G_id)
        for file in files:
            # if (os.path.isfile('c:/upload/' + G_id + "/" + file.filename)):
            #     # filename exist, need to rename the file and save
            fnewname = nfname.nf(app.config['ED_FOLDER'] + "/" + G_id + "/", file.filename)
            # else:
            #     fnewname = file.filename

            if job == "1": # encrypt and send file
                file.save(os.path.join(app.config['ED_FOLDER'] + "/" + "/" + G_id, fnewname))
                path = app.config['ED_FOLDER'] + "/" + G_id + "/" + fnewname
                try:
                    tapuksaya(path, pwd)
                    os.remove(path)
                    return send_file(path + ".aes", as_attachment=True)
                    os.remove(path + ".aes")
                    ec_type = '1'
                    mymessage = "Encrypt"
                except:
                    flash("Something wrong. Maybe wrong password, or wrong selection of encrypt/decrypt")
                    return render_template("Utility_ED.html")
            if job =="2": #Decryp and send file
                file.save(os.path.join(app.config['ED_FOLDER'] + "/" + G_id, file.filename))
                path = app.config['ED_FOLDER'] + "/" + G_id + "/" + file.filename
                try:
                    bukasaya(path, pwd)
                    os.remove(path)
                    return send_file(path[:-4], as_attachment=True)
                    os.remove(path[:-4])
                    mymessage = "Decrypt"
                except:
                    flash("Something wrong. Maybe wrong password, or wrong selection of encrypt/decrypt")
                    return render_template("Utility_ED.html")

            mymessage.append('File successfully encrypt/decrypt: ' + file.filename)
            flash(mymessage)
            return render_template("Utility_ED.html")

@app.route("/editit", methods=['GET'])
@login_required
def editit():
    if request.method =='GET':
        job = request.args.get('job')
        fn = request.args.get('fn')
        # db = get_db()
        # cur = db.cursor()
        # sql = "Select * from document_master where Document_ID = %s"
        # cur.execute(sql,fn)
        # db.commit()
        # re = cur.fetchone()
        dm = DocumentMaster()
        pe = dm.query.filter_by(Document_ID=fn).first()
        if job == "edit":
            form = DocForm(obj=pe)
            return render_template("edit_file.html", form=form)
        if job == "email":
            form = DocForm(obj=pe)
            return render_template("edit_file.html", form=form)
        if job == "delete":
            form = DocForm(obj=pe)
            return render_template("edit_file.html", form=form)

@app.route("/add_dialog", methods=['POST'])
@login_required
def add_dialog():
    if request.method =='POST':
        di = DocDialog()
        data = request.get_json()
        di.Doc_ID = data['ID']
        di.dialog = data['msg']
        di.Name = session["ID_Login"]
        try:
            dbs.session.add(di)
            dbs.session.commit()
            return jsonify({'data': 'Message saved successfully'})
        except:
            return jsonify({'error': 'Message saved failed !'})

@app.route("/get_dialog", methods=['POST'])
@login_required
def get_dialog():
    if request.method =='POST':
        # di = DocDialog()
        data = request.get_json()
        # #di.Doc_ID = data['ID']
        # #di.dialog = data['msg']
        # di.Name = session["ID_Login"]

        try:
            #row = di.query.filter_by(Doc_ID = data['ID']).order_by(desc(di.Date_Comment)).all()
            rem = dbs.session()
            sql = text("select dialog,Date_Comment,Name from docdialog where Doc_ID =" + data["ID"] + " order by Date_Comment desc")
            row = rem.execute(sql)
            #row = rem.fetchall()
            da = ''
            for d in row:
                da = da + "<b>" + d.Name + "@" + str(d.Date_Comment) + ": " + "</b>" + d.dialog + "<br /><br />"
            return jsonify({'data': da})
        except:
            return jsonify({'error': 'Error: Cannot get message !'})

@app.route("/registeremail", methods=['POST','GET'])
def registeremail():
    if request.method == "POST":
        emailpri= request.form.get('E_Mail')
        tokenpri = randomString(32)
        db = get_db()
        cur=db.cursor()
        #chek if email has been verified or not
        sql = "SELECT emailpri_verified from login where emailpri=%s"
        cur.execute(sql,emailpri)
        ret = cur.fetchone()
        if ret:
            if ret['emailpri_verified'] != 20:
                sql = "UPDATE login SET tokenpri=%s WHERE emailpri=%s"
                cur.execute(sql,(tokenpri,emailpri))
                db.commit()
                # send verify email
                subject = "Email Registration into PT Vads Document Management System - reregister"
                body = "Dear sir, \n \nPlease ensure that in order to \
really be able to use the system, and for the purpose of security of the system and documents, you are required to click the URL \
below to register your Email officially. \n\nhttp://127.0.0.1:5000/confirmedemail?token=" + tokenpri + "&email=" + emailpri + "\n\n \
                Your Login ID will be : " + emailpri + "\n\nThank you, \nAdministrator \nPT Vads Documents"
                try:
                    emailwithfile("sukkuriya@gmail.com", subject, body)
                    flash("Email for registration of your email has been sent. Please confirm your email as soon as possible")
                except:
                    flash("Email sending Fail. Please check your email or internet connection")
                return render_template("kosong.html")

            else:
                flash("Email had been verified earlier")
                return render_template("kosong.html")
        else:
            flash("Email not found in Database. Please register again")
            return render_template("kosong.html")


@app.route("/confirmedemail", methods=['GET'])
def confirmedemail():
    token = request.args.get('token')
    emailpri = request.args.get('email')
    db = get_db()
    cur = db.cursor()
    try:
        sql = "UPDATE login SET emailpri_verified=%s WHERE tokenpri=%s"
        cur.execute(sql,(20, token))
        db.commit()
        #successfull then change the token. So no twice try confirm from email.
        token = randomString(32)
        sql = "UPDATE login SET tokenpri=%s WHERE emailpri=%s"
        cur.execute(sql,(token,emailpri))
        db.commit()
        subject = "Successfull Email Registration into PT VADS Document Management System"

        body = "You have succefully register your Email into PT Vads Document management system. \n\nYou can start to login and use the system. \
        \n\nAdministrator\nPT Vads Document"
    except:
        subject = "FAIL Email Registration into PT VADS Document Management System"
        body = "You have failed to register your Email into PT Vads Document management system. \n\nPlease try to register again. \
        \n\nAdministrator\nPT Vads Document"
    emailwithfile(emailpri,subject,body)
    return render_template("register_2.html", res = "Successfull Email registration", lok = "Successfull Email registration")


if __name__ == "__main__":
    app.run(debug=True)
