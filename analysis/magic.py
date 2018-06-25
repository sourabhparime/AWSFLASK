import subprocess
from odo import odo
import os, shutil
from drive_upload import *


def run_salary(app, g):
    # delete previously saved temp files if any and create a new one
    shutil.rmtree("tmp", ignore_errors=True)
    os.mkdir("tmp")
    # need to find a better way to import with headers
    odo(app.config["SQLALCHEMY_DATABASE_URI"] + "::" + "test_features", "tmp/test_feat_retrieved.csv", )
    odo(app.config["SQLALCHEMY_DATABASE_URI"] + "::" + "train_features", "tmp/train_feat_retrieved.csv")
    odo(app.config["SQLALCHEMY_DATABASE_URI"] + "::" + "train_salaries", "tmp/train_sal_retrieved.csv")
    g.test_feat_path = "tmp/test_feat_retrieved.csv"
    g.train_feat_path = "tmp/train_feat_retrieved.csv"
    g.train_sal_path = "tmp/train_sal_retrieved.csv"
    print(os.getcwd())
    p = subprocess.Popen(
        "python salary_pred.py " + g.test_feat_path + " " + g.train_feat_path + " " + g.train_sal_path ,
        shell=False,
        cwd=os.getcwd() + "/analysis")
    p.wait()
    print("script run")
    return True
