from app import create_app, db
from app.models import User, Post

app = create_app() 

# app context important
with app.app_context():
    # create db
    db.create_all()
    print("created database!")

    # set admin
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(username="admin", role="admin")
        admin.set_password("password")
        db.session.add(admin)
        db.session.commit()
        print("created admin: admin / password")

    # admin posts
    if not Post.query.first():
        post1 = Post(
            title="Welcome to TechThoughts",
            content="This is our first dynamic blog post.",
            author=admin
        )
        post2 = Post(
            title="Database Design Patterns",
            content="Relational integrity is important.",
            author=admin
        )
        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()
        print("example posts created!")