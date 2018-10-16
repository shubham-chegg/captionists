from google.cloud import storage

BUCKET_NAME = "jhandei_audio"


def upload(source_file_name, destination_blob_name=None, bucket_name = BUCKET_NAME):
    """Uploads a file to the bucket."""
    if not destination_blob_name:
        destination_blob_name = source_file_name

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

    return "gs://{}/{}".format(bucket_name, destination_blob_name)