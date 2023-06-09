import os

tags = []
base_path = "/home/encryptedbee/tesla/projects/GSOC/FreeCAD-library"

def get_directories(path: str):
	if os.path.isfile(path):
		return
	tag = path.rsplit('/', 1)[-1]
	tags.append(tag)
	for p in os.listdir(path):
		get_directories(os.path.join(path, p))

get_directories(base_path)
tags.remove("FreeCAD-library")

with open("test/tags.txt", "w") as file:
	for tag in tags:
		file.write(tag+'\n')
