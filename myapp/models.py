from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:////Users/ellis/Documents/scripts/arboretum/orchestrator/orchestrator.db', echo=True)
SessionLocal = sessionmaker(bind=engine)