
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

import os


def get_directories(path: str, store: set):
	if os.path.isfile(path):
		return
	tag = path.rsplit('/', 1)[-1]
	store.add(tag)
	for p in os.listdir(path):
		get_directories(os.path.join(path, p), store)


def extract_tags(path, save_path):
	tags = set()
	get_directories(path, tags)
	tags.remove("FreeCAD-library")

	with open(save_path, "w", encoding="utf-8") as file:
		for tag in tags:
			file.write(tag+'\n')


if __name__ == "__main__":
	extract_tags("/home/encryptedbee/tesla/projects/GSOC/FreeCAD-library", "component_management_system/data/tags.txt")
