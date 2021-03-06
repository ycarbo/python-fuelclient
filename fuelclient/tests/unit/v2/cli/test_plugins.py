# -*- coding: utf-8 -*-
#
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
import tempfile

from fuelclient.tests.unit.v2.cli import test_engine
from fuelclient.tests.utils import fake_plugin


class TestPluginsCommand(test_engine.BaseCLITest):
    """Tests for fuel2 plugins * commands."""

    def setUp(self):
        super(TestPluginsCommand, self).setUp()
        self.name = 'fuel_plugin'
        self.version = '1.0.0'

        get_fake_plugins = fake_plugin.get_fake_plugins

        self.m_client.get_modified.return_value = get_fake_plugins(10)

    def test_plugin_list(self):
        args = 'plugins list'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('plugins', mock.ANY)
        self.m_client.get_all.assert_called_once_with()

    def test_plugin_list_sorted(self):
        args = 'plugins list -s name'
        self.exec_command(args)
        self.m_get_client.assert_called_once_with('plugins', mock.ANY)
        self.m_client.get_all.assert_called_once_with()

    def test_plugins_sync_all(self):
        args = 'plugins sync'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('plugins', mock.ANY)
        self.m_client.sync.assert_called_once_with(ids=None)

    def test_plugins_sync_specified_plugins(self):
        ids = [1, 2]
        args = 'plugins sync {ids}'.format(ids=' '.join(map(str, ids)))
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('plugins', mock.ANY)
        self.m_client.sync.assert_called_once_with(ids=ids)

    def exec_install(self, ext='rpm', force=False):
        path = tempfile.mkstemp(suffix='.{}'.format(ext))[1]
        args = 'plugins install {0} {1}'.format(path,
                                                '--force' if force else '')
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('plugins', mock.ANY)
        self.m_client.install.assert_called_once_with(path, force=force)

    def test_plugin_install(self):
        self.exec_install()

    def test_plugin_install_with_force(self):
        self.exec_install(force=True)

    def test_plugin_remove(self):
        args = 'plugins remove {0} {1}'.format(self.name, self.version)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('plugins', mock.ANY)
        self.m_client.remove.assert_called_once_with(self.name, self.version)
