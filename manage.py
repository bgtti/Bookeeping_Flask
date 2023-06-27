# Application script: where instance is defined
from app import create_app
from create_db import create_admin_acct
from app.extensions import db

app = create_app()

with app.app_context():
    db.create_all()
    create_admin_acct()

if __name__ == '__main__':
    app.run(debug=True)
