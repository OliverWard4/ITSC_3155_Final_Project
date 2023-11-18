from flask import Flask, render_template

app = Flask(__name__)

#Home page Route
@app.route('/')
def index():
    #Renders the home page
    return render_template('index.html')

#Sign up page route
@app.route('/signup')
def signUp():
    #Renders the sign up page
    return render_template('signup.html')

#Login page route
@app.route('/login')
def login():
    #Renders the login page
    return render_template('login.html')

if __name__ == "__main__":
    #Runs the application
    app.run(debug=True)