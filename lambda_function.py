import boto3


def lambda_handler(event, context):
    if 'detail' not in event:
        print("❌ Event does not contain 'detail'. Likely a manual test. Aborting.")
        return

    ec2 = boto3.client('ec2')

    try:
        for record in event['detail']['responseElements']['instancesSet']['items']:
            instance_id = record['instanceId']
            print(f"Tagging instance: {instance_id}")
            
            tags = [
                {'Key': 'LaunchedBy', 'Value': 'Lambda-AutoTag'},
                {'Key': 'Environment', 'Value': 'Dev'}
            ]

            ec2.create_tags(Resources=[instance_id], Tags=tags)
            print(f"✅ Tagged instance {instance_id} successfully.")
    except Exception as e:
        print(f"❌ Error while tagging: {e}")
