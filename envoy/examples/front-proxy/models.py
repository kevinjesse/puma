from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


class api(BaseModel, db.Model):
    """Model for the api table"""
    __tablename__ = 'api'

    id = db.Column(db.Integer, primary_key = True)
    api_type = db.Column(db.String)
    api_key = db.Column(db.String)

class crew(BaseModel, db.Model):
    """Model for the crew table"""
    __tablename__ = 'crew'

    id = db.Column(db.Integer, primary_key = True)
    tconst = db.Column(db.String)
    directors = db.Column(db.String)
    writers = db.Column(db.String)

class name(BaseModel, db.Model):
    """Model for the name table"""
    __tablename__ = 'name'

    id = db.Column(db.Integer, primary_key = True)
    nconst = db.Column(db.String)
    primaryname = db.Column(db.String)
    birthyear = db.Column(db.String)
    deathyear = db.Column(db.String)
    primaryprofession = db.Column(db.String)
    knownfortitles = db.Column(db.String)
    netflixCount = db.Column(db.String)

class ratings(BaseModel, db.Model):
    """Model for the api table"""
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key = True)
    tconst = db.Column(db.String)
    averagerating = db.Column(db.String)
    numvotes = db.Column(db.String)

class similar(BaseModel, db.Model):
    """Model for the api table"""
    __tablename__ = 'similar'

    id = db.Column(db.Integer, primary_key = True)
    tconst = db.Column(db.String)
    similarids = db.Column(db.String)

class stars(BaseModel, db.Model):
    """Model for the api table"""
    __tablename__ = 'stars'

    id = db.Column(db.Integer, primary_key = True)
    tconst = db.Column(db.String)
    principalcast = db.Column(db.String)

class title(BaseModel, db.Model):
    """Model for the api table"""
    __tablename__ = 'title'

    id = db.Column(db.Integer, primary_key = True)
    tconst = db.Column(db.String)
    primarytitle = db.Column(db.String)
    originaltitle = db.Column(db.String)
    startyear = db.Column(db.String)
    genres = db.Column(db.String)
    plot = db.Column(db.String)
    mpaa = db.Column(db.String)
    prodco = db.Column(db.String)
    runtimeminutes = db.Column(db.String)
    netflixid = db.Column(db.String)

class title_full(BaseModel, db.Model):
    """Model for the api table"""
    __tablename__ = 'title_full'

    id = db.Column(db.Integer, primary_key = True)
    tconst = db.Column(db.String)
    primarytitle = db.Column(db.String)
    originaltitle = db.Column(db.String)
    startyear = db.Column(db.String)
    genres = db.Column(db.String)
    plot = db.Column(db.String)
    mpaa = db.Column(db.String)
    prodco = db.Column(db.String)
    runtimeminutes = db.Column(db.String)
    netflixid = db.Column(db.String)
    titletype = db.Column(db.String)
    isadult = db.Column(db.String)
    endyear = db.Column(db.String)

class tmd_genres(BaseModel, db.Model):
    """Model for the api table"""
    __tablename__ = 'tmd_genres'

    id = db.Column(db.Integer, primary_key = True)
    tmd_id = db.Column(db.String)
    genre = db.Column(db.String)

class tmd_nowplaying(BaseModel, db.Model):
    """Model for the api table"""
    __tablename__ = 'tmd_nowplaying'

    id = db.Column(db.Integer, primary_key = True)
    tconst = db.Column(db.String)
    vote_count = db.Column(db.String)

class tmd_popular_actors(BaseModel, db.Model):
    """Model for the api table"""
    __tablename__ = 'tmd_popular_actors'

    id = db.Column(db.Integer, primary_key = True)
    nconst = db.Column(db.String)
    pos = db.Column(db.String)

class tmd_popular_movies(BaseModel, db.Model):
    """Model for the api table"""
    __tablename__ = 'tmd_popular_movies'

    id = db.Column(db.Integer, primary_key = True)
    tconst = db.Column(db.String)
    pos = db.Column(db.String)
