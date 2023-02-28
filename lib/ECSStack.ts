import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

export class FargateStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create a VPC for your Fargate service
    const vpc = new ec2.Vpc(this, 'FargateVpc', {
      maxAzs: 2 // maximum availability zones
    });

    // Create a Fargate cluster
    const cluster = new ecs.Cluster(this, 'FargateCluster', {
      vpc: vpc
    });

    // Create a Fargate task definition
    const taskDefinition = new ecs.FargateTaskDefinition(this, 'FargateTask');

    // Define your task definition properties and add a container to it

    // Create a Fargate service
    const service = new ecs.FargateService(this, 'FargateService', {
      cluster: cluster,
      taskDefinition: taskDefinition,
      desiredCount: 1
    });
  }
}
