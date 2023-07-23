from functools import lru_cache

from github import ContentFile, Github, Repository


@lru_cache
def get_repository(access_token, repository) -> Repository.Repository:
    g = Github(access_token)
    return g.get_user().get_repo(repository)



def update_file(repository: Repository.Repository, branch, raw_file_data, destination_file_path) -> ContentFile.ContentFile:

    all_files = []
    contents: list[ContentFile.ContentFile] = repository.get_contents("") # type: ignore

    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repository.get_contents(file_content.path)) # type: ignore
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="', '').replace('")', ''))

    if destination_file_path not in all_files:
        raise FileNotFoundError("The destination file path for found")

    contents = repository.get_contents(destination_file_path) # type: ignore

    return repository.update_file(
        contents.path, # type: ignore
        "committing files",
        raw_file_data,
        contents.sha, # type: ignore
        branch=branch,
    )["content"] # type: ignore


def upload_new_file(repository: Repository.Repository, branch, raw_file_data, destination_file_path) -> ContentFile.ContentFile:
    return repository.create_file(
        destination_file_path,
        "committing files",
        raw_file_data,
        branch=branch,
    )["content"] # type: ignore


# def upload_components(access_token: str, repo_name: str, branch: str, component_name: str, files: list[FileStorage], thumbnail: FileStorage|None):
#     repo = get_repository(access_token, repo_name)
#     response = []
#     for file in files:
#         # upload_new_file(
#         #     repo,
#         #     branch,
#         #     file.stream.read(),
#         #     f"{component_name}/{component_name}.{file.filename.rsplit('.', 1)[-1]}",
#         # )
#         print(f"{component_name}/{file.filename}")
