from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
import requests
import pandas as pd
from sqlalchemy import create_engine
import redis

# Setting up Redis and SQL Alchemy engine
redis_client = redis.Redis(host='localhost', port=6379, db=0)  # Corrected port for Redis
engine = create_engine('postgresql://postgres:2001@localhost/postgres')
# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=YOUR_API_KEY'
# response = requests.get(url)
# data = response.json()
# time_series_data = data['Time Series (5min)']
#
#     # Convert to DataFrame
# df = pd.DataFrame.from_dict(time_series_data, orient='index')
# df.index = pd.to_datetime(df.index)
# df.columns = ['open', 'high', 'low', 'close', 'volume']
# df = df.astype({
#         'open': 'float',
#         'high': 'float',
#         'low': 'float',
#         'close': 'float',
#         'volume': 'int'
#     })
#
#     # Add metadata
# meta_data = data['Meta Data']
# df['information'] = meta_data.get('1. Information', '')
# df['symbol'] = meta_data.get('2. Symbol', '')
# df['last_refreshed'] = datetime.strptime(meta_data.get('3. Last Refreshed', ''), '%Y-%m-%d %H:%M:%S')
# df['interval'] = meta_data.get('4. Interval', '')
# df['output_size'] = meta_data.get('5. Output Size', '')
# df['time_zone'] = meta_data.get('6. Time Zone', '')
#
#     # Save to PostgreSQL
# df.to_sql('stock_data', con=engine, if_exists='replace', index=False)
# print(df.columns)
#     # Optionally save latest data to Redis for quick access
# redis_client.set('latest_stock_data', df.head(1).to_json())
def fetch_and_update():
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=YOUR_API_KEY'
    response = requests.get(url)
    data = response.json()
    time_series_data = data['Time Series (5min)']

    # Convert to DataFrame
    df = pd.DataFrame.from_dict(time_series_data, orient='index')
    df.index = pd.to_datetime(df.index)
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    df = df.astype({
        'open': 'float',
        'high': 'float',
        'low': 'float',
        'close': 'float',
        'volume': 'int'
    })

    # Add metadata
    meta_data = data['Meta Data']
    df['information'] = meta_data.get('1. Information', '')
    df['symbol'] = meta_data.get('2. Symbol', '')
    df['last_refreshed'] = datetime.strptime(meta_data.get('3. Last Refreshed', ''), '%Y-%m-%d %H:%M:%S')
    df['interval'] = meta_data.get('4. Interval', '')
    df['output_size'] = meta_data.get('5. Output Size', '')
    df['time_zone'] = meta_data.get('6. Time Zone', '')

    # Save to PostgreSQL
    df.to_sql('stock_data', con=engine, if_exists='replace', index=False)
    print(df.columns)
    # Optionally save latest data to Redis for quick access
    redis_client.set('latest_stock_data', df.head(1).to_json())

# Schedule the function to run every 5 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_update, 'interval', minutes=5)
scheduler.start()

# To keep the script running
try:
    import time
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
