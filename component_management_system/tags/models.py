import uuid

from config import db, app
from sqlalchemy.dialects.postgresql import UUID


class Tag(db.Model):

    __tablename__ = "tags"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label = db.Column(db.String(32), unique=True)
    metadata_id = db.Column(db.Integer, db.ForeignKey("metadatas.id"), nullable=True)

def init_db():

    with app.app_context():
        print("creating db")

        new_tag = Tag(label="car")
        db.session.add(new_tag)
        db.session.commit()


# if __name__ == '__main__':
init_db()
