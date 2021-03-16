import multiprocessing

import boto3, logging

from config import OLD_BUCKET, OLD_PREFIX
from db import Images, generate_metadata, generate_session
from utils import S3Utils


def load_data(session, s3, name):
    object = s3.Object(OLD_BUCKET, f'{OLD_PREFIX}/{name}.png')
    object.put(Body=f'body of {name}')
    try:
        new_rec = Images(name=f'{name}.png', old_key=f'{OLD_PREFIX}/{name}.png')
        session.add(new_rec)
        session.commit()
    except Exception as e:
        logging.error(e)
        session.rollback()

def mp_worker(start, size):
    session = generate_session()
    s3 = S3Utils.get_s3_resource()
    for i in range(start, (start + size) + 1):
        load_data(session, s3, i)

def mp_load(n_cores = 4,load_size = 10000 ):
    batch_size = round(load_size / n_cores + 0.5)
    batches = range(0, n_cores * batch_size, batch_size)
    processes = [multiprocessing.Process(target=mp_worker, args=(rang, batch_size)) for rang in batches]

    for process in processes:
        process.start()

    for process in processes:
        process.join()


if __name__ == '__main__':
    mp_load()
