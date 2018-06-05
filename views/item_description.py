from flask import render_template, Blueprint, session

from models import LibraryItem, User
item_desc = Blueprint('item_description', __name__,
                      template_folder='templates')


@item_desc.route('/item_description/<int:item_id>')
def book_desc(item_id):
    user = User.query.get(session['id'])
    print([type(r) for r in user.roles])
    admin = user.has_role('ADMIN')

    authors_list = []
    item = LibraryItem.query.get_or_404(item_id)
    tags_list = item.tags_string()

    if item.type == 'book':
        authors_list = item.authors_string()

    return render_template('item_description.html',
                           item=item,
                           tags_list=tags_list,
                           authors_list=authors_list,
                           admin=admin)


@item_desc.errorhandler(404)
def not_found(error):
    message_body = 'Item does not exist!'
    message_title = 'Error!'
    return render_template('message.html',
                           message_title=message_title,
                           message_body=message_body), 404
