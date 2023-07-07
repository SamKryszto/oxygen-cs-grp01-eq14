import logging
import json
import time
import os
from signalrcore.hub_connection_builder import HubConnectionBuilder
import requests
from src.models import create_session, Event


class Main:
    def __init__(self):
        self._hub_connection = None
        self._session = None
        self.HOST = os.getenv("HOST", "http://34.95.34.5")
        if not os.getenv("TOKEN"):
            raise Exception("No token defined")
        self.TOKEN = os.getenv("TOKEN")
        self.TICKETS = int(os.getenv("TICKETS", "100"))
        self.T_MAX = int(os.getenv("T_MAX", "30"))
        self.T_MIN = int(os.getenv("T_MIN", "10"))
        self.DATABASE = os.getenv("DATABASE", "postgres")

    def __del__(self):
        if self._hub_connection is not None:
            self._hub_connection.stop()

    def setup(self):
        self._session = create_session(self.DATABASE)
        self.setSensorHub()

    def start(self):
        self.setup()
        self._hub_connection.start()

        print("Press CTRL+C to exit.")
        while True:
            time.sleep(2)

    def setSensorHub(self):
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.HOST}/SensorHub?token={self.TOKEN}")
            .configure_logging(logging.INFO)
            .with_automatic_reconnect(
                {
                    "type": "raw",
                    "keep_alive_interval": 10,
                    "reconnect_interval": 5,
                    "max_attempts": 999,
                }
            )
            .build()
        )

        self._hub_connection.on("ReceiveSensorData", self.onSensorDataReceived)
        self._hub_connection.on_open(lambda: print("||| Connection opened."))
        self._hub_connection.on_close(lambda: print("||| Connection closed."))
        self._hub_connection.on_error(
            lambda data: print(f"||| An exception was thrown closed: {data.error}")
        )

    def onSensorDataReceived(self, data):
        try:
            print(data[0]["date"] + " --> " + data[0]["data"])
            date = data[0]["date"]
            dp = float(data[0]["data"])
            self.send_temperature_to_fastapi(date, dp)
            self.analyzeDatapoint(date, dp)
        except Exception as err:
            print(err)

    def analyzeDatapoint(self, date, data):
        if float(data) >= float(self.T_MAX):
            self.sendActionToHvac(date, "TurnOnAc", self.TICKETS)
            self.send_event_to_database(date, "TurnOnAC")
        elif float(data) <= float(self.T_MIN):
            self.sendActionToHvac(date, "TurnOnHeater", self.TICKETS)
            self.send_event_to_database(date, "TurnOnHeater")

    def sendActionToHvac(self, date, action, nbTick):
        r = requests.get(f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{nbTick}")
        details = json.loads(r.text)
        print(details)

    def send_temperature_to_fastapi(self, date, dp):
        pass

    def send_event_to_database(self, timestamp, event):
        try:
            _event = Event(
                timestamp=timestamp,
                event=event,
            )
            self._session.add(_event)
            self._session.commit()
        # except requests.exceptions.RequestException as e:
        except Exception as e:
            raise Exception("Error sending event to database") from e


if __name__ == "__main__":
    main = Main()
    main.start()
