import json
import os
import boto3
import datetime

def get_user_health_data_from_dynamodb(user_id, start_time="0", end_time=str(datetime.datetime.now().timestamp() * 1000000000)):
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
      print('Event: ', event)
      user_id = event['user_id']
      start_date = event['start_time']
      end_date = event['end_time']
      health_data = []
      if start_date and end_date:
            start_time = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
            end_time = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
            start_time = int(start_time.timestamp()) * 1000000000
            end_time = int(end_time.timestamp()) * 1000000000
            health_data = get_user_health_data_from_dynamodb(user_id)
            print('Health Data: ', health_data)
            health_data = [item for item in health_data if start_time <= item['health_data']['heart_rate']['timestamp'] <= end_time]
            print('Filtered Health Data: ', health_data)
            
      return {
            'statusCode': 200,
            'body': json.dumps(health_data)
      }