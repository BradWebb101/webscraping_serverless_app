// Import the necessary DynamoDB classes
import { Table, AttributeType, BillingMode } from 'aws-cdk-lib/aws-dynamodb';
import { StreamViewType } from 'aws-cdk-lib/aws-dynamodb';
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';

export class DynamoDbStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // Create a new DynamoDB table
    const table = new Table(this, 'my-table', {
      partitionKey: { name: 'website', type: AttributeType.STRING },
      sortKey: { name: 'validation_type', type: AttributeType.NUMBER },
      billingMode: BillingMode.PAY_PER_REQUEST,
      stream: StreamViewType.NEW_AND_OLD_IMAGES,
    });

    
  }
}
