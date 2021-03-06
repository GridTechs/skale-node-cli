#   -*- coding: utf-8 -*-
#
#   This file is part of skale-node-cli
#
#   Copyright (C) 2019 SKALE Labs
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import mock
import requests

from tests.helper import response_mock, run_command_mock
from cli.node import (register_node, init_node, purge_node, update_node,
                      node_about, node_info)


def test_register_node(config):
    result = run_command_mock(
        'core.node.post',
        {'res': 1},
        register_node,
        ['--name', 'test-node', '--ip', '0.0.0.0', '--port', '8080'])
    assert result.exit_code == 0
    assert result.output == 'Node registered in SKALE manager.\nFor more info run < skale node info >\n'  # noqa

    result = run_command_mock(
        'core.node.post',
        {'errors': ['Strange error']},
        register_node,
        ['--name', 'test-node2', '--ip', '0.0.0.0', '--port', '80'])
    assert result.exit_code == 0
    assert result.output == "Node registration failed with error: ['Strange error']\n"


def test_register_node_with_prompted_ip(config):
    result = run_command_mock(
        'core.node.post',
        {'res': 1},
        register_node,
        ['--name', 'test-node', '--port', '8080'], input='0.0.0.0\n')
    assert result.exit_code == 0
    assert result.output == 'Enter node public IP: 0.0.0.0\nNode registered in SKALE manager.\nFor more info run < skale node info >\n'  # noqa


def test_register_node_with_default_port_and_name(config):
    result = run_command_mock(
        'core.node.post',
        {'res': 1},
        register_node,
        input='0.0.0.0\n')
    assert result.exit_code == 0
    assert result.output == 'Enter node public IP: 0.0.0.0\nNode registered in SKALE manager.\nFor more info run < skale node info >\n'  # noqa


def test_init_node(config):
    resp_mock = response_mock(requests.codes.created)
    with mock.patch('subprocess.run'), \
            mock.patch('cli.node.install_host_dependencies'), \
            mock.patch('core.node.prepare_host'), \
            mock.patch('core.host.init_data_dir'):
        result = run_command_mock(
            'core.node.post',
            resp_mock,
            init_node,
            ['--env-file', './tests/test-env'])
        assert result.exit_code == 0
        assert result.output == ''  # noqa


def test_purge(config):
    params = ['--yes']
    resp_mock = response_mock(requests.codes.created)
    with mock.patch('core.node.subprocess.run'):
        result = run_command_mock(
            'core.node.post',
            resp_mock,
            purge_node,
            params
        )
        assert result.exit_code == 0
        assert result.output == ''  # noqa


def test_update_node(config):
    params = ['--env-file', './tests/test-env', '--yes']
    resp_mock = response_mock(requests.codes.created)
    with mock.patch('subprocess.run'), \
            mock.patch('cli.node.install_host_dependencies'), \
            mock.patch('core.node.get_flask_secret_key'), \
            mock.patch('core.node.save_env_params'), \
            mock.patch('core.host.init_data_dir'):
        result = run_command_mock(
            'core.node.post',
            resp_mock,
            update_node,
            params,
            input='/dev/sdp')
        assert result.exit_code == 0
        assert result.output == ''


def test_node_info_node_about(config):
    response_data = {
        'libraries': {
            'javascript': 'N/A', 'python': '0.89.0'},
        'contracts': {
            'token': '0x3',
            'manager': '0x23'
        },
        'network': {
            'endpoint': 'ws://0.0.0.0:8080'
        },
        'local_wallet': {
            'address': '0xf',
            'eth_balance_wei': '15',
            'skale_balance_wei': '84312304',
            'eth_balance': '2.424',
            'skale_balance': '323.123'
        }
    }
    resp_mock = response_mock(
        requests.codes.ok,
        json_data={'data': response_data, 'res': 1}
    )
    result = run_command_mock('core.core.get_request', resp_mock, node_about)
    assert result.exit_code == 0
    assert result.output == "{'libraries': {'javascript': 'N/A', 'python': '0.89.0'}, 'contracts': {'token': '0x3', 'manager': '0x23'}, 'network': {'endpoint': 'ws://0.0.0.0:8080'}, 'local_wallet': {'address': '0xf', 'eth_balance_wei': '15', 'skale_balance_wei': '84312304', 'eth_balance': '2.424', 'skale_balance': '323.123'}}\n"  # noqa


def test_node_info_node_info(config):
    response_data = {'name': 'test', 'ip': '0.0.0.0',
                     'publicIP': '1.1.1.1',
                     'port': 10001,
                     'publicKey': '0x7',
                     'start_date': 1570114466,
                     'leaving_date': 0,
                     'last_reward_date': 1570628924, 'second_address': 0,
                     'status': 2, 'id': 32, 'owner': '0x23'}

    resp_mock = response_mock(
        requests.codes.ok,
        json_data={'data': response_data, 'res': 1}
    )
    result = run_command_mock('core.core.get_request', resp_mock, node_info)
    assert result.exit_code == 0
    assert result.output == '--------------------------------------------------\nNode info\nName: test\nIP: 0.0.0.0\nPublic IP: 1.1.1.1\nPort: 10001\nStatus: Active\n--------------------------------------------------\n'  # noqa
