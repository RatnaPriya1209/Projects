from pymongo import MongoClient
from datetime import datetime

def convert_forecast_for_mongo(forecast_list):
    return [
        {
            'ds': item['ds'].to_pydatetime() if hasattr(item['ds'], "to_pydatetime") else item['ds'],
            'yhat': float(item['yhat']),
            'yhat_lower': float(item['yhat_lower']),
            'yhat_upper': float(item['yhat_upper'])
        }
        for item in forecast_list
    ]

def save_forecast_to_mongo(forecast_data, store_id, dept_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['forecast_db']
    collection = db['sales_forecasts']

    document = {
        'store_id': int(store_id),
        'dept_id': int(dept_id),
        'forecast': convert_forecast_for_mongo(forecast_data),
        'timestamp': datetime.now()
    }

    collection.insert_one(document)
