from datetime import datetime, timedelta

from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError, TimeoutError
from werkzeug.security import generate_password_hash, check_password_hash

import pytz

from flask import (
    abort,
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    json
)

from config import DevConfig
from forms.copy import CopyAddForm, CopyEditForm
from forms.forms import (
    ContactForm,
    ForgotPass,
    LoginForm,
    PasswordForm,
    RegistrationForm,
    WishlistForm,
    RemoveForm
)
from init_db import db
from messages import ErrorMessage, SuccessMessage
from models import LibraryItem
from models.library import RentalLog, Copy, BookStatus
from models.books import Book
from models.users import User
from models.wishlist import WishListItem, Like
from send_email import send_confirmation_email, send_password_reset_email
from send_email.emails import send_email
from serializers.wishlist import WishListItemSchema

library = Blueprint('library', __name__,
                    template_folder='templates')


@library.route('/')
def index():
    return render_template('index.html')


@library.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'logged_in' in session:
            message_body = 'You are already logged in.'
            message_title = 'Error!'
            return render_template('message.html',
                                   message_title=message_title,
                                   message_body=message_body)
        else:
            form = LoginForm()
            return render_template('login.html',
                                   form=form,
                                   error=form.errors)
    else:
        form = LoginForm()
        try:

            if form.validate_on_submit():
                data = User.query.filter_by(email=form.email.data).first()
                if (data is not None and
                        check_password_hash(data.password_hash,
                                            form.password.data) and
                        data.active):

                    session['logged_in'] = True
                    session['id'] = data.id
                    session['email'] = data.email
                    return render_template('index.html', session=session)
                else:
                    message_body = 'Login failed or ' \
                                   'your account is not activated'
                    message_title = 'Error!'
                    return render_template('message.html',
                                           message_title=message_title,
                                           message_body=message_body)
            else:
                return render_template('login.html',
                                       title='Sign In',
                                       form=form,
                                       error=form.errors)
        except (ValueError, TypeError):
            message_body = 'Something went wrong'
            message_title = 'Error!'
            return render_template('message.html',
                                   message_title=message_title,
                                   message_body=message_body)


@library.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        form = RegistrationForm()
        return render_template('registration.html',
                               form=form,
                               error=form.errors)
    else:
        form = RegistrationForm()
        if form.validate_on_submit():
            try:
                if User.query.filter_by(email=form.email.data).first():
                    message_body = 'User already exists'
                    message_title = 'Oops!'
                    return render_template('message.html',
                                           message_title=message_title,
                                           message_body=message_body)

                else:
                    new_user = User(
                        email=form.email.data,
                        first_name=form.first_name.data,
                        surname=form.surname.data,
                        password_hash=generate_password_hash(
                            form.password.data))
                    send_confirmation_email(new_user.email)
                    db.session.add(new_user)
                    db.session.commit()
            except (ValueError, TypeError):
                message_body = 'Registration failed'
                message_title = 'Error!'
                return render_template('message.html',
                                       message_title=message_title,
                                       message_body=message_body)
        else:
            return render_template('registration.html',
                                   form=form,
                                   error=form.errors)
        message_body = 'The registration was successful.'
        message_title = 'Success!'
        return render_template('message.html',
                               message_title=message_title,
                               message_body=message_body)


@library.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        try:
            retrieve_book_data = db.session.query(Book).all()
        except TimeoutError:
            return abort(500)

        books = []
        for row in retrieve_book_data:
            book = []
            book.append(row.id)
            book.append(row.original_title)
            book.append([])
            while row.authors is not None:
                try:
                    book[2].append(str(row.authors.pop()))
                except IndexError:
                    break

            books.append(book)
        books.sort(key=lambda x: x[2])

        return render_template('search.html',
                               title='Search',
                               books=books)
    else:
        return abort(405)


@library.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        email_template = open(
            './templates/contact_confirmation.html', 'r').read()
        try:
            send_email(
                'Contact confirmation, title: ' + form.title.data,
                DevConfig.MAIL_USERNAME,
                [form.email.data],
                None,
                email_template)

            send_email(
                'Contact form: ' + form.title.data,
                DevConfig.MAIL_USERNAME,
                [DevConfig.MAIL_USERNAME],
                'Send by: ' + form.email.data + '\n\n' + form.message.data,
                None)
            return SuccessMessage\
                .message('Your email has been sent to administrator!')
        except TimeoutError:
            return ErrorMessage\
                .message('Oops, '
                         'some problem occurred'
                         ' and your email has not been sent ')
    return render_template('contact.html',
                           title='Contact',
                           form=form,
                           error=form.errors)


@library.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')


@library.route('/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(DevConfig.SECRET_KEY)
        email = confirm_serializer.loads(token,
                                         salt='email-confirmation-salt',
                                         max_age=3600)
    except RuntimeError:
        message_body = 'The confirmation link is invalid or has expired.'
        message_title = 'Error!'
        return render_template('message.html',
                               message_title=message_title,
                               message_body=message_body)

    user = User.query.filter_by(email=email).first()

    if user.active:
        message_body = 'Account already confirmed. Please login.'
        message_title = 'Error!'
        return render_template('message.html',
                               message_title=message_title,
                               message_body=message_body)
    else:
        user.active = True
        db.session.add(user)
        db.session.commit()
        message_body = 'Thank you for confirming your email address!'
        message_title = 'Success!'
        return render_template('message.html',
                               message_title=message_title,
                               message_body=message_body)


@library.route('/reset', methods=['GET', 'POST'])
def reset():
    form = ForgotPass()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.active:
                send_password_reset_email(user.email)
                message_body = 'Please check your email \
                                for a password reset link.'
                message_title = 'Success!'
                return render_template('message.html',
                                       message_title=message_title,
                                       message_body=message_body)
            else:
                message_body = 'Your email address must be confirmed \
                                before attempting a password reset.'
                message_title = 'Error!'
                return render_template('message.html',
                                       message_title=message_title,
                                       message_body=message_body)
        else:
            message_body = "This email doesn't exist"
            message_title = 'Error!'
            return render_template('message.html',
                                   message_title=message_title,
                                   message_body=message_body)
    return render_template('forgot_pass.html', form=form, error=form.errors)


@library.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        password_reset_serializer = URLSafeTimedSerializer(
            DevConfig.SECRET_KEY)
        email = password_reset_serializer.loads(token,
                                                salt='password-reset-salt',
                                                max_age=3600)
    except RuntimeError:
        message_body = 'The password reset link is invalid or has expired.'
        message_title = 'Error!'
        return render_template('message.html',
                               message_title=message_title,
                               message_body=message_body)

    form = PasswordForm()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=email).first_or_404()
        except ValueError:
            message_body = 'Invalid email address!'
            message_title = 'Error!'
            return render_template('message.html',
                                   message_title=message_title,
                                   message_body=message_body)

        user.password_hash = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('library.login'))

    return render_template('reset_password_with_token.html',
                           form=form,
                           token=token,
                           error=form.errors)


@library.route('/reservation/<copy_id>')
def reserve(copy_id):
    if 'logged_in' in session:
        try:
            copy = Copy.query.get(copy_id)
            copy.available_status = False
            res = RentalLog(
                copy_id=copy_id,
                user_id=session['id'],
                book_status=BookStatus.RESERVED,
                reservation_begin=datetime.now(tz=pytz.utc),
                reservation_end=datetime.now(tz=pytz.utc) + timedelta(hours=48)
            )
            db.session.add(res)
            db.session.commit()
            flash('pick up the book within two days!', 'Reservation done!')
        except IntegrityError:
            abort(500)
    return redirect(url_for('library.index'))


@library.route('/remove_item/<int:item_id>', methods=['GET', 'POST'])
def remove_item(item_id):
    try:
        user = User.query.get(session['id'])
        admin = user.has_role('ADMIN')
    except KeyError:
        abort(401)
    except Exception:
        abort(500)
    form = RemoveForm()
    item = LibraryItem.query.get_or_404(item_id)
    if form.validate_on_submit():
        db.session.delete(item)
        db.session.commit()
        flash('Item has been removed', 'success')
    authors_list = []
    if item.type == 'book':
        authors_list = item.authors_string
    return render_template('remove_item.html',
                           form=form,
                           item=item,
                           authors_list=authors_list,
                           admin=admin)


@library.route('/remove_copy/<int:item_id>/<int:copy_id>',
               methods=['GET', 'POST'])
def remove_copy(item_id, copy_id):
    try:
        user = User.query.get(session['id'])
        admin = user.has_role('ADMIN')
    except KeyError:
        abort(401)
    except Exception:
        abort(500)
    form = RemoveForm()
    item = LibraryItem.query.get_or_404(item_id)
    copy = Copy.query.filter_by(id=copy_id).first_or_404()
    authors_list = []
    if item.type == "book":
        authors_list = item.authors_string
    if form.validate_on_submit():
        db.session.delete(copy)
        db.session.commit()
        flash('Copy has been removed', 'success')
    return render_template('remove_copy.html',
                           form=form,
                           item=item,
                           copy=copy,
                           authors_list=authors_list,
                           admin=admin)


@library.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    try:
        user = User.query.get(session['id'])
        admin = user.has_role('ADMIN')
    except KeyError:
        abort(401)
    except Exception:
        abort(500)

    data = db.session.query(WishListItem).all()
    wish_list_schema = WishListItemSchema(many=True)
    output = wish_list_schema.dump(data)
    return render_template('wishlist.html', wishes=output, admin=admin)


@library.route('/addWish', methods=['GET', 'POST'])
def add_wish():
    form = WishlistForm()
    if form.validate_on_submit():
        try:
            new_wish_item = WishListItem(authors=form.authors.data,
                                         item_type=form.type.data,
                                         title=form.title.data,
                                         pub_year=datetime.strptime(
                                             form.pub_date.data,
                                             "%Y").date())

            db.session.add(new_wish_item)
            db.session.commit()
            return redirect(url_for('library.wishlist'))
        except exc.SQLAlchemyError:
            return ErrorMessage.message(error_body='Oops something went wrong')
    return render_template('wishlist_add.html', form=form, error=form.errors)


@library.route('/addLike', methods=['GET', 'POST'])
def add_like():
    wish_id = request.form['wish_id']
    user = User.query.filter_by(id=session['id']).first()
    if not Like.like_exists(wish_id, user):
        try:
            Like.like(wish_id, user)
        except exc.SQLAlchemyError:
            return ErrorMessage.message(error_body='Oops something went wrong')
    else:
        try:
            Like.unlike(wish_id, user)
        except exc.SQLAlchemyError:
            return ErrorMessage.message(error_body='Oops something went wrong')
    return json.dumps({'num_of_likes': len(WishListItem.query
                                                       .filter_by(id=wish_id)
                                                       .first().likes)})


@library.route('/delete-wish/<int:wish_id>', methods=['GET', 'POST'])
def delete_wish(wish_id):
    try:
        WishListItem.delete_wish(wish_id)
    except exc.SQLAlchemyError:
            return ErrorMessage.message(error_body='Oops something went wrong')
    return redirect(url_for('library.wishlist'))


@library.route('/item_description/<int:item_id>')
def item_description(item_id):
    try:
        user = User.query.get(session['id'])
        admin = user.has_role('ADMIN')
    except KeyError:
        abort(401)
    except Exception:
        abort(500)
    item = LibraryItem.query.get_or_404(item_id)
    tags_list = item.tags_string

    authors_list = []
    if item.type == 'book':
        authors_list = item.authors_string

    return render_template('item_description.html',
                           item=item,
                           tags_list=tags_list,
                           authors_list=authors_list,
                           admin=admin)


@library.route('/add_copy/<int:item_id>', methods=['GET', 'POST'])
def add_copy(item_id):
    form = CopyAddForm()
    if form.validate_on_submit():
        try:
            new_copy = Copy(
                asset_code=form.asset_code.data,
                library_item_id=item_id,
                shelf=form.shelf.data,
                has_cd_disk=form.has_cd_disk.data,
                available_status=True,
            )
            db.session.add(new_copy)
            db.session.commit()
            flash('Copy successfully added!')
            return redirect(url_for('library.item_description',
                                    item_id=item_id))
        except IntegrityError:
            abort(500)
    return render_template('copy_form.html',
                           form=form,
                           error=form.errors,
                           action='Add')


@library.route('/edit_copy/<int:copy_id>', methods=['GET', 'POST'])
def edit_copy(copy_id):
    copy = Copy.query.get_or_404(copy_id)
    item_id = copy.library_item_id
    form = CopyEditForm()
    if form.validate_on_submit():
        try:
            copy.asset_code = form.asset_code.data
            copy.shelf = form.shelf.data
            copy.has_cd_disk = form.has_cd_disk.data
            db.session.commit()
            flash('Copy successfully edited!')
            return redirect(url_for('library.item_description',
                                    item_id=item_id))
        except IntegrityError:
            abort(500)
    form.asset_code.data = copy.asset_code
    form.shelf.data = copy.shelf
    form.has_cd_disk.data = copy.has_cd_disk
    return render_template('copy_form.html',
                           form=form,
                           error=form.errors,
                           action='Edit')


@library.errorhandler(401)
def not_authorized(error):
    message_body = 'You are not authorized to visit this site!'
    message_title = 'Error!'
    return render_template('message.html',
                           message_title=message_title,
                           message_body=message_body), 401


@library.errorhandler(404)
def not_found(error):
    message_body = 'Page does not exist!'
    message_title = 'Error!'
    return render_template('message.html',
                           message_title=message_title,
                           message_body=message_body), 404


@library.errorhandler(405)
def method_not_allowed(error):
    message_body = 'Method not allowed!'
    message_title = 'Error!'
    return render_template('message.html',
                           message_title=message_title,
                           message_body=message_body), 405


@library.errorhandler(500)
def server_error(error):
    message_body = 'but something went wrong.'
    message_title = 'Don\'t panic!'
    return render_template('message.html',
                           message_title=message_title,
                           message_body=message_body), 500
