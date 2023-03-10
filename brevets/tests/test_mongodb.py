import nose
import logging
import arrow
from mongodbpy import insert_brevet, get_brevet

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

def test_insert():
    start_time = arrow.get("2023-02-17 00:00", "YYYY-MM-DD HH:mm")
    dist = 200
    checkpoints = {
        0:   (start_time, start_time.shift(hours=1)),
        50:  (start_time.shift(hours=1, minutes=28), start_time.shift(hours=3.5)),
        150: (start_time.shift(hours=4, minutes=25), start_time.shift(hours=10)),
        200: (start_time.shift(hours=5, minutes=53), start_time.shift(hours=13.5))
    }
    insert_check = insert_brevet(dist, start_time, checkpoints)
    assert isinstance(insert_check, str)

def test_get():
    start_time = arrow.get("2023-02-17 00:00", "YYYY-MM-DD HH:mm")
    dist = 200
    checkpoints = {
        0:   (start_time, start_time.shift(hours=1)),
        50:  (start_time.shift(hours=1, minutes=28), start_time.shift(hours=3.5)),
        150: (start_time.shift(hours=4, minutes=25), start_time.shift(hours=10)),
        200: (start_time.shift(hours=5, minutes=53), start_time.shift(hours=13.5))
    }
    insert_check = insert_brevet(dist, start_time, checkpoints)

    fetch = get_brevet()
    assert isinstance(fetch, str)