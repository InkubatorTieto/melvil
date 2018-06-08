import sys
import traceback

import ldap
from mimesis import Generic
from sqlalchemy.sql import exists

from config import Config
from models import User

g = Generic('en')


def connect_to_server():

    connection = ldap.initialize(Config.LDAP_PROVIDER)
    _username = Config.LDAP_USER
    _password = Config.LDAP_PASS

    try:
        connection.protocol_version = ldap.VERSION3
        connection.simple_bind_s(_username, _password)
        return connection

    except ldap.TIMELIMIT_EXCEEDED as error:
        print(error)
        return None


def parse_catalogue(connection,
                    ext=False,
                    groups=['OU=Users,', 'OU=External Users,']):
    '''
       Walks through specified LDAP groups in server and returns data
       of users in format [[<mail>, [<last_name>, <first_name>]]]
    '''

    def clear_names(full_name, suffix=()):
        '''Clear full name entry from redundant suffixes'''

        for suff in suffix:
            if full_name.endswith(suff):
                full_name = full_name.rstrip(suff)
        return full_name

    def set_filters(fltr_type, fltr_string, sep=','):
        '''Sets LDAP filtres for quering server'''

        fltr = fltr_type
        if not fltr.endswith('='):
            fltr += '='

        try:
            isinstance(fltr_string, str)
            fltr += fltr_string
            return fltr
        except TypeError as e:
            print(traceback.print_exc(file=sys.stdout))
            return None

    if not ext:
        base = groups[0] + Config.LDAP_BASE_DN
    else:
        base = groups[1] + Config.LDAP_BASE_DN

    # get all entries which are category Person
    type_fltr1 = 'objectCategory'
    cont_fltr1 = 'CN=Person,CN=Schema,CN=Configuration,DC=tieto,DC=com'
    _fltr1 = set_filters(type_fltr1,
                         cont_fltr1)

    # special case in OU=Users
    type_fltr2 = 'displayName'
    cont_fltr2 = 'Recommend Recommend'
    _fltr2 = set_filters(type_fltr2,
                         cont_fltr2)

    # get those entries which have attribute mail present
    type_fltr3 = 'mail'
    cont_fltr3 = '*'
    _fltr3 = set_filters(type_fltr3,
                         cont_fltr3)

    # _fltr -> look for human-users in group
    # _attrs -> retrieve full name and email from entry
    _attrs = ['displayName', 'mail']
    _fltr = '(&({0})(!({1}))({2}))'.format(_fltr1, _fltr2, _fltr3)
    _srch = connection.search_s(base, ldap.SCOPE_SUBTREE, _fltr, _attrs)

    user_data = []
    for _person_data in _srch:
        mail = str(_person_data[1]['mail'].pop(), encoding='utf-8')
        full_name = clear_names(
            str(_person_data[1]['displayName'].pop(),
                encoding='utf-8'),
            ('(EXT)', '(Ext)', 'OSS', 'DUAL')
        ).split(maxsplit=1)
        user_data.append([mail, full_name])

    return user_data


def set_users(session):

    def add_user(user_data, model):
        # checking if element exist, creates new if not
        check_user = session.query(exists().where(
            model.email == user_data[0])).scalar()
        if check_user:
            print("{}: User already exists".format(check_user))
        else:
            instance = model(email=user_data[0],
                             first_name=user_data[1][1],
                             surname=user_data[1][0],
                             password_hash=g.cryptographic.hash(),
                             active=g.development.boolean(),
                             roles=[])
            session.add(instance)
            session.commit()

    conn = connect_to_server()

    _users = []
    for flag in [True, False]:
        _users.extend(parse_catalogue(conn, ext=flag))

    for _user in _users:
        add_user(user_data=_user, model=User)
