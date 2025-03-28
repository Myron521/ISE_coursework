import os
import subprocess

def clone_repository(repo_url):
    """
    Clone the entire repository to the current environment.
    """
    try:
        subprocess.run(['git', 'clone', repo_url], check=True)
        print(f"Repository {repo_url} cloned successfully.")
    except subprocess.CalledProcessError:
        print(f"Failed to clone repository {repo_url}. Please check the network or repository address.")

def check_folder_exists(folder_path):
    """
    Check if a folder exists and print its contents if it does.
    """
    if os.path.exists(folder_path):
        print(f"{folder_path} folder cloned successfully, folder contents are as follows:")
        for root, dirs, files in os.walk(folder_path):
            level = root.replace(folder_path, '').count(os.sep)
            indent = ' ' * 4 * (level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            sub_indent = ' ' * 4 * (level + 1)
            for f in files:
                print('{}{}'.format(sub_indent, f))
    else:
        print(f"{folder_path} folder cloning failed. Please check the network or repository address.")