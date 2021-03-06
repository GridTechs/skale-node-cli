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
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import click
from terminaltables import SingleTable

from core.helper import get, safe_load_texts, upload_certs


TEXTS = safe_load_texts()


@click.group()
def ssl_cli():
    pass


@ssl_cli.group('ssl', help="sChains SSL commands")
def ssl():
    pass


@ssl.command(help="Status of the SSL certificates on the node")
def status():
    result = get('ssl_status')
    if not result:
        return
    if not result['status']:
        print(TEXTS['ssl']['no_cert'])
    else:
        table_data = [
            ['Issued to', result['issued_to']],
            ['Expiration date', result['expiration_date']]
        ]
        table = SingleTable(table_data)
        print('SSL certificates status:')
        print(table.table)


@ssl.command(help="Upload new SSL certificates")
@click.option(
    '--key-path', '-k',
    prompt="Enter path to the key file",
    help='Path to the key file'
)
@click.option(
    '--cert-path', '-c',
    prompt="Enter path to the certificate file",
    help='Path to the certificate file'
)
@click.option('--force', '-f', is_flag=True, help='Overwrite existing certificates')
def upload(key_path, cert_path, force):
    response = upload_certs(key_path, cert_path, force)
    if not response:
        print('Someting went wrong, sorry')
        return
    if response['res'] == 0:
        print(response['error_msg'])
        return
    print(TEXTS['ssl']['uploaded'])
