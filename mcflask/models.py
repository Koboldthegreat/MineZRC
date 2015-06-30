import urllib.request
import os.path #to check if database exists
import datetime

import mcflask.functions
from mcflask.encrypt import encryptPassword, checkPassword

from mcflask import db
from flask.ext.mongoengine.wtf import model_form

from mcflask import app


#new
"""
from mcflask import db
from flask.ext.mongoengine.wtf import model_form
"""

staffmembers = []
servers= []


def addServer(servername,displayname, is_new = False,):
    servers = Server.objects.all()
    if not any(server.name == servername for server in servers):
        image_url = 'static/img/servers/' + servername + '.png'
        server = Server(name = servername, displayname = displayname, image_url = image_url, is_new = is_new)
        server.save()
        print(servername + " added to servers")
    else:
        print("Server: " + servername + " already exists")

def addPost(title, author, content, tags = None):
    posts = Post.objects.all()
    if not any(post.title == title for post in posts):
        post = Server(title = title, author = author, tags = tags, content = content)
        post.save()
        print(title + " added to posts")
    else:
        print("Post with title: " + title + "already exists")

def addUser(ranking, displayname, is_staff = False,email = "Not Set Yet", password = None, confirmed = False, confkey = None):
    mcname = displayname.lower()
    users = User.objects.all()
    if password:
        encrypted_password = encryptPassword(password)
    else:
        encrypted_password = None
    if not any(user.mcname == mcname for user in users):
        user = User(ranking = ranking, mcname = mcname, displayname=displayname, is_staff = is_staff, email = email, password = encrypted_password, confirmed = confirmed, confkey = confkey)
        user.save()
        print(mcname + " added to users")
    else:
        print("User: " + mcname + ' already exists')

class Server(db.Document):
    name = db.StringField(required=True)
    displayname = db.StringField()
    image_url = db.StringField(required = True, max_length=255)
    is_new = db.BooleanField(default = False)





class User(db.Document):
    email = db.StringField(required=True)
    mcname = db.StringField(max_length=50, required=True)
    displayname = db.StringField(max_length=50, required=True)
    ranking = db.StringField(max_length=50)
    is_staff = db.BooleanField(default = False)
    confirmed = db.BooleanField(default = False)
    password = db.StringField()
    email = db.StringField()
    confkey = db.StringField()

    meta = {
        'allow_inheritance': True,
        'indexes': ['ranking', 'mcname'],
        'ordering': ['is_staff', 'ranking']

    }

    def getSkin(self):
        name = self.mcname
        path  = mcflask.functions.geturl('static/img/skin/') + name + '.png'
        if not os.path.exists(path):
            url = urllib.request.urlopen("https://minotar.net/skin/" + self.mcname).mcflask.functions.geturl()
            image = urllib.request.urlopen(url).read()
            file = open(path,'wb')
            file.write(image)
            file.close
        return path

    def getHead(self):
        path = "https://minotar.net/avatar/" + self.mcname + "/350.png"
        return path

    def updateHead(self):
        path = "https://minotar.net/avatar/" + self.mcname + "/350.png"
        return path


    def updateSkin(self):
        path  = mcflask.functions.geturl('static/img/skin/') + self.mcname + '.png'
        url = "https://minotar.net/skin/" + self.mcname
        urllib.request.urlretrieve(url, path)

        #image = urllib.request.urlopen(url).read()
        #file = open(path,'wb')
        #file.write(image)
        #file.close

        return path

    def addStaff(self):
        staffmembers.append(self)




class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name='Comment', required = True)
    author = db.StringField(verbose_name='Name', max_length=255, required=True)

class Post(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=120, required=True)
    author = db.ReferenceField(User)
    tags = db.ListField(db.StringField(max_length=30))
    content = db.StringField(required = True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']

    }

PostForm = model_form(Post)

def add_post(request):
    form = PostForm(request.POST)
    if request.method == 'POST' and form.validate():
        redirect('done')
    return render_template('add_post.html', form=form)
