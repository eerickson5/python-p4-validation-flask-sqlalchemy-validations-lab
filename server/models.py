from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("name")
    def validate_name(self, key, address):
        if address == None or len(address) < 1:
            raise ValueError("Authors need names.")
        currently_named = Author.query.filter(Author.name == address).first()
        if currently_named:
            raise ValueError("Class Author in models.py requires each record to have a unique name")
        return address

    @validates("phone_number")
    def validate_phone(self, key, address):
        regex = re.compile(r"^[0-9]{10}$")
        if re.match(regex, address):
            return address
        else:
            raise ValueError("Invalid phone number")


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates("content")
    def validates_content(self, key, address):
        if len(address) < 250:
            raise ValueError("Content too short")
        else:
            return address
        
    @validates("summary")
    def validates_summary(self, key, address):
        if len(address) > 250:
            raise ValueError("Summary too long")
        else:
            return address
        
    @validates("category")
    def validates_category(self, key, address):
        valid = {"Fiction", "Non-Fiction"}
        if address not in valid:
            raise ValueError("Invalid category.")
        else:
            return address
        
    @validates("title")
    def validates_title(self, key, address):
        if not address or len(address) == 0:
            raise ValueError("Invalid title.")
        
        required = {"Won't Believe", "Secret", "Top", "Guess"}
        has_required = False
        for pattern in required:
            if pattern in address:
                has_required = True
        if has_required:
            return address
        else:
            raise ValueError("Not exciting enough")

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
