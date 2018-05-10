from urllib.request import urlopen

def test():
    assert urlopen('http://localhost:5000/').getcode()==200