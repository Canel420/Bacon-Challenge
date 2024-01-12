from flask import render_template

import config
from routes import metrics
from init_database import init_db 

app = config.connex_app.app
app.register_blueprint(metrics, url_prefix='/api')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="0.0.0.0", debug=True)