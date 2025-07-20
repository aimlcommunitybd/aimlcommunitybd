from flask import Flask, render_template, send_from_directory
from flask import redirect

import os


app = Flask(__name__,)


@app.route('/')
def home():
    SOCIAL_LINKS = {
        'linkedin': 'https://www.linkedin.com/company/python-bangladesh/',
        'discord': 'https://discord.gg/sR52eYRFba', 
        'whatsapp': 'https://whatsapp.com/channel/0029VbAf0s70rGiMzJfG4u2B',
        'github': 'https://github.com/pythonbangladesh'
    }
    return render_template('index.html', social_links=SOCIAL_LINKS)


@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('assets', filename)


@app.route('/healthz')
def health():
    return "OK", 200


@app.route('/coc')
def coc():
    return render_template("legal/code-of-conduct.html")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"---------Starting app on port {port}-------------")
    app.run(debug=True, host='0.0.0.0', port=port)
