__author__ = 'Regend'

from db import db


class Project(db.Model):
    __tablename__ = 'Project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR)
    moduleId = db.Column(db.Integer)
    k8sAddr = db.Column(db.VARCHAR, nullable=True)
    privateAddr = db.Column(db.VARCHAR, nullable=True)
    publicAddr = db.Column(db.VARCHAR, nullable=True)
    env = db.Column(db.VARCHAR, nullable=True)
    http = db.Column(db.VARCHAR, nullable=True)
    remark = db.Column(db.VARCHAR, nullable=True)
    lastupdatetime = db.Column(db.DATE, nullable=True)

    def __repr__(self):
        return self.name


class Module(db.Model):
    __tablename__ = 'Module'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR)
    order = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return self.name
