import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as iam from 'aws-cdk-lib/aws-iam';

interface RedditScraperProps extends cdk.StackProps {
    projectName:string
  }
  

export class LambdaStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: RedditScraperProps) {
    super(scope, id, props);

    // Import the ECS service ARN from the ECS stack
    const serviceArn = cdk.Fn.importValue(`${props?.ecsStackName}-ServiceArn`);

    // Create a Lambda function to start the Fargate task
    const startTaskFunction = new lambda.Function(this, 'MyStartTaskFunction', {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: 'index.handler',
      code: lambda.Code.fromAsset('lambda'),
      environment: {
        SERVICE_ARN: serviceArn,
        CONTAINER_NAME: 'MyContainer',
      },
    });

    // Create a Lambda function to start the Fargate task
    const queryDataFunction = new lambda.Function(this, 'MyStartTaskFunction', {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: 'index.handler',
      code: lambda.Code.fromAsset('lambda'),
    });

    new cdk.CfnOutput(this, 'QueryLambdaARN', {
      value:queryDataFunction.functionArn,
      exportName: 'QueryLambdaFunctionARN'
    });

    new cdk.CfnOutput(this, 'QueryLambdaName', {
      value:queryDataFunction.functionName,
      exportName: 'QueryLambdaFunctionName'
    });

  }
}
