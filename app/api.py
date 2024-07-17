import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from os.path import join, dirname, exists

from Google.google import download_file
from Plots.plot import generate_plot_data, update_plot_data

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://localhost:9000",
    "https://api.gonzalo-oberreuter.de",
    "https://www.gonzalo-oberreuter.de",
    "https://gonzalo-oberreuter.de"
]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['GET', 'OPTION'],
        allow_headers=['Content-Type'],
        expose_headers=["*"]
)

def add_header(request: Request, response: Response):
    if 'Origin' in request.headers and request.headers['Origin'] in origins:
        response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']

@app.get("/plots")
async def get_plots(request: Request, response: Response):
    add_header(request, response)
    return generate_plot_data('./app/job-app.xlsx')

@app.get("/updatePlots")
async def get_updatePlots(request: Request, response: Response):
    add_header(request, response)
    return update_plot_data()

if (not exists('./app/job-app.xlsx')):
    download_file("job-app.xlsx")

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=9000)