from pymongo import MongoClient
from datetime import datetime
import os


host = os.environ.get('MONGO_HOST', 'localhost')
port = 27017
login = os.environ.get('MONGO_USERNAME', 'root')
password = os.environ.get('MONGO_PASSWORD', 'root')

if login != '':
    mongo_uri = f'mongodb://{login}:{password}@{host}:{port}/'
else:
    mongo_uri = f'mongodb://{host}:{port}/'


class DB_Barcode:
    def __init__(self, req_data):
        self.ip = req_data['ip']
        self.code = req_data['code']
        self.version = req_data['version']
        self.uid = req_data['uid']
        self.data = req_data['data']

        client = MongoClient(mongo_uri)
        self.db = client["Barcodes"]

        self.saveRequest()
        self.checkUser()

    def saveRequest(self):
        collection = self.db["Requests"]
        data = {
            "ip": self.ip,
            "code": self.code,
            "version": self.version,
            "uid": self.uid,
            "data": self.data,
            "date": datetime.now()
        }
        collection.insert_one(data)

    def checkUser(self):
        print(f'checkUser(uid:{self.uid})')
        collection = self.db["UsersData"]

        user = collection.find_one({"_id": self.uid})
        if user == None or user["available_date"] < datetime.now():
            raise 'Հաճախորդը գրացված չէ'

    def getBarcodeData(self):
        print(f'getBarcodeData(barcode:{self.data})')
        collection = self.db["BarcodesData"]

        data = collection.find_one({"_id": self.data})
        if data:
            return {
                "barcode": data["_id"],
                "name": data["name"],
                "code_atg": data["code_atg"],
                "is_kilogram": data["is_kilogram"],
                "is_tin": data["is_tin"]
            }
        else:
            raise Exception("I love Python!")

    def checkBarcodes(self):
        print(f'checkBarcodes(barcodes:{self.data})')
        collection = self.db["BarcodesData"]

        list = collection.find({"_id": {"$in": self.data}})
        Res = []
        for barcode in list:
            Res.append(barcode["_id"])
        return Res


if __name__ == '__main__':

    UserData = {
        'ip': 'localhost',
        'code': '1',
        'version': '1',
        'uid': 'test',
        'data': ['1','2', '3', '4', '5', '6', '7', '8', '9']
    }
    db = DB_Barcode(UserData)
    # print(db.getBarcodeData())
    print(db.checkBarcodes())