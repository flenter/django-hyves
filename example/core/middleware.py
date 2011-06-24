P3P_COMPACT = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"' 

class MiddlewareResponseInjectP3P(object):
    """Middleware to allow setting of cookies from iframes (served from a 
    different domain than the 'host' page. (this is needed for some versions 
    of internet explorer)

    Note: this does make safari/webkit accept cookies 
    """
    def __init__(self):
        self.process_response = self.inject

    def inject(self, request, response):
        response['P3P'] = P3P_COMPACT
        return response
