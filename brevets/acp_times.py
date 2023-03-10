"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow
from datetime import datetime, timedelta

MIN_SPEED = {
    200: 15,
    400: 15,
    600: 15,
    1000: 11.428,
    1300: 13.333,
}
MAX_SPEED = {
    200: 34,
    400: 32,
    600: 30,
    1000: 28,
    1300: 26,
}

#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#
# Define the minimum and maximum speeds for different brevet distances

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """

    #Edge cases
    if (control_dist_km > brevet_dist_km):
      control_dist_km = brevet_dist_km

    if (control_dist_km == 0):
      return brevet_start_time

    min_time = timedelta(hours=brevet_dist_km / MAX_SPEED[min(MAX_SPEED.keys(), key=lambda x: abs(x - brevet_dist_km))])
        
    # Calculate the time allowed for the control point based on the distance
    if control_dist_km <= brevet_dist_km * 1.1:
        time_allowed = min_time * (control_dist_km / brevet_dist_km / 1.1)
    elif control_dist_km <= brevet_dist_km * 1.2:
        time_allowed = min_time * (1 + (control_dist_km - brevet_dist_km * 1.1) / (brevet_dist_km * 0.2))
    else:
        time_allowed = min_time * (1 + 0.1 + (control_dist_km - brevet_dist_km * 1.2) / (brevet_dist_km * 0.3))

    # Calculate the opening time for the control point
    opening_time = brevet_start_time + time_allowed

    return opening_time

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """

    #Edge cases

    if (control_dist_km == 0):
      return brevet_start_time

    # Calculate the maximum time allowed for the control point
    max_time = timedelta(hours=brevet_dist_km / MIN_SPEED[min(MAX_SPEED.keys(), key=lambda x: abs(x - brevet_dist_km))])

    # Calculate the time allowed for the control point based on the distance
    if control_dist_km <= brevet_dist_km * 1.1:
        time_allowed = max_time * (control_dist_km / brevet_dist_km / 1.1)
    elif control_dist_km <= brevet_dist_km * 1.2:
        time_allowed = max_time * (1 + (control_dist_km - brevet_dist_km * 1.1) / (brevet_dist_km * 0.2))
    else:
        time_allowed = max_time * (1 + 0.1 + (control_dist_km - brevet_dist_km * 1.2) / (brevet_dist_km * 0.3))

    # Calculate the opening time for the control point
    closing_time = brevet_start_time + time_allowed

    return closing_time