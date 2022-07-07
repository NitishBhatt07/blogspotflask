from flask import Flask, render_template, flash , redirect, url_for, request
from Blog import app,db
from Blog.blogs.models import Posts
from Blog.blogs.forms import AddPostForm ,SearchForm
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename
import uuid as uuid
import os
from PIL import Image

def resizePost(image_name):
    img = Image.open('Blog/static/images/blog/'+image_name)

#     if os.path.exists("Blog/static/images/blog/" + img_name):
    resized = img.resize((380,255))
    resized.save("Blog/static/images/blog/"+image_name)


@app.route('/')
def home_page():
    posts = Posts.query.order_by(Posts.posted_on)
    return render_template('blog/posts.html',posts=posts)

@app.route('/add/post', methods=['GET','POST'])
@login_required
def add_post():
    form = AddPostForm()

    if request.method == 'POST':
        post_pic = form.post_pic.data
        if post_pic is not None:
            #secure filename
            post_pic_name = secure_filename(post_pic.filename)
            post_pic_name = str(uuid.uuid1())+"_"+post_pic_name
            # resize and save picture
            resizePost(post_pic_name)
        else:
            post_pic_name = 'empty'

        try:
            post = Posts(title=form.title.data,author=form.author.data,content=form.content.data,
                         post_pic=post_pic_name,poster_id=current_user.id)
            db.session.add(post)
            db.session.commit()

            form.title.data = ''
            form.author.data = ''
            form.content.data = ''
            flash("Post added Successfully",category='success')
            return render_template('blog/add_post.html', form=form)
        except:
            flash("Something Went Wrong",category='danger')
            return render_template('blog/add_post.html',form=form)

    return render_template('blog/add_post.html',form=form)


@app.route('/posts')
def posts():
    posts = Posts.query.order_by(Posts.posted_on)
    return render_template('blog/posts.html',posts=posts)

@app.route('/post/<int:id>')
@login_required
def post(id):
    post = db.session.query(Posts).filter(Posts.id==id).first()
    return render_template('blog/post.html',post=post)

@app.route('/edit/post/<int:id>', methods=['GET','POST'])
@login_required
def edit_post(id):
    form = AddPostForm()
    user_posts = db.session.query(Posts).filter(Posts.poster_id == current_user.id)
    total_posts = db.session.query(Posts).filter(Posts.poster_id == id).count()
    post_to_edit = db.session.query(Posts).filter(Posts.id == id).first()

    if form.validate_on_submit():
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
            return render_template('users/profile.html',user_posts=user_posts,total_posts=total_posts)
        except:
            flash("Something went wrong!", category='danger')
            return render_template('users/profile.html',user_posts=user_posts,total_posts=total_posts)

    if (current_user.id == post_to_edit.poster_id):
        return render_template('blog/edit_post.html',post_to_edit=post_to_edit,form=form)
    else:
        flash("Access Denied! You Can Only Edit Your Post", category='danger')
        return render_template('users/profile.html',user_posts=user_posts,total_posts=total_posts)


@app.route('/delete/post/<int:id>')
def delete_post(id):
    post_to_delete = db.session.query(Posts).filter(Posts.id == id).first()
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Post Deleted Successfully!", category='success')
        return redirect(url_for('profile'))
    except:
        flash("Something went wrong!", category='danger')
        return redirect(url_for('profile'))


## for search
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@app.route('/search', methods=['GET','POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        searched = form.searched.data

        searched_posts = Posts.query.filter(Posts.content.like('%' + searched + '%'))
        # return all post
        searched_posts = searched_posts.order_by(Posts.title).all()

        total_posts = len(searched_posts)

        #searched_posts = db.session.query(Posts).filter(Posts.content.like('%'+search+'%')).order_by(Posts.title).all()
        return render_template('blog/search.html',form=form,searched_posts=searched_posts,total_posts=total_posts)



@app.route('/test')
def test():
    post_to_edit = db.session.query(Posts).filter(Posts.id == id).first()
    return render_template('blog/test.html',post_to_edit=post_to_edit)
