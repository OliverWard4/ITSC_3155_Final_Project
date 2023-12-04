from flask import Blueprint, abort, request, render_template, url_for, redirect, flash
from flask_login import current_user
from corkboard import db
from corkboard.models import User, Board, Recent, Starred, Comment
from datetime import datetime, date

router = Blueprint('boards', __name__, url_prefix='/boards')

@router.route("/create")
def create():
    return render_template('new.html')

@router.post('/')
def create_board():
    title = request.form.get('boardTitle')
    description = request.form.get('boardDescription')
    content = request.form.get('boardContent')
    file = request.form.get('uploadFiles')
    user_id = current_user.id
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_posted = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    new_board = Board(title=title, description=description, content = content, file=file, user_id=user_id, date_posted=date_posted)

    if user_id is None:
        abort(400)

    db.session.add(new_board)
    db.session.commit()
    return redirect('/boards')

@router.get('/<int:id>')
def getBoard(id):
    board = Board.query.get_or_404(id)
    user = User.query.get(board.user_id)
    post_id = id
    comments = Comment.query.filter_by(post_id=post_id).all()

    comment_data = []

    for comment in comments:
        poster = User.query.get(comment.commentor_id)
        comment_data.append((comment, poster))

    return render_template('boardView.html', board=board, comments=comments, comment_data = comment_data, user=user)

def getAllBoards():
    boards = Board.query.all()
    return boards

def getUserBoards():
    user_id = current_user.id
    boards = Board.query.filter_by(user_id=user_id).all()
    return boards

@router.route('/<int:id>/edit', methods=['GET', 'POST'])
def editBoard(id):
    board_to_edit =  Board.query.get_or_404(id)
    if current_user.is_authenticated:
        if request.method == 'POST':
            board_to_edit.title = request.form.get('boardTitle')
            board_to_edit.description = request.form.get('boardDescription')
            board_to_edit.content = request.form.get('boardContent')
            board_to_edit.file = request.form.get('uploadFiles')
            try:
                db.session.commit()
                return redirect(f'/boards/{board_to_edit.id}')
            except:
                return abort(400, 'There was an issue with editing your board.')
        else:
            return render_template('edit-board.html', board=board_to_edit)
    else:
        return redirect('/login')
    
@router.post('/<int:id>/delete')
def deleteBoard(id):
        board_to_delete = Board.query.get_or_404(id)
        if current_user.is_authenticated:
            if board_to_delete.user_id == current_user.id:
                comments = Comment.query.filter_by(post_id=id).delete()
                
                db.session.delete(board_to_delete)
                db.session.commit()
                return redirect('/boards')
            else:
                return redirect('/home')
        else:
            return redirect('/login')

@router.post('/<int:id>/comment')
def createComment(id):
    board = Board.query.get_or_404(id)
    content = request.form.get('comment')
    post_id = board.id
    commentor_id = current_user.id
    newComment = Comment(content=content, post_id=post_id, commentor_id=commentor_id)

    if content is None:
        abort(400, 'Comment is missing')
    else:
        db.session.add(newComment)
        db.session.commit()
        return redirect(f'/boards/{post_id}')

@router.post('/<int:post_id>/comment/delete/<int:id>')
def deleteComment(post_id, id):
    comment_to_delete = Comment.query.get_or_404(id)

    db.session.delete(comment_to_delete)
    db.session.commit()
    
    return redirect(f'/boards/{post_id}')

def hasStarredBoard(id):
    board = Board.query.get_or_404(id)
    user_id = current_user.id
    hasStarred = Starred.query.filter_by(post_id=board.id, user_id=user_id).count()
    return hasStarred

@router.post('/<int:id>/star')
def starBoard(id):
    board = Board.query.get_or_404(id)
    user_id = current_user.id
    if(hasStarredBoard(board.id) == 0):
        star = Starred(post_id=board.id, user_id=user_id)
        db.session.add(star)
        flash('This board has been added to your Starred Boards list', 'success')
    else:
        Starred.query.filter_by(post_id=board.id, user_id=user_id).delete()
        flash('This board has been removed from your Starred Boards list', 'success')
    db.session.commit()
    return redirect('/boards/starred')



def getStarredBoards():
    user_id = current_user.id
    starredBoards = Starred.query.filter_by(user_id=user_id).all()
    return starredBoards