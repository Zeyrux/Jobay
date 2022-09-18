from . import db
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, SMALLINT, FLOAT


job_tag = db.Table(
    "job_tag",
    # db.Column("id_tag", TINYINT(unsigned=True), db.ForeignKey("tag.id"), nullable=False),
    db.Column(
        "id_tag", SMALLINT(unsigned=True), db.ForeignKey("tag.id"), nullable=False
    ),
    db.Column(
        "id_job", INTEGER(unsigned=True), db.ForeignKey("job.id"), nullable=False
    ),
)

user_tag = db.Table(
    "user_tag",
    db.Column(
        "id_user", INTEGER(unsigned=True), db.ForeignKey("user.id"), nullable=False
    ),
    db.Column(
        "id_tag", INTEGER(unsigned=True), db.ForeignKey("tag.id"), nullable=False
    ),
)

available_timeblock = db.Table(
    "available_timeblock",
    db.Column(
        "id_user", INTEGER(unsigned=True), db.ForeignKey("user.id"), nullable=False
    ),
    db.Column(
        "id_timeblock",
        INTEGER(unsigned=True),
        db.ForeignKey("timeblock.id"),
        nullable=False,
    ),
)


class City(db.Model):
    name = db.Column(VARCHAR(32), primary_key=True)
    locations = db.relationship("Location", backref="city", lazy="dynamic")


class Job(db.Model):
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    # id_status = db.Column(TINYINT(unsigned=True), db.ForeignKey('job.id'), nullable=False)
    id_status = db.Column(
        SMALLINT(unsigned=True), db.ForeignKey("status.id"), nullable=False
    )
    name = db.Column(VARCHAR(32), nullable=False)
    duration = db.Column(SMALLINT(unsigned=True), nullable=False)
    time_start = db.Column(FLOAT(unsigned=True), nullable=False)
    payment = db.Column(FLOAT(unsigned=True), nullable=False)
    id_employer = db.Column(
        INTEGER(unsigned=True), db.ForeignKey("user.id"), nullable=False
    )
    id_location = db.Column(
        INTEGER(unsigned=True), db.ForeignKey("location.id"), nullable=False
    )
    tags = db.relationship("Tag", secondary=job_tag, backref="jobs", lazy="dynamic")


class Location(db.Model):
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    post_code = db.Column(VARCHAR(10), nullable=False)
    id_city = db.Column(VARCHAR(32), db.ForeignKey("city.name"), nullable=False)
    users = db.relationship("User", backref="location", lazy="dynamic")
    jobs = db.relationship("Job", backref="location", lazy="dynamic")


class Message(db.Model):
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    id_user_send = db.Column(
        INTEGER(unsigned=True), db.ForeignKey("user.id"), nullable=False
    )
    id_user_receive = db.Column(
        INTEGER(unsigned=True), db.ForeignKey("user.id"), nullable=False
    )


class Status(db.Model):
    # id = db.Column(TINYINT(unsigned=True), primary_key=True)
    id = db.Column(SMALLINT(unsigned=True), primary_key=True)
    name = db.Column(VARCHAR(16), nullable=False)
    description = db.Column(VARCHAR(1024), default="")
    jobs = db.relationship("Job", backref="status", lazy="dynamic")


class Tag(db.Model):
    # id = db.Column(TINYINT(unsigned=True), primary_key=True)
    id = db.Column(SMALLINT(unsigned=True), primary_key=True)
    name = db.Column(VARCHAR(16), nullable=False)
    description = db.Column(VARCHAR(1024), default="")


class Timeblock(db.Model):
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    start = db.Column(FLOAT(unsigned=True), nullable=False)
    end = db.Column(FLOAT(unsigned=True), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    email = db.Column(VARCHAR(64), nullable=False, unique=True)
    first_name = db.Column(VARCHAR(32), nullable=False)
    last_name = db.Column(VARCHAR(16), nullable=False)
    password = db.Column(VARCHAR(88), nullable=False)
    id_location = db.Column(
        INTEGER(unsigned=True), db.ForeignKey("location.id"), nullable=False
    )
    completed_jobs = db.Column(INTEGER(unsigned=True), default=0)
    rating = db.Column(FLOAT(unsigned=True), default=0.0)
    cnt_ratings = db.Column(INTEGER(unsigned=True), default=0)
    description = db.Column(VARCHAR(2048), default="")
    timeblocks = db.relationship(
        "Timeblock", secondary=available_timeblock, backref="users", lazy="dynamic"
    )
    messages_send = db.relationship(
        "Message",
        foreign_keys="Message.id_user_send",
        backref="user_send",
        lazy="dynamic",
    )
    messages_receive = db.relationship(
        "Message",
        foreign_keys="Message.id_user_receive",
        backref="user_receive",
        lazy="dynamic",
    )
    tags = db.relationship("Tag", secondary=user_tag, backref="users", lazy="dynamic")
    employs = db.relationship("Job", backref="employer", lazy="dynamic")


def create_user(
    email: str,
    first_name: str,
    last_name: str,
    password: str,
    post_code: int,
    city: str,
) -> User:
    # check if user exists
    if User.query.filter_by(email=email).first():
        raise Exception("User already exists")
    # check if city exists
    city_db = City.query.filter_by(name=city).first()
    if not city_db:
        city_db = City(name=city)
        db.session.add(city_db)
        db.session.commit()
    # check if location exists
    location = city_db.locations.filter_by(post_code=post_code).first()
    if not location:
        location = Location(post_code=post_code, city=city_db)
        db.session.add(location)
        db.session.commit()
    # create new user
    user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password,
        location=location,
    )
    db.session.add(user)
    db.session.commit()
    return user
