import webapp2
import re
import logging

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from docs import Link

class BuildLinkFromEmail(InboundMailHandler):
  URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
    r'localhost|' # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

  def receive(self, message):
    plaintext_bodies = message.bodies('text/plain')
    subject = message.subject
    body = ""
    for plaintext_body in plaintext_bodies:
      body = body + plaintext_body[1].decode()

    link, summary, tags = BuildLinkFromEmail.parse_body(body)
    if link != None:
      Link.save_link(subject, link, summary, tags)

  @classmethod
  def parse_body(cls, body):
    lines = body.splitlines()
    summary = ""
    first = True
    link = None
    tags = []
    for line in lines:
      line_len = len(line)
      if line_len >0 and cls.is_url(line):
        link = line
      elif line_len>4 and line.startswith("[["):
        line = line.split(']]')[0]
        line = line[2:line_len-1]
        tags = line.split(",")
        tags = map(lambda x: x.strip(), tags)
      elif line_len>0:
        summary = summary + ("" if first else "\n") + line
        if first:
          first = False

    return link, summary, tags

  @classmethod
  def is_url(cls, str):
    str = str.strip()
    return cls.URL_REGEX.match(str) != None


app = webapp2.WSGIApplication([BuildLinkFromEmail.mapping()], debug=True)
