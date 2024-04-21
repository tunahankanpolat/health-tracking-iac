import json
import boto3
import datetime
from decimal import Decimal

def get_user_health_data_from_dynamodb(user_id, start_time=0, end_time=int(datetime.datetime.now().timestamp())):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_health_data')    
    response = table.query(
        IndexName='user_id_timestamp_index',
        KeyConditionExpression='user_id = :id AND time_stamp BETWEEN :start_time AND :end_time',
        ExpressionAttributeValues={
            ':id': int(user_id),
            ':start_time': int(start_time),
            ':end_time': int(end_time)
        }
    )
    items = response['Items']
    return items
    
def convert_heart_rate_from_decimal_to_int(obj):
    if isinstance(obj, list):
        return [convert_heart_rate_from_decimal_to_int(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_heart_rate_from_decimal_to_int(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return int(obj)  # or str(obj)
    else:
        return obj
        
def lambda_handler(event, context):
    body = json.loads(event['body'])
    print('Body: ', body)
    user_id = body.get('user_id')
    start_time = body.get('start_date')
    end_time = body.get('end_date')
    
    if not start_time:
        start_time = 0
    if not end_time:
        end_time = int(datetime.datetime.now().timestamp())*1000
        
    health_data = []
    if not user_id:
        return {
            'statusCode': 400,
            'body': json.dumps('User ID is required')
        }
    
    if start_time and end_time:
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        start_time = int(start_time.timestamp()) * 1000
        end_time = int(end_time.timestamp()) * 1000
        
    print("start_time: ",start_time)
    print("end_time: ", end_time)
    health_data = get_user_health_data_from_dynamodb(user_id, start_time, end_time)
    health_data = convert_heart_rate_from_decimal_to_int(health_data)
    print('Health Data: ', health_data)

    
    return {
        'statusCode': 200,
        'body': json.dumps(health_data)
    }