import xlrd

from datetime import datetime
from random import choice, randint

from nameparser import HumanName

from models import (Book, Author, Copy, Magazine)
from init_db import db


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
        language = choice(['polish', 'other', 'english'])
        if model.__name__ == "Book":
            rand_date = datetime.\
                strptime(str(randint(1978, int(datetime.today().year))),
                         '%Y')
            instance = model(language=language, pub_date=rand_date, **kwargs)
        elif model.__name__ == "Magazine":
            instance = model(language=language, **kwargs)
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

            if current_shelf == 'General':
                author = get_authors_data(authors)
                asset = str(current_sheet.cell_value(row_index, 3))
                book_properties = {'authors': author,
                                    'title': title,
                                    'asset': asset}
                book_list.append(book_properties)

            else:
                asset = str(current_sheet.cell_value(row_index, 3))
                book_properties = {'authors': author,
                                    'current_shelf': current_shelf,
                                    'title': title,
                                    'asset': asset}
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


# writing authors, books and copies data in database
def get_books(file_location):
    books_properties = get_book_data(file_location)
    asset_codes = []
    
    for book in books_properties:
        title = book['title']
        asset = book['asset']
        asset_codes.append(asset)
        authors = book['authors']
        list_of_authors = []

        if isinstance(authors, tuple):
            authors_id = []
            first_name = str(authors[0])
            last_name = str(authors[1])
            author = create_library_item(db.session, Author,
                                         last_name=last_name,
                                         first_name=first_name)
            id_of_auth = author.id
            authors_id.append(id_of_auth)
            list_of_authors.append(author)
            book = create_library_item(db.session, Book, title=title)
            book.authors.append(author)
            create_copy(book, asset)

        elif isinstance(authors, list):
            authors_id = []
            for auth_name in authors:
                f_name = str(auth_name[0])
                l_name = str(auth_name[1])
                author = create_library_item(db.session, Author,
                                             last_name=l_name,
                                             first_name=f_name)
                id_of_auth = author.id
                authors_id.append(id_of_auth)
                list_of_authors.append(author)
                book = create_library_item(db.session, Book,
                                           title=title)
                book.authors.append(author)
                create_copy(book, asset)


# writing magazine's data in database
def get_magazines(file_location):
    magazines_properties = get_magazine_data(file_location)
    for i in magazines_properties:
        title = i['title']
        issue = str(i['issue'])
        year = i['year']
        if not year:
            magazine = create_library_item(db.session, Magazine,
                                           title=title,
                                           issue=issue)

            create_library_item(db.session, Copy,
                                library_item_id=magazine.id,
                                library_item=magazine)
        else:
            year = datetime.strptime(str(int(i['year'])), '%Y')
            magazine = create_library_item(db.session, Magazine,
                                           title=title,
                                           year=year,
                                           issue=issue)

            create_library_item(db.session, Copy,
                                library_item_id=magazine.id,
                                library_item=magazine)
