from functools import wraps
from flask import request, Response, redirect, flash, session
from flask.ext.wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from mcflask.models import User, addUser

from mcflask.encrypt import encryptPassword, checkPassword

from mcflask.mail import sendMail

from mcflask import debug

import os,binascii


def requires_admin():
    if not session.get('usermcname'):
        return False
    user = User.objects.get(mcname = session['usermcname'])
    if user.ranking == 'owner' or user.ranking == 'admin' or user.ranking == 'webdeveloper':
        return True


class LoginForm(Form):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        try:

            user = User.objects.get(mcname = self.username.data.lower())
        except:
            self.username.errors.append('Unknown username')
            return False

        if not checkPassword(self.password.data, user.password):
            self.password.errors.append('Invalid password')
            return False

        if not user.confirmed:
            self.confirmed = False
            return False

        self.user = user
        return True




class RegisterForm(Form):
    username = StringField('Minecraft username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators = [DataRequired()])
    email = EmailField("Email Adress", validators = [DataRequired("Please enter your email address.")])
    recaptcha = RecaptchaField()

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        try:
            user = User.objects.get(mcname = self.username.data)
            self.username.errors.append('Minecraft username already registered!')
            return False

        except:
            if self.password.data == self.password_confirm.data:
                self.mcname = self.username.data

                confkey = str(binascii.b2a_hex(os.urandom(16)), "UTF-8")

                if debug:
                    print(confkey)

                addUser("Registered User", self.username.data, is_staff = False, password = self.password.data, email = self.email.data, confkey = confkey)

                sendMail("no-reply", self.email.data, "Confirm Account! - MineZRC Community", "Do jazz hands, click on the link to confirm your account and join the MineZRC community!!:  "+"http://www.minezrc.com/confirm/"+confkey)


                return True
            else:
                self.password.errors.append("Passwords doesn't match!")
                return False
