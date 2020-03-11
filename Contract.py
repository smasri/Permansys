## to list risk and show detail/Add detail/add mitigation
from flask import Blueprint
from flask import Flask, jsonify, render_template, request, flash, send_file, g, redirect, session, url_for
from pmsdb import *
contract = Blueprint('contract', __name__,
                    template_folder='templates',
                    static_folder='static')

@contract.route("/list_contract")
def list_contract():
    if session.get('Current_Topic') != 'Contract Management':
        session['Current_Topic'] = 'Contract Management'

    data = contract_register.query.filter_by(login = session['ID_Login'])
    col = contract_register.__table__.columns.keys()
    return render_template("list_contract.html", data = data, col = col)

@contract.route('/showdetail', methods=('GET', 'POST'))
def showdetail():
    session['Rid'] = request.args.get('fn')
    jobtype = request.args.get("job")
    RR = contract_register()
    #RR.superior = dbpms.Column(dbpms.String(40), info={'label': "Supervisor",'choices': [('0',"Pse Choose one"),('1',"Financial"),('2',"Market & Customer"),('3',"Internal Business"),('4',"Learning and Innovation")]})
    rr = RR.query.filter_by(ID=session['Rid']).first()
    preform = contract_registerForm
    form = preform(obj=rr)
    doc =DocumentMaster
    RR = doc.query.filter_by(jobtype=jobtype,jobid=session['Rid'],mainid=session['Rid'])
    docTable = DocumentMaster_table(RR)


    return render_template('contract_edit.html', docTable=docTable, form=form, formaction="/contract/updatedetail", fn=session['Rid'], route='showdetail')

@contract.route('/addnew', methods=('GET', 'POST'))
def addnew():

    RR = contract_register()
    RR.login = session['ID_Login']
    preform = contract_registerForm
    form = preform(request.form, obj=RR)
    if request.method == "POST":
        form.populate_obj(RR)
        dbpms.session.add(RR)
        dbpms.session.commit()
        data = contract_register.query.filter_by(login = session['ID_Login'])
        col = contract_register.__table__.columns.keys()
        return render_template("list_contract.html", data=data, col=col)
    return render_template("contract_add.html", form=form, formaction="/contract/addnew")

@contract.route('/updatedetail', methods=('GET', 'POST'))
def updatedetail():
    RR = contract_register()
    rr = RR.query.filter_by(ID=session['Rid']).first()
    preform = contract_registerForm
    form = preform(request.form, obj=rr)
    if request.method == "POST":
        form.populate_obj(rr)
        dbpms.session.merge(rr)
        dbpms.session.commit()
    return redirect('/contract/list_contract')

