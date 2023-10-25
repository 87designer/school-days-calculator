import numpy as np
from datetime import timedelta
from pandas.tseries.holiday import USFederalHolidayCalendar

# Holiday Calculations
cal = USFederalHolidayCalendar()


def add_bus_days(from_date, n_days):
    while n_days > 0:
        from_date += timedelta(days=1)
        weekday = from_date.weekday()
        if weekday >= 5:  # sunday = 6
            continue
        n_days -= 1
    return from_date


def calc_end_date(start_date, n_days, h_cal, trips):
    """Calculates HomeSchool Calendar End-Date.

    Parameters
    ----------
    start_date : str
        The first day of school
    n_days : int
        A list of US Federal Holidays
    h_cal : array
        A list of US Federal Holidays
    trips : list
        Additional trips/days off/vacations

    Returns
    -------
    str
        Date of final school day
    """
    holiday_range = start_date + timedelta(days=365)
    holidays = h_cal.holidays(start=str(start_date), end=str(holiday_range)).to_pydatetime()
    # Number of weekdays in Trip Range
    skips = 0
    for trip in trips:
        skips += np.busday_count(trip[0], trip[1])

    end_date = add_bus_days(start_date, (n_days + skips))

    added_holidays = 0
    for date in holidays:
        if start_date < date <= end_date:
            added_holidays += 1
        else:
            pass

    adj_date = add_bus_days(end_date, added_holidays)

    return adj_date
