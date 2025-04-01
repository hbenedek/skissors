import pandas as pd
from loguru import logger
from src.schemas import ActivityPoint, Activity


class LiftClassifier:
    def __init__(self, window: int = 20):
        self.window = window

    def predict(self, altitude: pd.Series, time: pd.Series):
        """Detect time spent on ski lifts, using average gradient in time window."""
        logger.info("Detecting ski lifts.")
        grad = altitude.diff() / time.diff()
        return grad.fillna(0).rolling(self.window).mean().fillna(0) <= 0

    def classify_ski_lift(self, activity: Activity) -> Activity:
        """Remove ActivityPoints from Activity, that were detected as time spent on ski lift."""
        df = pd.DataFrame(activity.streams)
        df["moving"] = self.predict(df["altitude"], df["time"])
        logger.info(f"Activity cropped from points: {len(df)} -> {sum(df['moving'])}.")

        activity.streams = df.apply(lambda x: ActivityPoint(*x), axis=1).to_list()
        return activity
