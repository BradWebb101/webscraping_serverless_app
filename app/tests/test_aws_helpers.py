import boto3
from datetime import datetime
from unittest.mock import Mock, patch
import pytest
from utils.aws_helpers import DynamoDb, S3, sqs_que


@pytest.fixture
def dynamodb():
    table_name = 'test-table'
    key_condition_expression = {'id': '1'}
    expression_attribute_values = {'#n': 'John'}
    return DynamoDb(table_name, key_condition_expression, expression_attribute_values)

@patch('boto3.client')
def test_get(mock_client, dynamodb):
    mock_client.return_value.query.return_value = {'Items': [{'id': {'N': '1'}, 'name': {'S': 'John'}}]}
    dynamodb.get()
    mock_client.return_value.query.assert_called_once_with(
        TableName='test-table',
        KeyConditionExpression={'id': '1'},
        ExpressionAttributeValues={'#n': 'John'}
    )

@patch('boto3.client')
def test_put(mock_client, dynamodb):
    mock_batch_writer = Mock()
    mock_client.return_value.batch_writer.return_value = mock_batch_writer
    items = [{'id': '1', 'name': 'John'}, {'id': '2', 'name': 'Jane'}]
    dynamodb.put(items)
    mock_batch_writer.put_item.assert_called_once_with(Item={'id': '1', 'name': 'John'})
    mock_batch_writer.put_item.assert_called_with(Item={'id': '2', 'name': 'Jane'})

@pytest.fixture
def s3():
    bucket_name = 'test-bucket'
    key = 'test-key'
    data = b'Hello, world!'
    return S3(bucket_name, key, data)

@patch('boto3.client')
def test_get_object(mock_client, s3):
    mock_client.return_value.get_object.return_value = {'Body': Mock(read=Mock(return_value=b'Hello, world!'))}
    assert s3.get() == b'Hello, world!'
    mock_client.return_value.get_object.assert_called_once_with(Bucket='test-bucket', Key='test-key')

@patch('boto3.client')
def test_put_object(mock_client, s3):
    s3.put()
    mock_client.return_value.put_object.assert_called_once_with(Bucket='test-bucket', Key='test-key', Body=b'Hello, world!')

@pytest.fixture
def sqs():
    que_url = 'test-que-url'
    return sqs_que(que_url)

@patch('boto3.client')
def test_send_message(mock_client, sqs):
    error_message = 'test-error-message'
    key = 'test-key'
    sqs.send_to_que(error_message, key)
    mock_client.return_value.send_message.assert_called_once_with(
        QueueUrl='test-que-url',
        MessageBody={
            'date': mock.ANY,
            'error_message': 'test-error-message',
            'key': 'test-key'
        }
    )
