#!/usr/bin/env python3
#
# Copyright (C) 2016 Savoir-faire Linux Inc
#
# Author:  Seva Ivanov <seva.ivanov@savoirfairelinux.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA.
#
import argparse
from ring_api import client

if __name__ == "__main__":
    parser = client.options_parser(
        desc='RESTful API of the Ring-daemon',
        force_rest=True
    )
    ring_opts = parser.parse_args()
    ring_api = client.Client(ring_opts)
    ring_api.start()