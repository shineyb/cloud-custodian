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

from .common import BaseTest

# from nose.tools import set_trace; set_trace()


class TestLicenseConfiguration(BaseTest):
    '''
    def test_tag_license_configuration(self):
        session_factory = self.record_flight_data(
            "test_license_configuration_tag"
        )
        p = self.load_policy(
            {
                "name": "tag-license-configuration",
                "resource": "license-configuration",
                "actions": [{"type": "tag", "key": "Category", "value": "TestValue"}],
            },
            session_factory=session_factory,
        )
        resources = p.run()
        for x in range(len(resources)):
            self.assertEqual(len(resources), 1)

    def test_remove_tag_license_configuration(self):
        session_factory = self.record_flight_data(
            "test_remove_tag_license_configuration"
        )
        p = self.load_policy(
            {
                "name": "untag-license-configuration",
                "resource": "license-configuration",
                "filters": [{"tag:Category": "TestValue"}],
                "actions": [{"type": "remove-tag", "tags": ["Category"]}],
            },
            session_factory=session_factory,
        )
        resources = p.run()
        self.assertEqual(len(resources), 1)

    
    def test_update_service_settings_license_configuration(self):
        session_factory = self.record_flight_data(
            "test_update_service_settings_license_configuration")
        p = self.load_policy(
            {
                "name": "update-service-settings",
                "resource": "service-settings",
                # "Filters" : "None"
            },
            session_factory=session_factory,

        )
        resources = p.run()
        self.assertEqual(len(resources), 1)
    

    def test_update_license_configuration(self):
        session_factory = self.record_flight_data("test_update_license_configuration")
        p = self.load_policy(
            {
                "name": "update-license-configuration",
                "resource": "license-configuration",
                # "Filters" : "None"
                "actions": [
                    {
                        "type": "update-license-configuration",
                        "Name": "Database License",
                        "Description": "testing",
                        "LicenseCount": 500
                    }
                ],
            },
            session_factory=session_factory,
        )
        resources = p.run()
        self.assertEqual(len(resources), 1)
        # client = session_factory().client("license-manager")
    '''
    def test_delete_license(self):
        session_factory = self.record_flight_data("test_delete")
        client = session_factory().client("license-manager")
        from nose.tools import set_trace; set_trace()
        license_arn = "arn:aws:license-manager:us-east-1:644160558196:license-configuration:lic-76b4409b49ff38b3817348ca9b02c3fb"
        result = client.list_license_configurations()
        self.assertEqual (len(result), 1)
        p = self.load_policy(
            {
                "name": "delete-license-configuration",
                "resource": "license-configuration",
                "filters": [{"tag:DeleteMe": "present"}],
                "actions": [{"type": "delete"}],
            },
            session_factory=session_factory,
        )

        resources = p.run()
        
        self.assertEqual(len(resources), 0)
