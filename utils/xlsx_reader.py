from datetime import datetime, timedelta

import pytz
import xlrd
from nameparser import HumanName
from sqlalchemy import and_

from init_db import db
from models import Author, Book, Copy, Magazine, User, RentalLog, BookStatus
from utils.ldap_utils import ldap_client, refine_data


def load_file(file_location):
    data = file_location
    workbook = xlrd.open_workbook(data)
    return workbook


def get_full_name(author):
    name = HumanName(str(author))

    def get_name_part(name_parts=[]):
        if name_parts:
            try:
                part_of_name = (name_parts[0] + " " + name_parts[1]).strip()
                return part_of_name
            except IndexError as e:
                print(e)
                return None

    first_name = get_name_part([name.first, name.middle])
    last_name = get_name_part([name.last, name.suffix])
    return first_name, last_name


# checking if element exist, creates new if not
def create_library_item(session, model, **kwargs):
    library_item = session.query(model).filter_by(**kwargs).first()
    if library_item:
        return library_item
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def create_copy(book, asset):
    if not asset:
        create_library_item(db.session, Copy,
                            library_item_id=book.id,
                            library_item=book)

    elif "płyta" in asset:
        create_library_item(db.session, Copy,
                            library_item_id=book.id,
                            library_item=book,
                            has_cd_disk=True)

    else:
        create_library_item(db.session, Copy,
                            library_item_id=book.id,
                            library_item=book,
                            asset_code=asset)


# reading author's data from file
def get_authors_data(authors):
    if (',' in authors and 'Jr.' not in authors) \
            or (' and ' in authors) \
            or ('&' in authors):
        split_authors = \
            authors.replace(' and ', ',').replace('&', ',').split(',')
        authors_names = []

        for auth in split_authors:
            first_name, last_name = get_full_name(auth)
            authors_names.append([first_name, last_name])
    else:
        authors_names = get_full_name(authors)

    return authors_names


# reads book's data from file
def get_book_data(file_location):
    book_list = []
    workbook = load_file(file_location)

    # excluding sheets with unnecessary data
    for sheet_index in range(workbook.nsheets - 2):
        current_sheet = workbook.sheet_by_index(sheet_index)
        rows = current_sheet.nrows

        # excluding data from the title of the column
        for row_index in range(1, rows):
            current_shelf = current_sheet.name
            title = (current_sheet.cell_value(row_index, 1)).strip()
            authors = current_sheet.cell_value(row_index, 2)
            author = get_authors_data(authors)
            asset = str(current_sheet.cell_value(row_index, 3))
            borrower_data = current_sheet.cell_value(row_index, 4)
            borrow_date = current_sheet.cell_value(row_index, 5)
            book_properties = {
                    'authors': author,
                    'title': title,
                    'asset': asset,
                    'borrower_data': borrower_data,
                    'borrow_date': borrow_date
                }

            if current_shelf != 'General':
                book_properties['current_shelf'] = current_shelf
            book_list.append(book_properties)

    return book_list


# reading magazine's data from file
def get_magazine_data(file_location):
    workbook = load_file(file_location)
    magazines_list = []
    current_sheet = workbook.sheet_by_index(2)
    rows = current_sheet.nrows

    # reading rows except the title of the column
    for row_index in range(1, rows):
        title = (current_sheet.cell_value(row_index, 1)).strip()
        year = current_sheet.cell_value(row_index, 2)
        issue = current_sheet.cell_value(row_index, 3)
        magazine_properties = {'title': title, 'year': year, 'issue': issue}
        magazines_list.append(magazine_properties)
    return magazines_list


# reading user data from LDAP and inserting it to database
def get_user_data(book_data):
    # extracts username from name and surname
    if not len(book_data['borrower_data']):
        return
    user_data = book_data['borrower_data'].lower().split()
    surname_len = len(user_data[1])
    if surname_len < 5:
        surname_part = (
            user_data[1][:surname_len] +
            user_data[1][-1] * (5-surname_len)
        )
    else:
        surname_part = user_data[1][:5]
    name_part = user_data[0][:3]
    user_name = surname_part + name_part
    # checks if user already in database, and insert it if needed
    ldap_user = ldap_client.get_object_details(user=user_name)
    ldap_employee_id = refine_data(ldap_user, 'employeeID')
    db_user = User.query.filter_by(employee_id=ldap_employee_id).first()
    if not db_user:
        new_user = User(
            email=refine_data(ldap_user, 'mail'),
            first_name=refine_data(ldap_user, 'givenName'),
            surname=refine_data(ldap_user, 'sn'),
            employee_id=refine_data(ldap_user, 'employeeID'),
            active=True
        )
        db.session.add(new_user)
        db.session.commit()
    return User.query.filter_by(employee_id=ldap_employee_id).first()


def reserve_copy(book_data, lib_item_id, asset_code):
    user = get_user_data(book_data)
    if asset_code:
        copy = Copy.query.filter(
            and_(
                Copy.library_item_id == lib_item_id,
                Copy.asset_code == asset_code
            )
        ).all()
    else:
        copy = Copy.query.filter_by(library_item_id=lib_item_id).all()
    if len(copy) > 1 and user:
        print('\nBook {} have multiple copies'.format(book_data))
        return
    elif user:
        copy[0].available_status = BookStatus.BORROWED
        return_time = datetime.now(tz=pytz.utc).replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=0
        ) + timedelta(days=30)
        borrow = RentalLog(
            copy_id=copy[0].id,
            user_id=user.id,
            book_status=BookStatus.BORROWED,
            _return_time=return_time
        )
        db.session.add(borrow)
        db.session.commit()


# writing authors, books and copies data in database
def get_books(file_location):
    books_properties = get_book_data(file_location)
    asset_codes = []
    for book in books_properties:
        try:
            title = book['title']
            asset = book['asset']
            asset_codes.append(asset)
            authors = book['authors']
            list_of_authors = []

            if isinstance(authors, tuple):
                authors_id = []
                first_name = str(authors[0])
                last_name = str(authors[1])
                author = create_library_item(
                    db.session,
                    Author,
                    last_name=last_name,
                    first_name=first_name
                )
                id_of_auth = author.id
                authors_id.append(id_of_auth)
                list_of_authors.append(author)
                lib_item = create_library_item(
                    db.session,
                    Book,
                    title=title,
                    language=''
                )
                lib_item.authors.append(author)
                create_copy(lib_item, asset)
                reserve_copy(book, lib_item.id, asset)

            elif isinstance(authors, list):
                authors_id = []
                for auth_name in authors:
                    f_name = str(auth_name[0])
                    l_name = str(auth_name[1])
                    author = create_library_item(
                        db.session,
                        Author,
                        last_name=l_name,
                        first_name=f_name
                    )
                    id_of_auth = author.id
                    authors_id.append(id_of_auth)
                    list_of_authors.append(author)
                    lib_item = create_library_item(
                        db.session,
                        Book,
                        title=title,
                        language=''
                    )
                    lib_item.authors.append(author)
                create_copy(lib_item, asset)
                reserve_copy(book, lib_item.id, asset)
        except TypeError:
            message = '\nuser not found in ldap - entry info:\n {}\n'
            print(message.format(book))


# writing magazine's data in database
def get_magazines(file_location):
    magazines_properties = get_magazine_data(file_location)
    for i in magazines_properties:
        title = i['title']
        issue = str(i['issue'])
        year = i['year']
        if not year:
            magazine = create_library_item(
                db.session,
                Magazine,
                title=title,
                issue=issue,
                language=''
            )

            create_library_item(db.session, Copy,
                                library_item_id=magazine.id,
                                library_item=magazine)
        else:
            year = datetime.strptime(str(int(i['year'])), '%Y')
            magazine = create_library_item(
                db.session,
                Magazine,
                title=title,
                year=year,
                issue=issue,
                language=''
            )

            create_library_item(db.session, Copy,
                                library_item_id=magazine.id,
                                library_item=magazine)
