import collections
import copy
import datetime
import logging
import re
import string
import urllib
import errors

from urlparse import urlparse

from google.appengine.ext import ndb
from model import Link as LinkModel

from google.appengine.api import search
from google.appengine.ext import ndb

class BaseDocumentManager(object):
  """Abstract class. Provides helper methods to manage search.Documents."""

  _INDEX_NAME = None
  _VISIBLE_PRINTABLE_ASCII = frozenset(
    set(string.printable) - set(string.whitespace))

  def __init__(self, doc, model):
    """Builds a dict of the fields mapped against the field names, for
    efficient access.
    """
    self.doc = doc
    self.model = model if model else None
    fields = doc.fields


  def getFieldVal(self, fname):
    """Get the value of the document field with the given name.  If there is
    more than one such field, the method returns None."""
    try:
      return self.doc.field(fname).value
    except ValueError:
      return None

  def setFirstField(self, new_field):
    """Set the value of the (first) document field with the given name."""
    for i, field in enumerate(self.doc.fields):
      if field.name == new_field.name:
        self.doc.fields[i] = new_field
        return True
    return False

  def setAllFields(sself, new_fields):
    """Set the value of the (first) document field with the given name."""
    for i, field in enumerate(self.doc.fields):
        self.doc.fields[i] = new_fields[i]

  @classmethod
  def isValidDocId(cls, doc_id):
    """Checks if the given id is a visible printable ASCII string not starting
    with '!'.  Whitespace characters are excluded.
    """
    for char in doc_id:
      if char not in cls._VISIBLE_PRINTABLE_ASCII:
        return False
    return not doc_id.startswith('!')

  @classmethod
  def getIndex(cls):
    return search.Index(name=cls._INDEX_NAME)

  @classmethod
  def deleteAllInIndex(cls):
    """Delete all the docs in the given index."""
    docindex = cls.getIndex()

    try:
      while True:
        # until no more documents, get a list of documents,
        # constraining the returned objects to contain only the doc ids,
        # extract the doc ids, and delete the docs.
        document_ids = [document.doc_id
                        for document in docindex.get_range(ids_only=True)]
        if not document_ids:
          break
        docindex.delete(document_ids)
    except search.Error:
      logging.exception("Error removing documents:")

  @classmethod
  def getDoc(cls, doc_id):
    """Return the document with the given doc id. One way to do this is via
    the get_range method, as shown here.  If the doc id is not in the
    index, the first doc in the index will be returned instead, so we need
    to check for that case."""
    if not doc_id:
      return None
    try:
      index = cls.getIndex()
      response = index.get_range(
          start_id=doc_id, limit=1, include_start_object=True)
      if response.results and response.results[0].doc_id == doc_id:
        return response.results[0]
      return None
    except search.InvalidRequest: # catches ill-formed doc ids
      return None

  @classmethod
  def removeDocById(cls, doc_id):
    """Remove the doc with the given doc id."""
    try:
      cls.getIndex().delete(doc_id)
    except search.Error:
      logging.exception("Error removing doc id %s.", doc_id)

  @classmethod
  def add(cls, documents):
    """wrapper for search index add method; specifies the index name."""
    try:
      return cls.getIndex().put(documents)
    except search.Error:
      logging.exception("Error adding documents.")


class Link(BaseDocumentManager):

    _INDEX_NAME = "LinkIndex"
    ID = "id"
    TITLE = "title"
    TAGS = "tags"
    CLICKS = "clicks"
    BODY = "body"
    DOMAIN = "domain"

    @classmethod
    def _buildFields(cls, id, title, body, domain, tags):
        fields = [
            search.TextField(name=cls.ID, value=id),
            search.TextField(name=cls.TITLE, value=title),
            search.AtomField(name=cls.DOMAIN, value=domain),
            search.TextField(name=cls.TAGS, value=" ".join(tags)),
            search.TextField(name=cls.BODY, value=body)
        ]
        return fields

    @classmethod
    def _buildDoc(cls, id, title, body, domain, tags=[]):
        if id and title:
            fields = cls._buildFields(id, title, body, domain, tags)
            doc = search.Document(doc_id = id, fields = fields)
            return doc
        raise errors.OperationFailedError('Missing fields value, when creating document')

    @classmethod
    def save_link(cls, title, url, body="", tags=[], clicks=0, unread=True):
        if not isinstance(url, str): # convert unicode to ascii for key generation purpose
          ascii_url = url.encode('ascii', 'xmlcharrefreplace')
        else:
          ascii_url = url
        key = ndb.Key(LinkModel, ascii_url)
        domain = urlparse(url).netloc
        if len(domain)>4 and domain.startswith('www.'):
            domain = domain[4:]
        link = LinkModel( key = key,
                          title = title,
                          url = url,
                          domain = domain,
                          body = body,
                          tags = tags,
                          clicks = clicks,
                          unread = unread )
        link.put()
        id = str(link.id)
        doc = cls._buildDoc(id, title, body, domain, tags)
        cls.add(doc)
        return cls(doc, link)

    @classmethod
    def delete_link(cls, id):
        link = LinkModel.get_by_id(id)
        if link:
            link.key.delete()
        linkDoc = cls.getDoc(id)
        if linkDoc:
            cls.removeDocById(id)

    @classmethod
    def search(cls, query_string):
      try:
        sq = search.Query(query_string=query_string.strip())
        results = cls.getIndex().search(sq)
      except search.Error:
        return []

      return [result.doc_id for result in results]


