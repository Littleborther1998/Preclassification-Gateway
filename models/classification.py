from db import  db

class ClassificationModel(db.Model):
    __tablename__ ='classification'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uniqueid = db.Column(db.String, db.ForeignKey('patents.uniqueid'))
    patentid = db.Column(db.String)
    rank = db.Column(db.Integer)
    precla_symbol = db.Column(db.String)
    confidence = db.Column(db.Float)
    source = db.Column(db.String)
    class_time = db.Column(db.Integer)
    patent = db.relationship('PatentModel')
    

    def __init__(self, uniqueid, patentid, rank, precla_symbol, confidence, source, class_time):
        self.uniqueid = uniqueid
        self.patentid = patentid
        self.rank = rank
        self.precla_symbol = precla_symbol
        self.confidence = confidence
        self.source = source
        self.class_time = class_time

    @classmethod
    def find_by_uniqueid(cls, uniqueid):
        return cls.query.filter_by(uniqueid = uniqueid)
    
    def find_by_extuuid(cls, patentid):
        return cls.query.filter_by(patendid = patentid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
      
      