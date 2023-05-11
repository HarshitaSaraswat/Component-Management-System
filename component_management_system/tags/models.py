from database import Base, db


class Tag(Base):

    __tablename__ = "tags"
    label = db.Column(db.String(32), unique=True)

    def __repr__(self):
        return f'<Tag "{self.label}">'
