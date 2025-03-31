from pageone import app, database

with app.app_context():
    database.create_all()

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
