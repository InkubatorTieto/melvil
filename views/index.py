from datetime import datetime, timedelta

from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError
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
from forms.edit_profile import EditProfileForm
from forms.forms import (
    BorrowForm,
    ContactForm,
    ForgotPass,
    LoginForm,
    PasswordForm,
    RegistrationForm,
    ReturnForm,
    SearchForm,
    WishlistForm,
    RemoveForm,
    EditPasswordForm
)
from init_db import db
from messages import ErrorMessage, SuccessMessage
from models import LibraryItem
from models.library import RentalLog, Copy, BookStatus
from models.users import User
from models.wishlist import WishListItem, Like
from models.decorators_roles import (
    require_role,
    require_logged_in,
    require_not_logged_in
)
from send_email import send_confirmation_email, send_password_reset_email
from send_email.emails import send_email

library = Blueprint('library', __name__,
                    template_folder='templates')


@library.route('/')
def index():
    return render_template('index.html')


@library.route('/login', methods=['GET', 'POST'])
@require_not_logged_in()
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
                    if data.has_role('ADMIN'):
                        session['admin'] = True
                    return render_template('index.html',
                                           session=session)
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
@require_not_logged_in()
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
@require_logged_in()
def search():
    try:
        user = User.query.get(session['id'])
        admin = user.has_role('ADMIN')
    except KeyError:
        abort(401)
    except Exception:
        abort(500)
    if request.method == 'GET':
        if not request.args or not request.args.get('query'):
            form = SearchForm()
            page = request.args.get('page', 1, type=int)
            try:
                paginate_query = LibraryItem.query.order_by(
                    LibraryItem.title.asc()).paginate(page,
                                                      error_out=True,
                                                      max_per_page=10)
                output = [d.serialize() for d in paginate_query.items]
                return render_template('search.html',
                                       all_query=output,
                                       admin=admin,
                                       pagination=paginate_query,
                                       endpoint='library.search',
                                       form=form)
            except RuntimeError:
                return ErrorMessage.message('Cannot connect to database!')
        elif request.args.get('query'):
            form = SearchForm()
            query_str = request.args.get('query')
            page = request.args.get('page', 1, type=int)
            try:
                paginate_query = (
                    LibraryItem.query.filter(LibraryItem.title.ilike(
                        '%{}%'.format(query_str)))).paginate(page,
                                                             error_out=True,
                                                             max_per_page=10)
                output = [d.serialize() for d in paginate_query.items]
            except RuntimeError:
                return ErrorMessage.message('Cannot connect to database!')
            return render_template('search.html',
                                   all_query=output,
                                   pagination=paginate_query,
                                   endpoint='library.search',
                                   admin=admin,
                                   form=form, )
        else:
            abort(405)


@library.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        email_template = open(
            './templates/email_template/contact_confirmation.html', 'r').read()
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
            return SuccessMessage \
                .message('Your email has been sent to administrator!')
        except TimeoutError:
            return ErrorMessage \
                .message('Oops, '
                         'some problem occurred'
                         ' and your email has not been sent ')
    return render_template('contact.html',
                           title='Contact',
                           form=form,
                           error=form.errors)


@library.route('/logout')
@require_logged_in()
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
@require_not_logged_in()
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
            message_title = '!'
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
@require_logged_in()
def reserve(copy_id):
    try:
        copy = Copy.query.get(copy_id)
        copy.available_status = BookStatus.RESERVED
        res = RentalLog(
            copy_id=copy_id,
            user_id=session['id'],
            book_status=BookStatus.RESERVED,
            reservation_begin=datetime.now(tz=pytz.utc),
            reservation_end=datetime.now(
                tz=pytz.utc) + timedelta(minutes=2))
        db.session.add(res)
        db.session.commit()
        flash('Pick up the book within two days!')
    except IntegrityError:
        abort(500)
    return redirect(url_for(
        'library_book_borrowing_dashboard.book_borrowing_dashboad'))


@library.route('/check_reservation_status_db')
def check_reservation_status_db():
    reserved_list = db.session.query(RentalLog) \
        .filter(RentalLog.book_status == BookStatus.RESERVED) \
        .all()
    db.session.query(Copy).filter(
        Copy.id.in_([obj.copy_id for obj in reserved_list])
    ).update(
        {Copy.available_status: BookStatus.RETURNED},
        synchronize_session='fetch'
    )
    db.session.query(RentalLog) \
        .filter(RentalLog.book_status == BookStatus.RESERVED) \
        .update({RentalLog.book_status: BookStatus.RETURNED})
    db.session.commit()
    return "OK"


@library.route('/remove_item/<int:item_id>', methods=['GET', 'POST'])
@require_role('ADMIN')
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
        flash(item.type.capitalize() + ' has been removed.')
        return redirect(url_for('library.search'))
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
@require_role('ADMIN')
def remove_copy(item_id, copy_id):
    user = User.query.get(session['id'])
    admin = user.has_role('ADMIN')
    form = RemoveForm()
    item = LibraryItem.query.get_or_404(item_id)
    copy = Copy.query.filter_by(id=copy_id).first_or_404()
    authors_list = []
    if item.type == "book":
        authors_list = item.authors_string
    if form.validate_on_submit():
        db.session.delete(copy)
        db.session.commit()
        flash('Copy has been removed.')
        return redirect(url_for('library.item_description',
                                item_id=item_id))
    return render_template('remove_copy.html',
                           form=form,
                           item=item,
                           copy=copy,
                           authors_list=authors_list,
                           admin=admin)


@library.route('/wishlist', methods=['GET', 'POST'])
@require_logged_in()
def wishlist():
    user = User.query.get(session['id'])
    admin = user.has_role('ADMIN')
    if request.method == 'GET':
        if not request.args or not request.args.get('query'):
            form = SearchForm()
            page = request.args.get('page', 1, type=int)
            if db.session.query(WishListItem).first() is None:
                return render_template('wishlist.html', admin=admin)
            try:
                data = (
                    WishListItem.query.order_by(
                        WishListItem.likes_count.desc()).order_by(
                        WishListItem.title.asc()).paginate(page,
                                                           error_out=True,
                                                           max_per_page=5))
            except RuntimeError:
                return ErrorMessage.message('Cannot connect to database!')
            output = [d.serialize() for d in data.items]
            return render_template('wishlist.html',
                                   wishes=output,
                                   admin=admin,
                                   pagination=data,
                                   endpoint='library.wishlist',
                                   form=form, )
        elif request.args.get('query'):
            form = SearchForm()
            query_str = request.args.get('query')
            page = request.args.get('page', 1, type=int)
            try:
                data = (
                    WishListItem.query.filter(WishListItem.title.ilike(
                        '%{}%'.format(query_str))).order_by(
                        WishListItem.likes_count.desc()).order_by(
                        WishListItem.title.asc()).paginate(page,
                                                           error_out=True,
                                                           max_per_page=5))
            except RuntimeError:
                return ErrorMessage.message('Cannot connect to database!')
            output = [d.serialize() for d in data.items]
            return render_template('wishlist.html',
                                   wishes=output,
                                   admin=admin,
                                   pagination=data,
                                   endpoint='library.wishlist',
                                   form=form, )
    else:
        abort(405)


@library.route('/add_wish', methods=['GET', 'POST'])
@require_logged_in()
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


@library.route('/add_like', methods=['GET', 'POST'])
@require_logged_in()
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


@library.route('/delete_wish/<int:wish_id>', methods=['GET', 'POST'])
@require_role('ADMIN')
def delete_wish(wish_id):
    try:
        WishListItem.delete_wish(wish_id)
    except exc.SQLAlchemyError:
        return ErrorMessage.message(error_body='Oops something went wrong')
    return redirect(url_for('library.wishlist'))


@library.route('/item_description/<int:item_id>')
@require_logged_in()
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
@require_role('ADMIN')
def add_copy(item_id):
    form = CopyAddForm()
    if form.validate_on_submit():
        try:
            new_copy = Copy(
                asset_code=form.asset_code.data,
                library_item_id=item_id,
                shelf=form.shelf.data,
                has_cd_disk=form.has_cd_disk.data,
                available_status=BookStatus.RETURNED,
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
@require_role('ADMIN')
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


@library.route('/edit_profile/<int:user_id>',
               methods=['GET', 'POST'])
@require_logged_in()
def edit_profile(user_id):
    try:
        user = User.query.get(session['id'])
    except KeyError:
        abort(401)
    except Exception:
        abort(500)
    form = EditProfileForm()
    if form.validate_on_submit():
        try:
            user.first_name = form.first_name.data
            user.surname = form.surname.data
            user.email = form.email.data
            db.session.commit()
            flash('Profile data has been updated!')
            return redirect(url_for('library.index'))
        except IntegrityError:
            abort(500)
    form.first_name.data = user.first_name
    form.surname.data = user.surname
    form.email.data = user.email
    return render_template('edit_profile.html',
                           form=form,
                           error=form.errors)


@library.route('/reservations', methods=['GET', 'POST'])
@require_role('ADMIN')
def admin_dashboard():
    try:
        user = User.query.get(session['id'])
        admin = user.has_role('ADMIN')
    except KeyError:
        abort(401)
    except Exception:
        abort(500)
    if request.method == 'GET':
        if not request.args or not request.args.get('search-query'):
            search_form = SearchForm(prefix="search")
            borrow_form = BorrowForm(prefix="borrow")
            return_form = ReturnForm(prefix="return")
            reserv_page = request.args.get('page', 1, type=int)
            borrow_page = request.args.get('page', 1, type=int)
            reserv_query = RentalLog.query.filter_by(book_status=1).order_by(
                RentalLog._reservation_begin.asc()).paginate(
                reserv_page, 10, False)
            borrow_query = RentalLog.query.filter_by(book_status=2).order_by(
                RentalLog._return_time.asc()).paginate(borrow_page, 10, False)
            return render_template('admin.html',
                                   reservations=reserv_query.items,
                                   borrows=borrow_query.items,
                                   admin=admin,
                                   pagin_reserv=reserv_query,
                                   pagin_borrow=borrow_query,
                                   endpoint='library.admin_dashboard',
                                   search_form=search_form,
                                   borrow_form=borrow_form,
                                   return_form=return_form)

        elif request.args.get('search-query'):
            search_form = SearchForm(prefix="search")
            borrow_form = BorrowForm(prefix="borrow")
            return_form = ReturnForm(prefix="return")
            query_str = request.args.get('search-query')
            reserv_page = request.args.get('page', 1, type=int)
            borrow_page = request.args.get('page', 1, type=int)
            reserv_query = RentalLog.query.filter_by(book_status=1).order_by(
                RentalLog._reservation_begin.asc())
            reserv_filter = reserv_query.filter(
                User.surname.ilike("%{}%".format(query_str))).paginate(
                reserv_page, 10, False)
            borrow_query = RentalLog.query.filter_by(book_status=2).order_by(
                RentalLog._return_time.asc())
            borrow_filter = borrow_query.filter(
                User.surname.ilike("%{}%".format(query_str))).paginate(
                borrow_page, 10, False)
            return render_template('admin.html',
                                   reservations=reserv_filter.items,
                                   borrows=borrow_filter.items,
                                   admin=admin,
                                   pagin_reserv=reserv_filter,
                                   pagin_borrow=borrow_filter,
                                   endpoint='library.admin_dashboard',
                                   search_form=search_form,
                                   borrow_form=borrow_form,
                                   return_form=return_form)

    elif request.method == 'POST':
        search_form = SearchForm(prefix="search")
        borrow_form = BorrowForm(prefix="borrow")
        return_form = ReturnForm(prefix="return")
        if borrow_form.submit.data and borrow_form.validate_on_submit():
            copy_asset = request.args.get('asset')
            borrow_item = Copy.query.filter_by(asset_code=copy_asset). \
                first_or_404()
            rental_log_change = RentalLog.query.filter_by(
                copy_id=borrow_item.id).first_or_404()
            try:
                borrow_item.available_status = BookStatus.BORROWED
                rental_log_change.book_status = BookStatus.BORROWED
                rental_log_change._borrow_time = datetime.now(tz=pytz.utc)
                rental_log_change._return_time = \
                    (datetime.now(tz=pytz.utc) + timedelta(days=14))
                db.session.commit()
            except exc.SQLAlchemyError:
                abort(500)
            flash('Item borrowed')
            return redirect(url_for('library.admin_dashboard'))

        if return_form.submit.data and return_form.validate_on_submit():
            copy_asset = request.args.get('asset')
            borrow_item = Copy.query.filter_by(asset_code=copy_asset).first()
            rental_log_change = RentalLog.query.filter_by(
                copy_id=borrow_item.id).first()
            try:
                borrow_item.available_status = BookStatus.RETURNED
                rental_log_change.book_status = BookStatus.RETURNED
                rental_log_change._borrow_time = None
                rental_log_change._return_time = datetime.now(tz=pytz.utc)
                db.session.commit()
            except exc.SQLAlchemyError:
                abort(500)
            flash('Item returned!')
            return redirect(url_for('library.admin_dashboard'))
    else:
        abort(500)


@library.route('/edit_password/<int:user_id>',
               methods=['GET', 'POST'])
@require_logged_in()
def edit_password(user_id):
    try:
        user = User.query.get(session['id'])
    except KeyError:
        abort(401)
    except Exception:
        abort(500)
    form = EditPasswordForm()
    if form.validate_on_submit():
        try:
            if check_password_hash(user.password_hash, form.password.data):
                user.password_hash = \
                    generate_password_hash(form.new_password.data)
                db.session.commit()
                return redirect(url_for('library.index'))
            else:
                message_body = "Incorrect current password"
                message_title = '!'
                return render_template('message.html',
                                       message_title=message_title,
                                       message_body=message_body)
        except IntegrityError:
            abort(500)
    return render_template('edit_password.html',
                           form=form,
                           error=form.errors)


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
