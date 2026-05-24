import os
import shutil
import stat
from git import Repo

TEMP_REPO_DIR = "temp_repos"


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def clone_repository(repo_url):

    try:

        repo_name = repo_url.split("/")[-1].replace(".git", "")

        local_path = os.path.join(TEMP_REPO_DIR, repo_name)

        # Remove old repo if exists
        if os.path.exists(local_path):

            shutil.rmtree(
                local_path,
                onerror=remove_readonly
            )

        # Clone repository
        Repo.clone_from(repo_url, local_path)

        return {
            "success": True,
            "repo_name": repo_name,
            "local_path": local_path
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }