from flask import render_template, Blueprint

from models import LibraryItem

item_desc = Blueprint('item_description', __name__,
                      template_folder='templates')


@item_desc.route('/item_description/<item_id>')
def book_desc(item_id):
    item = LibraryItem.query.get(item_id)

    return render_template('item_description.html', item=item)
