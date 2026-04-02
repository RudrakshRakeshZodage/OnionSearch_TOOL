import sys
import dns.resolver
from pymongo import MongoClient

# Attempt to resolve the NEW cluster provided by the user
NEW_URL = "mongodb+srv://sudhanshun10b3720_db_user:Sudhu%402005@cluster0.d6wfgzt.mongodb.net/?appName=Cluster0"

print(f"[DEBUG] Attempting to resolve NEW MongoDB SRV record: cluster0.d6wfgzt.mongodb.net")
try:
    srv_query = "_mongodb._tcp.cluster0.d6wfgzt.mongodb.net"
    answers = dns.resolver.resolve(srv_query, 'SRV')
    print(f"[SUCCESS] Resolved SRV record for NEW cluster. Found {len(answers)} shards.")
    
    print(f"\n[DEBUG] Attempting connection via MongoClient to NEW cluster...")
    client = MongoClient(NEW_URL, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("[SUCCESS] Successfully connected to the NEW MongoDB Atlas cluster!")
except Exception as e:
    print(f"[FAILURE] Connection to NEW cluster failed: {e}")
