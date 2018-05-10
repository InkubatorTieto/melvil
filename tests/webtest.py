from urllib import request


def inc(x):  # one more example
    return x + 1


class TestClass(object):

    def test_web_response(self): #every test function has to begin : test_
        try:
            handler = request.urlopen('http://localhost:5000/') #handler
            code = handler.getcode()
            if code == 200:
                assert True
            else:
                assert False
        except:
            assert False


    def test_simple(self): # one more, another type test
        assert True



    def test_answer(self):
        assert inc(3) == 5


