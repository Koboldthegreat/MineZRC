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



@app.route('/admin/post/add', methods = ['GET', 'POST'])
def adminCreatePost():
    if requires_admin():
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
    else:
        flash('You have to be logged as admin to access this page ', 'warning')
        return redirect('/')

@app.route('/admin/post/delete/<title>')
def adminDeletePost(title):
    if requires_admin():
        try:
            post = Post.objects.get(title = title)
            post.delete()
            flash(u'Successfully removed Post: %s. ' % title, 'success')
        except:
            flash(u"Post: %s doesn't exist!" % title, 'warning')

        return redirect(url_for('adminPanel'))
    else:
        flash('You have to be logged as admin to access this page ', 'warning')
        return redirect('/')

@app.route('/admin/user/delete/<mcname>')
def adminDeleteUser(mcname):
    if requires_admin():
        try:
            user = User.objects.get(mcname = mcname)
            user.delete()
            flash(u'Successfully removed User: %s. ' % user.mcname, 'warning')
        except:
            flash(u'MCname not valid!', 'danger')
        return redirect(url_for('adminPanel'))
    else:
        flash('You have to be logged as admin to access this page ', 'warning')
        return redirect('/')

@app.route('/admin/staff/add/<mcname>')
def adminAddStaff(mcname):
    if requires_admin():
        try:
            user = User.objects.get(mcname = mcname)
            user.update(is_staff = True)
            flash(u'Added %s to Staff ' % user.mcname, 'warning')
        except:
            flash(u'MCname not valid!', 'danger')
        return redirect(url_for('adminPanel'))
    else:
        flash('You have to be logged as admin to access this page ', 'warning')
        return redirect('/')

@app.route('/admin/staff/add/<mcname>')
def adminAddPanel(mcname):
    if requires_admin():
        try:
            user = User.objects.get(mcname = mcname)
            user.update(panel = True)
            flash(u'Added %s to Admins ' % user.mcname, 'warning')
        except:
            flash(u'MCname not valid!', 'danger')
        return redirect(url_for('adminPanel'))
    else:
        flash('You have to be logged as admin to access this page ', 'warning')
        return redirect('/')

@app.route('/admin/panel/remove/<mcname>')
def adminRemovePanel(mcname):
    if requires_admin():
        try:
            user = User.objects.get(mcname = mcname)
            user.update(panel = False)
            flash(u'Removed %s from Admins ' % user.mcname, 'warning')
        except:
            flash(u'MCname not valid!', 'danger')
        return redirect(url_for('adminPanel'))
    else:
        flash('You have to be logged as admin to access this page ', 'warning')
        return redirect('/')


@app.route('/admin/staff/remove/<mcname>')
def adminRemoveStaff(mcname):
    if requires_admin():
        try:
            user = User.objects.get(mcname = mcname)
            user.update(is_staff = False)
            flash(u'Removed %s from Staff ' % user.mcname, 'warning')
        except:
            flash(u'MCname not valid!', 'danger')
        return redirect(url_for('adminPanel'))
    else:
        flash('You have to be logged as admin to access this page ', 'warning')
        return redirect('/')



@app.route('/admin/post/edit/<title>' , methods = ['GET', 'POST'])
def adminEditPost(title):
    print(title)
    if requires_admin():
        try:
            post = Post.objects.get(title = title)
            backgroundlist = listdir(geturl('static/img/servers'))
            backgroundurl = "/static/img/servers/" + random.choice(backgroundlist)
            PostForm = model_form(Post, exclude=('created_at', 'comments', 'author'))(request.form)
            if request.method == 'POST':
                if True:
                    if PostForm.title.data:
                        post.update(title = PostForm.title.data)
                        title = PostForm.title.data
                    if PostForm.content.data:
                        post.update(content = PostForm.content.data)
                    if PostForm.tags.data:
                        post.update(tags = PostForm.tags.data)


                    flash(u'Successfully edited Post: %s. ' % title, 'success')
                return redirect(url_for('adminPanel'))

            else:
                return render_template('admin/edit_post.html', form = PostForm, post = post, create = True, background = backgroundurl)
        except:
            flash(u"Post doesn't exist!", 'danger')
        return redirect(url_for('adminPanel'))
    else:
        flash('You have to be logged as admin to access this page ', 'warning')
        return redirect('/')
