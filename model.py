import logging
from datetime import datetime, timedelta
from enecodhutils.pipeline import dh_kafka
from apscheduler.schedulers.blocking import BlockingScheduler
from enecodhutils.database.dh_mssql import SQLClient

import helpers
import settings

logging.basicConfig(format='%(asctime)s %(levelname)-4s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
mssql_client = SQLClient(settings.SQL_HOST, settings.SQL_USERNAME, settings.SQL_PASSWORD, settings.SQL_DATABASE,
                         settings.SQL_DRIVER, settings.DATA_SOURCE)


def run():
    """
    Main function which calls all other sub functions
    :return: None
    """
    try:
        logging.info('tennet_balance_delta: Start Process.')
        df = helpers.get_transform_data()

        # Produce data to kafka
        if len(df) > 0:
            dh_kafka.produce_msg_to_kafka(settings.BOOTSTRAP_SERVER, settings.KAFKA_TOPIC,
                                          df.to_json(orient='records'))
            mssql_client.update_processed_time(1, 0, processed_time=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                                               file_date=datetime.utcnow().date())

        logging.info('tennet_balance_delta: Process Finished')

    except:
        err_count = mssql_client.get_err_count()
        mssql_client.update_processed_time(0, err_count + 1)
        logging.error('tennet_balance_delta: Caught with processing error', exc_info=True)


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(run, 'cron', minute='*/5', max_instances=1,
                      coalesce=False, misfire_grace_time=90)
    scheduler.start()
