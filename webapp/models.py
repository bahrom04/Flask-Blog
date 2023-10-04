from webapp import db
from webapp import bcrypt
from webapp import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Accounts.query.get(int(user_id))


class Accounts(db.Model, UserMixin):
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


    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)
    

 

    
