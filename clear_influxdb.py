import os
from datetime import datetime
from influxdb_client import InfluxDBClient
from dotenv import load_dotenv

# Load .env
load_dotenv()

# InfluxDB connection
client = InfluxDBClient(
    url="http://localhost:8086",
    token=os.getenv("INFLUXDB_TOKEN"),
    org="fisens"
)

buckets_api = client.buckets_api()
delete_api = client.delete_api()

print("=" * 80)
print("🗑️  InfluxDB Data Clearer")
print("=" * 80)
print()

try:
    # List all buckets
    buckets = buckets_api.find_buckets()

    print("📦 Available Buckets:")
    for bucket in buckets.buckets:
        print(f"   - {bucket.name} (ID: {bucket.id})")

    print()
    print("=" * 80)
    print("⚠️  WARNING: This will DELETE all data from the 'sensors' bucket!")
    print("=" * 80)
    print()

    # Confirm deletion
    confirm = input("Type 'DELETE' to confirm clearing the 'sensors' bucket: ").strip()

    if confirm.upper() == "DELETE":
        print()
        print("🗑️  Deleting all data from 'sensors' bucket...")

        # Delete all data from sensors bucket
        delete_api.delete(
            start="1970-01-01T00:00:00Z",
            stop="2099-12-31T23:59:59Z",
            predicate='',  # Empty predicate deletes all
            bucket="sensors",
            org="fisens"
        )

        print()
        print("=" * 80)
        print("✅ SUCCESS! All data has been cleared from 'sensors' bucket")
        print("=" * 80)
        print()
        print("The bucket still exists and is ready for new data.")
        print()
    else:
        print()
        print("❌ Deletion cancelled. Data NOT deleted.")
        print()

except Exception as e:
    print(f"❌ Error: {e}")
    print()

finally:
    client.close()
