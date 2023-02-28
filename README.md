# Welcome to my websraping prototype

## Purpose
The purpose of this project is to explore the way to improve validation for a website scraping app. 

Website scraping is a hard approach for testing given the the underlying data you have no control over and can change without you knowing. The approach i have taken here is to use software and data testing processes to validate the scraping process at multiple checkpoints, with abnormalities being flagged at the point of failure for manual checking of the underlying data. 

## How we do it 
### Tech used: 
- AWS services: Lambda, Fargate, DynamoDB, SQS, Event Bridge
- Code: Typescript, Python 
- Tools: AWS CDK, Docker
- Python libraries: requests, bs4, jsonschema, 

### Validation approach: 
- Pytest: Testing of code written to ensure that the code is correct.
- Website metadata: Testing does the current scrape of the website match a snapshot scrape.
    - Does scrape unique tags == snapshot unique tags
    - Does scrape aggregate tags fit within bounds of acceptable range for the website
- Data validation: Does the data schema out of the scrape meet the requirements for the data.

## Infrastructure diagram
![alt text](./readme/Infrastructure.png)

## Current status 
This app is in testing for deployment. Will be ready for use in a few days.