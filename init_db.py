from app import create_app, db
from app.models import User

# create app
app = create_app()

# app context for alchemy
with app.app_context():
    # create db out of models
    db.create_all()
    print("created dtabase!")

    # create admin if not already
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", password="password", role="admin")
        db.session.add(admin)
        db.session.commit()
        print("created admin: admin / password")
    else:
        print("admin already exists")