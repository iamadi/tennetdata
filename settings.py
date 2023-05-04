import os
from pytz import timezone
from datetime import datetime, timedelta

# Curve metadata
CET_TIMEZONE = timezone('Europe/Amsterdam')
DMY = "%d-%m-%Y"

# Base URLs
URL = "http://www.tennet.org/english/operational_management/export_data.aspx?exporttype=balancedeltaIGCC&format=xml&datefrom={0}&dateto={0}&submit=1"

#Other components
CATEGORY_LIST = ['IGCCCONTRIBUTION_UP','IGCCCONTRIBUTION_DOWN','UPWARD_DISPATCH','DOWNWARD_DISPATCH','RESERVE_UPWARD_DISPATCH','RESERVE_DOWNWARD_DISPATCH',
 'EMERGENCY_POWER','MID_PRICE','MIN_PRICE','MAX_PRICE']

# Kafka Bootstrap server settings
BOOTSTRAP_SERVER = os.environ['KAFKAHOST']
KAFKA_TOPIC = os.environ['TOPIC']

# Credentials that can be used for local testing:-
SQL_DRIVER = os.environ['SQL_DRIVER']
SQL_HOST = os.environ['SQL_HOST']
SQL_USERNAME = os.environ['SQL_USERNAME']
SQL_PASSWORD = os.environ['SQL_PASSWORD']
SQL_DATABASE = os.environ['SQL_DATABASE']
SOURCE_DATABASE = 'learn_hub_prod'
DATA_SOURCE = 'tennet_balance_delta_aditya'
