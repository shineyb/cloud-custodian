from c7n.actions import BaseAction
from c7n.manager import resources
from c7n.query import QueryResourceManager, DescribeSource, ConfigSource, TypeInfo
from c7n.tags import universal_augment
from c7n.utils import type_schema, local_session
import pdb

class DescribeResource(DescribeSource):

    def augment(self, resources):
        pdb.set_trace()
        resources = super().augment(resources)
        return universal_augment(self.manager, resources)


@resources.register('lakeformation')
class LakeFormation(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'lakeformation'
        enum_spec = ('list_resources', 'ResourceInfoList',None)
        pdb.set_trace()
        arn = id = 'ResourceArn'
        detail_spec = ("describe_resource", "ResourceArn",'ResourceInfo',None)
        cfn_type = config_type = "AWS::LakeFormation::Resource"
        arn_type = 'Resource'
        universal_taggable = object()


    source_mapping = {
        'describe': DescribeResource,
        'config': ConfigSource
    }

