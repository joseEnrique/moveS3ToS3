import boto3

s3 = boto3.resource('s3', endpoint_url='http://localhost:8080',)

new_bucket_name = "new"
bucket_to_copy = "legacy"

copy_source = {
    'Bucket': 'legacy',
    'Key': '1'
 }
s3.meta.client.copy(copy_source, new_bucket_name, '1')

def get_matching_s3_keys(bucket, prefix='', suffix=''):
    """
    Generate the keys in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """

    session = boto3.session.Session()

    s3 = session.client(
        service_name='s3',
        endpoint_url='http://localhost:8080',

    )

    kwargs = {'Bucket': bucket}

    # If the prefix is a single string (not a tuple of strings), we can
    # do the filtering directly in the S3 API.
    if isinstance(prefix, str):
        kwargs['Prefix'] = prefix

    while True:

        # The S3 API response is a large blob of metadata.
        # 'Contents' contains information about the listed objects.
        resp = s3.list_objects_v2(**kwargs)
        for obj in resp['Contents']:
            key = obj['Key']
            if key.startswith(prefix) and key.endswith(suffix):
                yield key

        # The S3 API is paginated, returning up to 1000 keys at a time.
        # Pass the continuation token into the next response, until we
        # reach the final page (when this field is missing).
        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break


for key in get_matching_s3_keys(bucket='legacy'):
    print(key)