"""
    server.views
    ~~~~~~~~~~~~~~

    This module contains most of the views (read: non-error views)
    for our web app.

    :copyright: (c) 2016 whatever
    :license: lol don't steal this code pls
"""

from flask import render_template, request
from datetime import datetime, date, timedelta

from server import app, HOSTNAME


# **********************************************************
# User Interaction Section
# **********************************************************


@app.route("/list/<listid>", methods=['GET'])
def getlist(listid):
    """ Display a list with given listid from our database. """
    url = request.base_url
    try:
        the_list = Catalist.objects.get(listid=listid)
    except DoesNotExist:
        abort(404)
    if cmp_permission(query_cur_perm(the_list), "view") < 0:
        abort(403)
    msg = ('Access or share this list at:<br>'
           '<input type="url" id="listurl" value={0}>').format(url)

    return render_template('loadlist.html', listtitle=the_list.title,
                           entries=the_list.contents, message=msg)


def human_readable_time_since(tiem):
    """
    Give a human-readable representation of time elapsed since a given time

    :param tiem: a :attr:`datetime` object representing the given time.
    """
    now = datetime.utcnow()
    then = tiem
    delta = now - then  # in units of seconds

    # >10 days ago: just display the date instead.
    if delta.days > 10:
        yearQ = (then.timetuple()[0] != now.timetuple()[0])
        if yearQ:
            return then.strftime("%-* %Y %b %d")  # format as '1776 Jul 4'
        else:
            return then.strftime("%-* %b %d")  # format as 'Jul 4'

    # resolution should be in days if within [1, 10] days
    if delta.days > 0:
        return "{} day{} ago".format(delta.days,
                                     '' if delta.days == 1 else 's')

    secs = delta.seconds
    if secs < 60:
        return "just now"
    mins = secs / 60
    if mins < 60:
        return "{} minute{} ago".format(mins, '' if mins == 1 else 's')
    hrs = mins / 60
    return "{} hour{} ago".format(hrs, '' if hrs == 1 else 's')


app.jinja_env.globals.update(
    human_readable_time_since=human_readable_time_since)



@app.route("/preview/<listid>", methods=['GET'])
def preview_list(listid):
    """
    Fetch the list with given listid from our database,
    display with template
    """
    the_list = Catalist.objects.get(listid=listid)
    if cmp_permission(query_cur_perm(the_list), "view") < 0:
        abort(403)
    return render_template('preview.html', listtitle=the_list.title,
                           entries=the_list.contents)


@app.route("/about", methods=['GET', 'POST'])
def about():
    """ About us. """
    return render_template('about.html')


@app.route("/", methods=['GET', 'POST'])
def index():
    """ Our homepage! """
    return render_template('home.html')
