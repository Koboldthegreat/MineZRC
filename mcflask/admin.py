from flask import request, redirect, render_template, url_for, flash, abort
from flask.ext.mongoengine.wtf import model_form

from mcflask import app
from mcflask.models import User, Server, staffmembers, servers, Post, addPost

from functools import wraps
from mcflask.auth import requires_admin

from flask.ext.mongoengine.wtf import model_form

from mcflask.models import add_post, PostForm

@app.route('/admin')
def adminPosts():
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

@app.route('/admin/post/create', methods = ['GET', 'POST'])
def adminCreatePost():
    PostForm = model_form(Post, exclude=('created_at', 'comments', 'author'))(request.form)

    if request.method == 'POST' and PostForm.validate():
        print('adding post')
        return redirect('/admin')

    else:
        return render_template('admin/post.html', form = PostForm, create = True)
