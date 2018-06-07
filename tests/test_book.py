from flask import url_for, json
from models import Author


def test_add_author(db_author, client, session):

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    with client.session_transaction() as sess:

        response = client.post(url_for('library_books.add_book'),
                               data=json.dumps(db_author),
                               headers=headers,
                               follow_redirects=True)

    author = Author.query.filter_by(first_name=db_author['first_name'],
                                    last_name=db_author['surname']).first()
    print("to ja autor:", author)
    print("db-autoooor:", db_author)
    # assert author.first_name == db_author['first_name']
    #
    # assert author.last_name == db_author['last_name']


