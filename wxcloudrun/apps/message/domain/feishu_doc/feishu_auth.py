import json
import logging
import requests

from wxcloudrun.apps.message.domain.chain_message.constants import FEISHU_TENANT_ACCESS_TOKEN_URL
from wxcloudrun.apps.message.models import ChainProject

logger = logging.getLogger('log')


class FeishuAuth(object):

    def __init__(self, project_name: str):
        self._project_name = project_name
        self._app_id, self._app_secret, self._folder_token = self._get_app_access()
        self._tenant_access_token = self._gen_tenant_access_token()

    @property
    def folder_token(self):
        return self._folder_token

    @property
    def tenant_access_token(self) -> str:
        return self._tenant_access_token

    def _get_app_access(self):
        chain_project = ChainProject.objects.filter(project_name=self._project_name).first()
        if chain_project is None:
            return None
        else:
            return chain_project.feishu_app_id, \
                chain_project.feishu_app_secret, \
                chain_project.feishu_folder_token

    def _gen_tenant_access_token(self) -> str:
        # Define the URL
        url = FEISHU_TENANT_ACCESS_TOKEN_URL

        # Define the data to be sent
        data = json.dumps({
            "app_id": self._app_id,
            "app_secret": self._app_secret
        })

        # Define the headers
        headers = {
            'Content-Type': 'application/json'
        }

        # Send the POST request
        response = requests.post(url, data=data, headers=headers)

        # Check the status code
        if response.status_code == 200:
            response_json = json.loads(response.content)
            return response_json['tenant_access_token']
        else:
            logger.error('FeishuAuth._call_feishu_tenant_access_token Error! status_code: %s',
                         response.status_code)
