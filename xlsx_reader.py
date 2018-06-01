import xlrd
from nameparser import HumanName
from models import (Book, Author, Copy, Magazine, User)
from init_db import db
from sqlalchemy import exists


data = './data/biblioteka_oczyszczona.xlsx'
workbook = xlrd.open_workbook(data)

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        #print('already an instance', instance)
        #pass
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        #print('instance added ', instance)
        return instance

def get_author_name(authors):
    if (',' in authors and 'Jr.' not in authors) or (' and ' in authors) or ('&' in authors):
        split_authors = authors.replace(' and ', ',').replace('&', ',').split(',')
        ath = []
        first_names = []
        last_names = []
        for auth in split_authors:
            name = HumanName(str(auth))
            first_name = name.first + " " + name.middle
            last_name = name.last + " " + name.suffix
            first_names.append(first_name)
            last_names.append(last_name)
            ath = list(zip(first_names, last_names))
    else:
        name = HumanName(str(authors))
        first_name = name.first + " " + name.middle
        last_name = name.last + " " + name.suffix
        ath = (first_name, last_name)
    return ath


def get_book_data():
    book_list = []

    for sheet_index in range(workbook.nsheets-2):   # -2 excludes deleted books, magazines sheets
        current_sheet = workbook.sheet_by_index(sheet_index)
        rows = current_sheet.nrows

        for row_index in range(1, rows):    # there is no need to load title of the column
            current_shelf = current_sheet.name
            title = current_sheet.cell_value(row_index, 1)
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


def get_magazine_data():
    magazines_list = []
    current_sheet = workbook.sheet_by_index(2)
    rows = current_sheet.nrows

    for row_index in range(1, rows):  # there is no need to load title of the column
        title = current_sheet.cell_value(row_index, 1)
        year = current_sheet.cell_value(row_index, 2)
        issue = current_sheet.cell_value(row_index, 3)  # ISSUE
        magazine_properties = {'title': title, 'year': year, 'issue': issue}
        magazines_list.append(magazine_properties)
    return(magazines_list)


def get_book():
    books_properties = get_book_data()
    copies = []

    for elem in books_properties:
        title = elem['title']
        asset = elem['asset']
        authors = elem['authors']
        book_authors = []
        user_name = HumanName(elem['user'])
        #print(user_name)
        #users_f_name = user_name.first
        #users_l_name = user_name.last

        if type(authors) is tuple:
            authors_id = []
            f_name = str(authors[0])
            l_name = str(authors[1])
            #author = Author(first_name=f_name, last_name=l_name)
            #book_authors.append(author)
            my_Auth = get_or_create(db.session, Author, last_name=l_name, first_name=f_name)
            id_of_auth = my_Auth.id
            authors_id.append(id_of_auth)

        elif type(authors) is list:
            authors_id = []
            for i in authors:
                f_name = str(i[0])
                l_name = str(i[1])
                #author = Author(first_name=f_name, last_name=l_name)
                #book_authors.append(author)
                my_Auth = get_or_create(db.session, Author, last_name = l_name, first_name = f_name)
                id_of_auth = my_Auth.id
                authors_id.append(id_of_auth)

        else:
            book_authors = []
        #book = Book(title=title)
        #book_copy = get_or_create(db.session, Copy, title = title, asset_code = asset)
        #print(book_copy)
        #db.session.add(book)
        if asset and (asset != 'brak') and (asset != "płyta"):
            current_book = Book.query.filter_by(title=title).first()
            # c = db.session.query(Copy).filter(Copy.asset_code == asset)
            # if db.session.query(c.exists()):
            #     pass
            # else:
            #     copy = Copy(library_item=current_book, asset_code=asset)
            #     db.session.add(copy)
        else:
            pass
    db.session.commit()
    #print(db.session.query(Author).filter(Author.last_name=="Begg ").all())
    print(db.session.query(Book).filter(Book.title == "Feedback czyli informacja zwrotna").all())
    #print(db.session.query(Author).all())
    #print(db.session.query(Book).all())


def get_magazines():
    magazines_properties = get_magazine_data()
    for i in magazines_properties:
        title = i['title']
        issue = i['issue']
        year = i['year']
        magazine = Magazine(title = title, issue = issue, year = year)
    #     m = db.session.query(Magazine).filter(Magazine.title == title)
    #     if db.session.query(m.exists()):
    #         pass
    #     else:
    #         db.session.add(magazine)
    # db.session.commit()
    #print(db.session.query(Magazine).all())

# FIXME: checking if record exists already in database -> under construction, works for Authors
# TODO: find authors categorised in a wrong way -> manually from csv export -> manage with it in original file
# TODO: def separate function for magazines? - DONE
# TODO: do not take any null rows into consideration
# TODO: HOW TO HANDLE COPIES - DONE
# TODO: verify magazine adding