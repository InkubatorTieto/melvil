from flask import render_template, Blueprint, session, abort
from models import LibraryItem, User

item_desc = Blueprint('item_description', __name__,
                      template_folder='templates')


@item_desc.route('/item_description/<int:item_id>')
def item_description(item_id):
    try:
        user = User.query.get(session['id'])
        admin = user.has_role('ADMIN')
    except KeyError:
        abort(401)
    except Exception:
        abort(500)
    item = LibraryItem.query.get_or_404(item_id)
    tags_list = item.tags_string()

    authors_list = []
    if item.type == 'book':
        authors_list = item.authors_string()

    return render_template('item_description.html',
                           item=item,
                           tags_list=tags_list,
                           authors_list=authors_list,
                           admin=admin)


@item_desc.errorhandler(404)
def not_found(error):
    message_body = 'Page does not exist!'
    message_title = 'Error!'
    return render_template('message.html',
                           message_title=message_title,
                           message_body=message_body), 404


@item_desc.errorhandler(401)
def not_authorized(error):
    message_body = 'You are not authorized to visit this site!'
    message_title = 'Error!'
    return render_template('message.html',
                           message_title=message_title,
                           message_body=message_body), 401


@item_desc.errorhandler(500)
def server_error(error):
    message_body = 'but something went wrong.'
    message_title = 'Don\'t panic!'
    return render_template('message.html',
                           message_title=message_title,
                           message_body=message_body), 500
