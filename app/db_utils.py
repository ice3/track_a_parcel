"""Utilitary functions for database management."""

from app import db


def get_or_create(model, **kwargs):
    """Get a row if exist otherwise create it.

    Copy of django orm get_or_create.
    """
    instance = db.session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

