from oso import Oso
from sqlalchemy_oso import SQLAlchemyOso, SQLAlchemyAdapter
from app2.db import Base, SessionLocal
from app2 import models

# Create Oso instance
oso = Oso()

# Initialize SQLAlchemyOso with your models' Base
sqlalchemy_oso = SQLAlchemyOso(Base)

# Register classes so Polar knows them
# sqlalchemy_oso.register_models()

# Register adapter so authorized_query works
adapter = SQLAlchemyAdapter(SessionLocal())
oso.set_data_filtering_adapter(adapter)

# Load policy file
oso.load_files(["app2/policy.polar"])
