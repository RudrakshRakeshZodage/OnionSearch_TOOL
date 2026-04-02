import socket

shards = [
    "cluster0-shard-00-00.jmlmmop.mongodb.net",
    "cluster0-shard-00-01.jmlmmop.mongodb.net",
    "cluster0-shard-00-02.jmlmmop.mongodb.net"
]

for shard in shards:
    try:
        ip = socket.gethostbyname(shard)
        print(f"[SUCCESS] Resolved {shard} to {ip}")
    except socket.gaierror:
        print(f"[FAILURE] Could not resolve {shard}")
