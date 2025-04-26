from fastapi import FastAPI, Request, HTTPException
import uvicorn
import os
from datetime import datetime
import DB_Barcode

app = FastAPI()

@app.post("/Price/hs/BC/AvBC")
async def CheckBarcodes(request: Request):
    try:
        UserData = {
            'ip': request.client.host,
            'code': request.headers['code'],
            'version': request.headers['vers'],
            'uid': request.headers['uid'],
            'data': (await request.body()).decode('utf8')
        }
    except Exception:
        raise HTTPException(status_code=400)

    DB_Barcode.saveRequest(**UserData)

    if not DB_Barcode.checkUser(UserData['uid']):
        raise HTTPException(status_code=404, detail='Հաճախորդը գրացված չէ')

    BarcodeData = DB_Barcode.checkBarcodes(UserData['data'])

    return BarcodeData


@app.post("/Price/hs/BC/GD")
async def getBarcodeData(request: Request):
    try:
        UserData = {
            'ip': request.client.host,
            'code': request.headers['code'],
            'version': request.headers['vers'],
            'uid': request.headers['uid'],
            'data': (await request.body()).decode('utf8')
        }
    except Exception:
        raise HTTPException(status_code=400)

    DB_Barcode.saveRequest(**UserData)

    if not DB_Barcode.checkUser(UserData['uid']):
        raise HTTPException(status_code=404, detail='Հաճախորդը գրացված չէ')

    try:
        BarcodeData = DB_Barcode.getBarcodeData(UserData['data'])
    except Exception:
        raise HTTPException(status_code=404)

    return BarcodeData


@app.post('/Price/admin')
async def admin(request: Request):
    try:
        UserData = {
            'ip': request.client.host,
            'code': request.headers['code'],
            'version': request.headers['vers'],
            'uid': request.headers['uid'],
            'data': await request.json()
        }

        DB_Barcode.saveRequest(**UserData)
        if UserData['data']['action'] == 'addUser':
            available_date = datetime.strptime(UserData['data']['available_date'], "%d%m%Y")
            DB_Barcode.addUser(UserData['data']['uid'], available_date)
        elif UserData['data']['action'] == 'setBarcodeData':
            for barcode in UserData['data']['barcodes']:
                DB_Barcode.setBarcodeData(**barcode)
        else:
            raise HTTPException(status_code=404)


        return "Ok"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400)


if __name__ == "__main__":
    MYPORT = int(os.environ.get('MYPORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=MYPORT)