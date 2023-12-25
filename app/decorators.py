from functools import wraps

from .rest.models import UserTable

def admin_role(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    return func(*args, **kwargs)
  return wrapper