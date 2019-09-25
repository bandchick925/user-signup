from flask import Flask, request, redirect
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET'])
def display_form():
    template = jinja_env.get_template('hello_form.html')
    return template.render()


@app.route('/', methods=['POST'])
def validate_form():
    template = jinja_env.get_template('hello_form.html')
    name = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']

    global name_error, pword_error, verify_error, email_error
    name_error = ''
    pword_error = ''
    verify_error = ''
    email_error = ''

    def is_name_valid(name):
        global name_error
        if (len(name) > 3) and (len(name) < 20):
            if ' ' not in name:
                return True
            else:
                name_error = 'Name contains space character.'
                return False
        else:
            name_error = 'Name is shorter than 3 or longer than 20 characters.'
            return False

    def is_email_valid(email):
        global email_error
        if email == '':
            return True
        elif '@' in email and '.' in email:
            if (len(email) > 3) and (len(email) < 20):
                if ' ' not in email:
                    test = []
                    for i in email:
                        if i == '@' or i == '.':
                            test.append(i)
                    if len(test) != 2:
                        email_error = 'Not a valid email address.'
                        return False
                    else:
                        return True
                else:
                    email_error = 'Email address contains space character.'
                    return False
            else:
                email_error = 'Email shorter than 3 or longer than 20 characters.'
                return False
        else:
            email_error = 'Not a valid email address.'
            return False

    def pwords_match(pw, vpw):
        global pword_error, verify_error
        if pw == '':
            pword_error = 'Password field cannot be empty'
            return False

        elif ' ' in pw:
            pword_error = 'Password cannot contain spaces'
            return False

        elif vpw == '':
            verify_error = 'Password field cannot be empty'
            return False

        elif ' ' in vpw:
            verify_error = 'Password cannot contain spaces'
            return False

        elif (len(password) > 20) or (len(password) < 3):
            pword_error = 'Password shorter than 3 or longer than 20 characters'
            return False

        elif pw != vpw:
            pword_error = verify_error = 'Passwords don\'t match'
            return False
        else:
            return True

    if is_email_valid(email) and is_name_valid(name) and pwords_match(password, verify):
        return redirect('/welcome/?username={}'.format(name))
    else:
        return template.render(
            email_error=email_error,
            username_error=name_error,
            password_error=pword_error,
            verify_error=verify_error,
            username=name, email=email
        )


@app.route('/welcome/')
def greet_user():
    name = request.args.get('username')
    template = jinja_env.get_template('hello_greeting.html')
    return template.render(username=name)


app.run()
