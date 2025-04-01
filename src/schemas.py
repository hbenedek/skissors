from dataclasses import dataclass
from pydantic_settings import BaseSettings, SettingsConfigDict
import gpxpy
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    client_id: str
    client_secret: str
    refresh_token: str
    activity_prefix: str


@dataclass
class ActivityPoint:
    time: float
    distance: float
    latlng: list[float]
    altitude: float
    moving: bool | None = None


@dataclass
class Activity:
    id: int
    start_datetime: str
    streams: list[ActivityPoint] | None = None

    def create_gpx(self) -> None:
        "Create gpx file from list of activiy points."
        start_time = datetime.strptime(self.start_datetime, "%Y-%m-%dT%H:%M:%SZ")
        gpx = gpxpy.gpx.GPX()
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)
        for i, point in enumerate(self.streams):
            gpx_point = gpxpy.gpx.GPXTrackPoint(
                latitude=point.latlng[0],
                longitude=point.latlng[1],
                elevation=point.altitude,
                time=(
                    start_time + timedelta(seconds=point.time + 1)
                ),  # to prevent activity duplicate
            )

            extensions = ET.Element("gpxtpx:TrackPointExtension")
            gpx_temp = ET.SubElement(extensions, "gpxtpx:cad")
            gpx_temp.text = str(point.moving).lower()

            gpx_point.extensions.append(extensions)
            gpx_segment.points.append(gpx_point)

        with open(f"{self.id}.gpx", "w") as file:
            file.write(gpx.to_xml())
