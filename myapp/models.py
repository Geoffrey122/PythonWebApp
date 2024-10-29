from myapp import db  # Use relative import

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(20))

    def __repr__(self):
        return f'<User {self.uname}>'
