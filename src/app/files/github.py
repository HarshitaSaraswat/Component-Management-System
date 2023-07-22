from github import ContentFile, Github


def update_file(access_tocken, repository, branch, raw_file_data, destination_file_path) -> ContentFile.ContentFile:
    g = Github(access_tocken)
    repo = g.get_user().get_repo(repository)

    all_files = []
    contents = repo.get_contents("")

    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path)) # type: ignore
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="', '').replace('")', ''))

    if destination_file_path in all_files:
        contents = repo.get_contents(destination_file_path)
        response = repo.update_file(contents.path, "committing files", raw_file_data, contents.sha, branch=branch) # type: ignore
    else:
        raise FileNotFoundError("The destination file path for found")

    return response["content"] # type: ignore


def upload_new_file(access_tocken, repository, branch, raw_file_data, destination_file_path) -> ContentFile.ContentFile:
    g = Github(access_tocken)
    repo = g.get_user().get_repo(repository)
    response = repo.create_file(destination_file_path, "committing files", raw_file_data, branch=branch)

    return response["content"] # type: ignore


def upload_component(access_tocken, repository, branch, file, component_name):
    # TODO define...
    ...
