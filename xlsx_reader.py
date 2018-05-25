import xlrd
from nameparser import HumanName
from models import (Book, Author)
from init_db import db

data = './data/biblioteka.xlsx'
workbook = xlrd.open_workbook(data)


def get_author_name(authors):
    if (',' in authors and 'Jr.' not in authors) or (' and ' in authors) or ('&' in authors):
        splited_authors = authors.replace(' and ', ',').replace('&', ',').split(',')
        ath = []
        first_names = []
        last_names = []
        for auth in splited_authors:
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
    #book_dict = {}
    for sheet_index in range(workbook.nsheets-1):   # -2 excludes and deleted magazines sheet
        current_sheet = workbook.sheet_by_index(sheet_index)
        rows = current_sheet.nrows

        for row_index in range(1, rows): # there is no need to load title of the column
            current_shelf = current_sheet.name #TODO: which place in db? change the name of the property? ask Magda O.
            title = current_sheet.cell_value(row_index, 1)
            authors = current_sheet.cell_value(row_index, 2)
            asset = current_sheet.cell_value(row_index, 3)
            author = get_author_name(authors)

            if current_shelf == 'General':
                user = current_sheet.cell_value(row_index, 4)
                date_of_rental = current_sheet.cell(row_index, 5)
                status = current_sheet.cell(row_index, 5)
                author = get_author_name(authors)
                book_properties = {'authors': author, 'title': title, 'asset': asset, 'user': user}
                book_list.append(book_properties)
                #book_dict.update({'authors': author, 'title': title, 'asset': asset, 'user': user})
            elif current_shelf == 'Magazines':
                author = ' '
                title = ' '
                edition = current_sheet.cell_value(row_index, 2)
                number = current_sheet.cell_value(row_index, 3) # ISSUE
                magazine_properties = {'authors': author, 'title': title, 'asset': asset, 'user': user, 'edition': edition, 'number': number}
                #book_dict.update({'authors': author, 'title': title, 'asset': asset, 'user': user, 'edition': edition, 'number': number})
                book_list.append(magazine_properties)
            else:
                pass #TODO: ensure if there is any exception to cover in Managers section?
                #book ={'authors': author, 'current_shelf': current_shelf, 'title': title, 'asset': asset, 'user': user,
                    #'date_of_rental': date_of_rental, 'status': status}
                book_properties = {'authors': author, 'current_shelf': current_shelf, 'title': title, 'asset': asset, 'user': user,
                    'date_of_rental': date_of_rental, 'status': status}
                book_list.append(book_properties)
   # print(book_list)
    return book_list

def get_book():
    books_properties = get_book_data()

    for elem in books_properties:
        title = elem['title']
        asset = elem['asset']
        #   title = book['title']
        #   book = Book(title = title)
        #   book.title = title
        authors = elem['authors']
        book_authors = []
        if type(authors) is tuple:
            f_name = str(authors[0])
            l_name = str(authors[1])
            author = Author(first_name=f_name, last_name=l_name)
            book_authors.append(author)
            # print(f_name, l_name)
            db.session.add(author)
        elif type(authors) is list:
            for i in authors:
                f_name = str(i[0])
                l_name = str(i[1])
                author = Author(first_name=f_name, last_name=l_name)
                # print(authors, i, 'list!', author)
                db.session.add(author)
                book_authors.append(author)
        else:
            # author = None # for list of authors
            # print(authors, 'other type!', type(authors), author)
            book_authors = []
        book = Book(title=title, authors=book_authors)  # TODO: add asset_code = asset
    db.session.add(book)
    db.session.commit()

    # print(db.session.query(Author).all())
    print(db.session.query(Book).all())

#TODO: check if exists already in db!

# TODO: find inapropriate names -->  customize parser configuration
# TODO: find the solution for magazines - checked
# TODO: connect with DB - checked
# TODO: push parameters into db - under construction
# TODO: def func in order not to repeat code
