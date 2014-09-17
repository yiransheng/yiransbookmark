import logging
from time import mktime
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor

from settings import PAGE_SIZE

def to_epoch(value):
    """
    This is a view method to return the data in milli-seconds.

        :param value: Instance of `datetime.datetime`.
        :returns: `float` as the number of seconds since unix epoch.
    """
    return int(mktime(value.utctimetuple()) * 1000)


def from_epoch(value):
    """
        :param value:
            Instance of `float` as the number of seconds since unix epoch.
        :returns:
            Instance of `datetime.datetime`.
    """
    return datetime.utcfromtimestamp(value / 1000)


class Link(ndb.Model):
    id = ndb.ComputedProperty(lambda self: self.key.id() if self.key else None)
    title = ndb.StringProperty(required=True, indexed=False)
    body = ndb.TextProperty(required=False, indexed=False)
    url = ndb.StringProperty(required=True, indexed=False)
    domain = ndb.StringProperty(required=True, indexed=False)
    created_at = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
    unread = ndb.BooleanProperty(required=True, default=True)
    tags = ndb.StringProperty(repeated=True)
    clicks = ndb.IntegerProperty(default=0)

    @classmethod
    def get_by_id(cls, id):
        try:
            return ndb.Key(cls, id).get()
        except:
            return None

    @classmethod
    def get_all_links(cls, cursor=None):
        q = cls.query().order(-cls.created_at)
        cursor = Cursor(urlsafe=cursor) if cursor else None
        return q.fetch_page(PAGE_SIZE, start_cursor=cursor)


    def to_dict(self, includes=None, excludes=None):
      """Encodes an `ndb.Model` to a `dict`. By default, only `ndb.Property`
      attributes are included in the result.

          :param include:
              List of strings keys of class attributes. Can be the name of the
              either a method or property.
          :param exclude:
              List of string keys to omit from the return value.
          :returns: Instance of `dict`.
          :raises: `ValueError` if any key in the `include` param doesn't exist.
      """
      value = ndb.Model.to_dict(self)
      value['created_at'] = to_epoch(value['created_at'])
      # set the `id` of the entity's key by default..
      # if self.key:
      #    value['key'] = self.key.urlsafe()
      #    value['id'] = self.key.id()
      if includes:
          for inc in includes:
              attr = getattr(self, inc, None)
              if attr is None:
                  cls = self.__class__
                  logging.warn('entity_to_dict cannot encode `%s`. Property is \
  not defined on `%s.%s`.', inc, cls.__module__, cls.__name__)
                  continue
              if callable(attr):
                  value[inc] = attr()
              else:
                  value[inc] = attr
      if excludes:
          # exclude items from the result dict, by popping the keys
          # from the dict..
          [value.pop(exc) for exc in excludes
              if exc in value]
      return value

