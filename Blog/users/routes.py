from Blog import app, db, login_manager
from flask import Flask, flash, request, render_template, redirect, url_for

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid as uuid
import os

from Blog.users.forms import RegistrationForm, LoginForm
from Blog.users.models import Users
from Blog.blogs.models import Posts

from flask_login import login_user,logout_user, login_required, current_user


from PIL import Image
def resize(image_name,category):

    if category == 'profile':
        resize_tuple = (150, 150)
    elif category == 'cover':
        resize_tuple = (1100, 200)
    else:
        return redirect(url_for('edit_user', id=current_user.id))

    img = Image.open('Blog/static/images/user/'+image_name)

#     if os.path.exists("Blog/static/images/user/" + img_name):
    resized = img.resize(resize_tuple)
    if category == 'cover':
        resized = resized.filter(ImageFilter.BLUR)
    resized.save("Blog/static/images/user/"+image_name)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/register/', methods=['GET','POST'])
def register():
    form = RegistrationForm()

    username=form.username.data
    email = form.email.data
    bio = form.bio.data
    password = form.password.data
    confirm_password = form.confirm_password.data
    profile_pic = form.profile_pic.data
    cover_pic = form.cover_pic.data

    if form.validate_on_submit():
        if password == confirm_password:
            # Checking if same email is registered before
            # user = db.session.query(Users).filter_by(Users.email == email).first()
            user = Users.query.filter_by(email=email).first()
            if user is None:

                ###----- Generating and Adding Hashed Password to database -----##
                password_hash = generate_password_hash(password)

                # For Profile Pic
                if profile_pic is not None:
                    ###----- Adding profile pic to database -----##
                    # geting image name
                    profile_pic_name = secure_filename(profile_pic.filename)
                    # creating secure and unique profile pic name
                    profile_pic_name = str(uuid.uuid1())+"_"+profile_pic_name

                    # Resize and Save profile pic in static folder
                    resize(profile_pic_name,'profile')

                else:
                    profile_pic_name = "empty"

                ###----- Adding Cover pic to database -----##
                if cover_pic is not None:
                    # geting image name
                    cover_pic_name = secure_filename(cover_pic.filename)
                    # creating secure and unique profile pic name
                    cover_pic_name = str(uuid.uuid1()) + "_" + cover_pic_name

                    # Resize Save profile pic in static folder
                    resize(cover_pic_name, 'cover')
                else:
                    cover_pic_name = "empty"

                try:
                    user_to_signup = Users(username=username, email=email, bio=bio,
                                           password=password_hash,profile_pic=profile_pic_name,cover_pic=cover_pic_name)

                    form.username.data = ''
                    form.email.data = ''
                    form.bio.data = ''

                    db.session.add(user_to_signup)
                    db.session.commit()
                    flash("User Registered Successfully", category='success')
                    return render_template('users/registration.html', form=form)
                except:
                    flash("User is Already Registered ! Try another one ", category='warning')
                    return render_template('users/registration.html', form=form)
        else:
            flash("Both Password Must Match", category='warning')
            return render_template('users/registration.html', form=form)
    return render_template('users/registration.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                ##### Login User ###########
                login_user(user)
                user_posts = db.session.query(Posts).filter(Posts.poster_id == current_user.id)
                total_posts = db.session.query(Posts).filter(Posts.poster_id == current_user.id).count()
                flash("Your Welcome",category='success')
                return render_template('users/profile.html',user_posts=user_posts,total_posts=total_posts)
            else:
                flash("Email/Password is Invalid", category='danger')
                return render_template('users/login.html',form=form)
        else:
            flash("There is No user exists! Please SignUp first", category='danger')
            return render_template('users/login.html', form=form)
    return render_template('users/login.html',form=form)


@app.route('/edit/user/<int:id>', methods=['GET','POST'])
@login_required
def edit_user(id):
    form = RegistrationForm()
    user_to_edit = db.session.query(Users).filter(Users.id==id).first()

    user_posts = db.session.query(Posts).filter(Posts.poster_id == current_user.id)
    total_posts = db.session.query(Posts).filter(Posts.poster_id == current_user.id).count()

    if id == current_user.id:

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
                if os.path.exists("Blog/static/images/user/" + current_user.profile_pic):
                    os.remove("Blog/static/images/user/" + current_user.profile_pic)  # one file at a time

                ###----- Adding profile pic to database -----##
                # geting image name
                profile_pic_name = secure_filename(profile_pic.filename)
                # creating secure and unique profile pic name
                profile_pic_name = str(uuid.uuid1()) + "_" + profile_pic_name

                # Resize Save profile pic in static folder
                resize(profile_pic_name, 'profile')

                user_to_edit.profile_pic = profile_pic_name
            else:
                if os.path.exists("Blog/static/images/user/" + current_user.profile_pic):
                    user_to_edit.profile_pic = current_user.profile_pic
                else:
                    user_to_edit.profile_pic = "empty"

            ###----- Adding Cover pic to database -----##
            if cover_pic is not None:
                print("profile pic is not non")
                # remove old pic
                if os.path.exists("Blog/static/images/user/" + current_user.cover_pic):
                    os.remove("Blog/static/images/user/" + current_user.cover_pic)  # one file at a time
                # geting image name
                cover_pic_name = secure_filename(cover_pic.filename)
                # creating secure and unique profile pic name
                cover_pic_name = str(uuid.uuid1()) + "_" + cover_pic_name

                # Resize Save profile pic in static folder
                resize(cover_pic_name, 'cover')

                user_to_edit.cover_pic = cover_pic_name
            else:
                if os.path.exists("Blog/static/images/user/"+current_user.cover_pic):
                    user_to_edit.cover_pic  = current_user.cover_pic
                else:
                    user_to_edit.cover_pic = "empty"

            try:
                db.session.commit()
                flash("User Updated Successfully", category='success')
                return render_template('users/profile.html',user_posts=user_posts,total_posts=total_posts)
            except:
                flash("Something went wrong!", category='danger')
                return redirect(url_for('edit_user'))
    else:
        flash("Access Denied", category='danger')
        return render_template('users/profile.html',user_posts=user_posts,total_posts=total_posts)

    return render_template('users/edit_user.html',form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("User Logout Successfully", category='success')
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    id = current_user.id
    user_posts = db.session.query(Posts).filter(Posts.poster_id == id)
    total_posts = db.session.query(Posts).filter(Posts.poster_id == id).count()
    return render_template('users/profile.html',user_posts=user_posts,total_posts=total_posts)

@app.route('/profile1')
def profile1():
    return render_template('users/profile1.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'),404

@app.errorhandler(500)
def page_not_found(error):
    return render_template('error/500.html'),500




