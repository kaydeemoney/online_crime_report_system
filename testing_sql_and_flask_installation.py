try:
    import flask
    print(f"Flask is installed, version: {flask.__version__}")
except ImportError:
    print("Flask is not installed.")

try:
    import sqlalchemy
    print(f"SQLAlchemy is installed, version: {sqlalchemy.__version__}")
except ImportError:
    print("SQLAlchemy is not installed.")
