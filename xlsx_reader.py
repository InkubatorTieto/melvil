import xlrd
from nameparser import HumanName


data = './biblioteka.xlsx'
workbook = xlrd.open_workbook(data)


for sheet_index in range(workbook.nsheets-2):   # -2 excludes and deleted magazines sheet  #TODO: def func. properly
    current_sheet = workbook.sheet_by_index(sheet_index)
    # TODO: add name of the sheet to db
    rows = current_sheet.nrows
    cols = current_sheet.ncols
    for row_index in range(0, rows):
        current_row = current_sheet.row(row_index)
        title = current_sheet.cell_value(row_index, 1)
        asset = current_sheet.cell_value(row_index, 3)
        authors = (current_sheet.cell_value(row_index, 2))
        # TODO: add information about user, date of rental, status

        if (',' in authors and 'Jr.' not in authors) or (' and ' in authors) or ('&' in authors):
            splitted_authors = authors.replace(' and ', ',').replace('&', ',').split(',')
            splitted = []
            for auth in splitted_authors:
                splitted.append(auth)
                # TODO: remember to add all authors when multiple
                name = HumanName(str(auth))
                first_name = name.first
                last_name = name.last
                # TODO: add author to db

        else:
            name = HumanName(authors)
            first_name = name.first
            last_name = name.last
            # TODO: add author to db
        #print(title, authors, 'FIRST NAME: ', first_name, 'LAST NAME: ', last_name)


# TODO: find inapropriate names -->  customize parser configuration
# TODO: find the solution for magazines
# TODO: connect with DB
# TODO: push parameters into db
# TODO: def func in order not to repeat code