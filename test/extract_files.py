import json
import os

base_path = "/home/encryptedbee/tesla/projects/GSOC/FreeCAD-library"
base_url = "https://github.com/FreeCAD/FreeCAD-library/blob/master"

file_store_dict = dict()

component_exts = ["stl", "fcstd", "fcstd1", "step", "stp"]
image_exts = ["jpeg", "jpg", "png", "svg"]
info_exts = ["txt", "md"]
other_exts = set()


def build_url(path: str):
	sub_path = path.removeprefix(base_path).replace(" ", "%20")
	return base_url + sub_path


def data_extraction(node, file_list, path):
	name, ext = node.rsplit('.', 1)

	if name not in file_list:
		file_list[name] = {
			"components" : dict(),
			"images" : [],
			"info" : [],
			"others" : [],
		}

	store = file_list[name]

	if ext.lower() in component_exts:

		data = {
			ext : {
				"size" : os.path.getsize(path),
				"url" : build_url(path),
			}
		}

		store["components"].update(data)

	elif ext.lower() in image_exts:
		store["images"].append(build_url(path))

	elif ext.lower() in info_exts:
		store["info"].append(build_url(path))

	else:
		store["others"].append(node)
		other_exts.add(ext)


def place_node(nodes_itter, store: dict, path):
	try:
		node = next(nodes_itter)

		if '.' in node:
			if "files" not in store:
				store["files"] = {}

			data_extraction(node, store["files"], path)

			return

		if node not in store:
			store[node] = dict()

		place_node(nodes_itter, store[node], path)
	except:
		pass


def get_files(path: str):

	if os.path.isfile(path):
		short_path = path.removeprefix(base_path)
		nodes = short_path.split('/')
		nodes = [node for node in nodes if node]

		place_node(iter(nodes), file_store_dict, path)

	else:
		for file in os.listdir(path):
			get_files(os.path.join(path, file))

get_files(base_path)
# print(file_store_dict)
with open("test/files.json", "w") as file:
	json.dump(file_store_dict, file)

print(other_exts)
