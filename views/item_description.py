from flask import render_template, Blueprint

from models import LibraryItem


item_desc = Blueprint('item_description', __name__,
                      template_folder='templates')


@item_desc.route('/item_description/<int:item_id>')
def book_desc(item_id):
    authors_list = []
    item = LibraryItem.query.get(item_id)
    tags_list = item.tags_string()

    if item.type == 'book':
        authors_list = item.authors_string()

    return render_template('item_description.html',
                           item=item,
                           tags_list=tags_list,
                           authors_list=authors_list)
