# List all model as imports here to enable alembic to detect them
from db.base_model import Model
from api.users.models import User
from api.jobs.models import Job, Tag
