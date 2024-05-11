import json
import boto3

def lambda_handler(event, context):
    body = json.loads(event['body'])
    mac_address = body.get('mac_address')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('drug_box')
    try:
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
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def format_schedule(drug_schedule):
    result = {}
    for id, meds in drug_schedule.items():
        times_list = []
        for med in meds:
            for key, value in med.items():
                times_list.extend(value)
        result[id] = times_list
    return result
