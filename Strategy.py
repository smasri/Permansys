## to list risk and show detail/Add detail/add mitigation
from flask import Blueprint
from flask import Flask, jsonify, render_template, request, flash, send_file, g, redirect, session, url_for
from pmsdb import *
Strategy = Blueprint('Strategy', __name__,
                    template_folder='templates',
                    static_folder='static')

@Strategy.route("/list_Strategy")
def list_Strategy():
    if session.get('Current_Topic') != 'Strategy Management':
        session['Current_Topic'] = 'Strategy Management'
    #List all the risks and add mitigation in respond file.
    data = Strategy_register.query.all()
    table = Strategy_Table2(data)
    col = Strategy_register.__table__.columns.keys()
    return render_template("list_Strategy.html", table=table,  data = data, col = col)

@Strategy.route('/showdetail', methods=('GET', 'POST'))
def showdetail():
    session['Rid'] = request.args.get('fn')
    jobtype = request.args.get("job")
    RR = Strategy_register()
    rr = RR.query.filter_by(id=session['Rid']).first()
    preform = Strategy_registerForm
    form = preform(obj=rr)

    # get Mitigation details

    jobsel = Risk_respond.query.filter_by(jobid=session['Rid'], jobtype=jobtype).all()

    return render_template('Strategy_edit.html', form=form, jobsel=jobsel, formaction="/Strategy/updatedetail", fn=session['Rid'], route='showdetail')

@Strategy.route('/addnew', methods=('GET', 'POST'))
def addnew():

    RR = Strategy_register()
    preform = Strategy_registerForm
    form = preform(request.form, obj=RR)
    if request.method == "POST":
        form.populate_obj(RR)
        dbpms.session.add(RR)
        dbpms.session.commit()
        data = Strategy_register.query.all()
        col = Strategy_register.__table__.columns.keys()
        return render_template("list_Strategy.html", data=data, col=col)
    return render_template("Strategy_add.html", form=form, formaction="/Strategy/addnew")

@Strategy.route('/updatedetail', methods=('GET', 'POST'))
def updatedetail():
    RR = Strategy_register()
    rr = RR.query.filter_by(id=session['Rid']).first()
    preform = Strategy_registerForm
    form = preform(request.form, obj=rr)
    if request.method == "POST":
        form.populate_obj(rr)
        dbpms.session.merge(rr)
        dbpms.session.commit()
    return redirect('/Strategy/list_Strategy')

#route after mitigation_add
@Strategy.route('/addplaniso', methods=('GET', 'POST'))
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
        RR = Strategy_register()
        rr = RR.query.filter_by(id=fn).first()
        preform = Strategy_registerForm
        form = preform(obj=rr)

        return render_template("Strategy_edit.html", form=form, jobsel=data, col=col, formaction="/Strategy/updatedetail", fn=fn) #return to detail risk(form) / mitigationlist(data)
    return render_template("mitigation_add.html", form=form, jt=job, fn=fn, formaction="/Strategy/addplaniso",  tajuk ="Strategy Details Add")  # provide blank mitigation form

@Strategy.route('/editplaniso', methods=('GET', 'POST'))
def editplaniso():
    if request.method == "GET":
        mitID = request.args.get("mitID") #mitigation iD
        fn = request.args.get("fn") #Risk ID
        jt = request.args.get("job")
        RR = Risk_respond()
        rr = RR.query.filter_by(id=mitID).first()
        preform = mitigation_factory()
        form = preform(request.form, obj=rr)

        return render_template("mitigation_edit.html", form=form, jt=jt, fn=fn, mitID=mitID, formaction="/Strategy/editplaniso",  tajuk ="Strategy Details edit" )  # provide filled mitigation form
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
        RR = Strategy_register
        rr = RR.query.filter_by(id=fn).first()
        preform = Strategy_registerForm
        form = preform(obj=rr)
        return render_template("Strategy_edit.html", form=form, jobsel=data, col=col, formaction="/Strategy/updatedetail", fn=fn) #return to detail risk(form) / mitigationlist(data)
