# import smtplib
# import email.utils
# from email.mime.text import MIMEText
#
#
# msg = MIMEText('The body of your message.')
# msg['To'] = email.utils.formataddr(('Recipient Name',
#                                     'jahenstein@gmail.com'))
# msg['From'] = email.utils.formataddr(('Your Name', 'test@test.com'))
# msg['Subject'] = 'Your Subject'
#
# server = smtplib.SMTP()
# server.connect()
# server.sendmail('test@test.com', ['jahenstein@gmail.com'], msg.as_string())
