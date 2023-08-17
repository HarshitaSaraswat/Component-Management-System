
# SPDX-License-Identifier: MIT
# --------------------------------------------------------------
#|																|
#|             Copyright 2023 - 2023, Amulya Paritosh			|
#|																|
#|  This file is part of Component Library Plugin for FreeCAD.	|
#|																|
#|               This file was created as a part of				|
#|              Google Summer Of Code Program - 2023			|
#|																|
# --------------------------------------------------------------

from marshmallow import Schema, fields

from ..files.schemas import FileSchema
from ..licenses.schemas import SPDXSchema
from ..metadatas.schemas import MetadataSchema
from ..tags.schemas import TagSchema


class ComponentSchema(Schema):
	id = fields.String()
	metadata = fields.Nested(MetadataSchema)
	license = fields.Nested(SPDXSchema)
	files = fields.Nested(FileSchema, many=True)
	tags = fields.Nested(TagSchema, many=True)

component_schema = ComponentSchema()
components_schema = ComponentSchema(many=True)
