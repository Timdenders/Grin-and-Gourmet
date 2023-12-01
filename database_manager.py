from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm

Base = sqlalchemy.orm.declarative_base()


class UserData(Base):
    __tablename__ = 'user_data'
    user_name = Column(String, primary_key=True)


class ImageData(Base):
    __tablename__ = 'image_data'
    image_id = Column(String, primary_key=True)
    image_path = Column(String)
    image_description = Column(String)


class RecipeData(Base):
    __tablename__ = 'recipe_data'
    recipe_name = Column(String, primary_key=True)
    image_path = Column(String, ForeignKey('image_data.image_path'))
    image_description = Column(String, ForeignKey('image_data.image_description'))
    recipe_instructions = Column(String)
    recipe_rating = Column(Integer)


class SessionManager:
    def __init__(self):
        self.engine = create_engine('sqlite:///database.db', echo=True)
        Base.metadata.create_all(self.engine)
        self.session_maker = sessionmaker(bind=self.engine)

    def create_session(self):
        return self.session_maker()
