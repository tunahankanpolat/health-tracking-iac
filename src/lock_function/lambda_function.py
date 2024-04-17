import json
import boto3

def lambda_handler(event, context):
    # Gelen request'ten mac_address değerini alın
    print(event)
    body = json.loads(event['body'])
    mac_address = body.get('mac_address')
    print("mac_address", mac_address)
    # DynamoDB client'ını oluşturun
    dynamodb = boto3.resource('dynamodb')
    
    # Tabloyu seçin
    table = dynamodb.Table('rfid_tag')
    
    try:
        # Mac adresine göre veriyi alın
        response = table.get_item(
            Key={
                'mac_address': mac_address
            }
        )
        print("response", response)
        # İlgili RFID tag değerini alın
        rfid_tag = response['Item']['rfid_tag']
        
        # RFID tag değerini return edin
        return {
            'statusCode': 200,
            'body': rfid_tag
        }
    
    except Exception as e:
        # Hata durumunda uygun bir hata mesajı döndürün
        return {
            'statusCode': 500,
            'body': str(e)
        }
