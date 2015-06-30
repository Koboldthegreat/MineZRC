from flask import request, redirect, render_template, url_for, flash, abort, session
from flask.ext.mongoengine.wtf import model_form

from mcflask import app
from mcflask.models import User, Server, staffmembers, servers, Post, addPost

from functools import wraps
from mcflask.auth import requires_admin

from flask.ext.mongoengine.wtf import model_form

from mcflask.models import addPost, PostForm

from os import listdir
import random

from mcflask.functions import geturl

@app.route('/admin')
def adminPanel():

    if requires_admin():
        posts = Post.objects.all()
        users = User.objects.all()
        return render_template("admin/home.html", posts = posts, users = users)
    else:
        flash('You have to be logged as admin to access this page ', 'warning')
        return redirect('/')

@app.route('/admin/post/edit/<slug>', methods = ['GET','POST'])
def adminEditPost(slug):
    post = Post.objects.get_or_404(slug=slug)
    if request.method == 'POST':
        cls = post.__class__
        form_cls = model_form(cls,  exclude=('created_at', 'comments'))
        form = form_cls(request.form, inital=post._data)
    else:
        cls = post.__class__
        form_cls = model_form(cls,  exclude=('created_at', 'comments'))
        form = form_cls(obj=post)
    return render_template('admin/post.html', form = form, post = post)

@app.route('/admin/post/add', methods = ['GET', 'POST'])
def adminCreatePost():
    backgroundlist = listdir(geturl('static/img/servers'))
    backgroundurl = "/static/img/servers/" + random.choice(backgroundlist)


    PostForm = model_form(Post, exclude=('created_at', 'comments', 'author'))(request.form)

    if request.method == 'POST':
        if PostForm.validate_on_submit():
            print(PostForm.title.data)

            try:
                post = Post.objects.get(title = PostForm.title.data)
                PostForm.title.errors.append('Post with this title already exists')
                return False

            except:
                user = User.objects.get(mcname = session['usermcname'])
                post = Post(title = PostForm.title.data, author = user, content = PostForm.content.data, tags = PostForm.tags.data)
                post.save()
                flash(u'Successfully created Post: %s. ' % PostForm.title.data, 'success')
                return redirect(url_for('adminPanel'))

    else:
        return render_template('admin/add_post.html', form = PostForm, create = True, background = backgroundurl)
