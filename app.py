from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.text import MIMEText
from db import get_cursor, get_connection

app = Flask(__name__, template_folder='templates')
app.secret_key = 'This is Private'


@app.route('/', strict_slashes=False)
def index():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = get_cursor()
        try:
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['user_name'] = user['fullname']
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid email or password!', 'error')
        except Exception as e:
            print("❌ Login error:", e)
            flash('An error occurred during login!', 'error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        cursor = get_cursor()
        conn = get_connection()
        try:
            cursor.execute('SELECT 1 FROM users WHERE email = %s', (email,))
            if cursor.fetchone():
                flash('Email already registered!', 'error')
                return render_template('register.html')

            cursor.execute(
                'INSERT INTO users (fullname, email, password) VALUES (%s, %s, %s)',
                (fullname, email, hashed_password)
            )
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print("❌ Registration error:", e)
            conn.rollback()
            flash('An error occurred during registration!', 'error')

    return render_template('register.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        msg = MIMEText(f"Message from {name} ({email}):\n\n{message}")
        msg['Subject'] = 'Library Contact Form'
        msg['From'] = email
        msg['To'] = "example@gmail.com"  # use your own mail id for it

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("example@gmail.com", "0000 0000 0000 0000")  #use your own email id and app password created in gmail for it
            server.sendmail(email, "adminemail@gmail.com", msg.as_string())
            server.quit()
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            print("❌ Contact form error:", e)
            flash('Error sending message. Please try again later.', 'error')

        return redirect(url_for('contact'))

    return render_template('contact.html')


@app.route('/logout', strict_slashes=False)
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.debug = True
    app.run()
