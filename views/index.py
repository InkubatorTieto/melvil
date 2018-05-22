from flask import render_template
from . import library
from forms.forms import LoginForm, ContactForm, RegistrationForm

@library.route('/')
def index():
    return render_template('index.html')


@library.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if not form.validate_on_submit():
        pass
    print("Received data(login): ", form.email.data, form.password.data, form.remember_me.data )
    return render_template('login.html', form=form, error=form.errors)


@library.route('/search')
def search():
    return render_template('browse.html')


@library.route('/logout')
def logout():
    return render_template('index.html')


@library.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    print("Received data(contact): ", form.email.data, form.title.data, form.message.data )
    return render_template('contact.html', form=form)


@library.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        pass
    print("Received data(register): ", form.email.data, form.first_name.data, form.surname.data,
          form.password.data, form.confirmPass.data)
    return render_template('register.html', title='Register', form=form, error=form.errors)
