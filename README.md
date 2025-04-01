# ✂️  SKIssors

SKIssors detects ski lift ascents in your skiing activities and crops them. 

## 🚧 Under Construction

Strava interpolates consecutive data points; simply removing points from the activity does not solve the problem.
GPX format cannot encode pauses, future work is to explore other data formats like TCX, to encode pauses.

## ⛷️ Motivation 

As of 2025. january, there is no Skiing activity available on Garmin Forerunner 165.
I record skiing as a general activity, but metrics like average speed and distance are polluted by skilifts. 
Instead of stopping the activity on the lifts, I created this job to get rid of time intervals not spent skiing.

The project was inspired by [StravaMerger](https://github.com/jannisborn/stravamerger).


## ⚙️ Setup 

SKIssors uses the [Strava API](https://developers.strava.com/docs/reference/) to perform crud operations.

You will need to an API token with `read_all` and `write` scope.

Set the following env variables:
- `CLIENT_ID`
- `REFRESH_TOKEN`
- `CLIENT_SECRET`


