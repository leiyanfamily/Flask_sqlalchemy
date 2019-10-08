import functools

from db_config import db


def set_read_db(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        db.session().set_to_read()
        return f(*args, **kwargs)

    return wrapper


def set_write_db(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        db.session().set_to_write()
        return f(*args, **kwargs)

    return wrapper