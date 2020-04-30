from db import  db


class PatentModel(db.Model):
    __tablename__ ='patents'

    uniqueid = db.Column(db.String, primary_key=True)
    patentid = db.Column(db.String)
    filename = db.Column(db.String)
    zipfile = db.Column(db.LargeBinary)
    extuuid = db.Column(db.String)
    req_time = db.Column(db.Integer)

    def __init__(self, uniqueid, patentid, filename, zipfile, extuuid, req_time):
        self.uniqueid = uniqueid
        self.patentid = patentid
        self.filename = filename
        self.zipfile = zipfile
        self.extuuid = extuuid
        self.req_time = req_time


    @classmethod
    def find_by_uniqueid(cls, uniqueid):
        return cls.query.filter_by(uniqueid = uniqueid).first()

    def find_by_extuuid(cls, extuuid):
        return cls.query.filter_by(extuuid = extuuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    