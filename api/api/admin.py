"""
API functions relating to admin users.
"""

import pymongo
import api

from api.common import check, validate, safe_fail
from api.common import WebException, InternalException
from api.annotations import log_action

def give_admin_role(name=None, uid=None):
    """
    Give a particular user admin privileges.
    There is no option to give a particular user admin privileges by default.

    Args:
        name: the user's name
        uid: the user's id
    """

    db = api.common.get_conn()

    user = api.user.get_user(name=name, uid=uid)
    db.users.update({"uid": user["uid"]}, {"$set": {"admin": True}})

def set_problem_availability(pid, enabled):
    """
    Updates a problem's availability.

    Args:
        pid: the problem's pid
        disabled: whether or not the problem should be disabled.
    Returns:
        The updated problem object.
    """

    return api.problem.update_problem(pid, {"disabled": not(enabled)})

def get_api_exceptions(result_limit=50, sort_direction=pymongo.DESCENDING):
    """
    Retrieve api exceptions.

    Args:
        result_limit: the maximum number of exceptions to return.
        sort_direction: pymongo.ASCENDING or pymongo.DESCENDING
    """

    db = api.common.get_conn()

    results = db.exceptions.find().sort([("time", sort_direction)]).limit(result_limit)
    return list(results)
