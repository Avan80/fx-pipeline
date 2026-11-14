import requests

url = "https://open.er-api.com/v6/latest/USD"
response = requests.get(url, timeout=10)
response.raise_for_status()
data = response.json()

if data.get("result") == "success":
    egp_rate = data["rates"]["EGP"]
    time = data["time_last_update_utc"]
    clean_time = time[:-6]
    print(f"1.00 USD = {egp_rate:.2f} EGP as of {clean_time}")
else:
    print("Failed to retrieve data")
