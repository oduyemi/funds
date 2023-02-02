from flask import Flask, render_template, abort, request
starter = Flask(__name__)

@starter.route('/')
def landingpage():
    return render_template('index.html')


@starter.route('/donate')
def donatepage():
    return render_template('donate.html')

@starter.route('/invest')
def investpage():
    return render_template('invest.html')

@starter.route('/login')
def loginpage():
    return render_template('login.html')

@starter.route('/ngo')
def ngopage():
    return render_template('ngo.html')

@starter.route('/prestart')
def prestartuppage():
    return render_template('prestartup.html')

@starter.route('/startup')
def startuppage():
    return render_template('startup.html')









@starter.errorhandler(404)
def pagenotfound(error):
    return render_template('error404.html', error=error),404

@starter.errorhandler(500)
def internalerror(error):
    return 'Sorry, an error occured.', 500










if __name__ == '__main__':
    starter.config.from_pyfile("config.py")
    starter.run(debug = True, port = 6393)