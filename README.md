# Lambda Change EC2 Instance Type

Lambda function to change instance type of an EC2 instance.
It will skip processing if the instance is already using target instnace type.

You can schedule the Lambda function using an EventBridge scheduler.
Pass in payload which defines instance_id and new_instance_type.
```
{ "instance_id": "i-07b8ea23e20d96173", "new_instance_type": "m5.4xlarge" }
```

