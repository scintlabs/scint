import requests


class Github:
    def __init__(self, token):
        self.token = token


class FileContent:
    def __init__(self, content, link):
        self.content = content
        self.link = link


def get_docusaurus_path_from_github(github_url):
    import re

    match = re.match(r"docs/(.+\.mdx?)", github_url)
    if match:
        file_path = match.group(1)
        file_path = re.sub(r"\.mdx?$", "", file_path)
        path_segments = file_path.split("/")
        path_segments = [segment.lstrip("0123456789_") for segment in path_segments]
        file_path = "/".join(path_segments)
        return "/docs/" + file_path
    return github_url


def main(gh_auth, owner, repo, path="", ref="", result_format="github_object"):
    headers = {"Authorization": f"token {gh_auth.token}"}
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    if ref:
        url += f"?ref={ref}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    entries = response.json()
    if not isinstance(entries, list):
        entries = [entries]

    file_contents = []
    for entry in entries:
        if entry["type"] == "file":
            is_markdown = entry["name"].endswith(".md")
            is_mdx = entry["name"].endswith(".mdx")
            if is_markdown or is_mdx:
                link = get_docusaurus_path_from_github(entry["path"])
                content_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{entry['path']}"
                content_response = requests.get(content_url, headers=headers)
                content_response.raise_for_status()
                content = content_response.text
                file_contents.append(FileContent(content, link))
        elif entry["type"] == "dir":
            dir_contents = main(gh_auth, owner, repo, entry["path"], ref, result_format)
            file_contents.extend(dir_contents)
    return file_contents
