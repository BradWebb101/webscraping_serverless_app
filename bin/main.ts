#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { ECSStack } from '../lib/ECSStack';
import { LambdaStack } from '../lib/LambdaStack'

const app = new cdk.App();

const GLOBALS = {
  projectName:'RedditScraper',
}

const ec2Stack = new ECSStack(app, `${GLOBALS.projectName}ECSStack`, {
  ...GLOBALS
});

const lambdaStack = new LambdaStack(app, `${GLOBALS.projectName}LambdaStack`, {
  ...GLOBALS
});