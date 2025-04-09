from pendulum import DateTime
import pendulum


def format_time_from_now(release_date: DateTime) -> str:
    today = pendulum.now()
    interval = today.diff(release_date)
    date = today.subtract(
        years=interval.years,
        months=interval.months,
        weeks=interval.weeks,
        days=interval.days,
        hours=interval.hours,
        minutes=interval.minutes,
    ).diff_for_humans()
    return date
