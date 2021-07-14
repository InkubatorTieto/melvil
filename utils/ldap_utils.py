from flask_simpleldap import LDAP

ldap_client = LDAP()


def refine_data(obj, data_tag):
    out = obj[data_tag][0].decode('utf8')
    return out
