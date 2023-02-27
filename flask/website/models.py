from datetime import datetime
from email.policy import default

from . import db

from flask_login import UserMixin
from sqlalchemy.dialects.mysql import (
    INTEGER,
    VARCHAR,
    SMALLINT,
    FLOAT,
    TINYINT,
    BIGINT,
    BOOLEAN,
)


job_tag = db.Table(
    "job_tag",
    db.Column(
        "id_tag", TINYINT(unsigned=True), db.ForeignKey("tag.id"), nullable=False
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
        "id_tag", TINYINT(unsigned=True), db.ForeignKey("tag.id"), nullable=False
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

    def to_dict(self) -> dict:
        dict = self.__dict__.copy()
        dict.pop("_sa_instance_state", "")
        return dict


# TODO: add Job description
class Job(db.Model):
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    id_status = db.Column(
        TINYINT(unsigned=True), db.ForeignKey("status.id"), nullable=False
    )
    name = db.Column(VARCHAR(32), nullable=False)
    description = db.Column(VARCHAR(2000), nullable=False)
    duration = db.Column(SMALLINT(unsigned=True), nullable=False)
    time_start = db.Column(INTEGER(unsigned=True), nullable=False)
    payment = db.Column(INTEGER(unsigned=True), nullable=False)
    rating = db.Column(FLOAT(unsigned=True), nullable=False)
    id_employer = db.Column(
        INTEGER(unsigned=True), db.ForeignKey("user.id"), nullable=False
    )
    id_location = db.Column(
        INTEGER(unsigned=True), db.ForeignKey("location.id"), nullable=False
    )
    tags = db.relationship("Tag", secondary=job_tag, backref="jobs", lazy="dynamic")

    def to_dict(self, short=False) -> dict:
        if short:
            dict = {
                "id": self.id,
                "name": self.name,
                "duration": self.duration,
                "payment": self.payment,
                "time_start": self.time_start,
                "tags": [tag.name for tag in self.tags],
            }
        else:
            dict = self.__dict__.copy()
            dict.pop("_sa_instance_state", "")
        return dict


class Location(db.Model):
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    post_code = db.Column(VARCHAR(10), nullable=False)
    id_city = db.Column(VARCHAR(32), db.ForeignKey("city.name"), nullable=False)
    users = db.relationship("User", backref="location", lazy="dynamic")
    jobs = db.relationship("Job", backref="location", lazy="dynamic")

    def to_dict(self) -> dict:
        dict = self.__dict__.copy()
        dict.pop("_sa_instance_state", "")
        return dict


class Message(db.Model):
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    content = db.Column(VARCHAR(2000), nullable=False)
    time = db.Column(BIGINT(unsigned=True), nullable=False)
    received = db.Column(BOOLEAN(), default=False)
    id_user_send = db.Column(
        INTEGER(unsigned=True), db.ForeignKey("user.id"), nullable=False
    )
    id_user_receive = db.Column(
        INTEGER(unsigned=True), db.ForeignKey("user.id"), nullable=False
    )

    def to_dict(self) -> dict:
        dict = self.__dict__.copy()
        dict.pop("_sa_instance_state", "")
        return dict


class Status(db.Model):
    id = db.Column(TINYINT(unsigned=True), primary_key=True)
    name = db.Column(VARCHAR(16), nullable=False)
    description = db.Column(VARCHAR(1000), default="")
    jobs = db.relationship("Job", backref="status", lazy="dynamic")

    def to_dict(self) -> dict:
        dict = self.__dict__.copy()
        dict.pop("_sa_instance_state", "")
        return dict


class Tag(db.Model):
    id = db.Column(TINYINT(unsigned=True), primary_key=True)
    name = db.Column(VARCHAR(16), nullable=False)
    description = db.Column(VARCHAR(1000), default="")

    def to_dict(self) -> dict:
        dict = self.__dict__.copy()
        dict.pop("_sa_instance_state", "")
        return dict


class Timeblock(db.Model):
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    start = db.Column(INTEGER(unsigned=True), nullable=False)
    end = db.Column(INTEGER(unsigned=True), nullable=False)

    def to_dict(self) -> dict:
        dict = self.__dict__.copy()
        dict.pop("_sa_instance_state", "")
        return dict


class User(db.Model, UserMixin):
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    email = db.Column(VARCHAR(64), nullable=False, unique=True)
    first_name = db.Column(VARCHAR(32), nullable=False)
    last_name = db.Column(VARCHAR(32), nullable=False)
    password = db.Column(VARCHAR(88), nullable=False)
    id_location = db.Column(
        INTEGER(unsigned=True), db.ForeignKey("location.id"), nullable=False
    )
    completed_jobs = db.Column(INTEGER(unsigned=True), default=0)
    rating = db.Column(FLOAT(unsigned=True), default=0.0)
    cnt_ratings = db.Column(INTEGER(unsigned=True), default=0)
    description = db.Column(VARCHAR(2000), default="")
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

    def to_dict(self) -> dict:
        dict = self.__dict__.copy()
        dict.pop("_sa_instance_state")
        return dict


def create_city(name: str) -> City:
    city = City.query.filter_by(name=name).first()
    if not city:
        city = City(name=name)
        db.session.add(city)
        db.session.commit()
    return city


def create_location(post_code: str, city: City) -> Location:
    location = city.locations.filter_by(post_code=post_code).first()
    if not location:
        location = Location(post_code=post_code, city=city)
        db.session.add(location)
        db.session.commit()
    return location


def create_timeblock(
    start_day: int, start_time: str, end_day: int, end_time: str
) -> Timeblock:
    start = int(
        datetime(
            2000,
            1,
            start_day,
            int(start_time.split(":")[0]),
            int(start_time.split(":")[1]),
        ).timestamp()
    )
    end = int(
        datetime(
            2000, 1, end_day, int(end_time.split(":")[0]), int(end_time.split(":")[1])
        ).timestamp()
    )
    timeblock = Timeblock.query.filter_by(start=start, end=end).first()
    if not timeblock:
        timeblock = Timeblock(start=start, end=end)
        db.session.add(timeblock)
        db.session.commit()
    return timeblock


def create_user_db(
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
    city = create_city(city)
    location = create_location(post_code, city)
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


def get_rating_job(payment: int, duration: int, employer: User) -> float:
    # salery = payment / duration [min: 1, max: 50]
    # employer_score = employer.rating * (10 + employer.cnt_rating) [min: 10, max: 100++]
    # score = salery * employer_score

    salery = payment / duration
    if salery < 1:
        salery = 1
    elif salery > 50:
        salery = 50
    employer_rating = 1 if employer.rating < 1 else employer.rating
    employer_score = employer_rating * (10 + employer.cnt_ratings)
    return salery * employer_score


def create_job_db(
    employer: User,
    name: str,
    duration: int,
    time_start: int,
    payment: int,
    post_code: str,
    city: str,
    tags: list[str],
    status: Status = None,
) -> Job:
    if not status:
        status = Status.query.filter_by(name="Nicht Vergeben").first()
    for i, tag in enumerate(tags):
        tags[i] = Tag.query.filter_by(name=tag).first()
    city = create_city(city)
    location = create_location(post_code, city)
    job = Job(
        employer=employer,
        name=name,
        duration=duration,
        description="",
        time_start=time_start,
        payment=payment,
        rating=get_rating_job(payment, duration, employer),
        location=location,
        tags=tags,
        status=status,
    )
    db.session.add(job)
    db.session.commit()
    return job
