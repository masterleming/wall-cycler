# TimestampStore

from datetime import datetime


class TimestampStore:
    @staticmethod
    def readTimestamp(db):
        timestamp = db['last timestamp']
        msg = db['timestamp msg']

        return timestamp, msg

    @staticmethod
    def writeTimestamp(db, msg):
        db['last timestamp'] = datetime.now()
        db['timestamp msg'] = msg
