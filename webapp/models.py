from webapp import db

class Accounts(db.Model):
    # Connecting with existing accounts table
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
