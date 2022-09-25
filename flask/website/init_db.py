from .models import Status, Timeblock, User


def init_db(db):
    status_untaken = Status.query.filter_by(name="Nicht Vergeben").first()
    if not status_untaken:
        status_untaken = Status(
            name="Nicht Vergeben",
            description="Ich bin die lange description für nicht vergeben",
        )
        db.session.add(status_untaken)
        db.session.commit()
