from project import db
from project.models import User

db.create_all()

admin = User(username='admin', email='admin@example.com')

db.session.add(admin)
db.session.commit()
