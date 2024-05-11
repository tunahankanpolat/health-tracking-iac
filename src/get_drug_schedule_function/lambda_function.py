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
        print("drug_schedule", drug_schedule)
        return {
            'statusCode': 200,
            'body': drug_schedule
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
