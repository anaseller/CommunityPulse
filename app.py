
from flask import Flask
from src.core.app_runner import create_app

app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'



if __name__ == '__main__':
    app = create_app()
    app.run()




# if __name__ == '__main__':
#     app.run()
