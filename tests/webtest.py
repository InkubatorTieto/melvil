from urllib import request


def inc(x):  # one more example
    return x + 1


class TestClass(object):

    # every test function has to begin : test_
    def test_web_response(self):
        try:
            handler = request.urlopen('http://localhost:5000/')
            assert 200 == handler.getcode()
        except:
            assert False

    def test_simple(self):
        assert True

    def test_answer(self):
        assert inc(4) == 5
