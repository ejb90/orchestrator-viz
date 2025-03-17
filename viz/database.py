"""
Misc database functions
"""
import pathlib

import sqlalchemy
import sqlalchemy.ext
import sqlalchemy.orm


RDBMS = "sqlite"
DATABASE = pathlib.Path("orchestrator.db")
DB_ADDRESS = f"{RDBMS}:///{DATABASE}"

# Create base class for declarative models
BASE = sqlalchemy.orm.declarative_base()


# Define models
class User(BASE):
    __tablename__ = 'steps'
    
    id = sqlalchemy.Column(sqlalchemy.UUID, primary_key=True)
    path = sqlalchemy.Column(sqlalchemy.String)
    ctime = sqlalchemy.Column(sqlalchemy.DateTime)
    mtime = sqlalchemy.Column(sqlalchemy.DateTime)
    step = sqlalchemy.Column(sqlalchemy.PickleType)


def setup_database(db_path=DB_ADDRESS):
    """
    Set up SQLite database with tables
    
    Args:
        db_path (str):      SQLite database path
        
    Returns:
        None
    """
    # Create engine
    engine = sqlalchemy.create_engine(str(db_path), echo=False)
    # Create tables
    BASE.metadata.create_all(engine)


def add_step(db_path=DB_ADDRESS, step=None):
    """
    Add sample data to the database
    
    Args:
        db_path (str):              SQLite database path
        step (step.Step, None):     Step object

    """
    # Build wrapper class
    obj = User(
        id=step.uuid,
        path=str(step.path),
        ctime=step.ctime,
        mtime=step.mtime,
        step=step,
        )

    engine = sqlalchemy.create_engine(db_path, echo=False)
    session = sqlalchemy.orm.sessionmaker(bind=engine)()
    
    # Add users to session
    session.add(obj)
    
    # Commit changes
    session.commit()


def query_step(db_path=DB_ADDRESS, uuid=None):
    """
    Query and display data from the database
    
    Args:
        db_path (str):              SQLite database path
        uuid (uuid.UUID)            UUID of step to extract
    """

    engine = sqlalchemy.create_engine(db_path, echo=False)
    session = sqlalchemy.orm.sessionmaker(bind=engine)()
    obj = session.get(User, uuid)
    step = obj.step
    return step


if __name__ == "__main__":
    import uuid
    import viz.steps
    wf = viz.steps.make_tmp_workflow()

    setup_database()
    add_step(step=wf)
    print(wf.uuid)
