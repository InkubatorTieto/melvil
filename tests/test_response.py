from urllib import request


class TestClass(object):

    def test_response_200(self):
        try:
            response = request.urlopen('http://localhost:5000/')
            response = response.getcode()
            if response == 200:
                assert True
            else:
                assert False
        except :
            assert False
