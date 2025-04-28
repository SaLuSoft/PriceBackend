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
            'data': await request.json()
        }

        db = DB_Barcode.DB_Barcode(UserData)
        return db.checkBarcodes()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400)


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

        db = DB_Barcode.DB_Barcode(UserData)
        return db.getBarcodeData()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    port = int(os.environ.get('PY_PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)