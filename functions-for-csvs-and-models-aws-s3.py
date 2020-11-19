import pandas as pd
import pickle
import boto3
import joblib
from io import StringIO, BytesIO


client = boto3.client('s3',
                      aws_access_key_id = '*******************'
                      aws_secret_access_key = '**************************')
bucket_name = '***********' # name of the main folder (bucket) in S3


def upload_csv_to_s3(folder_path, filename, dataframe, upload_index):
    # upload_index should be True if the index should be saved or False if it shouldn't
    object_key = folder_path + filename
    csv_buffer = StringIO()
    dataframe.to_csv(csv_buffer, index = upload_index)
    client.put_object(Bucket = bucket_name, Key = object_key, Body = csv_buffer.getvalue())
    
def load_csv_from_s3(folder_path, filename, upload_index):
    # upload_index should be equal to the number of the column to use as the index column, or False if there is no index column
    object_key = folder_path + filename
    csv_obj = client.get_object(Bucket = bucket_name, Key = object_key)
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string), index_col = upload_index)
    return df

def upload_model_to_s3(folder_path, filename, model):
    object_key = folder_path + filename
    fo = BytesIO(pickle.dumps(model)) # adjust if you will not be using pickle to save your model
    client.upload_fileobj(fo, Bucket = bucket_name, Key = object_key)
    
def load_model_from_s3(folder_path, filename):
    object_key = folder_path + filename
    with BytesIO() as data:
        client.download_fileobj(bucket_name, object_key, data)
        data.seek(0)
        model = joblib.load(data) # adjust if you did not use pickle to save your model
    return model