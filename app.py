from flask import Flask

app = Flask(__name__)


@app.route('/api/v1/hello-world-{27}', methods=['GET'])
def hello_world():
    return 'Hello World, 27!'


if __name__ == '__main__':
    app.run()
