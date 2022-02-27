from flask import Flask

app = Flask(__name__)

from views import view

app.register_blueprint(view.bp)


@app.route('/', methods=['GET'])
def initial():
    return "Hello! dylee api server"


if __name__ == '__main__':
    app.run()