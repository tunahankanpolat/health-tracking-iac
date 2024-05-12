import json
import boto3

def lambda_handler(event, context):
    body = json.loads(event['body'])
    mac_address = body.get('mac_address')
    user_id = body.get('user_id')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('drug_box')
    try:
        if mac_address:
            response = table.get_item(
                Key={
                    'mac_address': mac_address
                }
            )
            drug_schedule = response['Item']['drug_schedule']
            formatted_schedule = format_schedule(drug_schedule)
            print("formatted_schedule", formatted_schedule)
            return {
                'statusCode': 200,
                'body': json.dumps(formatted_schedule, separators=(',', ':'))  # Boşluk olmadan JSON dönmek için
            }
        elif user_id:
            drug_schedule = get_drug_schedule_from_dynamodb(user_id)
            print("formatted_schedule", drug_schedule)
            return {
                'statusCode': 200,
                'body': json.dumps(drug_schedule, separators=(',', ':'))  # Boşluk olmadan JSON dönmek için
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('Mac address or user ID is required')
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def get_drug_schedule_from_dynamodb(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('drog_box')    
    response = table.query(
        IndexName='user_id_index',
        KeyConditionExpression='user_id = :id',
        ExpressionAttributeValues={
            ':id': int(user_id)
        }
    )
    items = response['Items']['drug_schedule']
    return items
    

def format_schedule(drug_schedule):
    result = {}
    for id, meds in drug_schedule.items():
        times_list = []
        for med in meds:
            for key, value in med.items():
                times_list.extend(value)
        result[id] = times_list
    return result
