import boto3
from discord_webhook import DiscordWebhook

# Your Discord webhook URL
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/yourwebhook/yourid'

# Define REQUIRED tags here
REQUIRED_TAGS = ["Project", "Environment", "Owner"]

def check_tags():
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    s3_client = boto3.client("s3", region_name="us-east-1")

    missing_tags_resources = []

    # -------- EC2 --------
    reservations = ec2_client.describe_instances()["Reservations"]
    for res in reservations:
        for instance in res["Instances"]:
            tags = instance.get("Tags", [])
            tag_keys = [tag["Key"] for tag in tags]

            missing = [key for key in REQUIRED_TAGS if key not in tag_keys]
            if missing:
                instance_id = instance["InstanceId"]
                missing_tags_resources.append(
                    f"EC2 Instance {instance_id} missing tags: {missing}"
                )

    # -------- S3 --------
    buckets = s3_client.list_buckets()["Buckets"]
    for bucket in buckets:
        bucket_name = bucket["Name"]

        try:
            tagging = s3_client.get_bucket_tagging(Bucket=bucket_name)
            tag_set = tagging["TagSet"]
            tag_keys = [tag["Key"] for tag in tag_set]
        except s3_client.exceptions.NoSuchTagSet:
            tag_keys = []

        missing = [key for key in REQUIRED_TAGS if key not in tag_keys]
        if missing:
            missing_tags_resources.append(
                f"S3 Bucket {bucket_name} missing tags: {missing}"
            )

    if missing_tags_resources:
        message = "**Missing Tags Detected!**\n\n" + "\n".join(missing_tags_resources)
        webhook = DiscordWebhook(
            url=DISCORD_WEBHOOK_URL,
            content=message
        )
        webhook.execute()
        print("[INFO] Sent alert to Discord.")
    else:
        print("[INFO] All resources have required tags.")

if __name__ == "__main__":
    check_tags()
