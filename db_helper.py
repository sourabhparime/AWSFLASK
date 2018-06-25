from __init__ import *
from odo import odo


def push_to_db(path,filename):
    print(path)
    odo(path, 'mysql+pymysql://user:password@localhost/fl::'+filename[:-4])
    return True


def clear_all_tables():
    # dropping all tables, I do not want to keep a list of emails submitted.
    db.drop_all()
    db.create_all()
    return True





