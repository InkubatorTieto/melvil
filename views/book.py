from datetime import datetime

from flask import Blueprint
from flask import render_template, request, session, abort
from copy import copy

from forms.book import BookForm, MixedForm, MagazineForm
from init_db import db
from models import User, Tag, Magazine, Book, Author, LibraryItem

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
            form = MixedForm()

        return render_template('add_book.html',
                               form=form,
                               error=form.errors
                               )
    else:
        form = MixedForm()
        if form.radio.data == 'book':
            del form.issue
            del form.title_of_magazine
            if form.validate_on_submit():
                tmp_authors = [[form.first_name.data, form.surname.data],
                               [form.first_name_1.data, form.surname_1.data],
                               [form.first_name_2.data, form.surname_2.data],
                               ]

                new_authors = []

                for first_name, surname in tmp_authors:
                    if first_name is not '' and surname is not '':
                        author = Author.query.filter_by(first_name=first_name,
                                                        last_name=surname
                                                        ).first()
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

            return render_template('add_book.html',
                                   form=form,
                                   error=form.errors)

        if form.radio.data == 'magazine':
            del form.publisher
            del form.original_title
            del form.isbn
            del form.title
            if form.validate_on_submit():

                tmp_tag = Tag.query.filter_by(name=form.tag.data).first()
                if not tmp_tag:
                    new_tag = Tag(
                        name=form.tag.data
                    )
                    db.session.add(new_tag)
                    db.session.commit()
                else:
                    new_tag = tmp_tag

                new_magazine = Magazine(
                    # for library_item model
                    title=form.title_of_magazine.data,
                    table_of_contents=form.table_of_contents.data,
                    language=form.language.data,
                    category=form.category.data,
                    tags=[new_tag],
                    description=form.description.data,
                    # for magazine model
                    year=datetime(year=int(form.pub_date.data),
                                  month=1,
                                  day=1),
                    issue=form.issue.data)

                db.session.add(new_magazine)
                db.session.commit()

                message_body = 'The magazine has been added.'
                message_title = 'Success!'
                return render_template('message.html',
                                       message_title=message_title,
                                       message_body=message_body)

            return render_template('add_book.html',
                                   form=form,
                                   error=form.errors)


@library_books.route('/edit_book/<int:item_id>', methods=['GET', 'POST'])
def edit_book(item_id):
    if request.method == 'GET':
        try:
            user = User.query.get(session['id'])
            admin = user.has_role('ADMIN')
        except KeyError:
            abort(401)
        except Exception:
            abort(500)

        item = LibraryItem.query.get_or_404(item_id)

        if item.type == 'book':
            form = create_get_form(item)
            return render_template('edit_book.html',
                                   form=form,
                                   error=form.errors,
                                   item_type=item.type)

        elif item.type == 'magazine':
            form = MagazineForm(
                title_of_magazine=item.title,
                issue=item.issue,
                table_of_contents=item.table_of_contents,
                language=item.language,
                category=item.category,
                tag=item.tags_string,
                description=item.description,
                pub_date=item.year
            )

            return render_template('edit_book.html',
                                   form=form,
                                   error=form.errors,
                                   item_type=item.type)

    else:

        item = LibraryItem.query.get_or_404(item_id)
        print(item)
        if item.type == 'book':
            form = BookForm(radio='book')
            to_validate = check_diff_book(form, item)
            for i in to_validate:
                i.validate(form)

            if not form.errors:
                update_book(form, item)
                message_body = 'The book has been updated.'
                message_title = 'Success!'
                return render_template('message.html',
                                       message_title=message_title,
                                       message_body=message_body)

            return render_template('edit_book.html',
                                   item_id=item.id,
                                   item_type=item.type,
                                   form=form,
                                   error=form.errors)
        if item.type == 'magazine':
            form = MagazineForm(radio='magazine')
            to_validate = check_diff_magazine(form, item)
            for i in to_validate:
                i.validate(form)

            if not form.errors:
                update_magazine(form, item)

                message_body = 'The magazine has been updated.'
                message_title = 'Success!'
                return render_template('message.html',
                                       message_title=message_title,
                                       message_body=message_body)

            return render_template('edit_book.html',
                                   item_id=item.id,
                                   item_type=item.type,
                                   form=form,
                                   error=form.errors)
        else:
            message_body = 'Oops something went wrong'
            message_title = 'Error!'
            return render_template('message.html',
                                   message_title=message_title,
                                   message_body=message_body)


def create_get_form(item):
    authors_list = item.authors
    if len(authors_list) == 1:
        form = BookForm(
            title=item.title,
            table_of_contents=item.table_of_contents,
            language=item.language,
            category=item.category,
            tag=item.tags_string,
            description=item.description,
            isbn=item.isbn,
            original_title=item.original_title,
            publisher=item.publisher,
            pub_date=item.pub_date,
            first_name=authors_list[0].first_name,
            surname=authors_list[0].last_name
        )

    elif len(authors_list) == 2:
        form = BookForm(
            title=item.title,
            table_of_contents=item.table_of_contents,
            language=item.language,
            category=item.category,
            tag=item.tags_string,
            description=item.description,
            isbn=item.isbn,
            original_title=item.original_title,
            publisher=item.publisher,
            pub_date=item.pub_date,
            first_name=authors_list[0].first_name,
            surname=authors_list[0].last_name,
            first_name_1=authors_list[1].first_name,
            surname_1=authors_list[1].last_name
        )

    elif len(authors_list) == 3:
        form = BookForm(
            title=item.title,
            table_of_contents=item.table_of_contents,
            language=item.language,
            category=item.category,
            tag=item.tags_string,
            description=item.description,
            isbn=item.isbn,
            original_title=item.original_title,
            publisher=item.publisher,
            pub_date=item.pub_date,
            first_name=authors_list[0].first_name,
            surname=authors_list[0].last_name,
            first_name_1=authors_list[1].first_name,
            surname_1=authors_list[1].last_name,
            first_name_2=authors_list[2].first_name,
            surname_2=authors_list[2].last_name
        )
    else:
        form = BookForm()
    return form


def check_diff_book(form, item):
    to_validate = []
    if form.title.data != item.title:
        to_validate.append(form.title)
    if form.table_of_contents.data != item.table_of_contents:
        to_validate.append(form.table_of_contents)
    if form.language.data != item.language:
        to_validate.append(form.language)
    if form.category.data != item.category:
        to_validate.append(form.category)
    if form.tag.data != item.tags_string:
        to_validate.append(form.tag)
    if form.description.data != item.description:
        to_validate.append(form.description)
    if form.isbn.data != item.isbn:
        to_validate.append(form.isbn)
    if form.original_title.data != item.original_title:
        to_validate.append(form.original_title)
    if form.publisher.data != item.publisher:
        to_validate.append(form.publisher)
    if form.pub_date.data != item.pub_date:
        to_validate.append(form.pub_date)
    try:
        if form.first_name.data != item.authors[0].first_name:
            to_validate.append(form.first_name)
        if form.surname.data != item.authors[0].last_name:
            to_validate.append(form.surname)
    except IndexError:
        pass

    try:
        if form.first_name_1.data != item.authors[1].first_name:
            to_validate.append(form.first_name_1)
        if form.surname_1.data == item.authors[1].last_name:
            to_validate.append(form.surname_1)
    except IndexError:
        pass

    try:
        if form.first_name_2.data != item.authors[2].first_name:
            to_validate.append(form.first_name_2)
        if form.surname_2.data == item.authors[2].last_name:
            to_validate.append(form.surname_2)
    except IndexError:
        pass
    return to_validate


def update_book(form, item):
    item.title = form.title.data
    item.table_of_contents = form.table_of_contents.data
    item.language = form.language.data
    item.category = form.category.data
    item.description = form.description.data
    item.isbn = form.isbn.data
    item.original_title = form.original_title.data
    item.publisher = form.publisher.data
    item.pub_date = datetime(year=int(form.pub_date.data),
                             month=1,
                             day=1)
    tag = Tag.query.filter_by(name=item.tags_string).first()
    tag.name = form.tag.data

    try:
        author = Author.query.filter_by(first_name=item.authors[0].first_name,
                                        last_name=item.authors[0].last_name
                                        ).first()
        author.first_name = form.first_name.data
        author.last_name = form.surname.data
    except IndexError:
        pass

    try:
        author_1 = Author.query.filter_by(first_name=item.authors[1].first_name_1,
                                          last_name=item.authors[1].last_name_2
                                          ).first()
        author_1.first_name_1 = form.first_name_1.data
        author_1.last_name_1 = form.surname_1.data
    except IndexError:
        pass

    try:
        author_2 = Author.query.filter_by(first_name=item.authors[2].first_name_2,
                                          last_name=item.authors[2].last_name_2
                                          ).first()

        author_2.first_name_2 = form.first_name_2.data
        author_2.last_name_2 = form.surname_2.data
    except IndexError:
        pass
    db.session.commit()


def check_diff_magazine(form, item):
    to_validate = []
    if form.title_of_magazine.data != item.title:
        to_validate.append(form.title_of_magazine)
    if form.table_of_contents.data != item.table_of_contents:
        to_validate.append(form.table_of_contents)
    if form.language.data != item.language:
        to_validate.append(form.language)
    if form.category.data != item.category:
        to_validate.append(form.category)
    if form.tag.data != item.tags_string:
        to_validate.append(form.tag)
    if form.description.data != item.description:
        to_validate.append(form.description)
    if form.pub_date.data != item.year:
        to_validate.append(form.pub_date)
    if form.issue.data != item.issue:
        to_validate.append(form.issue)

    return to_validate


def update_magazine(form, item):
    item.title = form.title_of_magazine.data
    item.table_of_contents = form.table_of_contents.data
    item.language = form.language.data
    item.category = form.category.data
    item.description = form.description.data
    item.issue = form.issue.data
    item.year = datetime(year=int(form.pub_date.data),
                         month=1,
                         day=1)
    tag = Tag.query.filter_by(name=item.tags_string).first()
    tag.name = form.tag.data
    db.session.commit()


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
