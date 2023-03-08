import os
import pytest
from unittest import mock
from bs4 import BeautifulSoup
from botocore.stub import Stubber
from botocore.session import Session
from jsonschema.exceptions import ValidationError

from utils.aws_helpers import S3, DynamoDb
from parser_and_validator.parser_and_validator import ParserAndValidator

@pytest.fixture
def parser_and_validator():
    project_name = 'test_project'
    key = 'test_key'
    key_condition_expression = {'test_key': 'test_value'}
    expression_attribute_values = {'test_value': 'test_expression'}
    parser_and_validator = ParserAndValidator(project_name, key, key_condition_expression, expression_attribute_values)
    return parser_and_validator

@pytest.fixture
def s3_stub():
    session = Session()
    s3_client = session.create_client('s3', region_name='us-west-2')
    stubber = Stubber(s3_client)
    response = {'Body': b'{"test_key": "test_value"}'}
    stubber.add_response('get_object', response, {'Bucket': 'test_project-bucket', 'Key': 'pickle/test_key'})
    stubber.activate()
    return s3_client

@pytest.fixture
def dynamodb_stub():
    session = Session()
    dynamodb_client = session.create_client('dynamodb', region_name='us-west-2')
    stubber = Stubber(dynamodb_client)
    response = {'schema': {'type': 'object'}, 'tags': ['test_tag'], 'site_ratio': 0.5}
    stubber.add_response('get_item', response, {'TableName': 'test_project', 'Key': {'test_key': {'S': 'test_value'}}})
    stubber.activate()
    return dynamodb_client

def test_load_s3_file(parser_and_validator, s3_stub):
    parser_and_validator.load_s3_file()
    assert parser_and_validator.soup == {"test_key": "test_value"}

def test_get_site_validation_data(parser_and_validator, dynamodb_stub):
    parser_and_validator.get_site_validation_data()
    assert parser_and_validator.schema == {'type': 'object'}
    assert parser_and_validator.tags == ['test_tag']
    assert parser_and_validator.site_ratio == 0.5

def test_validate_html_tags(parser_and_validator):
    parser_and_validator.soup = BeautifulSoup('<html><head><title>Test Page</title></head><body><h1>Heading</h1><p>Test paragraph.</p></body></html>', 'html.parser')
    parser_and_validator.tags = ['h1', 'p']
    parser_and_validator.site_ratio = 0.5
    assert parser_and_validator.validate_html_tags() == True

def test_counts_validation(parser_and_validator):
    parser_and_validator.soup = BeautifulSoup('<html><head><title>Test Page</title></head><body><h1>Heading</h1><p>Test paragraph.</p></body></html>', 'html.parser')
    parser_and_validator.tags = ['h1', 'p']
    parser_and_validator.site_data = {'h1': 1, 'p': 1}
    assert parser_and_validator.counts_validation() == True

def test_schema_validation(parser_and_validator):
    parser_and_validator.schema = {'type': 'object', 'properties': {'name': {'type': 'string'}, 'age': {'type': 'integer'}}}
    parser_and_validator.site_data = {'name': 'John', 'age': 30}
    assert parser_and_validator.schema_validation() == None
    with pytest.raises(ValidationError):
        parser_and_validator.schema = {'type': 'object', 'properties': {'name': {'type': 'string'}, 'age': {'type': 'integer'}}}
