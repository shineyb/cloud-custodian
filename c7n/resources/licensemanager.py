# Copyright 2019 Capital One Services, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import absolute_import, division, print_function, unicode_literals

from c7n.actions import (ActionRegistry, BaseAction)
from c7n.manager import resources
from c7n.query import QueryResourceManager
from c7n.utils import local_session, type_schema
from c7n.tags import RemoveTag, Tag

actions = ActionRegistry('license-configuration.actions')


@resources.register('license-configuration')
class LicenseConfiguration(QueryResourceManager):

    class resource_type(object):
        service = 'license-manager'
        enum_spec = ('list_license_configurations', 'LicenseConfigurations', None)
        detail_spec = (
            'get_license_configuration', 'LicenseConfigurationArn',
            'LicenseConfigurationArn', None)
        id = 'LicenseConfigurationArn'
        name = 'Name'
        date = None
        dimension = None
        filter_name = None

    permissions = ('license-manager:ListTagsForResource',)

    def augment(self, resources):
        client = local_session(self.session_factory).client('license-manager')
        from nose.tools import set_trace; set_trace()
        def _augment(r):
            # List tags for the license_configuration & set as attribute
            tags = self.retry(client.list_tags_for_resource,
                ResourceArn=r['LicenseConfigurationArn'])['Tags']
            r['Tags'] = tags
            return r

        # Describe license_configuration & then list tags
        resources = super(LicenseConfiguration, self).augment(resources)
        with self.executor_factory(max_workers=1) as w:
            return list(filter(None, w.map(_augment, resources)))


@LicenseConfiguration.action_registry.register('delete')
class DeleteLicenseConfiguration(BaseAction):
    """Deletes LicenseConfiguration(s)

    :example:

    .. code-block: yaml

        policies:
          - name: delete-license-Configuration
            resource: license-configuration
            filters:
              - "tag:DeleteMe": present
            actions:
              - delete
    """
    schema = type_schema('delete')
    permissions = ('license-manager:DeleteLicenseConfiguration',)

    def process(self, resources):
        if not len(resources):
            return

        client = local_session(self.manager.session_factory).client('license-manager')

        for n in resources:
            try:
                client.delete_license_configuration(
                    LicenseConfigurationArn=n['LicenseConfigurationArn'])
            except client.exceptions.ResourceNotFound:
                pass


@resources.register('service-settings')
class ServiceSettings(QueryResourceManager):

    class resource_type(object):
        service = 'license-manager'
        enum_spec = ('get_service_settings', "test", None)
        detail_spec = ('get_service_settings', None, None, None)
        id = None
        name = None
        date = None
        dimension = None
        filter_name = None

    permissions = ('service-settings:GetServiceSettings',)


@ServiceSettings.action_registry.register('update-service-settings')
class UpdateServiceSettings(BaseAction):
    """updates service settings  based on specified parameter
    using UpdateServiceSettings.

    'Update' is an array with with key value pairs that should be set to
    the property and value you wish to modify.

    :example:

    .. code-block:: yaml

            policies:
              - name:update-service-settings
                resource:service-settings
                filters:
                  - None
                actions:
                  - type:update-service-settings
                    update:
                      - property: 'SnsTopicArn'
                        value: 'arn:aws:sns:us-east-1:471176887411:
                                aws-license-manager-service-test-license-sns
    """

    schema = type_schema(
        'update-service-settings',
        update={
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'property': {'type': 'string', 'enum': [
                        'SnsTopicArn',
                    ]},
                    'value': {}
                },
            },
        },
        required=('update',))

    permissions = ('license-manager:UpdateServiceSettings',)

    def process(self, resources):
        c = local_session(self.manager.session_factory).client('license-manager')

        for r in resources:
            param = {}
            for update in self.data.get('update'):
                if r[update['property']] != update['value']:
                    param[update['property']] = update['value']
            if not param:
                continue
            c.update_service_settings(**param)


@LicenseConfiguration.action_registry.register('tag')
class CreateTag(Tag):

    permissions = ('license-manager:TagResource',)

    def process_resource_set(self, resources, tags):
        client = local_session(
            self.manager.session_factory).client('license-manager')

        tag_list = []
        for t in tags:
            tag_list.append({'Key': t['Key'], 'Value': t['Value']})
        for r in resources:
            client.tag_resource(ResourceArn=r['LicenseConfigurationArn'], Tags=tag_list)


@LicenseConfiguration.action_registry.register('remove-tag')
class RemoveTag(RemoveTag):

    permissions = ('license-manager:UntagResource',)

    def process_resource_set(self, resources, keys):
        client = local_session(
            self.manager.session_factory).client('license-manager')
        for r in resources:
            client.untag_resource(ResourceArn=r[self.id_key], TagKeys=keys)


@LicenseConfiguration.action_registry.register('update-license-configuration')
class UpdateLicenseConfiguration(BaseAction):

    """Updates license-manager based on specified parameter
    'Update' is an array with with key value pairs that should be set to
    the property and value you wish to modify.

    :example:

    .. code-block:: yaml

            policies:
              - name: update-license-configuration
                resource: license-configuration
                actions:
                  - type: update-license-configuration
                    Name: test-aws-license-manager
    """

    schema = {
        'type': 'object',
        'additionlProperties': False,
        'properties': {
            'type': {'enum': ['UpdateLicenseConfiguration']},
            'Description': {'type': 'string'},
            'LicenseConfigurationArn': {'type': 'string'},
            'LicenseConfigurationStatus': {'type': 'string'},
            'LicenseCount': {'type': 'integer'},
            'LicenseCountHardLimit': {'type': 'string'},
            'LicenseRules': {'type': 'array', 'items': {'type': 'string'}},
            'Name': {'type': 'string'}
        }
    }

    permissions = ('license-manager:UpdateLicenseConfiguration',)

    def process(self, resources):
        c = local_session(self.manager.session_factory).client('license-manager')
        params = dict(self.data)
        params.pop('type')

        for r in resources:
            params['LicenseConfigurationArn'] = r['LicenseConfigurationArn']
            c.update_license_configuration(**params)
