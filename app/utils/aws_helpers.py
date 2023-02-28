import boto3
from datetime import datetime

class DynamoDb():

    def __init__(self,table_name:str, key_condition_expression:dict[str, str],expression_attribute_values:str):
        self.dynamo_client = boto3.client('dynamodb')
        self.table_name = table_name
        self.key_condition_expression = key_condition_expression
        self.expression_attribute_values = expression_attribute_values

    def get(self):
        response = self.dynamo_client.query(
            TableName=self.table_name,
            KeyConditionExpression=self.key_condition_expression,
            ExpressionAttributeValues=self.expression_attribute_values
        )

    def put(self, items:dict):
        with self.dynamo_client.batch_writer(TableName=self.table_name) as batch:
            # iterate over the list of items and add them to the batch writer
            for item in items:
                batch.put_item(Item=item)

class S3():

    def __init__(self, bucket_name:str, key:str, data:bytes|None=None):
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name
        self.key = key
        self.data = data

    def get(self) -> dict:
        return self.s3_client.get_object(Bucket=self.bucket_name, Key=self.key)['Body'].read()

    def put(self) -> None:
        self.s3_client.put_object(Bucket=self.bucket_name, Key=self.key, Body=self.data)

class sqs_que():

    def __init__(self, que_arn:str):
        self.que_arn = que_arn
        self.sqs_client = boto3.client('sqs')

    def send_to_que(self, error_message, key):
        response = self.sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=(
            {'date':datetime.now(),
             'error_message':error_message,
             'key':key
            }
            )
        )
