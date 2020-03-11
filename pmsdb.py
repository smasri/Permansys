# coding: utf-8
from flask import Flask
import os
from sqlalchemy import Column, Date, DateTime, Float, Integer, String, Table
from flask_sqlalchemy import SQLAlchemy, Model
from flask_wtf import FlaskForm, RecaptchaField, Form
from sqlalchemy.sql import func
from wtforms_alchemy import ModelForm
from wtforms_alchemy.fields import QuerySelectField
from wtforms.fields import RadioField, Label,FileField, TextAreaField
from wtforms import StringField, TextField, SubmitField
from wtforms import validators
from flask_migrate import Migrate
from wtforms.fields.html5 import DateField, DateTimeField
from flask_table import Table, Col, LinkCol, DatetimeCol, DateCol
from sqlalchemy_utils import ColorType

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root22011963@localhost:3308/pms"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 100
dbpms = SQLAlchemy(app)
dbpms.Model.metadata.reflect(bind=dbpms.engine,schema='pms')
dbm = Migrate(app, dbpms)
################################################################################
# Reference for class Tables used for the program
################################################################################
def read(statement):
    """Executes a read query and returns a list of dicts, whose keys are column names."""
    try:
        data = dbpms.session.execute(statement).fetchall()
        results = []

        if len(data) == 0:
            return results

        # results from sqlalchemy are returned as a list of tuples; this procedure converts it into a list of dicts
        for row_number, row in enumerate(data):
            results.append({})
            for column_number, value in enumerate(row):
                results[row_number][row.keys()[column_number]] = value

        return results
    finally:
        dbpms.session.close()
class contract_register(dbpms.Model):
    __tablename__="contractregister"
    year = dbpms.Column(dbpms.String(4), info={'label': "Year"})
    quarter = dbpms.Column(dbpms.String(4), info={'label': "Quarter"})
    name = dbpms.Column(dbpms.String(200), info={'label': "Contract Name"})
    description = dbpms.Column(dbpms.Text(200), info={'label': "Description"})
    from_date = dbpms.Column(dbpms.DateTime, info={'label': "Start Date"})
    to_date = dbpms.Column(dbpms.DateTime, info={'label': "End Date"})
    date_entered = dbpms.Column(dbpms.DateTime, info={'label':'Date Entered'})
    date_submitted = dbpms.Column(dbpms.DateTime, info={'label':'Date Submitted'})
    date_confirmed = dbpms.Column(dbpms.DateTime, info={'label':'Date Confirmed'})
    login = dbpms.Column(dbpms.String(200), info={'label': "Login ID"})
    superior = dbpms.Column(dbpms.String(200), info={'label': "Superior" ,'choices': [('0',"Pse Choose one"),('1',"Financial"),('2',"Market & Customer"),('3',"Internal Business"),('4',"Learning and Innovation")]})
    comment = dbpms.Column(dbpms.Text(200), info={'label': "Comment"})
    ID = dbpms.Column(dbpms.Integer, primary_key = True)

class contract_registerForm(ModelForm):
    class Meta :
        model = contract_register
        include_primary_keys = True
        exclude = ['login', 'date_entered', 'date_submitted', 'date_confirmed']
    name = TextField("Contract Name")
    description = TextAreaField("Contract Description")
    jobtype = TextField("Job Type", default = 'contract')
    year = TextField("Effective Year")
    from_date = DateField('Start Date (mdy)', format='%Y-%m-%d')
    to_date = DateField('End Date (mdy)', format='%Y-%m-%d')

class contract_table(Table):
    ID = Col("ContractID")
    name = Col("Name")
    description = Col("Description")
    year = Col("Year")
    quarter = Col("Quarter")
    from_date = Col("Start Date")
    to_date = Col("End Date")
    date_entered = Col("Date Entered")
    date_submitted = Col("Date Submitted")
    date_confirmed = Col("Date Confirmed")
    superior = Col("Superior")
    comment = Col("Comment")
    classes = ['display compact']
    table_id = "Joblist"
    html_attrs = {"cellspacing": 0, "width": "100%"}


class Documentchange(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.document_change']
    __tablename__ = "document_change"
    id = dbpms.Column(dbpms.Integer, primary_key = True)
    date_input = dbpms.Column(dbpms.DateTime)
    input_by = dbpms.Column(dbpms.String(45), info={'label': "Load By"})
    version_No = dbpms.Column(dbpms.String(45), info={'label': "Version No"})
    changes = dbpms.Column(dbpms.String(200), info={'label': "Change Description"})
    approved_By = dbpms.Column(dbpms.String(45), info={'label': "Approved by"})
    change_ref = dbpms.Column(dbpms.String(45), info={'label': "Reference"})
    date_created = dbpms.Column(dbpms.DateTime, info={'label': "Date Uploaded"})

class DocumentchangeForm(ModelForm):
    class Meta:
        model = Documentchange

class Keykpi_register(dbpms.Model):
    __tablename__ = "keykpi"
    id = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    kpi_category = dbpms.Column(dbpms.String(10), info={'label': "KPI Category"})
    level_strategy_id = dbpms.Column(dbpms.String(10), info={'label': "Strategy ID"})
    okr_desc = dbpms.Column(dbpms.String(4), info={'label': "OKR Description"})
    kpi_description = dbpms.Column(dbpms.Text(250), info={'label': "KPI Description"})
    kpi_measure = dbpms.Column(dbpms.String(200), info={'label': "KPI Measure"})
    kpi_weight = dbpms.Column(dbpms.String(10), info={'label': "Weight"})
    year = dbpms.Column(dbpms.String(4), info={'label': "Year"})
    quarter = dbpms.Column(dbpms.String(2), info={'label': "Quarter"})
    kpi_start_date = dbpms.Column(dbpms.DateTime, info={'label': "Start Date"})
    kpi_end_date = dbpms.Column(dbpms.DateTime, info={'label': "End Date"})
    kpi_type = dbpms.Column(dbpms.String(10), info={'label': "KPI Type"}) # personel, Team
     # A, B, C - the higher the better, the lower the better, unlimited
    superior_id = dbpms.Column(dbpms.String(10), info={'label': "Superior ID"})
    kpi_achievement = dbpms.Column(dbpms.Text(200), info={'label': "KPI Achievement"})
    kpi_challenges = dbpms.Column(dbpms.Text(200), info={'label': "KPI Challenges"})
    superior_feedback = dbpms.Column(dbpms.Text(200), info={'label': "Superior Feedback"})
    recognition_achieved = dbpms.Column(dbpms.String(200), info={'label': "Recognition"})
    kpi_plan = dbpms.Column(dbpms.Text(500), info={'label': "KPI action plan"})
    job_description_id = dbpms.Column(dbpms.String(4), info={'label': "Job Description ID"})
    staff_id = dbpms.Column(dbpms.String(40), info={'label': "Staff ID"})
    date_created = dbpms.Column(dbpms.DateTime, server_default=func.now(), info={'label': "Date Created"})
    kpi_report_file = dbpms.Column(dbpms.Text(200), info={'label': "KPI report"})
    strategy_id = dbpms.Column(dbpms.Integer, dbpms.ForeignKey('strategy.id'), info={'label': "Strategy ID"})
    #isoregister = dbpms.relationship(Iso_register, backref='keykpi')
    #auditregister = dbpms.relationship(Audit_register, backref='keykpi')
    #postregister = dbpms.relationship(Post_register, backref='keykpi')
    #riskreg = dbpms.relationship(Risk_register, backref='keykpi')

class Keykpi_Table(Table):
    id = Col("KeyKPI ID")
    okr_desc = Col("OKR Desc")
    kpi_description = Col("KPI Desc")
    kpi_measure = Col("Measure")
    kpi_weight = Col("Weight")
    kpi_type = Col("Type")
    kpi_category = Col("Category")
    level_strategy_id = Col("Strategy ID")
    classes = ['display compact']
    table_id = "Joblist"
    html_attrs = {"cellspacing": 0, "width": "100%"}

class Keykpi_Table2(Keykpi_Table):
    okr_desc = LinkCol("OKR Desc", "pms_bp.selectplans", attr="okr_desc", url_kwargs=dict(id="id", jobtype="jobtype"))
    table_id = "Joblistselected"

class Keykpi_registerForm(ModelForm):
    class Meta:
        model = Keykpi_register
        exclude = ["date_created", "staff_id", "job_description_id" ]

class Strategy_register(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.strategy']
    __tablename__ = "strategy"
    id = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    core_strategy = dbpms.Column(dbpms.String(40), info={'label': "Core Strategy",'choices': [('0',"Pse Choose one"),('1',"Financial"),('2',"Market & Customer"),('3',"Internal Business"),('4',"Learning and Innovation")]})
    #level_strategy = dbpms.Column(dbpms.String(100), info={'label': "Focus"})
    year = dbpms.Column(dbpms.String(4), info={'label': "Year"})
    quarter = dbpms.Column(dbpms.String(2), info={'label': "Quarter"})
    description = dbpms.Column(dbpms.Text(250), info={'label': "Description"})
    key_result_area = dbpms.Column(dbpms.String(200), info={'label': "Objective Key Result"})
    key_measure = dbpms.Column(dbpms.String(100), info={'label': "Key Measure"})
    key_measure_target = dbpms.Column(dbpms.String(50), info={'label': "Key Measure Target"})
    #key_measure_type = dbpms.Column(dbpms.String(2), info={'label': "Key Measure Type"})
    weightage = dbpms.Column(dbpms.Integer, info={'label': "Weightage"})
    version = dbpms.Column(dbpms.String(2), info={'label': "Version"})
    date_created = dbpms.Column(dbpms.DateTime, server_default=func.now(), info={'label': "Date Created"})
    Key_kpi = dbpms.relationship('Keykpi_register', backref='strategy') #
#
class Strategy_Table(Table):
    id = Col("AuditID")
    core_strategy = Col("Core-Strategy")
    description = Col("Description")
    key_result_area = Col("KRA")
    key_measure = Col("KeyMeasure")
    key_measure_target = Col("KeyMeasureTarget")
    weightage = Col("Weight")
    classes = ['display compact']
    table_id = "Joblist"
    html_attrs = {"cellspacing": 0, "width": "100%"}

class Strategy_Table2(Strategy_Table):
    core_strategy = LinkCol("Core-Strategy", "Strategy.showdetail", attr="core_strategy", url_kwargs=dict(id="id", jobtype="jobtype"))
    table_id = "Filetest"

class Strategy_registerForm(ModelForm):
    class Meta:
        model = Strategy_register
        #Key_kpi = FlaskFormField(KeykpiForm)

f = read("select id,level_name from risklevel")
class Risk_register(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.riskregister']
    __tablename__ = "riskregister"
    core_risk = dbpms.Column(dbpms.String(40), info={'label': "Core Risk"})
    description = dbpms.Column(dbpms.Text(250), info={'label': "Risk Description"})
    risk_cause = dbpms.Column(dbpms.String(200), info={"label":"Cause of Risk"})
    risk_effect = dbpms.Column(dbpms.String(200), info={"label" : "Effect caused by Risk"})
    #level_risk = dbpms.Column(dbpms.String(100), info={'label': "Level of Risk",'choices': [(x['level_name'], x['level_name']) for x in f]})
    risk_probability = dbpms.Column(dbpms.String(4), info={'label':"Risk Probability (Select 1-10)",'choices': [(i, i) for i in range(1, 11)]}, nullable=False)
    risk_impact = dbpms.Column(dbpms.String(4), info={'label': "Risk Impact (Select 1-5)",'choices':[(str(x['id']), x['level_name']) for x in f]})
    risk_rating = dbpms.Column(dbpms.String(4), info={'label': "Risk Rating",'choices': [('0',"Pse Choose one"),('1',"Low"),('2',"Medium"),('3',"High"),('4',"Dangerous")]})
    risk_rangking = dbpms.Column(dbpms.String(4), info={'label': "Risk Rank"})
    risk_mitigation = dbpms.Column(dbpms.String(200), info={'label': "Action/Mitigation"})
    year = dbpms.Column(dbpms.String(4), info={'label': "Year"})
    quarter = dbpms.Column(dbpms.String(2), info={'label': "Quarter"})
    id = dbpms.Column(dbpms.Integer,primary_key=True, unique=True)
    date_created = dbpms.Column(dbpms.DateTime, default=func.now(), info={'label': "Risk record created"})
    #background_color = dbpms.Column(ColorType(), nullable=False)
    #keykpi_id = dbpms.Column(dbpms.Integer, dbpms.ForeignKey('keykpi.id')) #
    owner_id = dbpms.Column(dbpms.String(45), dbpms.ForeignKey('login.emailpri'), info={'label': "Risk Owner"})
    respond_id = dbpms.Column(dbpms.Integer, dbpms.ForeignKey('riskrespond.id'), info={'label': "Risk Respond ID"})
    #owner = dbpms.relationship('Key_kpi', foreign_keys=[owner_id])
    #respond = dbpms.relationship('Risk_respond', foreign_keys=[respond_id])

class Risk_table(Table):
    id = Col("RiskID")
    core_risk= Col("Core Risk")
    description = Col("Description")
    risk_probability=Col("Probability")
    risk_impact = Col("Impact")
    risk_rating = Col("Rating")
    table_id = "Joblist"
    classes = ['display compact']

class Risk_table2(Risk_table):
    core_risk = LinkCol("Core-Risk","pms_bp.selectplans",attr="core_risk", url_kwargs=dict(id="id", jobtype="jobtype"))
    table_id = "Joblistselected"

def risk_rating():
    return Risklevel.query

class Risk_registerForm(ModelForm):
    class Meta:
        model = Risk_register
        exclude = ["risk_impact"]
    risk_impact = RadioField("Risk Impact", choices=[(str(x['id']), x['level_name']) for x in f])
    risk_probability = RadioField("Risk Probability", choices=[(i, i) for i in range(1, 6)])
    risk_rating = RadioField( "Risk Rating", choices =[('1', "Low"),('2', "Medium"), ('3', "High"),('4', "Dangerous")])
    image = FileField('Image File')

def form_factory():
    class Risk_registerForm(ModelForm):
        class Meta:
            model = Risk_register
            exclude = ["risk_impact"]
        risk_impact = RadioField("Risk Impact", choices=[(str(x['id']), x['level_name']) for x in f])
        risk_probability = RadioField("Risk Probability", choices=[(i, i) for i in range(1, 6)])
        risk_rating = RadioField( "Risk Rating", choices =[('1', "Low"),('2', "Medium"), ('3', "High"),('4', "Dangerous")])
        image = FileField('Image File')
        def validate_image(form, field):
            if field.data:
                field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)
    return Risk_registerForm

class Risk_respond(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.riskrespond']
    __tablename__ = "riskrespond"
    mitigation = dbpms.Column(dbpms.String(200), info={'label': "Sub-Detail Name"})
    description = dbpms.Column(dbpms.Text(250), info={'label': "Description"})
    year = dbpms.Column(dbpms.String(4), info={'label': "Year"})
    quarter = dbpms.Column(dbpms.String(2), info={'label': "Quarter"})
    staff_responsible = dbpms.Column(dbpms.String(45), info={'label': "Staff ID"})
    division_responsible = dbpms.Column(dbpms.String(40), info={'label': "Division ID"})
    id = dbpms.Column(dbpms.Integer,primary_key=True, unique=True, info={'label': "Respond ID"})
    #date_created = dbpms.Column(dbpms.DateTime, server_default=func.now(), info={'label': "Date Created"})
    report_file = dbpms.Column(dbpms.String(200), info={'label': "Report File"})
    jobtype = dbpms.Column(dbpms.String(45), info={'label': "Job Type"})
    jobid = dbpms.Column(dbpms.Integer, info={'label': "Job Type ID"})
    groupid = dbpms.Column(dbpms.Integer, info={'label': "Group ID"})
    #riskreg_id = dbpms.Column(dbpms.Integer, dbpms.ForeignKey('riskregister.id'), info={'label': "Risk Category"})

class Risk_respondtable(Table):
    id=Col("PlanID")
    mitigation = Col("Plan")
    description = Col("Description")
    division_responsible = Col("Div Owner")
    table_id = "Joblist"
    classes = ['display compact']
    def get_tr_attrs(self, item):
        return {'id':'id'}

class Risk_respondtable2(Risk_respondtable):
    table_id = "Joblistselected"

class Risk_respondtable3(Table):
    MainID = Col("Main ID")
    EmailPri = Col("Login")
    id = Col("PlanID")
    mitigation = Col("Plan")
    description = Col("Description")
    division_responsible = Col("Div Owner")
    classes = ['table table-bordered']
class Risklevel(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.risklevel']
    __tablename__ = "risklevel"
    id = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    level_name = dbpms.Column(dbpms.String(100), info={'label': "Level Name"})
    level_description = dbpms.Column(dbpms.Text(200), info={'label': "Level Description"})

def mitigation_factory():
    class Risk_respondForm(ModelForm):
        class Meta:
            model = Risk_respond
    return Risk_respondForm

class Audit_register(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.auditregister']
    __tablename__ = "auditregister"
    core_audit = dbpms.Column(dbpms.String(100), info={'label': "Core Audit Issue",'choices': [('0',"Pse Choose one"),('1',"Financial"),('2',"Market & Customer"),('3',"Operation"),('4',"Learning and Support")]})
    audit_place = dbpms.Column(dbpms.String(200), info={'label': "Site/Section/Division of Audit"})
    audit_team = dbpms.Column(dbpms.String(200), info={'label': "Audit Team"})
    audit_entry_date = dbpms.Column(dbpms.Date, info={'label': "Dates Entry"})
    audit_exit_date = dbpms.Column(dbpms.Date, info={'label': "Dates Exit"})
    audit_scope = dbpms.Column(dbpms.String(4), info={'label': "Audit Scope"})
    audit_finding = dbpms.Column(dbpms.Text(500), info={'label': "Audit Finding"})
    audit_finding_level = dbpms.Column(dbpms.String(100), info={'label': "Audit Finding Level",'choices': [('0',"Pse Choose one"),('1',"Minor"),('2',"Moderate"),('3',"Major")]})
    audit_0peration_assessment = dbpms.Column(dbpms.String(100), info={'label': "Audit Operation Assessment",'choices': [('0', "Pse Choose one"), ('1', "Not Effective"), ('2', "Partial Effective"), ('3', "Effective")]})
    audit_recommendation = dbpms.Column(dbpms.Text(500), info={'label': "Recommendation"})
    year = dbpms.Column(dbpms.String(4), info={'label': "Year"})
    quarter = dbpms.Column(dbpms.String(2), info={'label': "Quarter"})
    audit_respond_target_date = dbpms.Column(dbpms.Date, info={'label': "Respond Target Date"})
    id = dbpms.Column(dbpms.Integer,primary_key=True, unique=True)
    date_created = dbpms.Column(dbpms.DateTime, server_default=func.now(), info={'label': "Date_created"})
    audit_report_file = dbpms.Column(dbpms.String(200), info={'label': "Audit Files"})
    owner_id = dbpms.Column(dbpms.String(45), dbpms.ForeignKey('login.emailpri'), info={'label': "Auditee ID"})
    respond_id = dbpms.Column(dbpms.Integer, dbpms.ForeignKey('auditrespond.id'), info={'label': "Respond ID"})

class Audit_Table(Table):
    id = Col("AuditID")
    core_audit = Col("Audit-Desc")
    audit_place = Col("PlaceAudited")
    audit_team = Col("TeamName")
    audit_scope = Col("Scope")
    audit_finding = Col("Findings")
    audit_finding_level = Col("FindingLevel")
    audit_Operation_assessment = Col("Assessment")
    audit_recommendation = Col("Recommendation")
    audit_respond_target_date = Col("TargetDate")
    classes = ['display compact']
    table_id = "Joblist"
    html_attrs = {"cellspacing": 0, "width": "100%"}

class Audit_Table2(Audit_Table):
    core_audit = LinkCol("Audit-Desc", "pms_bp.selectplans", attr="core_audit", url_kwargs=dict(id="id", jobtype="jobtype"))
    table_id = "Joblistselected"

class Audit_registerForm(ModelForm):
    class Meta:
        model = Audit_register

class Audit_respond(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.auditrespond']
    __tablename__ = "auditrespond"
    audit_recovery_plan = dbpms.Column(dbpms.Text(200), info={'label': "Audit Recovery Plans"})
    year = dbpms.Column(dbpms.String(4), info={'label': "Year"})
    quarter = dbpms.Column(dbpms.String(2), info={'label': "Quarter"})
    description = dbpms.Column(dbpms.Text(250), info={'label': "Description"})
    staff_responsible = dbpms.Column(dbpms.String(40), info={'label': "Staff Responsible"})
    division_responsible = dbpms.Column(dbpms.String(40), info={'label': "Division Responsible"})
    id = dbpms.Column(dbpms.Integer,primary_key=True, unique=True)
    date_created = dbpms.Column(dbpms.DateTime, server_default=func.now(), info={'label': "Date Created"})
    auditee_respond_date = dbpms.Column(dbpms.Date, info={'label': "Auditee Respond Date"})
    audit_report_file = dbpms.Column(dbpms.String(200), info={'label': "Audit Report File"})
    auditor_respond_assessment = dbpms.Column(dbpms.String(100), info={'label': "Audit Operation Assessment"})
    auditor_name = dbpms.Column(dbpms.String(150), info={'label': "Auditor Name"})
    auditor_comment = dbpms.Column(dbpms.Text(250), info={'label': "Auditor Comment"})
    auditor_respond_date = dbpms.Column(dbpms.Date, info={'label': "Auditor Respond Date"})

class Audit_respondForm(ModelForm):
    class Meta:
        model = Audit_respond

class ISO_register(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.isoregister']
    __tablename__ = "isoregister"
    id = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    core_iso_domainnum = dbpms.Column(dbpms.String(40), info={'label': "ISO Domain Number"})
    core_iso_description = dbpms.Column(dbpms.String(200), info={'label': "Domain Description"})
    iso_topic = dbpms.Column(dbpms.String(250), info={'label': "Iso Topic"})
    iso_objective = dbpms.Column(dbpms.Text(500), info={'label': "Objective"})
    iso_domain_serial = dbpms.Column(dbpms.String(40), info={'label': "Domain Serial No"})
    iso_domain_topic = dbpms.Column(dbpms.String(100), info={'label': "Domain Sub Topic"})
    iso_policy_description = dbpms.Column(dbpms.Text(1000), info={'label': "Domain sub Description"})
    year = dbpms.Column(dbpms.String(4), info={'label': "Year"})
    quarter = dbpms.Column(dbpms.String(2), info={'label': "Quarter"})
    date_created = dbpms.Column(dbpms.DateTime, server_default=func.now(), info={'label': "Date Created"})
    iso_report_file = dbpms.Column(dbpms.String(200), info={'label': "Iso Document"})
    owner_id = dbpms.Column(dbpms.String(45), dbpms.ForeignKey('login.emailpri'), info={'label': "Owner ID"})
    respond_id = dbpms.Column(dbpms.Integer, dbpms.ForeignKey('isorespond.id'), info={'label': "Respond ID"})

class ISO_Table(Table):
    id = Col("ISO-ID")
    core_iso_domainnum = Col("ISO-Domain")
    core_iso_description = Col("Description")
    iso_topic = Col("Topic")
    iso_objective = Col("Objective")
    iso_policy_description = Col("PolicyDesc")
    iso_domain_serial = Col("ISO Serial")
    iso_domain_topic = Col("Domain-Topic")
    classes = ['display compact']
    table_id = "Joblist"
    html_attrs = {"cellspacing": 0, "width": "100%"}

class ISO_Table2(ISO_Table):
    core_iso_domainnum = LinkCol("ISO-Domain", "pms_bp.selectplans", attr="core_iso_domainnum", url_kwargs=dict(id="id", jobtype="jobtype"))
    table_id = "Joblistselected"

class ISO_registerForm(ModelForm):
    class Meta:
        model = ISO_register
    #date_created = DateField('Date Created', format='%Y-%m-%d')
    date_updated = DateField("Date Updated", format='%d/%m/%Y')

class ISO_respond(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.isorespond']
    __tablename__="isorespond"
    id = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    year = dbpms.Column(dbpms.String(4), info={'label': "Year"})
    quarter = dbpms.Column(dbpms.String(2), info={'label': "Quarter"})
    staff_responsible = dbpms.Column(dbpms.String(40), info={'label': "Staff_responsible"})
    division_responsible = dbpms.Column(dbpms.String(40), info={'label': "Division Responsible"})
    date_created = dbpms.Column(dbpms.DateTime, server_default=func.now(), info={'label': "Date Created"})
    date_responded = dbpms.Column(dbpms.DateTime, server_default=func.now(), info={'label': "Date Responded"})
    iso_report_file = dbpms.Column(dbpms.String(200), info={'label': "Respond Document"})

class Iso_respondForm(ModelForm):
    class Meta:
        model = ISO_respond

class Training_schedule(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.trainingschedule']
    __tablename__ = "trainingschedule"
    id = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    training_start_date = dbpms.Column(dbpms.DateTime, info={'label': "Start Date"})
    training_end_date = dbpms.Column(dbpms.DateTime, info={'label': "End Date"})
    training_name = dbpms.Column(dbpms.String(200), info={'label': "Training Name"})
    description = dbpms.Column(dbpms.Text(250), info={'label': "Description"})
    training_room =  dbpms.Column(dbpms.String(200), info={'label': "Training Room"})
    training_address = dbpms.Column(dbpms.String(200), info={'label': "Training Address"})
    training_lecturer = dbpms.Column(dbpms.String(200), info={'label': "Training Lecturer"})
    training_internal = dbpms.Column(dbpms.String(2), info={'label': "Training Category", 'choices':[('1','Internal'),('2','External')]})
    training_ref_doc = dbpms.Column(dbpms.String(200), info={'label': "Training Documents"})
    trainingregister_id = dbpms.Column(dbpms.Integer, dbpms.ForeignKey('trainingregister.id'), info={'label': "TRaining Register ID"})

class Training_Schedule_Table(Table):
    id = Col("TrainScheduleID")
    training_name = Col("Training-Name")
    description = Col("Description")
    training_room = Col("Room")
    training_address = Col("Address")
    training_lecturer = Col("Lecturer")
    training_start_date = Col("Start-Date")
    training_end_date = Col("End-Date")
    classes = ['display compact']
    table_id = "Joblist"
    html_attrs = {"cellspacing": 0, "width": "100%"}

class Training_Schedule_Table2(Training_Schedule_Table):
    training_name = LinkCol("Schedule-Name", "pms_bp.selectplans", attr="training_name", url_kwargs=dict(id="id", jobtype="jobtype"))
    table_id = "Joblistselected"

class Training_scheduleForm(ModelForm):
    class Meta:
        model = Training_schedule

class Training_register(dbpms.Model):
    # __table__ = dbpms.Model.metadata.tables['pms.trainingregister']
    __tablename__ = "trainingregister"
    id = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    training_name = dbpms.Column(dbpms.Text, info={'label': "Training Name"})
    training_description = dbpms.Column(dbpms.Text, info={'label': "Description"})
    training_type = dbpms.Column(dbpms.String(200), info={'label': "Type"}) # Core, crossfunctional, functional
    training_category = dbpms.Column(dbpms.String(200), info={'label': "Category"}) #Technical, behaviour, emotional, leadership
    #trainingschedule = dbpms.relationship('Training_schedule', backref='trainingregister')
    competencyregister_id = dbpms.Column(dbpms.Integer, dbpms.ForeignKey('competencyregister.id')) #

class Training_Table(Table):
    id = Col("TrainID")
    training_name = Col("Training-Topic")
    training_description = Col("Description")
    training_type = Col("Type")
    training_category = Col("Category")
    classes = ['display compact']
    table_id = "Joblist"
    html_attrs = {"cellspacing": 0, "width": "100%"}

class Training_Table2(Training_Table):
    training_name = LinkCol("Training-Name", "pms_bp.selectplans", attr="training_name", url_kwargs=dict(id="id", jobtype="jobtype"))
    table_id = "Joblistselected"

class Training_registerForm(ModelForm):
    class Meta:
        model = Training_register

class Competency_register(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.competencyregister']
    __tablename__ = "competencyregister"
    id = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    competency_name = dbpms.Column(dbpms.Text, info={'label': "Competency Name"})
    competency_description = dbpms.Column(dbpms.Text(200), info={'label': "Description"})
    competency_type = dbpms.Column(dbpms.String(200), info={'label': "Competency Type"}) # Core, crossfunctional, functional
    competency_category = dbpms.Column(dbpms.String(200), info={'label': "Competency Category"}) #Technical, behaviour, emotional, leadership
    jobdescription_id = dbpms.Column(dbpms.Integer, dbpms.ForeignKey('jobdescription.id'), info={'label': "JobDesc ID"}) #
    # trainingregister = dbpms.relationship('Training_register', backref='competencyregister') #

class Competency_Table(Table):
    id = Col("CompetencyID")
    competency_name = Col("Competency-Name")
    competency_description = Col("Description")
    competency_type = Col("Type")
    competency_category = Col("Category")
    classes = ['display compact']
    table_id = "Joblist"
    html_attrs = {"cellspacing": 0, "width": "100%"}

class Competency_Table2(Competency_Table):
    competency_name = LinkCol("Competency-Name", "pms_bp.selectplans", attr="competency_name", url_kwargs=dict(id="id", jobtype="jobtype"))
    table_id = "Joblistselected"

class Competency_registerForm(ModelForm):
    class Meta:
        model = Competency_register

class Instruction_register(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.jobdescription']
    __tablename__ = "instruction"
    id = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    name = dbpms.Column(dbpms.String(45), info={'label': "Job Name"})
    description = dbpms.Column(dbpms.Text(200), info={'label': "Description"})
    reference = dbpms.Column(dbpms.String(10), info={'label': "Reference"}) #1. Own, 2. Risk, 3. ISO, 4. Audit 5. Compliant 6. Team Project,7. SuperiorInstruction
    responsibleperson = dbpms.Column(dbpms.String(100), info={'label': "Responsible Person"})
    startdate = dbpms.Column(dbpms.DateTime, info={'label': "Planned Start"})
    enddate = dbpms.Column(dbpms.DateTime, info={'label': "Planned End"})
    actualstart = dbpms.Column(dbpms.DateTime, info = {'label': "Actual Start"})
    actualend = dbpms.Column(dbpms.DateTime, info={'label': "Actual End"})
    budgetreference = dbpms.Column(dbpms.String(100), info={'label': "Budget Reference"})
    budgetamount = dbpms.Column(dbpms.String(100), info={'label': "Budget Amount"})
    specialinstruction = dbpms.Column(dbpms.Text, info={'label': "SpecialInstruction"})
    groupreference = dbpms.Column(dbpms.String(45), info={'label': "Group Reference"})

class Instruction_Table(Table):
    id = Col("InstructionID")
    name = Col("Name")
    description = Col("Description")
    reference = Col("Reference")
    specialinstruction = Col("Special-Instr")
    classes = ['display compact']
    table_id = "Joblist"
    html_attrs = {"cellspacing": 0, "width": "100%"}

class Instruction_Table2(Instruction_Table):
    name = LinkCol("Instruction-Name", "pms_bp.selectplans", attr="name", url_kwargs=dict(id="id", jobtype="jobtype"))
    table_id = "Joblistselected"

class Job_description(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.jobdescription']
    __tablename__ = "jobdescription"
    id = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    job_name = dbpms.Column(dbpms.String(100), info={'label': "Job Name"})
    job_objective = dbpms.Column(dbpms.Text(250), info={'label': "Objectives"})
    job_type = dbpms.Column(dbpms.String(10), info={'label': "Job Type"}) #1. Own, 2. Risk, 3. ISO, 4. Audit 5. Compliant 6. Team Project,7. SuperiorInstruction
    job_reportto_id = dbpms.Column(dbpms.String(200), info={'label': "Job Report_to ID"})
    job_file_ref = dbpms.Column(dbpms.String(200), info={'label': "Job Document"})
    job_deliverables = dbpms.Column(dbpms.Text(200), info={'label': "Deliverables"})
    job_key_process = dbpms.Column(dbpms.Text(200), info={'label': "Processes Involved"})
    year = dbpms.Column(dbpms.String(4), info={'label': "Year"})
    quarter = dbpms.Column(dbpms.String(2), info={'label': "Quarter"})
    date_created = dbpms.Column(dbpms.DateTime, server_default=func.now(), info={'label': "Date Created"})
    job_file = dbpms.Column(dbpms.String(200), info={'label': "Job Document"})
    postreg_id = dbpms.Column(dbpms.Integer, dbpms.ForeignKey('postregister.id'), info={'label': "Post ID"}) #
    # competency = dbpms.relationship('Competency_register', backref='jobdescription')

class Job_Table(Table):
    id = Col("JobID")
    job_name = Col("Name")
    job_objective = Col("Objective")
    job_deliverables = Col("Deliverables")
    job_type = Col("Job-Type")
    job_key_process = Col("Key-Process")
    classes = ['display compact']
    table_id = "Joblist"
    html_attrs = {"cellspacing": 0, "width": "100%"}

class Job_Table2(Job_Table):
    job_name = LinkCol("Job-Name", "pms_bp.selectplans", attr="job_name", url_kwargs=dict(id="id", jobtype="jobtype"))
    table_id = "Joblistselected"

class Job_descriptionForm(ModelForm):
    class Meta:
        model = Job_description

class Post_register(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.postregister']
    __tablename__ = "postregister"
    id = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    date_created = dbpms.Column(dbpms.DateTime, server_default=func.now(), info={'label': "Date Created"})
    post_name = dbpms.Column(dbpms.Text, info={'label': "Post Name"})
    post_grade = dbpms.Column(dbpms.Integer, info={'label': "Grade"})
    post_description = dbpms.Column(dbpms.Text(200), info={'label': "Description"})
    post_type = dbpms.Column(dbpms.String(200), info={'label': "Type"}) # Core, crossfunctional, functional
    post_category = dbpms.Column(dbpms.String(200), info={'label': "Category"}) #Technical, behaviour, emotional, leadership
    post_id_report_to = dbpms.Column(dbpms.Integer, info={'label': "Higher Post ID"})
    division_id = dbpms.Column(dbpms.Integer, dbpms.ForeignKey('division.id'), info={'label': "Division ID"}) #
    keykpi_id = dbpms.Column(dbpms.Integer, dbpms.ForeignKey('keykpi.id'), info={'label': "KPI ID"})  #
    # division = dbpms.relationship('Division', backref='postregister') #
    # keykpi = dbpms.relationship('Keykpi', backref='postregister')


class Post_Table(Table):
    id = Col("PostID")
    post_name = Col("Name")
    post_description = Col("Description")
    post_grade = Col("Post-Grade")
    post_type = Col("Post-Type")
    post_category = Col("Post-Category")
    classes = ['display compact']
    table_id = "Joblist"
    html_attrs = {"cellspacing": 0, "width": "100%"}

class Post_Table2(Post_Table):
    post_name = LinkCol("Post-Name", "pms_bp.selectplans", attr="post_name", url_kwargs=dict(id="id", jobtype="jobtype"))
    table_id = "Joblistselected"

class Post_registerForm(ModelForm):
    class Meta:
        model = Post_register

class Division(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.division']
    __tablename__ = "division"
    id = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    div_name = dbpms.Column(dbpms.String(200), info={'label': "Division Name"})
    div_description = dbpms.Column(dbpms.Text(200), info={'label': "Description"})
    postregister = dbpms.relationship('Post_register', backref='division')
    organisation_id = dbpms.Column(dbpms.Integer, dbpms.ForeignKey('organisation.id'))
    #organisation = dbpms.relationship('Organisation', backref='division')

class DivisionForm(ModelForm):
    class Meta:
        model = Division

class DocumentMaster(dbpms.Model):
    __tablename__ = 'document_master'

    Document_name = dbpms.Column(dbpms.String(200))
    Document_ID = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    Document_location = dbpms.Column(dbpms.String(300))
    Document_Group = dbpms.Column(dbpms.String(20))
    Document_SubGroup = dbpms.Column(dbpms.String(20))
    Owner_Name = dbpms.Column('Owner_Name', dbpms.String(50))
    Risk_Level = dbpms.Column(dbpms.Integer)
    Security_Level = dbpms.Column(dbpms.Integer)
    Document_Writer = dbpms.Column(dbpms.String(25))
    Document_Subdivision = dbpms.Column(dbpms.String(25))
    Document_Division = dbpms.Column(dbpms.String(25))
    Reference_Project = dbpms.Column(dbpms.String(20))
    Change_ID = dbpms.Column(dbpms.Float(asdecimal=True))
    Version = dbpms.Column(dbpms.String(1))
    Date_Created = dbpms.Column(dbpms.DateTime)
    Size = dbpms.Column(dbpms.Float(asdecimal=True))
    Date_Upload = dbpms.Column(dbpms.DateTime)
    Owner_ID = dbpms.Column(dbpms.String(50))
    Owner_Name = dbpms.Column(dbpms.String(100))
    Description = dbpms.Column(dbpms.String(200))
    Document_Purpose = dbpms.Column(dbpms.String(200))
    Date_Modified = dbpms.Column(dbpms.DateTime)
    Pwd = dbpms.Column(dbpms.String(128))
    Encrypt_Type = dbpms.Column(dbpms.String(3))
    Tot_Download = dbpms.Column(dbpms.Integer, info={'label': "Tot Download"})
    Tot_Read = dbpms.Column(dbpms.Integer, info={'label': "Tot Read"})
    #group_id = dbpms.Column(dbpms.Integer, dbpms.ForeignKey('group.id'), info={'label': "Group ID"})
    #group = dbpms.relationship('Group_primary', backref='documentmaster')
    #emailpri = dbpms.Column(dbpms.String(45), dbpms.ForeignKey('login.emailpri'), info={'label': "Owner ID"})
    jobtype = dbpms.Column(dbpms.String(20), info={'label': "JobType"})
    jobid = dbpms.Column(dbpms.Integer, info={'label': "TobID"})
    mainid = dbpms.Column(dbpms.Integer, info={'label': "MainID"})

class DocumentMaster_table(Table):
    document_name = LinkCol("Document Name", "app_tf.download", attr="Document_name", url_kwargs=dict(fn="Document_ID"))
    Date_Modified = Col("Date Modified")
    Owner_Name = Col("Owner Name")
    classes = ['display compact']
    table_id = "Joblist"
    html_attrs = {"cellspacing": 0, "width": "100%"}

class Document_master(dbpms.Model):
   # __table__ = dbpms.Model.metadata.tables['pms.documentmaster']
    __tablename__ = "documentmaster"
    document_name = dbpms.Column(dbpms.String(200), info={'label': "Doc name"})
    document_purpose = dbpms.Column(dbpms.String(200), info={'label': "Purpose"})
    description = dbpms.Column(dbpms.Text(200), info={'label': "Description"})
    security_level = dbpms.Column(dbpms.Integer, info={'label': "Security Level"})
    document_location = dbpms.Column(dbpms.String(300), info={'label': "Location"})
    document_group = dbpms.Column(dbpms.String(20), info={'label': "Group"})
    document_subGroup = dbpms.Column(dbpms.String(20), info={'label': "Document Subgroup"})
    owner_name = dbpms.Column(dbpms.String(50), info={'label': "Owner Name"})
    document_writer = dbpms.Column(dbpms.String(25), info={'label': "Doc Writer"})
    document_division = dbpms.Column(dbpms.String(25), info={'label': "Division"})
    document_subdivision = dbpms.Column(dbpms.String(25), info={'label': "Sub-Division"})
    version = dbpms.Column(dbpms.String(1), info={'label': "Version"})
    date_created = dbpms.Column(dbpms.DateTime, server_default=func.now(), info={'label': "Date Created"})
    size = dbpms.Column(dbpms.Integer, info={'label': "Size(kb)"})
    date_upload = dbpms.Column(dbpms.DateTime, info={'label': "Date Upload"})
    #owner_id= dbpms.Column(dbpms.String(50), info={'label': "Owner ID"})
    Document_ID = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    date_modified = dbpms.Column(dbpms.DateTime, info={'label': "Date Modified"})
    pwd = dbpms.Column(dbpms.String(128), info={'label': "Password"})
    encrypt_type = dbpms.Column(dbpms.String(3), info={'label': "EC Type"})
    tot_download = dbpms.Column(dbpms.Integer, info={'label': "Tot Download"})
    tot_read = dbpms.Column(dbpms.Integer, info={'label': "Tot Read"})
    group_id = dbpms.Column(dbpms.Integer, dbpms.ForeignKey('group.id'), info={'label': "Group ID"})
    #group = dbpms.relationship('Group_primary', backref='documentmaster')
    emailpri = dbpms.Column(dbpms.String(45), dbpms.ForeignKey('login.emailpri'), info={'label': "Owner ID"})
    jobtype = dbpms.Column(dbpms.String(20), info={'label': "JobType"})
    jobid = dbpms.Column(dbpms.Integer, info={'label': "TobID"})
    mainid = dbpms.Column(dbpms.Integer, info={'label': "MainID"})
    #login = dbpms.relationship('Login', backref='documentmaster')

class Document_table(Table):
    document_name = LinkCol("Document Name", "app_tf.download", attr="Document_ID", url_kwargs=dict(id="Document_ID"))
    date_modified = Col("Date Modified")
    Owner_name = Col("Owner Name")
    classes = ['display compact']
    table_id = "Joblist"
    html_attrs = {"cellspacing": 0, "width": "100%"}

class Document_masterForm(ModelForm):
    class Meta:
        model = Document_master

class Group_members(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.groupmembers']
    __tablename__ = "groupmembers"
    id = dbpms.Column(dbpms.Integer, primary_key=True, index=True)
    staff_authority = dbpms.Column(dbpms.String(2), info={'label': "Authority"})
    date_created = dbpms.Column(dbpms.DateTime, server_default=func.now(), info={'label': "Date Created"})
    member_status = dbpms.Column(dbpms.String(2), info={'label': "Member Status"})
    date_end = dbpms.Column(dbpms.DateTime, info={'label': "Member Ceased Date"})
    number_of_transaction = dbpms.Column(dbpms.Integer, info={'label': "Transaction Tot"})
    emailpri = dbpms.Column(dbpms.String(45), dbpms.ForeignKey('login.emailpri'), info={'label': "Member ID"}) #
    #login = dbpms.relationship('Login', backref='groupmembers')
    group_id = dbpms.Column(dbpms.Integer, dbpms.ForeignKey('group.id'), info={'label': "Group ID"}) #

class Group_membersForm(ModelForm):
    class Meta:
        model = Group_members

class Group_primary(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.group']
    __tablename__ = "group"
    id = dbpms.Column(dbpms.Integer, primary_key=True, index=True)
    group_name = dbpms.Column(dbpms.String(20), index=True)
    group_description = dbpms.Column(dbpms.Text(200), info={'label': "Description"})
    created_date = dbpms.Column(dbpms.DateTime, server_default=func.now(), info={'label': "Created Date"})
    active_status = dbpms.Column(dbpms.Integer, info={'label': "Active Status"})
    deleted_date = dbpms.Column(dbpms.DateTime, info={'label': "Delete Date"})
    # groupmembers = dbpms.relationship('Group_members', backref='group') #
    login_id = dbpms.Column(dbpms.String(45), dbpms.ForeignKey('login.emailpri'), info={'label': "Login ID"}) #
    #login = dbpms.relationship('Login', backref='group')
    # documentmaster = dbpms.relationship('Document_master', backref='group')
    # #emailpri = dbpms.Column(dbpms.String(45), dbpms.ForeignKey('login.emailpri'), info={'label': "Risk Category"})  #

class Group_primaryForm(ModelForm):
    class Meta:
        model = Group_primary

class Login(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.login']
    __tablename__ = "login"
    id = dbpms.Column(dbpms.Integer, primary_key=True)
    staff_id = dbpms.Column(dbpms.String(20), info={'label': "Staff ID"})
    date_register = dbpms.Column(dbpms.DateTime, server_default=func.now(), info={'label': "Date Register"})
    emailpri = dbpms.Column(dbpms.String(45), index=True, info={'label': "Email Primary"})
    emailsec = dbpms.Column(dbpms.String(45), info={'label': "Email Secondary"})
    password = dbpms.Column(dbpms.String(100), info={'label': "Password"})
    priviledgeid = dbpms.Column(dbpms.String(45), info={'label': "Priviledge ID"})
    ipaddress = dbpms.Column(dbpms.String(45), info={'label': "IP Address"})
    #postreg_id = dbpms.Column(dbpms.Integer, dbpms.ForeignKey('postregister.id'), info={'label': "Risk Category"}) #
    #competency = dbpms.relationship('Competency_register', backref='emailpri')
    #groupmembers = dbpms.relationship('Group_members', backref='emailpri') #
    #group = dbpms.relationship('Group_primary', backref='login') #
    #loginhistory = dbpms.relationship('Login_history', backref='login') #

class LoginForm(ModelForm):
    class Meta:
        model = Login

class LoginTable(Table):
    id = Col("ID")
    staff_id = Col("Staff ID")
    date_register = Col("Date Registered")
    emailpri = Col("LoginID")
    ipaddress = Col("Ip Address")
    classes = ['display compact']
    table_id = "Joblist"
    html_attrs = {"cellspacing":0 , "width":"100%"}

    def set_tr_attrs(self, id):
        return {'id': id}

class LoginTable2(LoginTable):
    table_id = "Joblistselected"

class Login_history(dbpms.Model):
    __table__ = dbpms.Model.metadata.tables['pms.login_history']

class Login_historyForm(ModelForm):
    class Meta:
        model = Login_history

class Organisation(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.organisation']
    __tablename__ = "organisation"
    id = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    organisation_name = dbpms.Column(dbpms.String(45), info={'label': "Organisation Name"})
    organisation_description = dbpms.Column(dbpms.Text(45), info={'label': "Description"})
    #postreg = dbpms.relationship('Division', backref='organisation')

class OrganisationForm(ModelForm):
    class Meta:
        model = Organisation

class Postlevel(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.postlevel']
    __tablename__ = "postlevel"
    id = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    post_level = dbpms.Column(dbpms.Integer, info={'label': "Post Level"})
    post_description = dbpms.Column(dbpms.Text, info={'label': "Description"})

class PostlevelForm(ModelForm):
    class Meta:
        model = Postlevel

class Securitylevel(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.securitylevel']
    __tablename__ = "securitylevel"
    id = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    security_Level = dbpms.Column(dbpms.String(50), info={'label': "Security Level"})
    security_description = dbpms.Column(dbpms.Text(200), info={'label': "Security Description"})

class SecuritylevelForm(ModelForm):
    class Meta:
        model = Securitylevel

class Docdialog(dbpms.Model):
    # __table__ = dbpms.Model.metadata.tables['pms.docdialog']
    __tablename__ = "docdialog"
    id = dbpms.Column(dbpms.Integer, primary_key=True)
    document_id = dbpms.Column(dbpms.String(200), info={'label': "Document ID"})
    dialog = dbpms.Column(dbpms.String(500), info={'label': "Dialog"})
    emailpri = dbpms.Column(dbpms.String(50), info={'label': "Login ID"})
    date_comment = dbpms.Column(dbpms.DateTime, server_default=func.now(), info={'label': "Date Comment"})

class DocdialogForm(ModelForm):
    class Meta:
        model = Docdialog

class Activitylevel(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.activitylevel']
    __tablename__ = "activitylevel"
    id = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    activity_level = dbpms.Column(dbpms.Integer, info={'label': "Activity Level"})
    activity_description = dbpms.Column(dbpms.Text, info={'label': "Description"})

class Staff_profile(dbpms.Model):
    #__table__ = dbpms.Model.metadata.tables['pms.staffprofile']
    __tablename__ = "staffprofile"

    id = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    first_name = dbpms.Column(dbpms.String(50), info={'label': "First Name"})
    last_name = dbpms.Column(dbpms.String(50), info={'label': "Last Name"})
    staff_id = dbpms.Column(dbpms.String(50), info={'label': "Staff ID"})
    phone = dbpms.Column(dbpms.String(50), info={'label': "Phone number"})
    homeaddress = dbpms.Column(dbpms.Text(500), info={'label': "Home Address"})
    officeaddress = dbpms.Column(dbpms.String(50), info={'label': "Office Address"})
    email= dbpms.Column(dbpms.String(50), info={'label': "Email"})
    post= dbpms.Column(dbpms.String(50), info={'label': "Post Name"})
    post_id = dbpms.Column(dbpms.String(50), info={'label': "Post ID"})
    salary = dbpms.Column(dbpms.String(50), info={'label': "Salary"})
    startdate = dbpms.Column(dbpms.String(50), info={'label': "Start Date Working"})
    enddate = dbpms.Column(dbpms.String(50), info={'label': "End Date Working"})
    grade = dbpms.Column(dbpms.String(50), info={'label': "Person Grade"})
    history = dbpms.Column(dbpms.String(50), info={'label': "History"})
    kpiid = dbpms.Column(dbpms.String(10), info={'label': "KPI ID"})
    instructionid = dbpms.Column(dbpms.String(10), info={'label': "Instruction ID"})
    jobdesid = dbpms.Column(dbpms.String(10), info={'label': "Job Desc ID"})
    trainingid = dbpms.Column(dbpms.String(10), info={'label': "Training ID"})
    auditid = dbpms.Column(dbpms.String(10), info={'label': "Audit ID"})
    riskid = dbpms.Column(dbpms.String(10), info={'label': "Risk ID"})
    isoid = dbpms.Column(dbpms.String(10), info={'label': "ISO ID"})

class Staff_profileForm:
    class Meta:
        model = Staff_profile

class Planprofile_register(dbpms.Model):
    __tablename__ = "planprofile"
    ID = dbpms.Column(dbpms.Integer, primary_key=True, unique=True)
    EmailPri = dbpms.Column(dbpms.String(45), index=True, info={'label': "Email Primary"})
    StaffID = dbpms.Column(dbpms.String(45), index=True, info={'label': "Staff ID"})
    MainID = dbpms.Column(dbpms.Integer, info={'label': "Main Work ID"})
    PlanID = dbpms.Column(dbpms.Integer, info={'label': "Plan ID"})
    DateCreated = dbpms.Column(dbpms.DateTime, server_default=func.now(), info={'label': "Date Created"})
    PlanType = dbpms.Column(dbpms.String(45), index=True, info={'label': "Plan Type"})
    Year = dbpms.Column(dbpms.String(4), info={'label': "Year"})
    Quarter = dbpms.Column(dbpms.String(4), info={'label': "Quarter"})
    StartDate= dbpms.Column(dbpms.String(50), info={'label': "Start Date"})
    EndDate= dbpms.Column(dbpms.String(50), info={'label': "End Date"})
    DocGroup=dbpms.Column(dbpms.String(45), index=True, info={'label': "Document Group"})

class Planprofile_table(Table):
    ID = LinkCol("ID","pms_bp.selectplans",attr="ID", url_kwargs=dict(id="ID"))
    EmailPri = Col("Login Email")
    PlanType = Col("Plan Type")
    MainID = Col("MainJob ID")
    PlanID = Col("Plan ID")
    DateCreated = Col("Date Created")
    table_id = "Joblist"

class Planprofile_Table2(Planprofile_table):
    table_id = "Joblistselected"

if __name__ == "__main__":
    app.run(debug=True)