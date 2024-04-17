import json
import boto3
import os
import requests
import datetime
import uuid

def get_fit_api_all_data(access_token):
    url = f'https://www.googleapis.com/fitness/v1/users/me/dataSources'
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    data_stream_id = f'derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm'
    current_time = int(datetime.datetime.now().timestamp()) * 1000000000
    dataset_id = f'0-{current_time}'
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
    

def get_access_and_refresh_tokens(client_id, client_secret, redirect_uri, code, state, code_verifier, platform):
    token_url = 'https://oauth2.googleapis.com/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    body = {
        'code': code,
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
        'code_verifier': code_verifier,
        'state': state
    }
    
    if platform == 'web':
        body['client_secret'] = client_secret

    response = requests.post(token_url, headers=headers, data=body)
    tokens = response.json()
    access_token = tokens.get('access_token')
    refresh_token = tokens.get('refresh_token')
    return access_token, refresh_token

def put_item_to_user_table(user_id, client_id, refresh_token, platform):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user')
    
    table.put_item(
        Item={
            'user_id': int(user_id),
            'refresh_token': refresh_token,
            'client_id': client_id,
            'platform': platform
        }
    )
    return

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


def get_user_health_data_from_dynamodb(user_id, start_time=None, end_time=None):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_health_data')
    
    if start_time and end_time:
        response = table.query(
            IndexName='user_id_timestamp_index',  # Updated index name
            KeyConditionExpression='user_id = :id AND time_stamp BETWEEN :start_time AND :end_time',
            ExpressionAttributeValues={
                ':id': int(user_id),
                ':start_time': int(start_time),
                ':end_time': int(end_time)
            }
        )
    else:
        response = table.query(
            IndexName='user_id_timestamp_index',  # Updated index name
            KeyConditionExpression='user_id = :id',
            ExpressionAttributeValues={
                ':id': int(user_id)
            }
        )
    
    items = response['Items']
    return items

      

def lambda_handler(event, context):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    client_secret = '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'
    print('Event: ', event)
    
    body = json.loads(event['body'])
    print('Body: ', body)
    code = body['code']
    user_id = body['id']
    state = body['state']
    code_verifier = body['codeVerifier']
    client_id = body['clientId']
    redirect_uri = body['redirectUri']
    platform = body['platform']
    
    health_data = get_user_health_data_from_dynamodb(user_id)
    print('Health Data: ', health_data)
    
    if health_data:
        return {
            'statusCode': 200,
            'body': json.dumps('User data already exists')
        }
        
    access_token, refresh_token = get_access_and_refresh_tokens(
        client_id, client_secret, redirect_uri, code, state, code_verifier, platform)
    put_item_to_user_table(user_id, client_id, refresh_token, platform)
    data = get_fit_api_all_data(access_token)
    print('Data: ', data)
    put_item_to_health_data_table(user_id, data)
    print(f'Access token: {access_token}')
    print(f'Refresh token: {refresh_token}')

    return {
        'statusCode': 200,
        'body': json.dumps('Access and refresh tokens retrieved successfully')
    }