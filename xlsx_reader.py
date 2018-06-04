import xlrd
from nameparser import HumanName
from models import (Book, Author, Copy, Magazine, User)
from init_db import db

data = './biblioteka_probna.xlsx'     # please ensure if you have a proper file in folder
workbook = xlrd.open_workbook(data)


def get_or_create(session, model, **kwargs):    # checks if element exist, creates new if not
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def get_author_name(authors):   # reads author's data from file
    if (',' in authors and 'Jr.' not in authors) or (' and ' in authors) or ('&' in authors):
        split_authors = authors.replace(' and ', ',').replace('&', ',').split(',')
        ath = []
        first_names = []
        last_names = []

        for auth in split_authors:
            name = HumanName(str(auth))
            first_name = (name.first + " " + name.middle).strip()
            last_name = (name.last + " " + name.suffix).strip()
            first_names.append(first_name)
            last_names.append(last_name)
            ath = list(zip(first_names, last_names))
    else:
        name = HumanName(str(authors))
        first_name = (name.first + " " + name.middle).strip()
        last_name = (name.last + " " + name.suffix).strip()
        ath = (first_name, last_name)

    return ath


def get_book_data():    # reads book's data from file
    book_list = []

    for sheet_index in range(workbook.nsheets-2):   # -2 excludes deleted books, magazines sheets
        current_sheet = workbook.sheet_by_index(sheet_index)
        rows = current_sheet.nrows

        for row_index in range(1, rows):    # there is no need to load title of the column
            current_shelf = current_sheet.name
            title = (current_sheet.cell_value(row_index, 1)).strip()
            authors = current_sheet.cell_value(row_index, 2)
            author = get_author_name(authors)

            if current_shelf == 'General':
                user = current_sheet.cell_value(row_index, 4)
                date_of_rental = current_sheet.cell(row_index, 5)
                status = current_sheet.cell(row_index, 5)
                author = get_author_name(authors)
                asset = current_sheet.cell_value(row_index, 3)
                book_properties = {'authors': author, 'title': title, 'asset': asset, 'user': user}
                book_list.append(book_properties)

            else:
                asset = current_sheet.cell_value(row_index, 3)
                book_properties = {'authors': author, 'current_shelf': current_shelf, 'title': title, 'asset': asset, 'user': user, 'date_of_rental': date_of_rental, 'status': status}     # delete unused parameters
                book_list.append(book_properties)

    return book_list


def get_magazine_data():    # reads magazine's data from file
    magazines_list = []
    current_sheet = workbook.sheet_by_index(2)
    rows = current_sheet.nrows

    for row_index in range(1, rows):  # there is no need to load title of the column
        title = (current_sheet.cell_value(row_index, 1)).strip()
        year = current_sheet.cell_value(row_index, 2)
        issue = current_sheet.cell_value(row_index, 3)
        magazine_properties = {'title': title, 'year': year, 'issue': issue}
        magazines_list.append(magazine_properties)
    return magazines_list


def get_book():     # writes authors, books and copies data in database
    books_properties = get_book_data()
    asset_codes = []

    for elem in books_properties:
        title = elem['title']
        asset = elem['asset']
        asset_codes.append(asset)
        authors = elem['authors']
        list_of_authors = []

        if type(authors) is tuple:
            authors_id = []
            f_name = str(authors[0])
            l_name = str(authors[1])
            author = get_or_create(db.session, Author, last_name=l_name, first_name=f_name)
            id_of_auth = author.id
            authors_id.append(id_of_auth)
            list_of_authors.append(author)
            book = get_or_create(db.session, Book, title=title)
            book.authors.append(author)

        elif type(authors) is list:
            authors_id = []
            for i in authors:
                f_name = str(i[0])
                l_name = str(i[1])
                author = get_or_create(db.session, Author, last_name=l_name, first_name=f_name)
                id_of_auth = author.id
                authors_id.append(id_of_auth)
                list_of_authors.append(author)
                book = get_or_create(db.session, Book, title=title)
                book.authors.append(author)
                if asset in asset_codes:
                    get_or_create(db.session, Copy, library_item_id=book.id, library_item=book)
                else:
                    get_or_create(db.session, Copy, library_item_id=book.id, library_item=book, asset_code=asset)


def get_magazines():    # writes magazine's data in database
    magazines_properties = get_magazine_data()
    for i in magazines_properties:
        title = i['title']
        issue = str(i['issue'])
        year = str(i['year'])
        get_or_create(db.session, Magazine, title=title, year=year, issue=issue)