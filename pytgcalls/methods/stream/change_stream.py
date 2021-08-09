import json
import os

import requests

from ..core import SpawnProcess


class ChangeStream(SpawnProcess):
    def __init__(self, pytgcalls):
        self.pytgcalls = pytgcalls

    # noinspection PyProtectedMember
    def change_stream(self, chat_id: int, file_path: str):
        js_core_state = self.pytgcalls.is_running_js_core()
        if (
            self.pytgcalls._app is not None and
            os.path.isfile(file_path)
        ):
            if js_core_state:
                self._spawn_process(
                    requests.post,
                    (
                        'http://'
                        f'{self.pytgcalls._host}:'
                        f'{self.pytgcalls._port}/'
                        'api_internal',
                        json.dumps({
                            'action': 'change_stream',
                            'chat_id': chat_id,
                            'file_path': file_path,
                            'session_id': self.pytgcalls._session_id,
                        }),
                    ),
                )
            else:
                self.pytgcalls._waiting_start_request.append([
                    self.change_stream,
                    (
                        chat_id,
                        file_path,
                    )
                ])
        else:
            code_err = 'PYROGRAM_CLIENT_IS_NOT_RUNNING'
            if not os.path.isfile(file_path):
                code_err = 'FILE_NOT_FOUND'
            raise Exception(f'Error internal: {code_err}')
