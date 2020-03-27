from flask import Flask

app = Flask('__main__')


@app.route("/")
def get_news():
    return "No news is good news"


if __name__ == '__main__':
    app.run(debug=True)
