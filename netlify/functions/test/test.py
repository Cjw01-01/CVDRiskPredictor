def lambda_handler(event, context):
    """Simple test function to verify Netlify Functions are working"""
    return {
        "statusCode": 200,
        "body": '{"status": "test function works"}',
        "headers": {
            "Content-Type": "application/json"
        }
    }

