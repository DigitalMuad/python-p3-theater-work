from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Database setup
DATABASE_URL = 'sqlite:///moringa_theater.db'
engine = create_engine(DATABASE_URL)

# Use the new declarative base pattern for SQLAlchemy 2.0 compatibility
Base = declarative_base()

# Create a session factory
Session = sessionmaker(bind=engine)

# Define the Role model
class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    character_name = Column(String)

    # Relationship to Audition
    auditions = relationship('Audition', back_populates='role')

    # Methods
    def actors(self):
        return [audition.actor for audition in self.auditions]

    def locations(self):
        return [audition.location for audition in self.auditions]

    def lead(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[0] if hired_auditions else 'no actor has been hired for this role'

    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[1] if len(hired_auditions) > 1 else 'no actor has been hired for understudy for this role'

# Define the Audition model
class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer, primary_key=True)
    actor = Column(String)
    location = Column(String)
    phone = Column(Integer)
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'))

    # Relationship to Role
    role = relationship('Role', back_populates='auditions')

    # Methods
    def call_back(self):
        self.hired = True

# Create tables
Base.metadata.create_all(engine)

