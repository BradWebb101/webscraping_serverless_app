import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as iam from 'aws-cdk-lib/aws-iam'

export class DynamoStack extends Construct {
  constructor(scope: Construct, id: string, props?: any) {
    super(scope, id);

    const { projectName } = props
    const lambdaFunctionARN = cdk.Fn.importValue('LambdaFunctionARN');

    // Create the DynamoDB table
    const table = new dynamodb.Table(this, `${projectName}Table`, {
      tableName : `${projectName}-table`,
      partitionKey: { name: 'item', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST, 
    });

    table.grantFullAccess(new iam.ArnPrincipal(lambdaFunctionARN))

    new cdk.CfnOutput(this, 'TableARN', {
      value: table.tableArn,
      exportName: 'DynamoTableARN'
    });

    new cdk.CfnOutput(this, 'TableName', {
      value: table.tableName,
      exportName: 'DynamoTableName'
    });
  }}