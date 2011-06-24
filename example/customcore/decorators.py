try:
    from functools import update_wrapper, warps
except ImportError:
    from django.utils.functional import update_wrapper, wraps #Python 2.4 fallback
from inspect import getmodule    
    
from django.utils.hashcompat import md5_constructor as md5
from django.core.cache import cache

LOCK_EXPIRE = 60 * 5


def make_blocking(view_func):
    """Checks for a value in the cache to see if the current method is already
    called.
    
    .. note::
       Caching is required and should be shared by all processes.
       
    .. note::
       the lock_id is based on a hash of the args and kwargs and the namespace,
       method name. So a different set of arguments is enough to 'unblock'
       
    .. note::
       returns without doing much when the view_func is locked
    """
    
    
    blocking_id = getmodule(view_func).__name__ + '.' + view_func.func_name 
  
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        method = unicode(args)+unicode(kwargs)
        digest = md5(method).hexdigest()
    
        lock_id = "%s-lock-%s" % (blocking_id, digest)
        
        acquire_lock = lambda : cache.add(lock_id, 'true', LOCK_EXPIRE)
        
        release_lock = lambda : cache.delete(lock_id)
        
        if acquire_lock():
            value = cache.get(lock_id)
            try:
                value = view_func(*args, **kwargs)
            finally:
                release_lock()
                return value
       
    
    return _wrapped_view
