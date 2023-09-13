import os


def export_required_vars(request):
    data = {}
    git_actions = os.environ.get("GITHUB_ACTIONS", None)
    data["IS_GITHUB_ACTIONS"] = True if git_actions else False
    return data
