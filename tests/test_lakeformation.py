from .common import BaseTest
import pdb



class LakeFormationTest(BaseTest):

    def test_lakeformation_value_filter(self):
        factory = self.record_flight_data("test_lakeformation_value_filter")
        p = self.load_policy({
            'name': 'example-abc-123',
            'resource': 'lakeformation'},
            session_factory=factory)
        resources = p.run()


