from datetime import datetime
import pandas as pd
import numpy as np
import os
from Google.google import download_file


def generate_plot_data(file_name: str) -> dict:

    frame = pd.read_excel(file_name)
    frame['Sent Date'] = pd.to_datetime(frame['Sent Date'], format='%d-%m-%Y')
    frame = frame.sort_values(by='Sent Date')

    frame['Sent Date'] = pd.to_datetime(frame['Sent Date']) - pd.to_timedelta(7, unit='d')
    frame['Quantity'] = 1

    frame = frame.groupby(pd.Grouper(key='Sent Date', freq='W-MON'))['Quantity'].sum()

    x = [datetime.strftime(x,"%d-%m-%Y") for x in frame.index]
    y = [val.item() for val in list(np.cumsum(frame.values))]

    if len(x) > 20:
        x = x[-20:]
        y = y[-20:]

    return {'x_axis' : x, 'y_axis': y}

def update_plot_data() -> dict:
    ns = os.path.getctime('./app/job-app.xlsx')
    c_ti = datetime.fromtimestamp(ns)
    today = datetime.today()
    delta = today - c_ti
    body = {}
    if delta.days >= 1:
        download_file()
        try:
            body |= generate_plot_data('./app/job-app-tmp.xlsx')
            os.remove('./app/job-app.xlsx')
            os.rename('./app/job-app-tmp.xlsx', './app/job-app.xlsx')
            print("New file successfully downloaded.")
        except Exception as error:
            print(error)
            body |= generate_plot_data('./app/job-app.xlsx')
    else:
        print("Regenerating data")
        body |= generate_plot_data('./app/job-app.xlsx')
    return body