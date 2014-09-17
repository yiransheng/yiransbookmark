class Error(Exception):
  """Base error type."""

  def __init__(self, error_message):
    self.error_message = error_message


class NotFoundError(Error):
  """Raised when necessary entities are missing."""


class OperationFailedError(Error):
  """Raised when necessary operation has failed."""
