from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os
from Google.google import download_file


def generate_plot_data(file_name: str) -> dict:

    frame = pd.read_excel(file_name)
    frame['Sent Date'] = pd.to_datetime(frame['Sent Date'], format='%d-%m-%Y')
    frame['Rejection Date'] = frame['Sent Date'] + frame['Time past [day]'].apply(timedelta)

    app_frame = frame.sort_values(by='Sent Date')

    app_frame['Sent Date'] = pd.to_datetime(app_frame['Sent Date']) - pd.to_timedelta(7, unit='d')
    app_frame['Quantity'] = 1
    app_frame = app_frame.groupby(pd.Grouper(key='Sent Date', freq='W-MON'))['Quantity'].sum()
    app_x = [datetime.strftime(x,"%d-%m-%Y") for x in app_frame.index]
    app_y = [val.item() for val in list(np.cumsum(app_frame.values))]

    rej_frame = frame[frame['Resolution'] == 'Rejected']
    rej_frame = rej_frame.sort_values(by='Rejection Date')
    rej_frame['Rejection Date'] = pd.to_datetime(rej_frame['Rejection Date']) - pd.to_timedelta(7, unit='d')
    rej_frame['Quantity'] = 1
    rej_frame = rej_frame.groupby(pd.Grouper(key='Rejection Date', origin=app_frame.index[0], freq='W-MON'))['Quantity'].sum()
    len_diff = len(app_x) - len(rej_frame.index)
    rej_x = app_x[:len_diff] + [datetime.strftime(x,"%d-%m-%Y") for x in rej_frame.index]
    rej_y = [0 for _ in range(len_diff)] + [val.item() for val in list(np.cumsum(rej_frame.values))]

    if len(app_x) > 20:
        app_x = app_x[-20:]
        app_y = app_y[-20:]
    
    if len(rej_x) > 20:
        rej_x = rej_x[-20:]
        rej_y = rej_y[-20:]

    ns = os.path.getctime('./app/job-app.xlsx')
    c_ti = datetime.fromtimestamp(ns)

    return {'applications': {'x_axis' : app_x, 'y_axis': app_y}, 'rejections': {'x_axis' : rej_x, 'y_axis': rej_y}, 'last_updated': str(c_ti)}

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