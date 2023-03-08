import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import * as path from 'path';

export class ECSStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: any) {
    super(scope, id, props);

    const { projectName } = props

    // Create a VPC for your Fargate service
    const vpc = new ec2.Vpc(this, `${projectName}FargateVpc`, {
      maxAzs: 2 // maximum availability zones
    });

    // Create a Fargate cluster
    const cluster = new ecs.Cluster(this, `${projectName}FargateCluster`, {
      vpc: vpc
    });

    // Create a Fargate task definition
    const taskDefinition = new ecs.FargateTaskDefinition(this, `${projectName}FargateTask`);

    // Define your task definition properties and add a container to it
    const scrapeContainer = taskDefinition.addContainer('ScrapeFargateContainer', {
      image: ecs.ContainerImage.fromAsset(path.join(__dirname, 'app')),
      memoryLimitMiB: 512
    });

    // Define your task definition properties and add a container to it
    const parseContainer = taskDefinition.addContainer('ParseFargateContainer', {
      image: ecs.ContainerImage.fromAsset(path.join(__dirname, 'app')),
      memoryLimitMiB: 512
    });

     // Create the ECS service with the task definition
     const service = new ecs.FargateService(this, `${projectName}FargateService`, {
      cluster,
      taskDefinition,
      desiredCount: 1,
      serviceName: `${projectName}FargateService`,
    });
  }
}
