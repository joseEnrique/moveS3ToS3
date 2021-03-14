import boto3
import multiprocessing as mp
import os

s3 = boto3.resource('s3', endpoint_url='http://localhost:8080',)
bucket = s3.Bucket('legacy')



def s3_download(object_key_file):
    print ("ntra")
    bucket.download_file(object_key_file[0], object_key_file[1])
    print('downloaded file with object name... {}'.format(object_key_file[0]))
    print('downloaded file with file name... {}'.format(object_key_file[1]))


def parallel_s3_download():
    object_key_file = []
    for s3_object in bucket.objects.all():
        # Need to split s3_object.key into path and file name, else it will give error file not found.
        path, filename = os.path.split(s3_object.key)
        print(path,filename)
        object_key_file.append((s3_object.key, filename))
    object_key_file.pop(0)
    pool = mp.Pool(min(mp.cpu_count(), len(object_key_file)))  # number of workers
    pool.map(s3_download, object_key_file, chunksize=1)
    pool.close()


if __name__ == "__main__":
    parallel_s3_download()
    print('downloading zip file')
