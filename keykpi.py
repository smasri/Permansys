## to list risk and show detail/Add detail/add mitigation
from flask import Blueprint
from flask import Flask, jsonify, render_template, request, flash, send_file, g, redirect, session, url_for
from pmsdb import *
kpi = Blueprint('kpi', __name__,
                    template_folder='templates',
                    static_folder='static')

@kpi.route("/list_kpi")
def list_kpi():
    if session.get('Current_Topic') != 'KPI Management':
        session['Current_Topic'] = 'KPI Management'
    #List all the risks and add mitigation in respond file.
    data = Keykpi_register.query.all()
    col = Keykpi_register.__table__.columns.keys()
    return render_template("list_kpi.html", data = data, col = col)

@kpi.route('/showdetail', methods=('GET', 'POST'))
def showdetail():
    session['Rid'] = request.args.get('fn')
    jobtype = request.args.get("job")
    RR = Keykpi_register()
    rr = RR.query.filter_by(id=session['Rid']).first()
    preform = Keykpi_registerForm
    form = preform(obj=rr)

    # get Mitigation details

    jobsel = Risk_respond.query.filter_by(jobid=session['Rid'], jobtype=jobtype).all()

    return render_template('kpi_edit.html', form=form, jobsel=jobsel, formaction="/kpi/updatedetail", \
                           fn=session['Rid'], route='showdetail', tajuk = "Manage KPI-edit", tajuk2="KPI Breakdown details", sub1 ="Sub KPI")

@kpi.route('/addnew', methods=('GET', 'POST'))
def addnew():

    RR = Keykpi_register()
    preform = Keykpi_registerForm
    form = preform(request.form, obj=RR)
    if request.method == "POST":
        form.populate_obj(RR)
        dbpms.session.add(RR)
        dbpms.session.commit()
        data = Keykpi_register.query.all()
        col = Keykpi_register.__table__.columns.keys()
        return render_template("list_kpi.html", data=data, col=col)
    return render_template("kpi_add.html", form=form, formaction="/kpi/addnew",tajuk = "Manage KPI-add", tajuk2="KPI Breakdown details", sub1 ="Sub KPI")

@kpi.route('/updatedetail', methods=('GET', 'POST'))
def updatedetail():
    RR = Keykpi_register()
    rr = RR.query.filter_by(id=session['Rid']).first()
    preform = Keykpi_registerForm
    form = preform(request.form, obj=rr)
    if request.method == "POST":
        form.populate_obj(rr)
        dbpms.session.merge(rr)
        dbpms.session.commit()
    return redirect('/kpi/list_kpi')

#route after mitigation_add
@kpi.route('/addplaniso', methods=('GET', 'POST'))
def addplaniso():

    fn = request.args.get("fn")
    job = request.args.get("job")
    rr = Risk_respond()
    preform = mitigation_factory()
    form = preform(request.form, obj=rr)

    if request.method == "POST":
        fn = request.form.get("jobid")
        jt = request.form.get("jobtype")
        form.populate_obj(rr)
        dbpms.session.add(rr)
        dbpms.session.commit()

        data = Risk_respond.query.filter_by(jobtype=jt, jobid=fn).all()
        col = Risk_respond.__table__.columns.keys()
        RR = Keykpi_register()
        rr = RR.query.filter_by(id=fn).first()
        preform = Keykpi_registerForm
        form = preform(obj=rr)

        return render_template("kpi_edit.html", form=form, jobsel=data, col=col, formaction="/kpi/updatedetail", \
                               fn=fn, tajuk = "Manage KPI-edit", tajuk2="KPI Breakdown details", sub1 ="Sub KPI") #return to detail risk(form) / mitigationlist(data)
    return render_template("mitigation_add.html", form=form, jt=job, fn=fn, formaction="/kpi/addplaniso",  tajuk ="KPI Details Add")  # provide blank mitigation form

@kpi.route('/editplaniso', methods=('GET', 'POST'))
def editplaniso():
    if request.method == "GET":
        mitID = request.args.get("mitID") #mitigation iD
        fn = request.args.get("fn") #Risk ID
        jt = request.args.get("job")
        RR = Risk_respond()
        rr = RR.query.filter_by(id=mitID).first()
        preform = mitigation_factory()
        form = preform(request.form, obj=rr)

        return render_template("mitigation_edit.html", form=form, jt=jt, fn=fn, mitID=mitID, formaction="/kpi/editplaniso",  tajuk ="KPI Details edit" )  # provide filled mitigation form
    if request.method == "POST":
        fn = request.form.get("jobid")
        jt = request.form.get("jobtype")
        mitID = request.form.get("mitID")  # mitigation iD
        RR = Risk_respond()
        rr = RR.query.filter_by(id=mitID).first()
        preform = mitigation_factory()
        form = preform(request.form, obj=rr)
        form.populate_obj(rr)
        dbpms.session.merge(rr)
        dbpms.session.commit()

        data = Risk_respond.query.filter_by(jobtype = jt, jobid = fn).all()
        col = Risk_respond.__table__.columns.keys()
        RR = Keykpi_register
        rr = RR.query.filter_by(id=fn).first()
        preform = Keykpi_registerForm
        form = preform(obj=rr)
        return render_template("kpi_edit.html", form=form, jobsel=data, col=col, formaction="/kpi/updatedetail", fn=fn, tajuk = "Manage KPI-edit", tajuk2="KPI Breakdown details", sub1 ="Sub KPI") #return to detail risk(form) / mitigationlist(data)
