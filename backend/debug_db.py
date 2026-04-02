import sys
try:
    import dns.resolver
    print("[SUCCESS] 'dnspython' is installed.")
except ImportError:
    print("[FAILURE] 'dnspython' is MISSING. Run: pip install dnspython")
    sys.exit(1)

from pymongo import MongoClient
import socket

MONGO_URL = "mongodb+srv://sudhanshun10b3720_db_user:Sudhu%402005@cluster0.jmlmmop.mongodb.net/?appName=Cluster0"

print(f"\n[DEBUG] Attempting to resolve MongoDB SRV record...")
try:
    # Manual SRV check
    srv_query = "_mongodb._tcp.cluster0.jmlmmop.mongodb.net"
    answers = dns.resolver.resolve(srv_query, 'SRV')
    print(f"[SUCCESS] Resolved SRV record. Found {len(answers)} shards.")
except Exception as e:
    print(f"[FAILURE] DNS SRV Resolution failed: {e}")
    print("This usually means your local DNS (or VPN) blocks SRV records.")

print(f"\n[DEBUG] Attempting connection via MongoClient...")
try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    # The 'ping' command is cheap and does not require auth
    client.admin.command('ping')
    print("[SUCCESS] Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"[FAILURE] Could not connect to MongoDB: {e}")
