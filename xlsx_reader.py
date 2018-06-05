import xlrd

from nameparser import HumanName

from models import (Book, Author, Copy, Magazine)
from init_db import db

# please ensure if you have a proper file in your folder
data = './biblioteka_probna.xlsx'
workbook = xlrd.open_workbook(data)


def get_first_name(author):
    name = HumanName(str(author))
    first_name = (name.first + " " + name.middle).strip()
    return first_name


def get_last_name(author):
    name = HumanName(str(author))
    last_name = (name.last + " " + name.suffix).strip()
    return last_name


# checking if element exist, creates new if not
def get_or_create_library_item(session, model, **kwargs):
    library_item = session.query(model).filter_by(**kwargs).first()
    if library_item:
        return library_item
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


# reading author's data from file
def get_authors_data(authors):
    if (',' in authors and 'Jr.' not in authors) \
            or (' and ' in authors) \
            or ('&' in authors):
        split_authors = \
            authors.replace(' and ', ',').replace('&', ',').split(',')
        first_names = []
        last_names = []

        for auth in split_authors:
            first_name = get_first_name(auth)
            first_names.append(first_name)
            last_name = get_last_name(auth)
            last_names.append(last_name)
        authors_names = list(zip(first_names, last_names))
    else:
        first_name = get_first_name(authors)
        last_name = get_last_name(authors)
        authors_names = (first_name, last_name)

    return authors_names


# reads book's data from file
def get_book_data():
    book_list = []

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

            if current_shelf == 'General':
                user = current_sheet.cell_value(row_index, 4)
                date_of_rental = current_sheet.cell(row_index, 5)
                status = current_sheet.cell(row_index, 5)
                author = get_authors_data(authors)
                asset = current_sheet.cell_value(row_index, 3)
                book_properties = {'authors': author,
                                   'title': title,
                                   'asset': asset,
                                   'user': user}
                book_list.append(book_properties)

            else:
                asset = current_sheet.cell_value(row_index, 3)
                book_properties = {'authors': author,
                                   'current_shelf': current_shelf,
                                   'title': title,
                                   'asset': asset,
                                   'user': user,
                                   'date_of_rental': date_of_rental,
                                   'status': status}
                book_list.append(book_properties)

    return book_list


# reading magazine's data from file
def get_magazine_data():
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


# writing authors, books and copies data in database
def get_book():
    books_properties = get_book_data()
    asset_codes = []

    for book in books_properties:
        title = book['title']
        asset = book['asset']
        asset_codes.append(asset)
        authors = book['authors']
        list_of_authors = []

        if type(authors) is tuple:
            authors_id = []
            first_name = str(authors[0])
            last_name = str(authors[1])
            author = get_or_create_library_item(db.session, Author,
                                                last_name=last_name,
                                                first_name=first_name)
            id_of_auth = author.id
            authors_id.append(id_of_auth)
            list_of_authors.append(author)
            book = get_or_create_library_item(db.session, Book, title=title)
            book.authors.append(author)

        elif type(authors) is list:
            authors_id = []
            for auth_name in authors:
                f_name = str(auth_name[0])
                l_name = str(auth_name[1])
                author = get_or_create_library_item(db.session, Author,
                                                    last_name=l_name,
                                                    first_name=f_name)
                id_of_auth = author.id
                authors_id.append(id_of_auth)
                list_of_authors.append(author)
                book = get_or_create_library_item(db.session, Book,
                                                  title=title)
                book.authors.append(author)
                if asset in asset_codes:
                    get_or_create_library_item(db.session, Copy,
                                               library_item_id=book.id,
                                               library_item=book)
                else:
                    get_or_create_library_item(db.session, Copy,
                                               library_item_id=book.id,
                                               library_item=book,
                                               asset_code=asset)
    print(db.session.query(Book).all())
    print(db.session.query(Author).all())


# writing magazine's data in database
def get_magazines():
    magazines_properties = get_magazine_data()
    for i in magazines_properties:
        title = i['title']
        issue = str(i['issue'])
        year = str(i['year'])
        get_or_create_library_item(db.session, Magazine,
                                   title=title,
                                   year=year,
                                   issue=issue)
    print(db.session.query(Magazine).all())
