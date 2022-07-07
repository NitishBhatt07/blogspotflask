from flask import Flask, render_template, url_for, flash, redirect, request
from Blog import app,db
from flask_login import current_user, login_required
from Blog.users.models import Users
from Blog.blogs.models import Posts
from Blog.users.forms import RegistrationForm
from Blog.blogs.forms import AddPostForm
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os
import uuid as uuid


from PIL import Image
def resizeUser(image_name,category):
    if category == 'profile':
        resize_tuple = (150, 150)
    elif category == 'cover':
        resize_tuple = (1100, 200)
    else:
        return redirect(url_for('edit_user', id=current_user.id))

    img = Image.open('Blog/static/images/user/'+image_name)

    if os.path.exists("Blog/static/images/user/" + img_name):
        resized = img.resize(resize_tuple)
        if category == 'cover':
            resized = resized.filter(ImageFilter.BLUR)
        resized.save("Blog/static/images/user/"+image_name)


def resizePost(image_name):
    img = Image.open('Blog/static/images/blog/'+image_name)

    if os.path.exists("Blog/static/images/blog/" + img_name):
        resized = img.resize((380,255))
        resized.save("Blog/static/images/blog/"+image_name)



@app.route('/admin')
@login_required
def admin():
    if current_user.id == 213214678:
        all_users = db.session.query(Users).order_by(Users.registered_on)
        all_posts = db.session.query(Posts).order_by(Posts.posted_on)
        return render_template('admin/dashboard.html',all_posts=all_posts,all_users=all_users)
    else:
        flash("Access Denied ! Only Admin Can Access this Page", category='danger')
        return redirect(url_for('profile'))


@app.route('/admin/delete/post/<int:id>')
@login_required
def deletePostAdmin(id):
    post_to_delete = db.session.query(Posts).filter(Posts.id == id).first()
    if current_user.id == 213214678:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash("Post deleted Successfully",category='success')
            return redirect(url_for('admin'))
        except:
            flash("Something Went Wrong", category='danger')
            return redirect(url_for('admin'))
    else:
        flash("Access Denied ! Only Admin Can Access this Page", category='danger')
        return redirect(url_for('profile'))


@app.route('/admin/delete/user/<int:id>')
@login_required
def deleteUserAdmin(id):
    user_to_delete = db.session.query(Users).filter(Users.id == id).first()
    if current_user.id == 213214678:
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User deleted Successfully",category='success')
            return redirect(url_for('admin'))
        except:
            flash("Something Went Wrong", category='danger')
            return redirect(url_for('admin'))
    else:
        flash("Access Denied ! Only Admin Can Access this Page", category='danger')
        return redirect(url_for('profile'))


@app.route('/admin/edit/user/<int:id>', methods=['GET','POST'])
@login_required
def editUserAdmin(id):
    form = RegistrationForm()
    user_to_edit = db.session.query(Users).filter(Users.id==id).first()

    if current_user.id == 213214678:

        if request.method =='POST':
            user_to_edit.username = form.username.data
            user_to_edit.email = form.email.data
            user_to_edit.bio = form.bio.data
            user_to_edit.password = generate_password_hash(form.password.data)
            profile_pic = form.profile_pic.data
            cover_pic = form.cover_pic.data

            # For Profile Pic
            if profile_pic is not None:
                # remove old pic
                if os.path.exists("Blog/static/images/user/" + user_to_edit.profile_pic):
                    os.remove("Blog/static/images/user/" + user_to_edit.profile_pic)  # one file at a time

                ###----- Adding profile pic to database -----##
                # geting image name
                profile_pic_name = secure_filename(profile_pic.filename)
                # creating secure and unique profile pic name
                profile_pic_name = str(uuid.uuid1()) + "_" + profile_pic_name

                # Resize Save profile pic in static folder
                resizeUser(profile_pic_name, 'profile')

                user_to_edit.profile_pic = profile_pic_name
            else:
                if os.path.exists("Blog/static/images/user/" + user_to_edit.profile_pic):
                    user_to_edit.profile_pic = user_to_edit.profile_pic
                else:
                    user_to_edit.profile_pic = "empty"

            ###----- Adding Cover pic to database -----##
            if cover_pic is not None:
                print("profile pic is not non")
                # remove old pic
                if os.path.exists("Blog/static/images/user/" + user_to_edit.cover_pic):
                    os.remove("Blog/static/images/user/" + user_to_edit.cover_pic)  # one file at a time
                # geting image name
                cover_pic_name = secure_filename(cover_pic.filename)
                # creating secure and unique profile pic name
                cover_pic_name = str(uuid.uuid1()) + "_" + cover_pic_name

                # Resize Save profile pic in static folder
                resizeUser(cover_pic_name, 'cover')

                user_to_edit.cover_pic = cover_pic_name
            else:
                if os.path.exists("Blog/static/images/user/"+user_to_edit.cover_pic):
                    user_to_edit.cover_pic  = user_to_edit.cover_pic
                else:
                    user_to_edit.cover_pic = "empty"

            try:
                db.session.commit()
                flash("User Updated Successfully", category='success')
                return redirect(url_for('admin'))
            except:
                flash("Something went wrong!", category='danger')
                return redirect(url_for('admin'))
    else:
        flash("Access Denied! Only Admin can Access this Page", category='danger')
        return redirect(url_for('profile'))

    return render_template('admin/edit_user.html',form=form,user_to_edit=user_to_edit)



@app.route('/admin/edit/post/<int:id>', methods=['GET','POST'])
@login_required
def editPostAdmin(id):
    form = AddPostForm()
    post_to_edit = db.session.query(Posts).filter(Posts.id == id).first()

    if current_user.id == 213214678:
        if request.method == 'POST':
            post_to_edit.title = form.title.data
            post_to_edit.author = form.author.data
            post_to_edit.content = form.content.data
            post_pic = form.post_pic.data

            # For Profile Pic
            if post_pic is not None:
                # remove old pic
                if os.path.exists("Blog/static/images/blog/" + post_to_edit.post_pic):
                    os.remove("Blog/static/images/blog/" + post_to_edit.post_pic)  # one file at a time

                ###----- Adding profile pic to database -----##
                # geting image name
                post_pic_name = secure_filename(post_pic.filename)
                # creating secure and unique profile pic name
                post_pic_name = str(uuid.uuid1()) + "_" + post_pic_name

                # Resize Save profile pic in static folder
                resizePost(post_pic_name)

                post_to_edit.post_pic = post_pic_name
            else:
                if os.path.exists("Blog/static/images/blog/" + post_to_edit.post_pic):
                    post_to_edit.post_pic = post_to_edit.post_pic
                else:
                    post_to_edit.post_pic = "empty"

            try:
                db.session.commit()
                flash("Post Updated Successfully", category='success')
                return redirect(url_for('admin'))
            except:
                flash("Something went wrong!", category='danger')
                return redirect(url_for('admin'))

    else:
        flash("Access Denied! Only Admin can Access this Page", category='danger')
        return redirect(url_for('profile'))

    return render_template('admin/edit_post.html', form=form,post_to_edit=post_to_edit)


