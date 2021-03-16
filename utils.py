import logging

import boto3
from sqlalchemy import func

from config import OLD_BUCKET, NEW_BUCKET, URL_ENDPOINT, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from db import Images


class S3Utils:
    @staticmethod
    def get_s3_resource():
        #Here we could **kwargs
        return boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY, endpoint_url=URL_ENDPOINT)

    @staticmethod
    def transfer_s3_to_s3(s3session, old_key, new_key, new_bucket_name=NEW_BUCKET, bucket_to_copy=OLD_BUCKET):
        try:
            copy_source = {
                'Bucket': bucket_to_copy,
                'Key': old_key
            }
            s3session.meta.client.copy(copy_source, new_bucket_name, new_key)
            return True
        except Exception as e:
            logging.error(e)
            return False


class MariaUtils:
    @staticmethod
    def get_not_processed_key(session, limit=5):
        while session.query(Images).filter(Images.new_key == None).count() > 0:
            for i in session.query(Images).filter(Images.new_key == None).order_by(func.rand()).limit(limit).all():
                yield i

    @staticmethod
    def update_element(session, pic, new_key):
        try:
            pic.new_key = new_key
            session.add(pic)
            session.commit()
        except:
            session.rollback()
