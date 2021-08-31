"""Blogly application."""

from flask_debugtoolbar import DebugToolbarExtension

from flask import Flask, request, redirect, render_template,flash
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
app.config['SECRET_KEY'] = 'ihaveasecret'


toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    """ home-page with recent list of posts"""
    posts=Post.query.order_by(Post.create_at.desc()).limit(5).all()
    return render_template('homepage.html',posts=posts)


@app.route('/users')
def list_user():
    """showing list of users"""
    user=User.query.order_by(User.first_name,User.last_name).all()
    return render_template("list.html",user=user)


@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """showing detail of user"""
    user=User.query.get_or_404(user_id)
    return render_template("detail.html",user=user)

@app.route('/users/new', methods=['GET'])
def get_new_user_form():
    ''' showing a form to create a new user'''
    return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def new_user():
    ''' adding new user with post method  and redirecting to user list'''

    first_name=request.form['first_name']
    last_name=request.form['last_name']
    image_url=request.form['image_url'] or None 

    new_guy= User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_guy)
    db.session.commit()
    # flash(f"User {new_guy.first_name} {new_guy.last_name} is created ")

    return redirect('/users')



@app.route('/users/<int:user_id>/edit')
def user_edit_page(user_id):
    """show a form to edit an existing user"""

    user=User.query.get_or_404(user_id)
    return render_template('edit.html',user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_or_edit(user_id):
    """Handling form submission from edit page"""

    user=User.query.get_or_404(user_id)
    user.first_name=request.form['first_name']
    user.last_name=request.form['last_name']
    user.image_url=request.form['image_url'] 

    
    db.session.add(user)
    db.session.commit()

    flash(f"User {user.first_name} {user.last_name} is edited ")

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def deleting_user(user_id):
    '''handle form submission from delete button/deleting the user'''
    user=User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.first_name} {user.last_name} is deleted ")
    return redirect("/users")




#########post section#########

@app.route('/users/<int:user_id>/posts/new')
def show_form_to_add_post(user_id):
    '''Show form to add a post for that user.'''
    user=User.query.get_or_404(user_id)
    tags=Tag.query.all()
    return render_template('postform.html', user=user,tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def handle_add_form_add_post(user_id):
    '''Handle add form; add post and redirect to the user detail page.'''

    user=User.query.get_or_404(user_id)
    tag_ids=[int(num) for num in request.form.getlist('tags')]
    tags= Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post=Post(title=request.form['title'],
                  content=request.form['content'],
                  user=user, tags=tags)
    db.session.add(new_post)
    db.session.commit()
    flash(f" Post '{new_post.title}' is added")
    return redirect(f'/users/{user_id}')



@app.route('/posts/<int:post_id>')
def show_post(post_id):
    '''show a post detailed page'''
    post=Post.query.get_or_404(post_id)

    return render_template('showpost.html',post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""
    post=Post.query.get_or_404(post_id)
    tags=Tag.query.all()
    return render_template('editpost.html',post=post,tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post_form(post_id):
    """Handle post edit form"""
    post=Post.query.get_or_404(post_id)

    post.title=request.form['title']
    post.content=request.form['content']

    
    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title} edited")
    return redirect(f'/users/{post.user_id}')


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    '''delete post'''
    post=Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted")
    return redirect(f'/users/{post.user_id}')




    ##########################   tag route    #######

@app.route('/tags')
def all_tag():
    """list al tags"""
    tags=Tag.query.all()
    return render_template('alltag.html',tags=tags)

@app.route('/tags/new')
def tag_new_form():
    """form to create new_tag """
    posts=Post.query.all()
    return render_template('tagnewform.html',posts=posts)

@app.route('/tags/new',methods=['POST'])
def tag_new_form_adding():
    """adding new tag,form submission """
    post_ids=[ int(num) for num in request.form.getlist('posts')]
    posts= Post.query.filter(Post.id.in_(post_ids)).all()

    new_tag=Tag(name=request.form['name'],
                posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<int:tag_id>')
def show_tag_detail(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""

    tag=Tag.query.get_or_404(tag_id)

    return render_template('tagdetailpage.html',tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def show_tag_edit_form(tag_id):
    '''Show edit form for a tag.'''

    tag=Tag.query.get_or_404(tag_id)
    posts=Post.query.all()
    return render_template('tag_edit_form.html',tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def handle_tag_edit_form(tag_id):
    tag=Tag.query.get_or_404(tag_id)
    tag.name=request.form["name"]
    post_ids= [int(num) for num in request.form.getlist('posts')]

    tag.posts=Post.query.filter(Post.id.in_(post_ids)).all()


    db.session.add(tag)
    db.session.commit()
    flash(f" Tag {tag.name} is edited")
    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    ''''delete tag'''
    tag=Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name} is deleted")
    return redirect('/tags')

    











