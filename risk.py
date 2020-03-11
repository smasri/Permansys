## to list risk and show detail/Add detail/add mitigation
from flask import Blueprint
from flask import Flask, jsonify, render_template, request, flash, send_file, g, redirect, session, url_for
from pmsdb import *
risk = Blueprint('risk', __name__,
                    template_folder='templates',
                    static_folder='static')

@risk.route("/list_risk")
def list_risk():
    if session.get('Current_Topic') != 'Risk Management':
        session['Current_Topic'] = 'Risk Management'
    #List all the risks and add mitigation in respond file.
    data = Risk_register.query.all()
    dbpms.session.remove()
    col = Risk_register.__table__.columns.keys()
    return render_template("list_risk.html", data = data, col = col)

@risk.route('/showdetail', methods=('GET', 'POST'))
def showdetail():
    session['Rid'] = request.args.get('fn')
    jobtype = request.args.get("job")
    RR = Risk_register()
    rr = RR.query.filter_by(id=session['Rid']).first()
    dbpms.session.remove()
    preform = form_factory()
    form = preform(obj=rr)
    # get Mitigation details

    jobsel = Risk_respond.query.filter_by(jobid=session['Rid'], jobtype=jobtype).all()

    return render_template('job_edit.html', form=form, jobsel=jobsel, formaction="/risk/updatedetail", fn=session['Rid'], route='showdetail')

@risk.route('/addnew', methods=('GET', 'POST'))
def addnew():

    RR = Risk_register()
    preform = form_factory()
    form = preform(request.form, obj=RR)
    if request.method == "POST":
        form.populate_obj(RR)
        dbpms.session.add(RR)
        dbpms.session.commit()
        data = Risk_register.query.all()
        dbpms.session.remove()
        col = Risk_register.__table__.columns.keys()
        return render_template("list_risk.html", data=data, col=col)
    return render_template("job_add.html", form=form, formaction="/risk/addnew")

@risk.route('/updatedetail', methods=('GET', 'POST'))
def updatedetail():
    RR = Risk_register()
    rr = RR.query.filter_by(id=session['Rid']).first()
    dbpms.session.remove()
    preform = form_factory()
    form = preform(request.form, obj=rr)
    if request.method == "POST":
        form.populate_obj(rr)
        dbpms.session.merge(rr)
        dbpms.session.commit()
    return redirect('/risk/list_risk')

#route after mitigation_add
@risk.route('/addplaniso', methods=('GET', 'POST'))
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

        data = Risk_respond.query.filter_by(jobtype = jt, jobid = fn).all()
        dbpms.session.remove()
        col = Risk_respond.__table__.columns.keys()
        RR = Risk_register()
        rr = RR.query.filter_by(id=fn).first()
        preform = form_factory()
        form = preform(obj=rr)

        return render_template("job_edit.html", form=form, jobsel=data, col=col, formaction="/risk/updatedetail", fn=fn) #return to detail risk(form) / mitigationlist(data)
    return render_template("mitigation_add.html", form=form, jt=job, fn=fn, formaction="/risk/addplaniso",  tajuk =" Risk Mitigation Add")  # provide blank mitigation form

@risk.route('/editplaniso', methods=('GET', 'POST'))
def editplaniso():
    if request.method == "GET":
        mitID = request.args.get("mitID") #mitigation iD
        fn = request.args.get("fn") #Risk ID
        jt = request.args.get("job")
        RR = Risk_respond()
        rr = RR.query.filter_by(id=mitID).first()
        dbpms.session.remove()
        preform = mitigation_factory()
        form = preform(request.form, obj=rr)

        return render_template("mitigation_edit.html", form=form, jt=jt, fn=fn, mitID=mitID, formaction="/risk/editplaniso", tajuk ="Risk Mitigation edit" )  # provide filled mitigation form
    if request.method == "POST":
        fn = request.form.get("jobid")
        jt = request.form.get("jobtype")
        mitID = request.form.get("mitID")  # mitigation iD
        RR = Risk_respond()
        rr = RR.query.filter_by(id=mitID).first()
        dbpms.session.remove()
        preform = mitigation_factory()
        form = preform(request.form, obj=rr)
        form.populate_obj(rr)
        dbpms.session.merge(rr)
        dbpms.session.commit()

        data = Risk_respond.query.filter_by(jobtype=jt, jobid=fn).all()
        dbpms.session.remove()
        col = Risk_respond.__table__.columns.keys()
        RR = Risk_register
        rr = RR.query.filter_by(id=fn).first()
        preform = form_factory()
        form = preform(obj=rr)
        return render_template("job_edit.html", form=form, jobsel=data, col=col, formaction="/risk/updatedetail", fn=fn) #return to detail risk(form) / mitigationlist(data)
