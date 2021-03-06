# -*- coding: utf-8 -*-

#    Copyright 2015 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock
from six import StringIO

from fuelclient.cli.actions import node
from fuelclient.tests.unit.v1 import base


GRAPH_API_OUTPUT = "digraph G { A -> B -> C }"
TASKS_API_OUTPUT = [
    {'id': 'primary-controller'},
    {'id': 'sync-time'},
]


class TestNodeStartAction(base.UnitTestCase):

    @mock.patch.object(node.NodeAction, 'get_env_id', return_value=None)
    def test_node_not_assigend(self, _):
        for method in ('--deploy', '--provision'):
            with mock.patch('sys.stderr', new=StringIO()) as mstderr:
                self.assertRaises(SystemExit,
                                  self.execute,
                                  ['fuel', 'node', method, '--node', '8'])
                self.assertIn(
                    "Input nodes are not assigned to any environment!",
                    mstderr.getvalue())
