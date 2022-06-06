from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def log_reg ():
    if 'user_id' in session:
        return redirect('/success')
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    
    if not User.validate_user_login(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.create_user(data)
    session['user_id'] = id
    
    # user.User.create(request.form)

    return redirect("/success")



@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Wrong Email")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Password Password")
        return redirect('/')
    session['user_id'] = user.id
    
    return redirect('/success')


@app.route('/success')
def success():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('page.html', user=User.get_one(data))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
