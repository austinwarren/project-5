"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow
#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
        control_dist_km: number, control distance in kilometers
        brevet_dist_km: number, nominal distance of the brevet
            in kilometers, which must be one of 200, 300, 400, 600,
            or 1000 (the only official ACP brevet distances)
        brevet_start_time: An arrow object

    Returns:
        An arrow object indicating the control open time.
        This will be in the same time zone as the brevet start time.
    """
    minutes = 0
    i = 0
    speed1 = [(200, 200, 34), (400, 200, 32), (600, 200, 30), (1000, 400, 28), (1300, 300, 26)]

    # If the control distance is greater than the brevet distance,
    # set the control distance to the brevet distance.
    if brevet_dist_km < control_dist_km:
        control_dist_km = brevet_dist_km

    while i < len(speed1) and control_dist_km > speed1[i][0]:
        for dist, x, maximum in speed1:
            minutes += (x / maximum) * 60
        i += 1

    if i < len(speed1):
        dist, x, maximum = speed1[i]
        minutes += ((control_dist_km - (dist - x)) / maximum) * 60

    rounded = round(minutes)
    return brevet_start_time.shift(minutes=rounded)



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
    minutes = 0
    i = 0
    speed2 = [(600,600,15),(1000,400,11.428),(1300,300,13.333)]

    if brevet_dist_km < control_dist_km:
        control_dist_km = brevet_dist_km

    speed2_iter = iter(speed2)

    while True:
        try:
            dist, x, maximum = next(speed2_iter)
        except StopIteration:
            if control_dist_km > x:
                minutes += round(((control_dist_km - x) / maximum) * 60)
            break
        
        if control_dist_km > dist:
            minutes += (x / maximum) * 60
        elif control_dist_km <= 60:
            minutes += ((control_dist_km/20) + 1) * 60
            break
        else:
            minutes += ((control_dist_km - (dist - x)) / maximum) * 60
            break
        
    rounded = round(minutes)
    return brevet_start_time.shift(minutes=rounded)