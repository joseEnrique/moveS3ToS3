import boto3
from boto3 import s3
from sqlalchemy import func

from db import Images


class DtoS3:
    @staticmethod
    def get_s3_resource():
        return boto3.resource('s3', endpoint_url='http://localhost:8080')

    @staticmethod
    def transfer_s3_to_s3(s3session, old_key, new_key, new_bucket_name="new", bucket_to_copy="legacy") -> bool:
        try:
            copy_source = {
                'Bucket': bucket_to_copy,
                'Key': old_key
            }
            s3session.meta.client.copy(copy_source, new_bucket_name, new_key)
            return True
        except Exception as e:
            print (e,old_key)
            return False


class DtoMaria:
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
