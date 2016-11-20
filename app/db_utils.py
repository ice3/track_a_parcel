"""Utilitary functions for database management."""


def get_or_create(session, model, **kwargs):
    """Get a row if exist otherwise create it.

    Copy of django orm get_or_create.
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

