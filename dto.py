from boto3 import s3
from sqlalchemy import func

from db import Pictures


class DtoS3:
    @staticmethod
    def transfer(s3session,key):
        new_bucket_name = "new"
        bucket_to_copy = "legacy"

        copy_source = {
            'Bucket': bucket_to_copy,
            'Key': key
        }
        s3session.meta.client.copy(copy_source, new_bucket_name, key)


class DtoMaria:
    @staticmethod
    def get_not_processed_key(session) -> Pictures:
        while session.query(Pictures).filter(Pictures.new_route is None).count() > 0:
            ran_object = session.query(Pictures).filter(Pictures.new_route is None).order_by(func.rand()).first()
            yield ran_object

    @staticmethod
    def update_element(session, pic):
        try:
            pic.new_route = 'updated'
            session.add(pic)
            session.commit()
        except:
            session.rollback()

