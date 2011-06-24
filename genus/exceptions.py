#from exceptions import IOError



class GenusTransportError(IOError):
    """IOError subclass to show Genus specific errors. More specific and easier
    to catch
    """
    
    def __init__(self, msg, status, *args, **kwargs):
        self.msg = msg
        self.status = status


        
        super(GenusTransportError, self).__init__(*args, **kwargs)
	#logger.exception(
        
    def __str__(self):
        import logging
        import sys, traceback

        serialized = u'GenusTransportError occured, with '+ unicode(self.msg)\
                + u' status: ' + unicode(self.status)

#        logger = logging.getLogger()
#        logger.warn(serialized, extra={
#		'stack': ''.join(traceback.format_exception(*sys.exc_info()))
#	})
        return serialized
              
        
