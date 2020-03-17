#!/usr/bin/env python
import random
import string

from flask import Flask
app = Flask(__name__)


def _random_string(length):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(int(length)))

@app.route('/content/<length>')
def hello_world(length):
    return _random_string(length)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')