import json
import os
import requests
import boto3
import datetime
import uuid

def get_fit_api_data(access_token, timedelta_hours=24):
    url = f'https://www.googleapis.com/fitness/v1/users/me/dataSources'
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    current_time = datetime.datetime.now()
    timedelta_ago = current_time - datetime.timedelta(hours=timedelta_hours)
    
    start_time = int(timedelta_ago.timestamp()) * 1000000000
    end_time = int(current_time.timestamp()) * 1000000000
    
    data_stream_id = f'derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm'
    dataset_id = f'{start_time}-{end_time}'
    dataset_url = f'{url}/{data_stream_id}/datasets/{dataset_id}'
    response = requests.get(dataset_url, headers=headers)
    data = response.json()
    data = convert_heart_rate_data_format(data)
    return data

def convert_heart_rate_data_format(data):
    heart_rate_data = data['point']
    heart_rate_list = []
    for heart_rate in heart_rate_data:
        heart_rate_list.append({'timestamp': heart_rate['startTimeNanos'], 'heart_rate': heart_rate['value'][0]['fpVal']})
    return heart_rate_list

def get_access_token_using_refresh_token(client_id, client_secret, refresh_token, platform):
    token_url = 'https://oauth2.googleapis.com/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    body = {
        'client_id': client_id,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    
    if platform == 'web':
        body['client_secret'] = client_secret
        
    response = requests.post(token_url, headers=headers, data=body)
    tokens = response.json()
    access_token = tokens.get('access_token')
    
    return access_token

def get_all_users_from_user_table():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user')
    response = table.scan()
    items = response['Items']
    return items


def put_item_to_health_data_table(user_id, data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_health_data')
    
    with table.batch_writer() as batch:
        for item in data:
            timestamp = int(item['timestamp'])  # Convert timestamp to number
            del item['timestamp']
            entry_id = str(uuid.uuid4()) 
            batch.put_item(
                Item={
                    'entry_id': entry_id,
                    'user_id': int(user_id),
                    'time_stamp': timestamp,
                    'health_data': item
                }
            )
    return

def lambda_handler(event, context):
      os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
      os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
      client_secret = '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'
      print('Event: ', event)
      
      users = get_all_users_from_user_table()
      print('Users: ', users)
      
      for user in users:
            user_id = user['user_id']
            client_id = user['client_id']
            refresh_token = user['refresh_token']
            platform = user['platform']
            
            access_token = get_access_token_using_refresh_token(client_id, client_secret, refresh_token, platform)
            data = get_fit_api_data(access_token, 24)
            print('Data: ', data)
            put_item_to_health_data_table(user_id, data)
      return {
            'statusCode': 200,
            'body': 'Access tokens have been successfully updated'
      }