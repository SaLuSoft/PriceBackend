from fastapi import FastAPI, Request, HTTPException
import uvicorn
import os
import DB_Barcode


env = {
    'PY_PORT': int(os.environ.get('PY_PORT')),
    'MONGO_HOST': os.environ.get('MONGO_HOST'),
    'MONGO_PORT': int(os.environ.get('MONGO_PORT')),
    'MONGO_USERNAME': os.environ.get('MONGO_INITDB_ROOT_USERNAME'),
    'MONGO_PASSWORD': os.environ.get('MONGO_INITDB_ROOT_PASSWORD')
}
print('env', env)

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

        db = DB_Barcode.DB_Barcode(env, UserData)
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

        db = DB_Barcode.DB_Barcode(env, UserData)
        return db.getBarcodeData()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=env['PY_PORT'])