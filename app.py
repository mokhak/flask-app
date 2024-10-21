from flask import Flask, request, redirect, render_template_string, url_for, flash
import string
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages

# Dictionary to store shortened URLs
url_mapping = {}

# HTML template in a string
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Shortener</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 100px; }
        input, button { padding: 10px; font-size: 16px; margin: 5px; }
    </style>
</head>
<body>
    <h1>Simple URL Shortener</h1>
    <form method="POST" action="/">
        <input type="url" name="original_url" placeholder="Enter a URL" required>
        <button type="submit">Shorten URL</button>
    </form>

    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <p style="color: green;">{{ messages[0] }}</p>
      {% endif %}
    {% endwith %}

    <ul>
    {% for short_url, original_url in url_mapping.items() %}
        <li><a href="{{ short_url }}" target="_blank">{{ request.host_url }}{{ short_url }}</a> → {{ original_url }}</li>
    {% endfor %}
    </ul>
</body>
</html>
"""

# Helper function to generate a short URL key
def generate_short_key(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['original_url']
        short_key = generate_short_key()

        # Store the mapping of short key to original URL
        url_mapping[short_key] = original_url

        flash(f"Shortened URL: {request.host_url}{short_key}")
        return redirect(url_for('home'))

    return render_template_string(template, url_mapping=url_mapping)

@app.route('/<short_key>')
def redirect_to_url(short_key):
    original_url = url_mapping.get(short_key)
    if original_url:
        return redirect(original_url)
    else:
        return "<h1>URL not found!</h1>", 404

if __name__ == '__main__':
    app.run(debug=True)
