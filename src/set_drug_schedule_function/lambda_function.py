import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
      body = json.loads(event['body'])
      user_id = body.get('user_id')
      drug_schedule = body.get('drug_schedule')
      print("user_id: ", user_id)
      print("drug_schedule: ", drug_schedule)
      dynamodb = boto3.resource('dynamodb')
      table = dynamodb.Table('drug_box')
      try:
            if not user_id:
                  return {
                        'statusCode': 400,
                        'body': json.dumps('User ID is required')
                  }
            if not drug_schedule:
                  return {
                        'statusCode': 400,
                        'body': json.dumps('Drug Schedule is required')
                  }
            set_drug_schedule(user_id, drug_schedule, dynamodb, table)
      except Exception as e:
            print("e: ", e)
            return {
                  'statusCode': 500,
                  'body': str(e)
            }

def set_drug_schedule(user_id, drug_schedule, dynamodb, table):
      try:
            drug_box = get_drug_box_from_dynamodb(user_id, dynamodb, table)
            if not drug_box:
                  return {
                  'statusCode': 404,
                  'body': json.dumps('User ID not found')
                  }
            print("drug_box: ", drug_box)
            print("mac_address: ", drug_box['mac_address'])
            response = table.update_item(
                  Key={'mac_address': drug_box['mac_address']},
                  UpdateExpression='SET drug_schedule = :new_schedule',
                  ExpressionAttributeValues={':new_schedule': drug_schedule},
                  ReturnValues='UPDATED_NEW'
            )
            print("response: ", response)
            # Check if the update was successful
            if response.get('Attributes'):
                  return {
                  'statusCode': 200,
                  'body': json.dumps('Drug schedule updated successfully')
                  }
            else:
                  return {
                  'statusCode': 404,
                  'body': json.dumps('User ID not found')
                  }
      except Exception as e:
            print("e: ", e)
            return {
                  'statusCode': 500,
                  'body': str(e)
            }
    
    
def get_drug_box_from_dynamodb(user_id, dynamodb=None, table=None):
    response = table.query(
        IndexName='user_id_index',
        KeyConditionExpression='user_id = :id',
        ExpressionAttributeValues={
            ':id': int(user_id),
        }
    )
    print("response['Items']", response['Items'])
    return response['Items'][0]
    
    
def format_schedule(drug_schedule):
    result = {}
    for id, meds in drug_schedule.items():
        times_list = []
        for med in meds:
            for key, value in med.items():
                times_list.extend(value)
        result[id] = times_list
    return result
