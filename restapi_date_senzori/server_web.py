import time
import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse


app = FastAPI()

# Modelul pentru datele de senzor
class DateSenzor(BaseModel):
    timestamp: float
    tip: str
    valoare: float


# Listă pentru stocarea datelor senzorilor
lista_date_senzori = []


# Endpoint pentru primirea datelor senzorilor
@app.post("/senzori")
async def receive_sensor_data(data: DateSenzor):
    lista_date_senzori.append(data)
    return {"status": "Datele au fost primite"}


# Endpoint pentru a afișa datele într-o pagină HTML
@app.get("/", response_class=HTMLResponse)
async def display_data():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Date senzori</title>
        <!-- Bootstrap CSS -->
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    </head>

    <body>
        <div class="container mt-5">
            <h1 class="mb-4">Date senzori</h1>
            <button onclick="location.reload()" class="btn btn-primary mb-3">Reîncarcă</button>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Tip de senzor</th>
                        <th>Valoare</th>
                    </tr>
                </thead>
            <tbody>
    """
    
    # Generează un tabel cu 5 rânduri care cuprind
    # ultimele înregistrări de la client
    for data in lista_date_senzori[-5:]:
        dt_object = datetime.datetime.fromtimestamp(data.timestamp)
        timp_formatat = dt_object.strftime("%H:%M:%S")
        html_content += f"""
            <tr>
                <td>{timp_formatat}</td>
                <td>{data.tip}</td>
                <td>{data.valoare}</td>
            </tr>
        """
        
    html_content += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)