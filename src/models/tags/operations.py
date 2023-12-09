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

from typing import Literal

from flask import Response, abort, make_response

from ...log import logger
from ..utils import PsudoPagination, paginated_schema, search_query
from ..utils.pagination import MAX_PER_PAGE
from .models import Tag
from .schemas import tag_schema, tags_schema


def read_all():
    """
    Retrieves all tags.

    Returns:
            dict: A dictionary representing the paginated result of all tags.

    Example:
            ```python
            result = read_all()
            print(result)
            ```
    """

    query: list[Tag] = Tag.query.all()
    psudo_paged_query = PsudoPagination(0, None, query, len(query))
    return paginated_schema(tags_schema).dump(psudo_paged_query)


def read_page(page=None, page_size=None):
    """
    Retrieves a paginated result of tags.

    Args:
            page (int): The page number.
            page_size (int): The number of tags per page.

    Returns:
            dict: A dictionary representing the paginated result of tags.

    Example:
            ```python
            result = read_page(page=1, page_size=10)
            print(result)
            ```
    """

    if not all((page, page_size)):
        return read_all()
    query = Tag.query.paginate(page=page, per_page=page_size, max_per_page=MAX_PER_PAGE)
    return paginated_schema(tags_schema).dump(query)


def read_one(pk) -> tuple[dict[str, str], Literal[200]]:
    """
    Retrieves a tag by its primary key.

    Args:
            pk: The primary key of the tag.

    Returns:
            tuple: A tuple containing a dictionary representing the tag and a status code indicating success.

    Raises:
            HTTPException: Raised when the tag with the specified primary key is not found.

    Example:
            ```python
            result = read_one(pk=1)
            print(result)
            ```
    """

    tag: Tag | None = Tag.query.filter(Tag.id == pk).one_or_none()

    if tag is None:
        abort(404, f"Tag with id {pk} not found!")
    return tag_schema.dump(tag), 200


def create(tag) -> tuple[dict[str, str], Literal[201]]:
    """
    Creates a new tag.

    Args:
            tag (dict): A dictionary representing the tag to be created.

    Returns:
            tuple: A tuple containing a dictionary representing the created tag and a status code indicating success.

    Raises:
            HTTPException: Raised when a tag with the same label already exists.

    Example:
            ```python
            new_tag = {"label": "example"}
            result = create(new_tag)
            print(result)
            ```
    """

    label: str = tag.get("label")
    existing_tag: Tag | None = Tag.query.filter(Tag.label == label).one_or_none()

    if existing_tag is not None:
        abort(406, f"Tag with label {label} already exists")

    new_tag: Tag = tag_schema.load(tag)
    new_tag.create()
    return tag_schema.dump(new_tag), 201


def delete(pk) -> Response:
    """
    Deletes a tag by its primary key.

    Args:
            pk: The primary key of the tag to be deleted.

    Returns:
            Response: A response indicating the success of the deletion.

    Raises:
            HTTPException: Raised when the tag with the specified primary key is not found.

    Example:
            ```python
            result = delete(pk=1)
            print(result)
            ```
    """

    existing_tag: Tag | None = Tag.query.filter(Tag.id == pk).one_or_none()

    if existing_tag is None:
        abort(404, f"Tag with id {pk} not found")

    existing_tag.delete()
    return make_response(f"{existing_tag.label}:{pk} successfully deleted", 200)


def get_metadatas(tag):
    """
    Retrieves the metadata of a tag.

    Args:
            tag: The label of the tag.

    Returns:
            None

    Example:
            ```python
            get_metadatas(tag="example")
            ```
    """

    existing_tag: Tag | None = Tag.query.filter(Tag.label == tag).one_or_none()

    if existing_tag is not None:
        logger.info(existing_tag.metadatas)
    else:
        logger.info(existing_tag)


def search(search_key):
    """
    Searches for tags based on a search key.

    Args:
            search_key: The search key to match against tag labels.

    Returns:
            list: A list of tags matching the search key.

    Example:
            ```python
            result = search(search_key="example")
            print(result)
            ```
    """

    tags = search_query(Tag, Tag.label, search_key)
    return tags_schema.dump(tags)
