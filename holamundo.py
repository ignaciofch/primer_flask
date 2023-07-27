from flask import Flask

aplicacion = Flask(__name__)

@aplicacion.route('/')
def holamundo():
    return 'hola mundo'

