import datetime
from discord_webhook import DiscordWebhook

# =========================================
# CONFIG
# =========================================

# Put your real Discord webhook URL here
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/yourwebhook/yourid'

# Change this to simulate different costs
COST = 1.25

# Threshold for sending an alert
THRESHOLD = 0.80

# =========================================
# MAIN LOGIC
# =========================================

def check_cost():
    # Instead of querying AWS, we simulate the cost
    amount = COST

    print(f"[INFO] AWS cost: ${amount:.2f}")

    if amount > THRESHOLD:
        message = f"⚠️ AWS cost alert!\nYour usage is ${amount:.2f} this month."
        
        print(f"[INFO] Sending alert to Discord...")

        webhook = DiscordWebhook(
            url=DISCORD_WEBHOOK_URL,
            content=message
        )
        response = webhook.execute()

        print(f"[INFO] Discord response: {response}")

    else:
        print("[INFO] Cost is under the threshold. No alert needed.")

if __name__ == "__main__":
    check_cost()
