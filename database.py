from sqlmodel import SQLModel, create_engine, Session

# Database URL for SQLite
DATABASE_URL = "sqlite:///dabbewala.db"


# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)


# Create a tables for db.
def create_tables():
    SQLModel.metadata.create_all(engine)


# Get a new database session
def get_session():
    with Session(engine) as session:
        yield session
