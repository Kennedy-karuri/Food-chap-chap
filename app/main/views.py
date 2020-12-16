from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from ..requests import get_quotes
from flask_login import login_required
from .forms import UpdateProfile,PostForm,CommentForm
from ..models import User,PhotoProfile,Post,Comment,Subscribe
from .. import db,photos
from flask_login import login_required, current_user
import markdown2


@main.route('/')
def index():
    quotes = get_quotes()
    
    title = 'Food chap-chap'
    return render_template('index.html', title = title,quotes = quotes)


@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():

        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user_photo = PhotoProfile(pic_path = path,user = user)
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/order/new', methods=['GET', 'POST'])
@login_required
def order():
    """
    View Post function that returns the Order made and data
    """
    order_form = OrderForm()
    if order_form.validate_on_submit():
        order_title = order_form.order_title.data
        description = order_form.description.data
        new_order = Order(order_title=order_title, description=description, author=current_user)
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for('main.all'))
    title = 'New Order | food'
    return render_template('order.html', title=title, post_form=post_form)


@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    order = Order.query.get_or_404(id)
    if order.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    # flash('Your order has been deleted', 'successfully')
    return redirect(url_for('main.all'))


@main.route('/Update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_order(id):
    order = Order.query.get_or_404(id)
    if order.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        order.order_title = form.order_title.data
        order.description = form.description.data
        db.session.commit()
        flash('Your order has been Updated', 'successfully')
        return redirect(url_for('main.all'))
    elif request.method == 'GET':
        form.order_title.data = order.post_title
        form.description.data = order.description
    return render_template('update_order.html', form=form)

#Subscribe
@main.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    '''
    Function to send email upon subscription
    '''
    if request.method == 'POST':
        email = request.form['email']
        new_email = Subscribe(email=email)
        db.session.add(new_email)
        db.session.commit()
        flash('Thank you for subscribing')
        return redirect(url_for('main.index'))