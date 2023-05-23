import json
import logging
import time
from typing import Callable, Any

import requests

from wxcloudrun.common.exceptions import ExternalServerException, HttpRequestException

logger = logging.getLogger('log')


def exponential_backoff_retry(delay: int, max_retries: int, func: Callable[..., dict], **kwargs) -> dict:
    retries = 1
    while retries < max_retries:
        try:
            return func(**kwargs)
        except Exception:
            if retries == max_retries:
                break
            else:
                time.sleep(delay)
                delay *= 2
                retries += 1


def _request(log_prefix, method, url, **kwargs) -> dict:
    # Send the POST request
    response = requests.request(method, url, **kwargs)

    # Check the status code
    if response.status_code == 200:
        response_json = json.loads(response.content)

        if response_json['code'] != 0:
            error_msg = f'{log_prefix} ExternalServerException, ' \
                        f'code: {response_json["code"]}, ' \
                        f'msg: {response_json["msg"]}'
            logger.error(error_msg)
            raise ExternalServerException(error_msg)

        return response_json

    else:
        error_msg = f'{log_prefix} HttpRequestException, ' \
                    f'status_code: {response.status_code}, ' \
                    f'content: {response.content}'
        logger.error(error_msg)
        raise HttpRequestException(error_msg)


class FeishuHttpClient(object):

    @staticmethod
    def request(log_prefix, method, url, **kwargs) -> dict:
        return exponential_backoff_retry(1, 3, _request,
                                         log_prefix=log_prefix, method=method, url=url, **kwargs)
