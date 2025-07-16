from peewee import SqliteDatabase, CharField, DateTimeField, Model
from config import BASEDIR
from datetime import datetime
import os

db = SqliteDatabase(os.path.join(BASEDIR, "log", "visits.db"))


class BaseModel(Model):
    class Meta:
        database = db

class Visit(BaseModel):
    ip = CharField(max_length=60)
    timestamp = DateTimeField(default=datetime.now)
    # 0- means site loaded
    type = CharField(default='0')

db.connect()
db.create_tables([Visit])
db.close()
