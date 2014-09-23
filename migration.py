import webapp2
from google.appengine.ext import deferred

from model import Link
from docs import Link as LinkDoc

def migrate():
    LinkDoc.deleteAllInIndex()
    q = Link.query()
    links = q.fetch(65535)
    for link in links:
        title = link.title
        url = link.url
        tags = link.tags
        body = link.body
        link.key.delete()
        LinkDoc.save_link(title, url, body, tags)


class UpdateHandler(webapp2.RequestHandler):
    def get(self):
        deferred.defer(migrate)
        self.response.out.write('Schema migration successfully initiated.')

app = webapp2.WSGIApplication([('/update_schema', UpdateHandler)])


