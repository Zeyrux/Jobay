from .models import Status, Tag


def init_db(db):
    status_untaken = Status.query.filter_by(name="Nicht Vergeben").first()
    if not status_untaken:
        status_untaken = Status(
            name="Nicht Vergeben",
            description="Ich bin die lange description für nicht vergeben",
        )
        db.session.add(status_untaken)
    tags = [tag.name for tag in Tag.query.all()]
    if not "Software" in tags:
        tag = Tag(
            name="Software",
            description="Für Personen mit Kenntnissen in der Software entwicklung.",
        )
        db.session.add(tag)
    if not "Gärtner" in tags:
        tag = Tag(name="Gärtner", description="Gärtner halt")
        db.session.add(tag)
    if not "Testiger9101234" in tags:
        tag = Tag(name="Testiger9101234", description="Testiger9101234")
        db.session.add(tag)
    if not "Testiger1234567" in tags:
        tag = Tag(name="Testiger1234567", description="Testiger1234567")
        db.session.add(tag)
    db.session.commit()
