## to list risk and show detail/Add detail/add mitigation
from flask import Blueprint
from flask import Flask, jsonify, render_template, request, flash, send_file, g, redirect, session, url_for
from pmsdb import *
job = Blueprint('job', __name__,
                    template_folder='templates',
                    static_folder='static')

@job.route("/list_JOB")
def list_JOB():
    if session.get('Current_Topic') != 'Job Description Management':
        session['Current_Topic'] = 'Job Description Management'
    #List all the risks and add mitigation in respond file.
    data = Job_description.query.all()
    col = Job_description.__table__.columns.keys()
    return render_template("list_JOB.html", data = data, col = col)

@job.route('/showdetail', methods=('GET', 'POST'))
def showdetail():
    session['Rid'] = request.args.get('fn')
    jobtype = request.args.get("job")
    RR = Job_description()
    rr = RR.query.filter_by(id=session['Rid']).first()
    preform = Job_descriptionForm
    form = preform(obj=rr)

    # get Mitigation details

    jobsel = Risk_respond.query.filter_by(jobid=session['Rid'], jobtype=jobtype).all()

    return render_template('Jobd_edit.html', form=form, jobsel=jobsel, formaction="/job/updatedetail", fn=session['Rid'], route='showdetail')

@job.route('/addnew', methods=('GET', 'POST'))
def addnew():

    RR = Job_description()
    preform = Job_descriptionForm
    form = preform(request.form, obj=RR)
    if request.method == "POST":
        form.populate_obj(RR)
        dbpms.session.add(RR)
        dbpms.session.commit()
        data = Job_description.query.all()
        col = Job_description.__table__.columns.keys()
        return render_template("list_ISO.html", data=data, col=col)
    return render_template("jobd_add.html", form=form, formaction="/job/addnew")

@job.route('/updatedetail', methods=('GET', 'POST'))
def updatedetail():
    RR = Job_description()
    rr = RR.query.filter_by(id=session['Rid']).first()
    preform = Job_descriptionForm
    form = preform(request.form, obj=rr)
    if request.method == "POST":
        form.populate_obj(rr)
        dbpms.session.merge(rr)
        dbpms.session.commit()
    return redirect('/job/list_JOB')

#route after mitigation_add
@job.route('/addplaniso', methods=('GET', 'POST'))
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
        RR = Job_description()
        rr = RR.query.filter_by(id=fn).first()
        preform = Job_descriptionForm
        form = preform(obj=rr)

        return render_template("jobd_edit.html", form=form, jobsel=data, col=col, formaction="/job/updatedetail", fn=fn) #return to detail risk(form) / mitigationlist(data)
    return render_template("mitigation_add.html", form=form, jt=job, fn=fn, formaction="/job/addplaniso",  tajuk ="Job Description Details Add")  # provide blank mitigation form

@job.route('/editplaniso', methods=('GET', 'POST'))
def editplaniso():
    if request.method == "GET":
        mitID = request.args.get("mitID") #mitigation iD
        fn = request.args.get("fn") #Risk ID
        jt = request.args.get("job")
        RR = Risk_respond()
        rr = RR.query.filter_by(id=mitID).first()
        preform = mitigation_factory()
        form = preform(request.form, obj=rr)

        return render_template("mitigation_edit.html", form=form, jt=jt, fn=fn, mitID=mitID, formaction="/job/editplaniso",  tajuk ="Job Description Details Edit" )  # provide filled mitigation form
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
        RR = Job_description
        rr = RR.query.filter_by(id=fn).first()
        preform = Job_descriptionForm
        form = preform(obj=rr)
        return render_template("jobd_edit.html", form=form, jobsel=data, col=col, formaction="/job/updatedetail", fn=fn) #return to detail risk(form) / mitigationlist(data)
