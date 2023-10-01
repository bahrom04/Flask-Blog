from webapp import db
from webapp import bcrypt


class Accounts(db.Model):
    # Connecting with existing accounts table
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password= db.Column(db.String(50), nullable=False)

    @property
    def password_decode(self):
        return self.password
    
    @password_decode.setter
    def password_decode(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    



    
