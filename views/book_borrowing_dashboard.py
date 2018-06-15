from flask import render_template, session
from flask import Blueprint
from init_db import db
from sqlalchemy import desc

library_book_boorrowing_dashboard = Blueprint('library_book_borrowing_dashboard', __name__,
                          template_folder='templates')

@library_book_boorrowing_dashboard.route('/borrowedBooks', methods=["GET", "POST"])
def book_borrowing_dashboad():

    if 'logged_in' in session:
        reserved_items = db.session.query(LibraryItem, RentalLog._reservation_begin,
                                          RentalLog._reservation_end).\
            filter(RentalLog.book_status == BookStatus.RESERVED).\
            filter(RentalLog.user_id == session['id']).\
            filter(RentalLog.copy_id == Copy.id).\
            filter(LibraryItem.id == Copy.library_item_id). \
            order_by(desc(RentalLog._reservation_begin)).\
            all()

        borrowed_items = db.session.query(LibraryItem, RentalLog._borrow_time,
                                          RentalLog._return_time).\
            filter(RentalLog.book_status == BookStatus.BORROWED).\
            filter(RentalLog.user_id == session['id']). \
            filter(RentalLog.copy_id == Copy.id). \
            filter(LibraryItem.id == Copy.library_item_id). \
            order_by(desc(RentalLog._borrow_time)).\
            all()

        num_of_reserved = db.session.query(LibraryItem, RentalLog._reservation_begin,
                                           RentalLog._reservation_begin). \
            filter(RentalLog.book_status == BookStatus.RESERVED).\
            filter(RentalLog.user_id == session['id']).\
            filter(RentalLog.copy_id == Copy.id).\
            filter(LibraryItem.id == Copy.library_item_id). \
            count()

        num_of_borrowed = db.session.query(LibraryItem, RentalLog._borrow_time,
                                           RentalLog._return_time).\
            filter(RentalLog.book_status == BookStatus.BORROWED).\
            filter(RentalLog.user_id == session['id']).\
            filter(RentalLog.copy_id == Copy.id).\
            filter(LibraryItem.id == Copy.library_item_id).\
            count()

        return render_template('book_borrowing_dashboard.html', reserved_books=reserved_items,
                               borrowed_books=borrowed_items, num_of_reserved=num_of_reserved,
                               num_of_borrowed=num_of_borrowed)

    else:
        message_title = "Login Required"
        message_body = "You must log in first!"
        return render_template('message.html',
                               message_title=message_title,
                               message_body=message_body)
