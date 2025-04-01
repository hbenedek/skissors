from src.transform import LiftClassifier
from src.crud import StravaRepository
from src.schemas import Settings
import urllib3

urllib3.disable_warnings()

if __name__ == "__main__":
    settings = Settings()
    repository = StravaRepository(**settings.model_dump())
    classifier = LiftClassifier()

    activity = repository.get_activity()
    activity = classifier.classify_ski_lift(activity)
    activity.create_gpx()
    repository.upload_activity(activity)
