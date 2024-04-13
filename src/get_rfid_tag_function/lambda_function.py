import json
import boto3

def lambda_handler(event, context):
    body = json.loads(event['body'])
    mac_address = body.get('mac_address')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('rfid_tag')
    try:
        response = table.get_item(
            Key={
                'mac_address': mac_address
            }
        )
        rfid_tag = response['Item']['rfid_tag']
        return {
            'statusCode': 200,
            'body': rfid_tag
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
