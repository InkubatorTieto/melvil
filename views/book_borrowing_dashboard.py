from flask import render_template, session
from flask import Blueprint
from init_db import db
from sqlalchemy import desc
from models import LibraryItem
from models.library import RentalLog, Copy, BookStatus

library_book_borrowing_dashboard = \
    Blueprint('library_book_borrowing_dashboard', __name__,
              template_folder='templates')


@library_book_borrowing_dashboard.route(
    '/borrowedBooks', methods=["GET", "POST"])
def book_borrowing_dashboad():

    if 'logged_in' in session:
        current_user_id = session['id']
        reserved_items = get_reserved_items(db.session, current_user_id)
        borrowed_items = get_borrowed_items(db.session, current_user_id)
        num_of_reserved = len(reserved_items)
        num_of_borrowed = len(borrowed_items)

        return render_template('book_borrowing_dashboard.html',
                               reserved_books=reserved_items,
                               borrowed_books=borrowed_items,
                               num_of_reserved=num_of_reserved,
                               num_of_borrowed=num_of_borrowed)

    else:
        message_title = "Login Required"
        message_body = "You must log in first!"
        return render_template('message.html',
                               message_title=message_title,
                               message_body=message_body)


def get_reserved_items(s_db, current_user_id):
    reserved_items = s_db.query(LibraryItem, RentalLog._reservation_begin,
                                RentalLog._reservation_end). \
        filter(RentalLog.book_status == BookStatus.RESERVED). \
        filter(RentalLog.user_id == current_user_id). \
        filter(RentalLog.copy_id == Copy.id). \
        filter(LibraryItem.id == Copy.library_item_id). \
        order_by(desc(RentalLog._reservation_begin)). \
        all()
    return reserved_items


def get_borrowed_items(s_db, current_user_id):
    borrowed_items = s_db.query(LibraryItem, RentalLog._borrow_time,
                                RentalLog._return_time). \
        filter(RentalLog.book_status == BookStatus.BORROWED). \
        filter(RentalLog.user_id == current_user_id). \
        filter(RentalLog.copy_id == Copy.id). \
        filter(LibraryItem.id == Copy.library_item_id). \
        order_by(desc(RentalLog._borrow_time)). \
        all()
    return borrowed_items
