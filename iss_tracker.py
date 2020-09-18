import json
import sys
import datetime
import requests
import time

ADAFRUIT_IO_USERNAME = "nnnnnn"
ADAFRUIT_IO_KEY = "xxxxxx"
FEED_KEY = "iss-position"


def main():
    while True:
        iss_data = requests.get("http://api.open-notify.org/iss-now.json").json()

        if iss_data['message'] == 'success':
            long = iss_data['iss_position']['longitude']
            lat = iss_data['iss_position']['latitude']
            timestamp = iss_data['timestamp']
        else:
            print("Could not fetch ISS location data")
            sys.exit()

        dt_object = datetime.datetime.fromtimestamp(timestamp)
        url = f"https://io.adafruit.com/api/v2/{ADAFRUIT_IO_USERNAME}/feeds/{FEED_KEY}/data"

        header = {
            "Content-Type": "application/json",
            "X-AIO-Key": ADAFRUIT_IO_KEY
        }

        data = {
            "value": str(dt_object),
            "lat": lat,
            "lon": long
        }

        json_data = json.dumps(data)

        resp = requests.post(url, data=json_data, headers=header)
        if resp.status_code == 200:
            print(f"Posted ISS position @ {lat}, {long}")
        else:
            print("Error posting ISS data")

        time.sleep(60)



if __name__ == '__main__':
    main()
