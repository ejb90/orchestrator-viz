"""Make a class which is then added to the database."""

import pathlib

import sqlalchemy
import sqlalchemy.ext
import sqlalchemy.orm


RDBMS = "sqlite"
DATABASE = pathlib.Path("analyser.db")
DB_ADDRESS = f"{RDBMS}:///{DATABASE}"

# Create base class for declarative models
BASE = sqlalchemy.orm.declarative_base()


class Result(BASE):
    """
    Wrapper class for results inside the database
    """

    __tablename__ = "results"

    id = sqlalchemy.Column(sqlalchemy.UUID, primary_key=True)
    version = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    model = sqlalchemy.Column(sqlalchemy.String)
    path = sqlalchemy.Column(sqlalchemy.String)
    datetime = sqlalchemy.Column(sqlalchemy.DateTime)

    storage = sqlalchemy.Column(sqlalchemy.Float)
    runtime = sqlalchemy.Column(sqlalchemy.Float)
    cpuhours = sqlalchemy.Column(sqlalchemy.Float)
    memory_total_hwm = sqlalchemy.Column(sqlalchemy.Float)
    memory_max_node_hwm = sqlalchemy.Column(sqlalchemy.Float)
    memory_mean_node_hwm = sqlalchemy.Column(sqlalchemy.Float)
    memory_min_node_hwm = sqlalchemy.Column(sqlalchemy.Float)
    
    equilibriation_time = sqlalchemy.Column(sqlalchemy.Float)
    equilibriation_temperature = sqlalchemy.Column(sqlalchemy.Float)
    internal_energy = sqlalchemy.Column(sqlalchemy.Float)
    total_ie = sqlalchemy.Column(sqlalchemy.Float)
    total_er = sqlalchemy.Column(sqlalchemy.Float)
    energy_conservation = sqlalchemy.Column(sqlalchemy.Float)

    step = sqlalchemy.Column(sqlalchemy.PickleType)    
    result = sqlalchemy.Column(sqlalchemy.PickleType)


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


def add_result(db_path=DB_ADDRESS, result=None):
    """
    Add sample data to the database

    Args:
        db_path (str):              SQLite database path
        step (step.Step, None):     Step object

    Returns:
        None
    """
    # Build wrapper class
    obj = Result(
        id = result.id,
        version = result.version,
        name = result.name,
        model = result.model,
        path = str(result.path),
        datetime = result.datetime,

        storage = result.storage,
        runtime = result.runtime,
        cpuhours = result.cpuhours,
        memory_total_hwm = result.memory_total_hwm,
        memory_max_node_hwm = result.memory_max_node_hwm,
        memory_mean_node_hwm = result.memory_mean_node_hwm,
        memory_min_node_hwm = result.memory_min_node_hwm,
        
        equilibriation_time = result.equilibriation_time,
        equilibriation_temperature = result.equilibriation_temperature,
        internal_energy = result.internal_energy,
        total_ie = result.total_ie,
        total_er = result.total_er,
        energy_conservation = result.energy_conservation,

        step = None,
        result = result,
    )

    engine = sqlalchemy.create_engine(db_path, echo=False)
    session = sqlalchemy.orm.sessionmaker(bind=engine)()

    # Add users to session
    session.add(obj)

    # Commit changes
    session.commit()


def query_result_by_uuid(db_path=DB_ADDRESS, uuid=None):
    """
    Query and display data from the database

    Args:
        db_path (str):              SQLite database path
        uuid (uuid.UUID)            UUID of step to extract

    Returns:
        step (step.Step)            Retrieved step
    """

    engine = sqlalchemy.create_engine(db_path, echo=False)
    session = sqlalchemy.orm.sessionmaker(bind=engine)()
    obj = session.get(Result, uuid)
    step = obj.step if obj is not None else None
    return step

