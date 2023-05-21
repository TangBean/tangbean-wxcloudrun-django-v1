class InvalidInputException(Exception):
    error_msg = 'Invaild input'


class HttpRequestException(Exception):
    def __init__(self, error_msg):
        super().__init__(f'HTTP request error, error msg: {error_msg}')


class ExternalServerException(Exception):
    def __init__(self, error_msg):
        super().__init__(f'External server error, error msg: {error_msg}')
