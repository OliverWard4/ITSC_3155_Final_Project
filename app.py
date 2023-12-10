import os
import secrets
from PIL import Image
<<<<<<< HEAD
from flask import render_template, url_for, flash, redirect, request
from corkboard import app, db, bcrypt, mail
from corkboard.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from corkboard.models import User, Post, Board
from corkboard.posts import router, getAllBoards, getUserBoards
=======
from flask import render_template, url_for, flash, redirect, request,  send_from_directory,  abort, current_app, jsonify
from corkboard import app, db, bcrypt, mail, UPLOAD_FOLDER
from corkboard.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, PostForm
from corkboard.models import User, Board, Comment, Starred
>>>>>>> 95821f2cadc23830aeb43850efab87e55950bdfc
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from werkzeug.utils import secure_filename





@app.route("/")
def index():
    template_name = 'landingPage.html'
    return render_template('landingPage.html',template_name=template_name)

@app.route("/")
@app.route("/home")
def home():
    template_name = 'home.html'
    page = request.args.get('page', 1, type=int)
    posts = Board.query.order_by(Board.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, template_name=template_name)

@app.route('/home/favoriteboards')
@login_required  # Require authentication to access this route
def favoriteboards():
    template_name='starredBoards.html'
    # Fetch the liked posts by the current user from the Starred model
    liked_posts = Board.query.join(Starred, (Starred.post_id == Board.id)).filter(
        Starred.author == current_user.id).order_by(Board.date_posted.desc()).all()

    return render_template('starredBoards.html', liked_posts=liked_posts, template_name='starredBoards.html')

@app.route("/home/landingPage")
def landingPage():
    template_name = 'landingPage.html'
    return render_template('landingPage.html', template_name=template_name)

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('landingPage'))

@app.route("/contactus")
def contactus():
    return render_template('contactus.html')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn




@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)




def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)










ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file1(file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    file_fn = random_hex + f_ext

    # Ensure the 'static/uploads' directory exists
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, file_fn)

    file.save(file_path)

    return file_fn

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        file = form.file.data

        if file and allowed_file(file.filename):
            file_path = save_file1(file)
        else:
            file_path = None  # Handle the case where no valid file is provided

        board = Board(title=title, content=content, author=current_user, file_path=file_path)
        db.session.add(board)
        db.session.commit()

        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))

    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route('/static/uploads/<path:filename>')
def serve_static(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
    
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Board.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)




@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Board.query.get_or_404(post_id)

    # Ensure only the author can update the post
    if post.author != current_user:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        # Handle file upload if necessary
        file = form.file.data
        if file:
            # Save the file using the save_file1 function
            file_path = save_file1(file)
            
            # Update post file path
            post.file_path = file_path

        # Update post data
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()

        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))

    # Pre-populate form fields after validating form submission
    form.title.data = post.title
    form.content.data = post.content

    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')



@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Board.query.get_or_404(post_id)

    # Check if the current user is the author of the post
    if post.author != current_user:
        abort(403)

    try:
        # Delete all associated comments first
        Comment.query.filter_by(post_id=post.id).delete()
        Starred.query.filter_by(post_id=post.id).delete()

        # Delete the post
        db.session.delete(post)
        db.session.commit()

        flash('Your post and associated comments have been deleted!', 'success')
    except Exception as e:
        # Handle exceptions if necessary
        flash(f'Error deleting post: {str(e)}', 'error')

    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Board.query.filter_by(author=user)\
        .order_by(Board.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user,   template_name='user_posts.html')




@app.route("/create_comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        # Fetch the post from the database
        post = Board.query.get(post_id)

        if post:
            comment = Comment(text=text, author=current_user, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('post', post_id=post_id))
            
        else:
            flash('Post does not exist.', category='error')
  

@app.route("/searching")
def search():
    q = request.args.get("q")
    print(q)

    if q:
        results = Board.query.filter(Board.title.icontains(q) | Board.user_id.icontains(q)).order_by(Board.date_posted.desc()).limit(20).all()
    else: 
        results = []
    
    return render_template("search_results.html", results=results)



@app.route("/delete_comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author_id and current_user.id != comment.board.author_id:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        # Store post_id before deleting the comment
        post_id = comment.board.id
        
        db.session.delete(comment)
        db.session.commit()

        # Redirect to the 'post' route with the appropriate post_id
        return redirect(url_for('post', post_id=post_id))



@app.route("/like_post/<post_id>", methods=['GET'])
@login_required
def like_post(post_id):
    post = Board.query.filter_by(id=post_id).first()
    like = Starred.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        # Handle the case where the post does not exist
        flash('Post does not exist.', 'error')

    if like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Starred(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    # Assuming you have a 'post' route that displays a single post
    return redirect(url_for('home'))





@app.route('/home/search_user', methods=['GET', 'POST'])
@login_required
def search_user():
    template_name='search_user.html'
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()


        if user:
            # Redirect to the user_posts route with the username parameter
            return redirect(url_for('user_posts', username=user.username))
        else:
            error_message = 'User not found.'
            return render_template('search_user.html', error_message=error_message, template_name=template_name )

    return render_template('search_user.html', template_name=template_name)

if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()
    app.run(debug=True)
