## to list risk and show detail/Add detail/add mitigation
from flask import Blueprint
from flask import Flask, jsonify, render_template, request, flash, send_file, g, redirect, session, url_for
from pmsdb import *
post = Blueprint('post', __name__,
                    template_folder='templates',
                    static_folder='static')

@post.route("/list_Post")
def list_Post():
    if session.get('Current_Topic') != 'Post Management':
        session['Current_Topic'] = 'Post Management'
    #List all the risks and add mitigation in respond file.
    data = Post_register.query.all()
    col = Post_register.__table__.columns.keys()
    return render_template("list_post.html", data = data, col = col)

@post.route('/showdetail', methods=('GET', 'POST'))
def showdetail():
    session['Rid'] = request.args.get('fn')
    jobtype = request.args.get("job")
    RR = Post_register()
    rr = RR.query.filter_by(id=session['Rid']).first()
    preform = Post_registerForm
    form = preform(obj=rr)

    # get Mitigation details

    jobsel = Risk_respond.query.filter_by(jobid=session['Rid'], jobtype=jobtype).all()

    return render_template('post_edit.html', form=form, jobsel=jobsel, formaction="/post/updatedetail", fn=session['Rid'], route='showdetail')

@post.route('/addnew', methods=('GET', 'POST'))
def addnew():

    RR = Post_register()
    preform = Post_registerForm
    form = preform(request.form, obj=RR)
    if request.method == "POST":
        form.populate_obj(RR)
        dbpms.session.add(RR)
        dbpms.session.commit()
        data = Post_register.query.all()
        col = Post_register.__table__.columns.keys()
        return render_template("list_post.html", data=data, col=col)
    return render_template("post_add.html", form=form, formaction="/post/addnew")

@post.route('/updatedetail', methods=('GET', 'POST'))
def updatedetail():
    RR = Post_register()
    rr = RR.query.filter_by(id=session['Rid']).first()
    preform = Post_registerForm
    form = preform(request.form, obj=rr)
    if request.method == "POST":
        form.populate_obj(rr)
        dbpms.session.merge(rr)
        dbpms.session.commit()
    return redirect('/post/list_Post')

#route after mitigation_add
@post.route('/addplaniso', methods=('GET', 'POST'))
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
        RR = Post_register()
        rr = RR.query.filter_by(id=fn).first()
        preform = Post_registerForm
        form = preform(obj=rr)

        return render_template("post_edit.html", form=form, jobsel=data, col=col, formaction="/post/updatedetail", fn=fn) #return to detail risk(form) / mitigationlist(data)
    return render_template("mitigation_add.html", form=form, jt=job, fn=fn, formaction="/post/addplaniso",  tajuk ="Post Details Add")  # provide blank mitigation form

@post.route('/editplaniso', methods=('GET', 'POST'))
def editplaniso():
    if request.method == "GET":
        mitID = request.args.get("mitID") #mitigation iD
        fn = request.args.get("fn") #Risk ID
        jt = request.args.get("job")
        RR = Risk_respond()
        rr = RR.query.filter_by(id=mitID).first()
        preform = mitigation_factory()
        form = preform(request.form, obj=rr)

        return render_template("mitigation_edit.html", form=form, jt=jt, fn=fn, mitID=mitID, formaction="/post/editplaniso",  tajuk ="Post Details edit" )  # provide filled mitigation form
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
        RR = Post_register
        rr = RR.query.filter_by(id=fn).first()
        preform = Post_registerForm
        form = preform(obj=rr)
        return render_template("post_edit.html", form=form, jobsel=data, col=col, formaction="/post/updatedetail", fn=fn) #return to detail risk(form) / mitigationlist(data)
