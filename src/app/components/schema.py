from marshmallow import fields

from ..files.schemas import FileSchema
from ..licenses.schemas import SPDXSchema
from ..metadatas.schemas import MetadataSchema
from ..tags.schemas import TagSchema


class ComponentSchema(MetadataSchema):
	license = fields.Nested(SPDXSchema)
	files = fields.Nested(FileSchema, many=True)
	tags = fields.Nested(TagSchema, many=True)

component_schema = ComponentSchema()
components_schema = ComponentSchema(many=True)
