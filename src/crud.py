from loguru import logger
import requests
from src.schemas import Activity
from src.schemas import ActivityPoint


class StravaRepository:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        refresh_token: str,
        activity_prefix: str,
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.activity_prefix = activity_prefix  # name of the activity to crop
        self.set_access_token()

    def set_access_token(self) -> None:
        """Refresh Strava access token."""
        logger.info("Setting up Strava connection started.")
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
        }
        response = requests.post(
            "https://www.strava.com/oauth/token", data=payload, verify=False
        )
        response.raise_for_status()
        self.access_token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        logger.info("Access token successfully retreived.")

    def get_activity(self) -> Activity:
        """Fetch skiing activity to crop, based on the sport type and name."""
        logger.info("Fetching recent skiing activities from Strava.")
        params = {"per_page": 100, "page": 1}
        response = requests.get(
            "https://www.strava.com/api/v3/athlete/activities",
            headers=self.headers,
            params=params,
        )
        response.raise_for_status()
        activities = [
            r
            for r in response.json()
            if self.activity_prefix == r["name"] and r["sport_type"] == "AlpineSki"
        ]
        if activities:
            activity = activities.pop()
            logger.info(f"Activity found with id: {activity['id']}")
        else:
            logger.info("No activity found.")
            return
        streams = self.get_streams_by_id(activity["id"])
        activity = Activity(
            id=activity["id"], streams=streams, start_datetime=activity["start_date"]
        )
        logger.info("Activity successfully fetched.")
        return activity

    def get_streams_by_id(self, id) -> list[ActivityPoint]:
        """Fetch the corresponding stream data for a given activity."""
        logger.info(f"Fetching activity streams for {id}.")
        type_to_stream = {}
        for key in ["altitude", "time", "latlng", "distance"]:
            params = {"keys": [key]}
            response = requests.get(
                f"https://www.strava.com/api/v3/activities/{id}/streams",
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            idx = 0 if key in ["latlng", "distance"] else 1
            if response.status_code == 200 and key in [
                e["type"] for e in response.json()
            ]:
                stream = response.json()[idx]["data"]
                dtype = response.json()[idx]["type"]
                type_to_stream[dtype] = stream
        return [
            ActivityPoint(**dict(zip(type_to_stream.keys(), values)))
            for values in zip(*type_to_stream.values())
        ]

    def upload_activity(self, activity: Activity):
        """Upload an activiy with gpx data to Strava."""
        data = {
            "data_type": "gpx",
            "trainer": "0",
            "commute": "0",
            "sport_type": "AlpineSki",
            "name": "Test",
            "description": "✂️  cut with SKIssors",
        }
        files = {"file": open(f"{activity.id}.gpx", "rb")}

        response = requests.post(
            "https://www.strava.com/api/v3/uploads",
            headers=self.headers,
            data=data,
            files=files,
        )
        logger.info("Cropped Activity uploaded to Strava.")
        return response
