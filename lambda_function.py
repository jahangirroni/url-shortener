import json
import hashlib
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('urls')

def lambda_handler(event, context):
    # Get the original URL from the request
    body = json.loads(event['body'])
    original_url = body.get('url')
    
    if not original_url:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'url parameter is required'})
        }
    
    # Create a short code (first 6 characters of MD5 hash)
    short_code = hashlib.md5(original_url.encode()).hexdigest()[:6]
    
    # Store in DynamoDB
    table.put_item(Item={
        'code': short_code,
        'url': original_url
    })
    
    # Return the short URL
    return {
        'statusCode': 200,
        'body': json.dumps({
            'short_url': f'https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/{short_code}'
        })
    }
