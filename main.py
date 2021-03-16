import logging

import requests

from config import NEW_BUCKET, OLD_BUCKET, NEW_PREFIX, OLD_PREFIX, LOAD_FILES, URL_ENDPOINT
from db import generate_session, generate_metadata
from load_files import load_data
from utils import MariaUtils, S3Utils

if __name__ == '__main__':
    generate_metadata()
    session = generate_session()
    s3 = S3Utils.get_s3_resource()

    if LOAD_FILES in ['true', 'True', 'yes']:
        requests.put(f'{URL_ENDPOINT}/{OLD_BUCKET}')
        requests.put(f'{URL_ENDPOINT}/{NEW_BUCKET}')

        for name_i in range(10000):
            load_data(session, s3, name_i)
        logging.info("Loaded !")

    for object_not_migrated in MariaUtils.get_not_processed_key(session):
        new_key = f'{NEW_PREFIX}/{object_not_migrated.name}'
        old_key = f'{OLD_PREFIX}/{object_not_migrated.name}'
        transferred = S3Utils.transfer_s3_to_s3(s3, old_key, new_key, NEW_BUCKET, OLD_BUCKET)
        if transferred:
            MariaUtils.update_element(session, object_not_migrated, new_key)
            logging.info("Processed", object_not_migrated.old_key)
        logging.info("Done !")
