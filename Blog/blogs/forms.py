from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,EmailField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField

class AddPostForm(FlaskForm):
    title = StringField("Title",validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    post_pic = FileField("Cover Picture")
    submit = SubmitField('Post')

class SearchForm(FlaskForm):
    searched = EmailField("searched", validators=[DataRequired()])
    submit = SubmitField("Submit")