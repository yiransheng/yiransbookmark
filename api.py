from functools import wraps
from hashlib import sha1
from flask import render_template, request, Response, Flask, flash, redirect, url_for, abort, jsonify
import re
from unicodedata import normalize
import datetime, time
from unicodedata import normalize
import markdown

from google.appengine.api import users


from model import Link as L
from docs import Link
from query import to_query_string

app = Flask(__name__)
app.config.from_object('settings')

@app.errorhandler(404)
def page_not_found(e):
  return jsonify(error=404, message="404 Not Found"), 404


@app.errorhandler(500)
def server_error(e):
  return jsonify(error=500, message="500 Internal Error"), 500

def requires_authentication(f):
    @wraps(f)
    def _auth_decorator(*args, **kwargs):
        if not users.is_current_user_admin():
            return jsonify(url=users.create_login_url(request.url))

        return f(*args, **kwargs)

    return _auth_decorator

@app.route("/api/v1/link", methods=["GET"])
def get_all_links():
  next_page_cur = request.args.get('next')
  links, cursor, more = L.get_all_links(next_page_cur)
  if len(links):
    links = [l.to_dict() for l in links]
    return jsonify(size=len(links), \
                   data=links, \
                   next=cursor.urlsafe() if more else None, \
                   more=more)
  else:
    return jsonify(size=0, data=[], next=None, more=False)

@app.route("/api/v1/search/link", methods=["GET"])
def search_link():
  query = request.args.get('query')
  if not query:
    return jsonify(size=0, data=[])

  query_string = to_query_string(query)
  if query_string == '':
    return jsonify(size=0, data=[])

  ids = Link.search(query_string)
  if len(ids):
    links = map(lambda x:L.get_by_id(x), ids)
    links = [l.to_dict() for l in links]
    return jsonify(size = len(links), data=links)
  else:
    return jsonify(size=0, data=[])

@app.route("/api/v1/link/<id>", methods=["POST"])
@requires_authentication
def update_link(id):
  link = L.get_by_id(id)
  if link == None:
    return jsonify(success=False, message="No link exisit by id: "+str(id))
  title = request.form.get('title')
  body = request.form.get('body')
  unread = request.form.get('unread', type=bool)
  tags = request.form.getlist('tags')
  clicks = int(request.form.get('clicks'))
  if title != link.title or body != link.body or tags != link.tags:
    Link.save_link(title, link.url, body, tags, clicks, unread)
  elif unread != link.unread or clicks != link.clicks:
    link.unread = unread
    link.clicks = clicks
    link.put()

  return jsonify(success=True, size=1, data=link)

@app.route("/api/v1/link/<id>", methods=["DELETE"])
@requires_authentication
def delete_link(id):
  Link.delete_link(id)
