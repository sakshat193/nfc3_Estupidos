from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///example.db"  # Replace with your database URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    mobile_number = Column(String(10), unique=True, nullable=False)

def init_db():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Insert initial data
    with SessionLocal() as session:
        # Check if the database is empty
        if not session.query(User).first():
            # Create initial users with all required fields
            users = [
                User(name="Akshat Singh", username="akshat", password="password123", mobile_number="1234567890"),
                User(name="Ayush Patel", username="ayush", password="password456", mobile_number="0987654321"),
                User(name="Bhargavi Naik", username="bhargavi", password="password789", mobile_number="1234554321"),
            ]
            session.add_all(users)
            session.commit()


