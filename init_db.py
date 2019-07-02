from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(engine_options={'isolation_level': 'SERIALIZABLE'})
