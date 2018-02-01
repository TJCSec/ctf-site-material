from flask import Flask, render_template, request
from mail import validate_email, add_user_to_list, send_confirmation_email
from mailgun_config import list_name, paid_account
import string, random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if not request.method == 'POST':
        verif = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + "-_") for _ in range(42))
        return render_template("index.html", verif=verif)

    name = request.form['name']
    email_address = request.form['email']
    if paid_account and not validate_email(email_address):
        return render_template("index.html", invalid_email=True)

    if not add_user_to_list(name, email_address, list_name):
        return render_template("index.html", add_error=True)

    if not send_confirmation_email(name, email_address):
        return render_template("index.html", conf_email_error=True)

    return render_template("index.html", success=True)

if __name__ == '__main__':
    app.run(port=9020, debug=True)
