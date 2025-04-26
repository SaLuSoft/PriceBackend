from pymongo import MongoClient
from datetime import datetime

host = 'mongodb'
port = 27017

def saveRequest(ip, code, version, uid, data):
    print(f'saveRequest(ip:{ip}, code:{code}, version:{version}, uid:{uid}, data:{data})')

    client = MongoClient(f'mongodb://{host}:{port}') #root:root@
    collection = client["Barcodes"]["Requests"]

    data = {
        "ip": ip,
        "code": code,
        "version": version,
        "uid": uid,
        "data": data,
        "date": datetime.now()
    }
    collection.insert_one(data)


def checkUser(uid):
    print(f'checkUser(uid:{uid})')
    client = MongoClient(f'mongodb://root:root@{host}:{port}')
    collection = client["Barcodes"]["UsersData"]

    user = collection.find_one({"_id": uid})
    if user:
        return user["available_date"] > datetime.now()
    else:
        return False


def addUser(uid, available_date):
    client = MongoClient(f'mongodb://root:root@{host}:{port}')
    collection = client["Barcodes"]["UsersData"]

    data = {
        "_id": uid,
        "available_date": available_date
    }

    if collection.find_one({"_id": uid}):
        collection.update_one({"_id": uid}, {"$set": data})
    else:
        collection.insert_one(data)
    print(f'addUser(uid:{uid}, available_date:{available_date})')


def setBarcodeData(barcode, name, code_atg, is_kilogram, is_tin):
    print(f'setBarcodeData(barcode:{barcode})')
    client = MongoClient(f'mongodb://root:root@{host}:{port}')
    collection = client["Barcodes"]["BarcodesData"]

    data = {
        "_id": barcode,
        "name": name,
        "code_atg": code_atg,
        "is_kilogram": is_kilogram,
        "is_tin": is_tin
    }

    if collection.find_one({"_id": barcode}):
        collection.update_one({"_id": barcode}, {"$set": data})
    else:
        collection.insert_one(data)


def getBarcodeData(barcode):
    print(f'getBarcodeData(barcode:{barcode})')
    client = MongoClient(f'mongodb://root:root@{host}:{port}')
    collection = client["Barcodes"]["BarcodesData"]

    data = collection.find_one({"_id": barcode})
    if data:
        return {
            "barcode": data["_id"],
            "name": data["name"],
            "code_atg": data["code_atg"],
            "is_kilogram": data["is_kilogram"],
            "is_tin": data["is_tin"]
        }
    else:
        raise Exception("I know Python!")


def checkBarcodes(barcodes):
    print(f'checkBarcodes(barcodes:{barcodes})')
    client = MongoClient(f'mongodb://root:root@{host}:{port}')
    collection = client["Barcodes"]["BarcodesData"]

    list = collection.find({"_id": {"$in": barcodes}})
    Res = []
    for barcode in list:
        Res.append(barcode["_id"])
    return Res


class DB_Barcode:
    def __init__(self, req_data):
        self.ip = req_data['ip']
        self.code = req_data['code']
        self.version = req_data['version']
        self.uid = req_data['uid']
        self.data = req_data['data']

    def saveRequest(self):
        client = MongoClient(f'mongodb://root:root@{host}:{port}')
        collection = client["Barcodes"]["Requests"]




if __name__ == '__main__':
    # saveRequest('localhost', 1, 1 , 'test', '1111')
    # addUser('test', datetime.strptime('01122025', "%d%m%Y"))
    # print(f'checkUser test is {checkUser("test")}')
    # print(f'checkUser test1 is {checkUser("test1")}')
    # setBarcodeData('2', 'apranq2', '0002', True, True)
    # print(getBarcodeData('2'))
    print(checkBarcodes(['1', '2', '3', '4']))

