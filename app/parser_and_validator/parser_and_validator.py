import os
import boto3
import jsonschema
import pickle
from bs4 import BeautifulSoup
from jsonschema.exceptions import ValidationError

from aws_helpers import S3, DynamoDb

class ParserAndValidator():

    def __init__(self, project_name:str, key:str, key_condition_expression:dict[str, str],expression_attribute_values:str):
        self.project_name = project_name
        self.key = key
        self.key_condition_expression = key_condition_expression
        self.expression_attribute_values = expression_attribute_values
        self.dynamo_client = boto3.client('dynamodb')
        self.s3_client = boto3.client('s3')
        self.load_s3_file()
        self.get_site_validation_data()

    def load_s3_file(self):
        #Get data from s3
        response = S3.get(Bucket=f'{self.project_name}-bucket', Key=f'pickle/{self.key}')
        # unpickle and store as soup
        self.soup = pickle.loads(response)

    def get_site_validation_data(self):
        key_condition_expression=None 
        expression_attribute_values=None
        response = DynamoDb.get(self.project_name,key_condition_expression,expression_attribute_values)
        self.schema = response.get('schema',None)
        self.tags = response.get('tags',None)
        self.site_ratio = response.get('site_ratio',None)

    def validate_html_tags(self) -> bool:
        soup_tags = {tag.name for tag in self.soup}
        count = sum(item1 in self.tags for item1 in soup_tags)
        #Add in field for site ratio
        return count / len(soup_tags) > self.site_data.site_ratio

    def counts_validation(self) -> bool:
        #Add in tags list to dynamo db 
        response = DynamoDb.get(self.project_name, self.key_condition_expression, self.expression_attribute_values)
        self.site_data = response.get('Item', None)
        tag_counts = {tag: len(self.soup.find_all(tag)) for tag in self.tags}
        return self.site_data == tag_counts

    def schema_validation(self) -> bool:
        response = DynamoDb.get(self.project_name, self.key_condition_expression, self.expression_attribute_values)
        self.site_data = response.get('Item', None)
        for data_item in self.site_data:
            jsonschema.validate(data_item, self.schema)
        
           
    
    def parse_website(self, soup:BeautifulSoup, parsing_schema:dict[str:str]) -> None:
        website_data = {
            key: self.soup.find_all(key) for key in self.parsing_schema.keys()
        }
        self.dynamo_client.put(website_data)

def main():
    project_name = os.getenv('PROJECT_NAME')
    key = os.getenv('KEY')
    key_condition_expression = os.getenv('KEY_ATTR_VAL')
    expression_attribute_values = os.getenv('EXP_ATTR_VAL')
    sqs_url = os.getenv('SQS_URL')
    val = ParserAndValidator(project_name, key)
    val.validate_html_tags()
    val.counts_validation()
    val.schema_validation()

if __name__ == '__main__':
    main()
    