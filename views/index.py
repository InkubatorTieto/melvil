from datetime import datetime, timedelta

from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import MultiDict
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

from config import Config
from forms.copy import CopyAddForm, CopyEditForm
from forms.forms import (
    BorrowForm,
    ContactForm,
    LoginForm,
    ReturnForm,
    SearchForm,
    WishlistForm,
    RemoveForm
)
from init_db import db
from ldap_utils.ldap_utils import ldap_client, refine_data
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
from send_email.emails import send_email
from utils.search_book import search_book


library = Blueprint('library', __name__,
                    template_folder='templates')


@library.route('/')
def index():
    return render_template('index.html')


@library.route('/login', methods=['GET', 'POST'])
@require_not_logged_in()
def login():

    """
    Login view for client.
    Connects to active directory check credentials
    and login.
    Retrieves desired data about user from LDAP.
    """

    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = form.username.data
            passwd = form.password.data
            test_conn = ldap_client.bind_user(user, passwd)
            message_title = 'Error!'
            if not test_conn or passwd == '':
                message_body = 'Invalid username and/or password'
                return render_template(
                    'message.html',
                    message_title=message_title,
                    message_body=message_body
                )
            else:
                user_ldap = ldap_client.get_object_details(user=user)
                if refine_data(user_ldap, 'l') != 'Wroclaw':
                    message_body = 'Only employees from Wroclaw are accepted'
                    return render_template(
                        'message.html',
                        message_title=message_title,
                        message_body=message_body
                    )
                user_ldap_data = {
                    'mail': refine_data(user_ldap, 'mail'),
                    'givenName': refine_data(user_ldap, 'givenName'),
                    'sn': refine_data(user_ldap, 'sn'),
                    'employeeID': refine_data(user_ldap, 'employeeID')
                }
                user_db = User.query.filter_by(
                    employee_id=user_ldap_data['employeeID']
                ).first()
                if not user_db:
                    new_user = User(
                        email=user_ldap_data['mail'],
                        first_name=user_ldap_data['givenName'],
                        surname=user_ldap_data['sn'],
                        employee_id=user_ldap_data['employeeID'],
                        active=True
                    )
                    db.session.add(new_user)
                    db.session.commit()
                else:
                    user_db_data = {
                        'mail': user_db.email,
                        'givenName': user_db.first_name,
                        'sn': user_db.surname,
                        'employeeID': user_db.employee_id
                    }
                    if user_db_data != user_ldap_data:
                        user_db.email = user_ldap_data['mail']
                        user_db.first_name = user_ldap_data['givenName']
                        user_db.surname = user_ldap_data['sn']
                        user_db.employee_id = user_ldap_data['employeeID']
                        db.session.commit()

                user_db = User.query.filter_by(
                    employee_id=user_ldap_data['employeeID']
                ).first()
                session['logged_in'] = True
                session['id'] = user_db.id
                session['email'] = user_db.email
                if user_db.has_role('ADMIN'):
                    session['admin'] = True
                return render_template('index.html', session=session)
    elif request.method != 'GET':
        abort(405)

    return render_template('login.html',
                           form=form,
                           error=form.errors)


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
        if not request.args.get('query'):
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
            form = SearchForm(formdata=MultiDict({
                'query': request.args.get('query'),
                'search_by': request.args.get('search_by')
            }))
            search_by = request.args.get('search_by')
            query_str = request.args.get('query')
            page = request.args.get('page', 1, type=int)
            try:
                paginate_query = LibraryItem.query.filter(
                    search_book(search_by, query_str)
                ).paginate(page, error_out=True, max_per_page=10)
                output = [d.serialize() for d in paginate_query.items]
            except RuntimeError:
                return ErrorMessage.message('Cannot connect to database!')
            return render_template('search.html',
                                   all_query=output,
                                   pagination=paginate_query,
                                   endpoint='library.search',
                                   admin=admin,
                                   form=form,
                                   query_str=query_str,
                                   search_by=search_by)
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
                Config.MAIL_SENDER,
                [form.email.data],
                None,
                email_template)
            send_email(
                'Contact form: ' + form.title.data,
                Config.MAIL_SENDER,
                [Config.MAIL_ADMINS],
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


@library.route('/reservation/<copy_id>')
@require_logged_in()
def reserve(copy_id):
    try:
        copy = Copy.query.get(copy_id)
        if copy.available_status != BookStatus.RETURNED:
            abort(409)
        copy.available_status = BookStatus.RESERVED
        reservation_begin = datetime.now(tz=pytz.utc)

        res = RentalLog(
            copy_id=copy_id,
            user_id=session['id'],
            book_status=BookStatus.RESERVED,
            reservation_begin=reservation_begin,
            reservation_end=(
                reservation_begin
                .replace(hour=23, minute=59, second=59, microsecond=0) +
                timedelta(days=2)
            )
        )
        db.session.add(res)
        db.session.commit()
        flash('Pick up the book within two days!')
    except IntegrityError:
        abort(500)
    return redirect(url_for(
        'library_book_borrowing_dashboard.book_borrowing_dashboad'))


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
            copy_id = request.args.get('copy_id')
            borrow_item = Copy.query.filter_by(id=copy_id). \
                first_or_404()
            rental_log_change = RentalLog.query.filter_by(
                copy_id=copy_id
            ).order_by(RentalLog.id.desc()).first_or_404()
            try:
                borrow_time = datetime.now(tz=pytz.utc)

                borrow_item.available_status = BookStatus.BORROWED
                rental_log_change.book_status = BookStatus.BORROWED
                rental_log_change._borrow_time = borrow_time
                rental_log_change._return_time = borrow_time \
                    .replace(hour=23, minute=59, second=59, microsecond=0) \
                    + timedelta(days=30)
                db.session.commit()
            except exc.SQLAlchemyError:
                abort(500)
            flash('Item borrowed')
            return redirect(url_for('library.admin_dashboard'))

        if return_form.submit.data and return_form.validate_on_submit():
            copy_asset = request.args.get('asset')
            borrow_item = Copy.query.filter_by(asset_code=copy_asset).first()
            rental_log_change = RentalLog.query.filter_by(
                copy_id=borrow_item.id
            ).order_by(RentalLog.id.desc()).first_or_404()
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


@library.errorhandler(409)
def conflict(error):
    message_body = 'Someone already changed this resource!'
    message_title = 'Conflict!'
    return render_template('message.html',
                           message_title=message_title,
                           message_body=message_body), 409


@library.errorhandler(500)
def server_error(error):
    message_body = 'but something went wrong.'
    message_title = 'Don\'t panic!'
    return render_template('message.html',
                           message_title=message_title,
                           message_body=message_body), 500
