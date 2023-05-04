import logging
import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup


import settings


def get_transform_data():
    logging.info('tennet_balance_delta API: Started checking xml data.')
    # get current date
    today = dt.date.today().strftime('%Y-%m-%d')
    # create the API URL with the current date
    api_url = settings.URL.format(today)
    # send a request to the API
    response = requests.get(api_url)
    logging.info('tennet_balance_delta API: Finished checking data from API endpoint')
    logging.info('tennet_balance_delta: Started transforming data.')
    xml_data = response.text
    soup = BeautifulSoup(xml_data, "lxml-xml")

    data = []
    for record in soup.find_all("Record"):
        row = {}
        for field in record.find_all():
            row[field.name] = field.text
        data.append(row)

    df = pd.DataFrame(data)
    datetime_col = pd.to_datetime(df.DATE.astype(str) + ' ' + df.TIME.astype(str)).dt.tz_localize(settings.CET_TIMEZONE
                                                                                            ).dt.tz_convert('UTC').dt.strftime('%Y-%m-%d %H:%M:%S')
    df.insert(1, 'datetime', datetime_col)
    transformed_df = pd.melt(df, id_vars='datetime',
                             value_vars=settings.CATEGORY_LIST, var_name='category', value_name='value')
    transformed_df.fillna(np.NaN, inplace=True)
    transformed_df['processed_time'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    logging.info('tennet_balance_delta: Finished transforming data.')

    return transformed_df
