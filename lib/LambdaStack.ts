import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as iam from 'aws-cdk-lib/aws-iam';

export class LambdaStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Import the ECS service ARN from the ECS stack
    const serviceArn = cdk.Fn.importValue(`${props?.ecsStackName}-ServiceArn`);

    // Create a Lambda function to start the Fargate task
    const startTaskFunction = new lambda.Function(this, 'MyStartTaskFunction', {
      runtime: lambda.Runtime.NODEJS_14_X,
      handler: 'index.handler',
      code: lambda.Code.fromAsset('lambda'),
      environment: {
        SERVICE_ARN: serviceArn,
        CONTAINER_NAME: 'MyContainer',
      },
    });

    // Grant permissions to the Lambda function to start the Fargate task
    startTaskFunction.addToRolePolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: [
        'ecs:RunTask',
        'ecs:StopTask',
        'ecs:DescribeTasks',
        'logs:CreateLogGroup',
        'logs:CreateLogStream',
        'logs:PutLogEvents',
      ],
      resources: [
        serviceArn,
      ],
    }));
  }
}
