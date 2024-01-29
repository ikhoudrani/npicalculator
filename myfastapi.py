from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from npicalculator import npicalculator
from pydantic import BaseModel
import pymongo
import csv
import io

app = FastAPI()

client = pymongo.MongoClient(host='localhost', port=27017)
database = client.calculatorDB
collection = database.operation_and_result

class NPIExpression(BaseModel):
    expression: str

class OperationResult(BaseModel):
    operation: str
    result: int


@app.post("/calculate")
async def calculate(npi_expression: NPIExpression):
    try:
        result = npicalculator(npi_expression.expression)
        await save_operation_result(npi_expression.expression, result)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/save_operation_result")
async def save_operation_result(operation: str, result: int):
    try:
        operation_result = {
            "operation": operation,
            "result": result
        }
        collection.insert_one(operation_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de l'enregistrement de l'opération")

    return {"message": "Opération enregistrée"}


@app.get("/download_csv")
def download_csv():
    cursor = collection.find({})
    print(cursor)
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')  

    writer.writerow(['Operation', 'Result'])

    for doc in cursor:
        writer.writerow([doc['operation'], doc['result']])

    output.seek(0)
    return Response(content=output.read(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=operations_results.csv"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
