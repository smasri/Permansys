## to list risk and show detail/Add detail/add mitigation
from flask import Blueprint
from flask import Flask, jsonify, render_template, request, flash, send_file, g, redirect, session, url_for
from pmsdb import *
trn = Blueprint('trn', __name__,
                    template_folder='templates',
                    static_folder='static')

@trn.route("/list_training")
def list_training():
    if session.get('Current_Topic') != 'Training Management':
        session['Current_Topic'] = 'Training Management'
    #List all the risks and add mitigation in respond file.
    data = Training_register.query.all()
    col = Training_register.__table__.columns.keys()
    return render_template("list_training.html", data = data, col = col)

@trn.route('/showdetail', methods=('GET', 'POST'))
def showdetail():
    session['Rid'] = request.args.get('fn')
    jobtype = request.args.get("job")
    RR = Training_register()
    rr = RR.query.filter_by(id=session['Rid']).first()
    preform = Training_registerForm
    form = preform(obj=rr)

    # get Mitigation details

    jobsel = Risk_respond.query.filter_by(jobid=session['Rid'], jobtype=jobtype).all()

    return render_template('training_edit.html', form=form, jobsel=jobsel, formaction="/trn/updatedetail", fn=session['Rid'], route='showdetail')

@trn.route('/addnew', methods=('GET', 'POST'))
def addnew():

    RR = Training_register()
    preform = Training_registerForm
    form = preform(request.form, obj=RR)
    if request.method == "POST":
        form.populate_obj(RR)
        dbpms.session.add(RR)
        dbpms.session.commit()
        data = Training_register.query.all()
        col = Training_register.__table__.columns.keys()
        return render_template("list_training.html", data=data, col=col)
    return render_template("training_add.html", form=form, formaction="/trn/addnew")

@trn.route('/updatedetail', methods=('GET', 'POST'))
def updatedetail():
    RR = Training_register()
    rr = RR.query.filter_by(id=session['Rid']).first()
    preform = Training_registerForm
    form = preform(request.form, obj=rr)
    if request.method == "POST":
        form.populate_obj(rr)
        dbpms.session.merge(rr)
        dbpms.session.commit()
    return redirect('/trn/list_training')

#route after mitigation_add
@trn.route('/addplaniso', methods=('GET', 'POST'))
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
        RR = Training_register()
        rr = RR.query.filter_by(id=fn).first()
        preform = Training_registerForm
        form = preform(obj=rr)

        return render_template("training_edit.html", form=form, jobsel=data, col=col, formaction="/trn/updatedetail", fn=fn) #return to detail risk(form) / mitigationlist(data)
    return render_template("mitigation_add.html", form=form, jt=job, fn=fn, formaction="/trn/addplaniso",  tajuk ="Training Details Add")  # provide blank mitigation form

@trn.route('/editplaniso', methods=('GET', 'POST'))
def editplaniso():
    if request.method == "GET":
        mitID = request.args.get("mitID") #mitigation iD
        fn = request.args.get("fn") #Risk ID
        jt = request.args.get("job")
        RR = Risk_respond()
        rr = RR.query.filter_by(id=mitID).first()
        preform = mitigation_factory()
        form = preform(request.form, obj=rr)

        return render_template("mitigation_edit.html", form=form, jt=jt, fn=fn, mitID=mitID, formaction="/trn/editplaniso", tajuk ="Training Details edit")  # provide filled mitigation form
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
        RR = Training_register
        rr = RR.query.filter_by(id=fn).first()
        preform = Training_registerForm
        form = preform(obj=rr)
        return render_template("training_edit.html", form=form, jobsel=data, col=col, formaction="/trn/updatedetail", fn=fn) #return to detail risk(form) / mitigationlist(data)
