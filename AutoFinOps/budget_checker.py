import boto3
from discord_webhook import DiscordWebhook
import datetime

def check_cost():
    client = boto3.client('ce', region_name='us-east-1')

    start = datetime.date.today().replace(day=1)
    end = datetime.date.today()

    cost_data = client.get_cost_and_usage(
        TimePeriod={
            'Start': str(start),
            'End': str(end)
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost']
    )

    amount = float(cost_data['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
    print(f"Current AWS Cost: ${amount:.2f}")

    if amount > 0.80:
        message = f"⚠️ AWS cost alert! Your usage is ${amount:.2f} this month."
        webhook = DiscordWebhook(
            url='https://discord.com/api/webhooks/1389261209106387149/lY3q917Q2jfkLoS0uC4wqzHjmupPrtGkUy0gtbbJz_0TuJatlbyNVv2kquxEMCQA88cd',
            content=message
        )
        webhook.execute()

if __name__ == "__main__":
    check_cost()