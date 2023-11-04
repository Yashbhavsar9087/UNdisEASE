from flask import Flask
import smtplib
from flask import Flask,render_template,request,redirect,flash
from bs4 import BeautifulSoup
import requests
from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm
from app.base.models import User, Appoinment

from app.base.util import verify_pass

@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/send_link')
def send_link():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    fromaddr = "yashjbhavsar2001@gmail.com"
    toaddr = "jay.munjapara@somaiya.edu"

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = " Appoinment  "

    body = "Google Meet : https://meet.google.com/xeu-oswr-foi  "
    msg.attach(MIMEText(body,'plain'))

    server = smtplib.SMTP('smtp.gmail.com', port=587)
    server.starttls()
    server.login(fromaddr, "uvbjgxwnvomdpxhg")

    text = msg.as_string()
    server.sendmail(fromaddr,toaddr,text)
    server.quit()

    return redirect(url_for('base_blueprint.schedule'))

@blueprint.route('/send_prescription')
def send_prescription():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    fromaddr = "yashjbhavsar2001@gmail.com"
    toaddr = "jay.munjapara@somaiya.edu"

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = " Prescription - Secret key = evathon "

    body = "Prescription : Paracetamol 500mg 2 times a day after lunch and dinner.  Next Visit : 2 weeks later.  "

    msg.attach(MIMEText(body,'plain'))

    server = smtplib.SMTP('smtp.gmail.com', port=587)
    server.starttls()
    server.login(fromaddr, "uvbjgxwnvomdpxhg")

    text = msg.as_string()
    server.sendmail(fromaddr,toaddr,text)
    server.quit()

    return redirect(url_for('base_blueprint.doctor_login'))

@blueprint.route('/doctor_login')
def doctor_login():
    
    return render_template('doctor.html',)
    # return render_template( 'doctor.html')

@blueprint.route('/schedule')
def schedule():
    import sqlite3
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    cursor1 = cur.execute('SELECT user_name,user_num,appointment_for,appointment_description,date,time,duration FROM Appoinment')
    x = cursor1.fetchall()

    return render_template('schedule.html', items=x)
    
@blueprint.route('/prescription_form')
def prescription_form():
    
    return render_template('prescription_form.html',)


@blueprint.route('/add_appoinment', methods=['GET', 'POST'])
def add_appoinment():
    # login_form = LoginForm(request.form)
    # create_account_form = CreateAccountForm(request.form)
    # if 'register' in request.form:

    #     username  = request.form['username']
    #     email     = request.form['email'   ]

    #     # Check usename exists
    #     user = User.query.filter_by(username=username).first()
    #     if user:
    #         return render_template( 'accounts/register.html', 
    #                                 msg='Username already registered',
    #                                 success=False,
    #                                 form=create_account_form)

    #     # Check email exists
    #     user = User.query.filter_by(email=email).first()
    #     if user:
    #         return render_template( 'accounts/register.html', 
    #                                 msg='Email already registered', 
    #                                 success=False,
    #                                 form=create_account_form)

    #     # else we can create the user
    if request.form:
        print(request.form)
        appoinment = Appoinment(**request.form)
        # print(appoinment)
        db.session.add(appoinment)

        db.session.commit()
        return render_template( 'index.html')
    return render_template( 'appoinment.html')



# @blueprint.route('/add_appoinment', methods=['GET', 'POST'])
# def add_appoinment():
#         flash("you are successfuly logged in")
#         return render_template( 'index.html')

## Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        
        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()
        
        # Check the password
        if user and verify_pass( password, user.password):
            login_user(user)
            if user.category == 'Doctor':
                return redirect(url_for('base_blueprint.doctor_login'))
            else :
                return redirect(url_for('base_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template( 'accounts/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html',
                                form=login_form)
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username  = request.form['username']
        email     = request.form['email'   ]

        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template( 'accounts/register.html', 
                                    msg='Username already registered',
                                    success=False,
                                    form=create_account_form)

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template( 'accounts/register.html', 
                                    msg='Email already registered', 
                                    success=False,
                                    form=create_account_form)

        # else we can create the user
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template( 'accounts/register.html', 
                                msg='User created please <a href="/login">login</a>', 
                                success=True,
                                form=create_account_form)

    else:
        return render_template( 'accounts/register.html', form=create_account_form)

@blueprint.route('/analysis', methods = ['GET', 'POST'])
def analysis():
        
    source = requests.get('https://www.speakrj.com/audit/report/ashchanchlani/twitter').text

    soup = BeautifulSoup(source,'lxml')
    article = soup.find('div',class_='d-flex')
    head = article.find_all('p', class_='report-header-number')
    tw=[]
    for i in head:
        x = i.text
        if " " in x:
            x=x.split()[0]
        tw.append(x)
    return render_template('doctor.html', tw = tw, segment='index',)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500
