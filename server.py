from applications import app
from waitress import serve

if __name__ == '__main__':
    print(app.config)
    serve(app, host='0.0.0.0', port=3007)
