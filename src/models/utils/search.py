# SPDX-License-Identifier: MIT
# --------------------------------------------------------------
# |																|
# |             Copyright 2023 - 2023, Amulya Paritosh			|
# |																|
# |  This file is part of Component Library Plugin for FreeCAD.	|
# |																|
# |               This file was created as a part of				|
# |              Google Summer Of Code Program - 2023			|
# |																|
# --------------------------------------------------------------

import re

from flask_sqlalchemy.query import Query


def search_query(model, model_attribute, search_str: str):
    """
    Searches for tags in the given model based on a search string.

    Args:
            model: The model to search in.
            model_attribute: The attribute of the model to search in.
            search_str (str): The search string.

    Returns:
            list[model]: The list of tags matching the search criteria.

    Example:
            ```python
            tags = search_query(Tag, Tag.name, "python")
            ```
    """

    tags: list[model] = model.query.filter(model_attribute.contains(search_str)).all()

    for word in search_str.split(" "):
        query: list[Query] = model.query.filter(model_attribute.contains(word)).all()
        tags.extend(q for q in query if q not in tags)

    return tags
