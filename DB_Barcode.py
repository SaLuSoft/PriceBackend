from pymongo import MongoClient
from datetime import datetime


class DB_Barcode:
    def __init__(self, env, req_data):
        self.ip = req_data['ip']
        self.code = req_data['code']
        self.version = req_data['version']
        self.uid = req_data['uid']
        self.data = req_data['data']

        mongo_uri = f'mongodb://{env["MONGO_USERNAME"]}:{env["MONGO_PASSWORD"]}@{env["MONGO_HOST"]}:{env["MONGO_PORT"]}/'

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
            raise Exception('Հաճախորդը գրացված չէ')

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
            raise Exception("Շտրիխկոդը չի գտնվել")

    def checkBarcodes(self):
        print(f'checkBarcodes(barcodes:{self.data})')
        collection = self.db["BarcodesData"]

        list_barcodes = self.data.split('|')
        list = collection.find({"_id": {"$in": list_barcodes}})
        Res = []
        for barcode in list:
            Res.append(barcode["_id"])
        return '|'.join(Res)


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