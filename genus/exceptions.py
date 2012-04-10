"""Genus' own exceptions
"""

class GenusTransportError(IOError):
    """IOError subclass to show Genus specific errors. More specific and easier
    to catch
    """

    def __init__(self, msg, status, *args, **kwargs):
        self.msg = msg
        self.status = status

        super(GenusTransportError, self).__init__(*args, **kwargs)

    def __str__(self):
        """Format the string representation"""
        serialized = u'GenusTransportError occured, with '+ unicode(self.msg)\
                + u' status: ' + unicode(self.status)

        return serialized
