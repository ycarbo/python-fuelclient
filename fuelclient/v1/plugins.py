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

import collections
import six

from fuelclient import objects
from fuelclient.v1 import base_v1


class PluginsClient(base_v1.BaseV1Client):

    _entity_wrapper = objects.Plugins

    def get_all(self):
        """Get plugins data and re-format 'releases' info to display
         supported 'os', 'version' in a user-friendly way, e.g.:
                ubuntu (liberty-8.0, liberty-9.0, mitaka-9.0)
                centos (liberty-8.0), ubuntu (liberty-8.0)

        :returns: list of plugins
        :rtype: list
        """
        # Replace original nested 'releases' dictionary (from plugins meta
        # dictionary) to a new user-friendly form with releases info, i.e.
        # 'os', 'version' that specific plugin supports
        plugins = self._entity_wrapper.get_all_data()
        for plugin in plugins:
            releases = collections.defaultdict(list)
            for key in plugin['releases']:
                releases[key['os']].append(key['version'])
            plugin['releases'] = ', '.join('{} ({})'.format(k, ', '.join(v))
                                           for k, v in six.iteritems(releases))
        return plugins

    def sync(self, ids):
        """Synchronise plugins on file system with plugins in API service.

        :param ids: List of ids for filtering plugins
        :type ids: list
        """

        self._entity_wrapper.sync(plugin_ids=ids)

    def install(self, plugin_path, force=False):
        """Install plugin archive and register in API service.

        :param plugin_path: Path to plugin file
        :type plugin_path: str
        :param force: Update existent plugin even if it is not updatable
        :type force: bool
        """
        return self._entity_wrapper.install(plugin_path, force=force)

    def remove(self, plugin_name, plugin_version):
        """Remove the plugin package, and update data in API service.

        :param str plugin_name: Name of plugin to remove
        :param str plugin_version: Version of plugin to remove
        """
        return self._entity_wrapper.remove(plugin_name, plugin_version)


def get_client(connection):
    return PluginsClient(connection)
