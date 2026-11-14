import os
from datetime import datetime, timezone
import psycopg2
import requests

url = "https://open.er-api.com/v6/latest/USD"
response = requests.get(url, timeout=10)
data = response.json()

if data.get("result") == "success":
    egp_rate = data["rates"]["EGP"]
    time = data["time_last_update_utc"]
    clean_time = time[:-6]
    print(f"1.00 USD = {egp_rate:.2f} EGP as of {clean_time}")

    provider_ts = datetime.fromtimestamp(data["time_last_update_unix"], tz=timezone.utc)
    conn = psycopg2.connect(
        host="localhost",
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        dbname=os.environ["POSTGRES_DB"],
    )
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO rates (base, target, rate, provider_updated_at) "
        "VALUES (%s, %s, %s, %s) "
        "ON CONFLICT (base, target, provider_updated_at) DO NOTHING",
        ("USD", "EGP", egp_rate, provider_ts),
    )
    conn.commit()
    conn.close()
else:
    print("Failed to retrieve data")
