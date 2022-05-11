from c7n.manager import resources
from c7n import query
from c7n.query import QueryResourceManager, ConfigSource, TypeInfo
from c7n.tags import universal_augment


class DescribeResource(query.DescribeSource):
    def augment(self, resources):
        return universal_augment(
            self.manager,
            super(DescribeResource, self).augment(resources))


@resources.register('lakeformation')
class LakeFormation(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'lakeformation'
        enum_spec = ('list_resources', 'ResourceInfoList[].ResourceArn', None)
        arn = id = 'ResourceArn'
        name = 'name'
        detail_spec = ("describe_resource", "ResourceArn", None, "ResourceInfo")
        cfn_type = "AWS::LakeFormation::Resource"
        arn_type = 'Resource'
        universal_taggable = object()

    source_mapping = {
        'describe': DescribeResource,
        'config': ConfigSource
    }
