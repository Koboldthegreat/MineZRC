from flask import request, session, g, redirect, url_for, \
                abort, render_template, flash
from contextlib import closing
import minecraft_status

from flask.ext.mongoengine.wtf import model_form

import os.path

from os import listdir
import random


from mcflask.models import User, Server, staffmembers, servers, Post
from mcflask import app
from mcflask.functions import geturl
from mcflask.auth import LoginForm, RegisterForm, userEditForm

from flask.ext.wtf import Form

from mcflask.auth import requires_admin




def getUsers(type, mcname = None):
    if type == "staff":
        users = User.objects(is_staff = True)
        return users
    elif type == "username":
        user = User.objects(mcname = mcname)
        return user

def getServers():
    servers = Server.objects.all()
    return servers


def getStatus():
    status = minecraft_status.GetMCStatus(app.config["MCURL"])
    return status

def printstatus():
    status = getStatus()
    if status[0]:
        message = ['Server is online']
        message.append('MOTD is: %s' % status[1])
        message.append('Currently %s/%s players online' % (status[2], status[3]))
        return str(message)

    else:
        return 'Server is offline'

@app.route("/")
def home():
    loginform = LoginForm()
    status = getStatus()
    if status[0]:
          barWidth = int(status[2]) / int(status[3]) * 100
    else:
          barWidth = False
    backgroundlist = listdir(geturl('static/img/servers'))
    backgroundurl = "/static/img/servers/" + random.choice(backgroundlist)

    #get staff members
    staffmembers = getUsers('staff')

    posts = Post.objects.all()

    return render_template('homepage.html', status = status, barWidth = barWidth, moderators = staffmembers, background = backgroundurl, page = 'home', loginform = loginform, posts = posts )

@app.route('/post/<title>')
def viewPost(title):

    backgroundlist = listdir(geturl('static/img/servers'))
    backgroundurl = "/static/img/servers/" + random.choice(backgroundlist)

    post = Post.objects.get_or_404(title = title)
    loginform = LoginForm()
    return render_template('post.html', loginform = loginform, post = post, background = backgroundurl)

@app.route('/user/<username>')
def viewer(username):

    player = User.objects.get(mcname = username.lower())
    return render_template('viewer.html', player = player)


@app.route('/play')
def play():
    loginform = LoginForm()
    servers = getServers()
    return render_template('play.html', servers = servers, page = 'play', loginform = loginform)

@app.route("/forum")
def forum():
    loginform = LoginForm()
    return render_template("comingsoon.html", loginform = loginform)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    loginform = LoginForm()
    registerform = RegisterForm()
    if request.method == 'POST':
        if registerform.validate_on_submit():
            flash(u'Successfully created user: %s. Account confirmation link has been sent to your mail.' % registerform.username.data, 'success')
            return redirect(url_for('home'))
    backgroundlist = listdir(geturl('static/img/servers'))
    backgroundurl = "/static/img/servers/" + random.choice(backgroundlist)
    return render_template("register.html", loginform = loginform, registerform = registerform, background = backgroundurl)

@app.route('/user/edit/<mcname>' , methods = ['GET', 'POST'])
def userEdit(mcname):

    if session['usermcname'] == mcname or requires_admin:
        try:
            user = User.objects.get(mcname = mcname)
        except:
            flash(u"User doesn't exist!", "warning")
            return redirect(url_for('home'))
        loginform = LoginForm()
        form = userEditForm()
        if request.method == 'POST':
            if form.validate(user = user):
                flash(u'Successfully edited user: %s' % user.mcname, 'success')
                return redirect(url_for('home'))
        backgroundlist = listdir(geturl('static/img/servers'))
        backgroundurl = "/static/img/servers/" + random.choice(backgroundlist)
        return render_template("useredit.html", loginform = loginform, form = form, background = backgroundurl, user=user)
    else:
        flash(u"You don't have permission to edit this account", 'danger')
        return redirect(url_for('home'))


@app.route('/confirm/<user>/<confkey>')
def confirm(user, confkey):
    loginform = LoginForm()
    user = User.objects.get(mcname = user)
    print(user)
    if user.confkey == confkey and not user.confirmed:
        user.confirmed = True
        flash(u"Acount confirmed! You're ready for total epicness in the MineZRC community!!", 'success')
        user.save()
        session['usermcname'] = user.mcname
    elif user.confirmed:
        flash(u"User is already confirmed!", 'warning')
    else:
        flash(u"Something went wrong!! Try to recreate your account!", 'warning')
    return redirect(url_for('home'))



@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        loginform = LoginForm()
        if loginform.validate_on_submit():
            if not loginform.confirmed:
                flash('User not confirmed yet. Please open the confirmation link in your mail.', 'warning')
            else:

                flash(u'Logged in as %s' % loginform.user.mcname, 'success')
                session['usermcname'] = loginform.user.mcname
                session['panel'] = loginform.user
        else:
            flash(u'Invalid username or password', 'error')
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('usermcname', None)
    session.pop('panel', False)
    flash(u'You have been succesfully logged out' , 'succes')
    return redirect(url_for('home'))
