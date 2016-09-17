"""
    catalist.api
    ~~~~~~~~~~~~

    This module implements our web app's API. All operations
    we'll probably need are here (however poorly written they
    may be). Relevant permissions are required everywhere.

    :copyright: (c) 2016 Rachel Wu, Tony Zhang
    :license: lol don't steal this code
"""

# Good luck brought to you by Safety Pig
# http://qr.ae/RgLMU8
#
#                          _
#  _._ _..._ .-',     _.._(`))
# '-. `     '  /-._.-'    ',/
#    )         \            '.
#   / _    _    |             \
#  |  a    a    /              |
#  \   .-.                     ;
#   '-('' ).-'       ,'       ;
#      '-;           |      .'
#         \           \    /
#         | 7  .__  _.-\   \
#         | |  |  ``/  /`  /
#        /,_|  |   /,_/   /
#           /,_/      '`-'
#
#           http://www.asciiworld.com/-Mangas,48-.html
#                   and T O T O R O <3
#                           ~ t o t o r o ~
#
#                              !         !
#                             ! !       ! !
#                            ! . !     ! . !
#                               ^^^^^^^^^ ^
#                             ^             ^
#                           ^  (0)       (0)  ^
#                          ^        ""         ^
#                         ^   ***************    ^
#                       ^   *                 *   ^
#                      ^   *   /\   /\   /\    *    ^
#                     ^   *                     *    ^
#                    ^   *   /\   /\   /\   /\   *    ^
#                   ^   *                         *    ^
#                   ^  *                           *   ^
#                   ^  *                           *   ^
#                    ^ *                           *  ^
#                     ^*                           * ^
#                      ^ *                        * ^
#                      ^  *                      *  ^
#                        ^  *       ) (         * ^
#                            ^^^^^^^^ ^^^^^^^^^

from flask import Flask, render_template, jsonify, \
    request, redirect, url_for, make_response, Blueprint
from flask.ext.security import Security, login_required
import flask.ext.security as flask_security
from flask.ext.mongoengine import *

from datetime import datetime, date, timedelta
import uuid as uuid_module

from permissions import *
from database import Role, User, Catalist, CatalistEntry, CatalistKVP
import database as dbase
from views import get_id

# **********************************************************
# THE API!!!
# **********************************************************

api_blueprint = Blueprint('api', __name__)

# # # # # # # # # # # # # #
# EXCEPTION HANDLING
# # # # # # # # # # # # # #


class InvalidAPIUsage(Exception):
    """
    A class for exceptions to raise in invalid API usage.
    Shamelessly pillaged from `Flask's documentation
    <http://flask.pocoo.org/docs/0.10/patterns/apierrors/>`_
    """
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@api_blueprint.errorhandler(InvalidAPIUsage)
def handle_invalid_usage(error):
    print("\033[93m{} -- {}\033[0m".format(error.status_code, error.message))
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response



@api_blueprint.route("/similarity", methods=['GET'])
def query_similarity():
    """
    sdfs
    """
    image_uuid = request.form["image-uuid"]
    if image_uuid not in uuid_set:
        raise InvalidAPIUsage("Invalid image ID", status_code=400)

    adjective = request.form["adjective"]
    if not adjective.isalnum():
        raise InvalidAPIUsage("Adjective must be alphanumeric", status_code=400)


    if adjective not in cache:
        train(adjective)
    similarity = derpy_conv_net.predict("tmp/{}".format(image_uuid))
    return jsonify(adjectiveness=similarity)

