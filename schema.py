from __init__ import *


class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(80), unique=False)
    email = db.Column(db.VARCHAR(120), unique=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class Test_Features(db.Model):
    __tablename__ = "Test_Features"

    jobId = db.Column(db.VARCHAR(80), primary_key=True)
    companyId = db.Column(db.VARCHAR(10), unique=False)
    jobType = db.Column(db.VARCHAR(80), unique=False)
    degree = db.Column(db.VARCHAR(80), unique=False)
    major = db.Column(db.VARCHAR(80), unique=False)
    industry = db.Column(db.VARCHAR(80), unique=False)
    yearsOfExperience = db.Column(db.NUMERIC, unique=False)
    milesFromMetropolis = db.Column(db.NUMERIC, unique=False)

    def __init__(self, jobId, companyId, jobType, degree, major, industry, yearsOfExperience, milesFromMetropolis):
        self.jobId = jobId
        self.companyId = companyId
        self.jobType - jobType
        self.degree = degree
        self.major = major
        self.industry = industry
        self.yearsOfExperience = yearsOfExperience
        self.milesFromMetropolis = milesFromMetropolis


class Train_Features(db.Model):
    __tablename__ = "Train_Features"

    jobId = db.Column(db.VARCHAR(80), primary_key=True)
    companyId = db.Column(db.VARCHAR(10), unique=False)
    jobType = db.Column(db.VARCHAR(80), unique=False)
    degree = db.Column(db.VARCHAR(80), unique=False)
    major = db.Column(db.VARCHAR(80), unique=False)
    industry = db.Column(db.VARCHAR(80), unique=False)
    yearsOfExperience = db.Column(db.NUMERIC, unique=False)
    milesFromMetropolis = db.Column(db.NUMERIC, unique=False)

    def __init__(self, jobId, companyId, jobType,  degree, major, industry, yearsOfExperience, milesFromMetropolis):
        self.jobId = jobId
        self.companyId = companyId
        self.jobType = jobType
        self.degree = degree
        self.major = major
        self.industry = industry
        self.yearsOfExperience = yearsOfExperience
        self.milesFromMetropolis = milesFromMetropolis


class Train_salaries(db.Model):
    __tablename__ = "Train_Salaries"

    jobId = db.Column(db.VARCHAR(80), primary_key=True)
    salary = db.Column(db.Numeric, unique=False)

    def __init__(self, jobId, salary):
        self.jobId = jobId
        self.salary = salary
