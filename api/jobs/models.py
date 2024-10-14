from db.base_model import Model
from sqlalchemy import Column, String, Integer, Enum, ForeignKey, DateTime, Table, and_
from sqlalchemy.orm import relationship, Session
from api.users.models import User
from .schema import JobStatus, JobCreationRequest
from datetime import datetime


job_tag_association = Table(
    "job_tag",
    Model.metadata,
    Column("job_id", Integer, ForeignKey("job.id")),
    Column("tag_id", Integer, ForeignKey("tag.id")),
)


class Tag(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    # Many-to-Many relationship with Job
    jobs = relationship("Job", secondary=job_tag_association, back_populates="tags")


class Job(Model):
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    salary_range = Column(String, nullable=False)
    location = Column(String, nullable=False)
    job_owner = Column(ForeignKey(User.id), nullable=False)
    status = Column(Enum(JobStatus), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    last_updated = Column(DateTime, onupdate=datetime.now)

    # Many-to-Many relationship with Tag
    tags = relationship("Tag", secondary=job_tag_association, back_populates="jobs")


class JobManager:
    """A Manager to handle creation, updation and deletion of the Job"""

    @classmethod
    def create_job(cls, job: JobCreationRequest, user_id: int, db: Session):
        try:
            db_job = Job(
                title=job.title,
                description=job.description,
                salary_range=job.salary_range,
                location=",".join(job.location),
                job_owner=user_id,
                status=job.status,
            )            
            db_job.tags.extend([cls.create_or_return_tag(tag, db) for tag in job.tags])
            db.add(db_job)
            db.commit()
            db.refresh(db_job)
            return db_job
        except Exception as e:
            db.rollback()
            raise e

    @classmethod
    def get_job_posts(cls, db: Session, **kwargs):
        filterset = {k: v for k, v in kwargs.items() if v is not None}
        if not filterset:
            return db.query(Job).all()
        filters = cls.generate_filterset(filterset)
        return db.query(Job).filter(filters).all()

    @classmethod
    def create_or_return_tag(cls, tag_name, db: Session):
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            new_tag = Tag(name=tag_name)
            db.add(new_tag)
            db.commit()
            db.refresh(new_tag)
            return new_tag
        return tag

    @classmethod
    def generate_filterset(cls, filterset: dict):
        filters = []
        if filterset.get("id"):
            filters.append(Job.id == filterset.get("id"))
        if filterset.get("title"):
            filters.append(Job.title.ilike(f"%{filterset['title']}%"))
        return and_(*filters)
