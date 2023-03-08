import * as cdk from 'aws-cdk-lib';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import { Construct } from 'constructs';

interface RedditScraperProps extends cdk.StackProps {
    projectName:string
    queue:sqs.Queue
  }


export class SqsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: RedditScraperProps) {
    super(scope, id, props);
    queue:sqs.Queue
    // Create a new SQS queue
    this.queue = new sqs.Queue(this, 'MyQueue', {
      queueName: 'my-queue-name'
    });

    // Output the URL of the queue
    new cdk.CfnOutput(this, 'QueueUrl', {
      value: queue.queueUrl
    });
  }
}
