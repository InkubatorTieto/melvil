from flask import render_template, request, session
from forms.book import BookForm
from flask import Blueprint

library_books = Blueprint('library_books', __name__,
                          template_folder='templates')


@library_books.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'GET':
        # if 'logged_in' not in session:
        #     message_body = 'You are not logged in.'
        #     message_title = 'Error!'
        #     return render_template('message.html',
        #                            message_title=message_title,
        #                            message_body=message_body)
        # else:
        form = BookForm()
        return render_template('add_book.html',
                               form=form,
                               error=form.errors)
    else:
        form = BookForm()

        # if form.validate_on_submit():
        print( form.pub_date.data)
        print(form.title.data)

        return render_template('add_book.html',
                               form=form,
                               error=form.errors)
