#!/usr/bin/env python3
"""Read-only upstream GitHub source audit. Uses public GitHub REST API."""
import json
import sys
import urllib.error
import urllib.request

REPOS = {
    "device": "Realme-Pad-Dev/android_device_realme_RMP6768",
    "kernel": "Realme-Pad-Dev/android_kernel_realme_RMP6768",
    "vendor": "Realme-Pad-Dev/android_vendor_realme_RMP6768",
    "recovery": "Realme-Pad-Dev/android_recovery_realme_RMP6768",
}
HEADERS = {"Accept": "application/vnd.github+json", "User-Agent": "RealmePad-Windows-ARM-research"}

def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)

def main():
    output = {}
    for role, repo in REPOS.items():
        try:
            info = fetch("https://api.github.com/repos/" + repo)
            branch = info["default_branch"]
            commit = fetch("https://api.github.com/repos/" + repo + "/commits/" + branch)
            output[role] = {
                "repository": repo,
                "branch": branch,
                "commit": commit["sha"],
                "url": info["html_url"],
                "archived": info["archived"],
            }
        except (urllib.error.URLError, KeyError, ValueError) as exc:
            output[role] = {"repository": repo, "error": str(exc)}
    print(json.dumps(output, indent=2, sort_keys=True))
    return 1 if any("error" in value for value in output.values()) else 0

if __name__ == "__main__":
    sys.exit(main())
