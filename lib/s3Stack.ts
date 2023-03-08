import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3'
import * as s3deploy from 'aws-cdk-lib/aws-s3-deployment';
import { RemovalPolicy, Tags } from 'aws-cdk-lib';

export class KYCBucketStack extends cdk.Stack {
    storageBucket: s3.Bucket;
    siteBucket: s3.Bucket
  
  constructor(scope: Construct, id: string, props?: any) {
    super(scope, id, props);

    const { businesstags, env, executionRole } = props

    this.storageBucket = new s3.Bucket(this, `${businesstags.projectName}-bucket`, {
      bucketName: `${businesstags.projectName}-bucket`,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      versioned: true,
      removalPolicy: RemovalPolicy.DESTROY
    });

     // create S3 bucket
     this.siteBucket = new s3.Bucket(this, `${businesstags.projectName}-static-website`, {
        websiteIndexDocument: 'index.html',
      });
  
      // create S3 deployment
      new s3deploy.BucketDeployment(this, `${businesstags.projectName}-static-website-deployment`, {
        sources: [s3deploy.Source.asset('../site/index.html')],
        destinationBucket: this.siteBucket
      });
    }
  }

