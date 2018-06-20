# from flask import url_for
#
#
# def test_reset_password_status_code_for_get(client):
#     resp = client.get(url_for('library.reset'),
#                       follow_redirects=True)
#     assert resp.status_code == 200, \
#         "Reset password GET view wrong response"
#
#
# # def test_reset_password_status_code_for_post(client, forgot_pass):
# #     resp = client.post(url_for('library.reset'),
# #                       data=forgot_pass.data,
# #                       follow_redirects=True)
# #     assert resp.status_code == 200, \
# #         "Request request:GET good response"
# #
# #
# # def test_reset_POST_no_data(app):
# #     with app.test_client() as c:
# #         try:
# #             c.post(url_for('library.reset'),
# #                        follow_redirects=True)
# #             assert False, "No error when no password passed"
# #         except :
# #             assert True