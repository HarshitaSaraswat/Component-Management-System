
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
		query:list[Query] = model.query.filter(model_attribute.contains(word)).all()
		tags.extend(q for q in query if q not in tags)

	return tags


def make_fuzzy_query(value: str):
	"""
	Creates a fuzzy query for the given value.

	Args:
		value (str): The value to be used in the fuzzy query.

	Returns:
		dict: The fuzzy query.

	Example:
		```python
		query = make_fuzzy_query("example")
		```
	"""

	return {
		"fuzzy": {
			"name": {
				"value": value,
				"fuzziness": "AUTO",
				"transpositions": True,
				"max_expansions": 100,
				"boost": 5,
			}
		}
	}


def make_regexp_query(value: str):
	"""
	Creates a fuzzy query.

	Returns:
		dict: The fuzzy query.
	"""

	return {
		"regexp": {
			"name": {
				"value": value,
				"flags": "ALL",
				"case_insensitive": True,
			}
		}
	}


def make_must_query_list(search_key: str):
	"""
	Creates a list of fuzzy queries based on the given search key.

	Args:
		search_key (str): The search key.

	Returns:
		list[dict]: The list of fuzzy queries.

	Example:
		```python
		query_list = make_must_query_list("example, test")
		```
	"""

	value_list = re.split(r" |,|\||-|_|\.", search_key)
	return [make_fuzzy_query(value) for value in value_list]


def make_should_query_list(search_key: str):
	"""
	Creates a list of queries based on the given search key.

	Args:
		search_key (str): The search key.

	Returns:
		list[dict]: The list of queries.

	Example:
		```python
		query_list = make_should_query_list("example, test")
		```
	"""

	value_list = re.split(r" |,|\||-|_|\.", search_key)
	query_list = [make_fuzzy_query(value) for value in value_list]
	query_list.extend(make_regexp_query(value) for value in value_list)
	query_list.append(
	    {
	        "more_like_this" : {
	            "fields" : ["name"],
	            "like" : search_key,
	            "min_term_freq" : 1,
	            "max_query_terms" : 12
	        }
	    }
	)

	return query_list


def make_elasticsearch_query(search_key: str):
	"""
	Creates an Elasticsearch query based on the given search key.

	Args:
		search_key (str): The search key.

	Returns:
		dict: The Elasticsearch query.

	Example:
		```python
		query = make_elasticsearch_query("example, test")
		```
	"""

	return {
		"bool": {
			# "must": make_must_query_list(search_key),
			"should": make_should_query_list(search_key),
		}
	}
