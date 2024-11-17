class NoDataError(Exception):
    def __init__(self, url):
        message = f"API did returned any result for this URL ---> {url}"
        super().__init__(message)


class NetworkError(Exception):
    def __init__(self, req):
        message=F"Issue with network while accessing API -- "
        super().__init__(message)
    pass

 