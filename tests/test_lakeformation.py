from .common import BaseTest


class LakeFormationTest(BaseTest):

    def test_lakeformation_value_filter(self):
        factory = self.replay_flight_data("test_lakeformation_query_resources")
        p = self.load_policy({
            'name': 'list_lakeformation_resources',
            'resource': 'lakeformation',
            "filters": [{"RoleArn": "present"}], },
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 2)
        TagsList = resources[0]['Tags']
        self.assertEqual((TagsList[0])['Key'], 'ResourceCreator')
        self.assertEqual((TagsList[0])['Value'], 'kapil')
