import boto3
from boto3 import s3
from sqlalchemy import func

from db import Pictures


class DtoS3:
    @staticmethod
    def get_s3_resource():
        return boto3.resource('s3', endpoint_url='http://localhost:8080')

    @staticmethod
    def transfer_s3_to_s3(s3session, old_key, new_key, new_bucket_name="new", bucket_to_copy="legacy"):
        try:
            copy_source = {
                'Bucket': bucket_to_copy,
                'Key': old_key
            }
            s3session.meta.client.copy(copy_source, new_bucket_name, new_key)
            return True
        except Exception as e:
            return False


class DtoMaria:
    @staticmethod
    def get_not_processed_key(session) -> Pictures:
        while session.query(Pictures).filter(Pictures.new_route == None).count() > 0:
            for i in session.query(Pictures).filter(Pictures.new_route == None).order_by(func.rand()).limit(5).all():
                # ran_object = session.query(Pictures).filter(Pictures.new_route is None).order_by(func.rand()).first()
                yield i

    @staticmethod
    def update_element(session, pic):
        try:
            pic.new_route = 'updated'
            session.add(pic)
            session.commit()
        except:
            session.rollback()
