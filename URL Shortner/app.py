from flask import Flask, request, render_template, redirect
import hashlib

app = Flask(__name__)

urls = {}
hashes = set()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['original_url']
    if original_url in urls:
        short_url = urls[original_url]
    else:
        hash_val = hashlib.md5(original_url.encode()).hexdigest()[:6]
        short_url = f'http://localhost:5000/{hash_val}'
        urls[original_url] = short_url
        hashes.add(hash_val)
    return render_template('shorten.html', original_url=original_url, short_url=short_url)

@app.route('/<hash_val>')
def redirect_url(hash_val):
    if hash_val in hashes:
        original_url = next(key for key, value in urls.items() if value.endswith(hash_val))
        return redirect(original_url)
    return 'URL not found'

if __name__ == '__main__':
    app.run(debug=True)
