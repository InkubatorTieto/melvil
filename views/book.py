from flask import render_template, request, session
from forms.book import BookForm
from flask import Blueprint
from datetime import datetime
from models.books import Book, Author
from models.library import Tag
from init_db import db

library_books = Blueprint('library_books', __name__,
                          template_folder='templates')


@library_books.route('/add_book', methods=['GET', 'POST'])
def add_book():

    if request.method == 'GET':
        if 'logged_in' not in session:
            message_body = 'You are not logged in.'
            message_title = 'Error!'
            return render_template('message.html',
                                   message_title=message_title,
                                   message_body=message_body)
        else:
            form = BookForm()

        return render_template('add_book.html',
                               form=form,
                               error=form.errors)
    else:
        form = BookForm()
        if form.validate_on_submit():
            tmp_authors = [[form.first_name.data, form.surname.data],
                           [form.first_name_1.data, form.surname_1.data],
                           [form.first_name_2.data, form.surname_2.data],
                           ]

            new_authors = []

            for first_name, surname in tmp_authors:
                if first_name is not '' and surname is not '':
                    author = Author.query.filter_by(first_name=first_name,
                                                    last_name=surname).first()
                    if not author:
                        new_author = Author(
                            first_name=first_name,
                            last_name=surname
                        )
                        new_authors.append(new_author)
                        db.session.add(new_author)
                        db.session.commit()
                    else:
                        new_authors.append(author)

            tmp_tag = Tag.query.filter_by(name=form.tag.data).first()
            if not tmp_tag:
                new_tag = Tag(
                    name=form.tag.data
                )
                db.session.add(new_tag)
                db.session.commit()
            else:
                new_tag = tmp_tag

            new_book = Book(
                # for library_item model
                title=form.title.data,
                table_of_contents=form.table_of_contents.data,
                language=form.language.data,
                category=form.category.data,
                tags=[new_tag],
                description=form.description.data,
                # for Book model
                isbn=form.isbn.data,
                authors=new_authors,
                original_title=form.original_title.data,
                publisher=form.publisher.data,
                pub_date=datetime(year=int(form.pub_date.data),
                                  month=1,
                                  day=1))
            if book_exists(new_book):
                message_body = 'This book already exists.'
                message_title = 'Oops!'
                return render_template('message.html',
                                       message_title=message_title,
                                       message_body=message_body)
            db.session.add(new_book)
            db.session.commit()

            message_body = 'The book has been added.'
            message_title = 'Success!'
            return render_template('message.html',
                                   message_title=message_title,
                                   message_body=message_body)
        # print(form.errors)
        return render_template('add_book.html',
                               form=form,
                               error=form.errors)


def book_exists(newbook):
    results = Book.query.filter(Book.title.startswith(newbook.title[:2])).all()
    for i in results:
        if i.isbn == newbook.isbn:
            return False
        i = str(i.title)
        i = i.replace(" ", "").replace("_", "") \
            .replace("-", "").replace(",", ""). \
            replace(".", "").lower()
        tmp = str(newbook.title)
        tmp = tmp.replace(" ", "").replace("_", "") \
            .replace("-", "").replace(",", ""). \
            replace(".", "").lower()
        if i == tmp:
            return False
        else:
            return True
