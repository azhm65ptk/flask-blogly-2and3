from flask_sqlalchemy import SQLAlchemy
import datetime

db=SQLAlchemy()

DEFAULT_IMAGE_URL="https://picsum.photos/536/354"

def connect_db(app):
    "Connecting the database "
    db.app=app
    db.init_app(app)




class User(db.Model):
    """create a User model for SQLAlchemy."""
    __tablenmae__="user"

    id= db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name= db.Column(db.String(50),
                    nullable=False,
                    unique=True)
    last_name= db.Column(db.String(50),
                    nullable=False,
                    unique=True)
    image_url=db.Column(db.Text,
                    nullable=False,
                    default= DEFAULT_IMAGE_URL)

    posts=db.relationship('Post', backref='user', cascade="all, delete-orphan")

class Post(db.Model):
    '''create a post model '''

    __tablename__='post'

    id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title= db.Column(db.String(300),nullable=False)
    content=db.Column(db.Text, nullable=False)

    create_at=db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)



class Tag(db.Model):
    """create a tag model"""
    __tablename__='tag'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.Text,nullable=False, unique=True)

    posts=db.relationship('Post',secondary='post_tag',
                            backref='tags')


class PostTag(db.Model):
    __tablename__='post_tag'
    """PostTag together"""
    post_id=db.Column(db.Integer, db.ForeignKey('post.id'),
                        primary_key=True)
    tag_id=db.Column(db.Integer, db.ForeignKey('tag.id'),
                        primary_key=True)





   


