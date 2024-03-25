from datetime import date, timedelta
import math
from typing import Generator

import click
import holidays


@click.command()
@click.option(
    "--start",
    default=lambda: str(date.today()),
    type=date.fromisoformat,
    help="Start date marking the relevant month",
)
@click.option(
    "--ptc",
    default=20,
    type=float,
    help="Per cent of work days commitment",
)
@click.option(
    "--country",
    default="cz",
    type=str.upper,
    help="Country to determine holidays for",
)
def main(start: date, ptc: float, country: str):
    country_holidays = holidays.country_holidays(country)

    first_day = start.replace(day=1)
    last_day = start.replace(day=1, month=start.month + 1) - timedelta(days=1)

    workdays = [
        day
        for day in iter_weekdays(first_day, last_day)
        if day.weekday() < 5 and day not in country_holidays
    ]

    click.echo(f"Workdays in {start.strftime('%B %Y')}: {len(workdays)}")
    click.echo(f"{ptc:.1f}% commitment: {calc_commitment(len(workdays), ptc)} days")


def calc_commitment(workdays_count: int, ptc: float) -> int:
    return math.ceil(workdays_count * ptc / 100)


def iter_weekdays(start: date, end: date) -> Generator[date, None, None]:
    day = start
    while day <= end:
        yield day
        day += timedelta(days=1)


if __name__ == "__main__":
    main()
