from __init__ import *
from schema import Users
from odo import odo


def ins_usr():
    users = Users("dfghjkl", "spaim2@uic.edu")  # type: Users
    db.session.add(users)
    db.session.commit()


def push_to_db(path,filename):
    print(path)
    odo(path, 'mysql+pymysql://user:password@localhost/fl::'+filename[:-4])
    return True


def clear_all_tables():
    db.drop_all()
    db.create_all()
    return True





