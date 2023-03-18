"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)
"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
from mongodbpy import insert_brevet, get_brevet
import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############

@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    

    brevet_dist_km = request.args.get("brevet_dist_km", 999, type=float)
    start_time = request.args.get("start_time", type=str)
    start_time = arrow.get(start_time, "YYYY-MM-DDTHH:mm")
    app.logger.debug("km={}".format(km))
    app.logger.debug("start_time={}".format(start_time))
    app.logger.debug("brevet_dist_km={}".format(brevet_dist_km))
    app.logger.debug("request.args: {}".format(request.args))

    # FIXME!
    # Right now, only the current time is passed as the start time
    # and control distance is fixed to 200
    # You should get these from the webpage!
    open_time = acp_times.open_time(km, brevet_dist_km, start_time).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, brevet_dist_km, start_time).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

@app.route("/insert", methods=["POST"])
def insert():
    try:
        input_json = request.json
        brevet_dist_km = input_json["brevet_dist_km"] # Should be a string
        start_time = input_json["start_time"] # Should be a string
        checkpoints = input_json["checkpoints"] # Should be a list of dictionaries


        return flask.jsonify(result={},
                        message="Inserted!", 
                        status=1,
                        mongo_id=insert_brevet(brevet_dist_km, start_time, checkpoints))
    except:
        return flask.jsonify(result={},
                        message="Oh no! Server error!", 
                        status=0, 
                        mongo_id='None')
    
@app.route("/fetch_brevet")
def fetch_brevet():
    try:
        brevet_dist_km, start_time, checkpoints = get_brevet()
        return flask.jsonify(
                result={"brevet_dist_km": brevet_dist_km, "start_time": start_time, "checkpoints": checkpoints}, 
                status=1,
                message="Successfully fetched a brevet list!")
    except:
        return flask.jsonify(
                result={}, 
                status=0,
                message="Something went wrong, couldn't fetch any lists!")

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
