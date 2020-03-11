## to list risk and show detail/Add detail/add mitigation
from flask import Blueprint
from flask import Flask, jsonify, render_template, request, flash, send_file, g, redirect, session, url_for
from pmsdb import *
comt = Blueprint('comt', __name__,
                    template_folder='templates',
                    static_folder='static')


@comt.route("/list_comt")
def list_comt():
    if session.get('Current_Topic') != 'Competency Management':
        session['Current_Topic'] = 'Competency Management'
    #List all the risks and add mitigation in respond file.
    data = Competency_register.query.all()
    col = Competency_register.__table__.columns.keys()
    return render_template("list_comt.html", data = data, col = col)

@comt.route('/showdetail', methods=('GET', 'POST'))
def showdetail():
    session['Rid'] = request.args.get('fn')
    jobtype = request.args.get("job")
    RR = Competency_register()
    rr = RR.query.filter_by(id=session['Rid']).first()
    preform = Competency_registerForm
    form = preform(obj=rr)

    # get Mitigation details

    jobsel = Risk_respond.query.filter_by(jobid=session['Rid'], jobtype=jobtype).all()

    return render_template('comt_edit.html', form=form, jobsel=jobsel, formaction="/comt/updatedetail", fn=session['Rid'], route='showdetail')

@comt.route('/addnew', methods=('GET', 'POST'))
def addnew():

    RR = Competency_register()
    preform = Competency_registerForm
    form = preform(request.form, obj=RR)
    if request.method == "POST":
        form.populate_obj(RR)
        dbpms.session.add(RR)
        dbpms.session.commit()
        data = Competency_register.query.all()
        col = Competency_register.__table__.columns.keys()
        return render_template("list_comt.html", data=data, col=col)
    return render_template("comt_add.html", form=form, formaction="/comt/addnew")

@comt.route('/updatedetail', methods=('GET', 'POST'))
def updatedetail():
    RR = Competency_register()
    rr = RR.query.filter_by(id=session['Rid']).first()
    preform = Competency_registerForm
    form = preform(request.form, obj=rr)
    if request.method == "POST":
        form.populate_obj(rr)
        dbpms.session.merge(rr)
        dbpms.session.commit()
    return redirect('/comt/list_comt')

#route after mitigation_add
@comt.route('/addplaniso', methods=('GET', 'POST'))
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
        RR = Competency_register()
        rr = RR.query.filter_by(id=fn).first()
        preform = Competency_registerForm
        form = preform(obj=rr)

        return render_template("comt_edit.html", form=form, jobsel=data, col=col, formaction="/comt/updatedetail", fn=fn) #return to detail risk(form) / mitigationlist(data)
    return render_template("mitigation_add.html", form=form, jt=job, fn=fn, formaction="/comt/addplaniso",  tajuk ="Competency Details Add")  # provide blank mitigation form

@comt.route('/editplaniso', methods=('GET', 'POST'))
def editplaniso():
    if request.method == "GET":
        mitID = request.args.get("mitID") #mitigation iD
        fn = request.args.get("fn") #Risk ID
        jt = request.args.get("job")
        RR = Risk_respond()
        rr = RR.query.filter_by(id=mitID).first()
        preform = mitigation_factory()
        form = preform(request.form, obj=rr)

        return render_template("mitigation_edit.html", form=form, jt=jt, fn=fn, mitID=mitID, formaction="/comt/editplaniso",  tajuk ="Competency Details edit" )  # provide filled mitigation form
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
        RR = Competency_register
        rr = RR.query.filter_by(id=fn).first()
        preform = Competency_registerForm
        form = preform(obj=rr)
        return render_template("comt_edit.html", form=form, jobsel=data, col=col, formaction="/comt/updatedetail", fn=fn) #return to detail risk(form) / mitigationlist(data)
