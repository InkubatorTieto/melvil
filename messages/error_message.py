from flask import render_template


class ErrorMessage:
    @classmethod
    def message(cls, error_body):
        message_body = error_body
        message_title = "Error!"
        return render_template(
            "message.html",
            message_title=message_title,
            message_body=message_body,
        )
