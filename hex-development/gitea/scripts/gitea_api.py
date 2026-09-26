#!/usr/bin/env python3
"""Small Gitea API client. Credentials come only from the process environment."""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Redirect refused; verify the configured Gitea origin")


def target(base, endpoint):
    url = urllib.parse.urlsplit(base)
    if url.scheme not in ("https", "http") or not url.netloc or url.query or url.fragment:
        raise ValueError("GITEA_URL must be an absolute HTTP(S) instance URL")
    if url.scheme == "http" and url.hostname not in ("localhost", "127.0.0.1", "::1"):
        raise ValueError("HTTPS required except for loopback testing")
    if url.username or url.password:
        raise ValueError("Credentials must not be embedded in GITEA_URL")
    path = urllib.parse.urlsplit(endpoint)
    decoded = urllib.parse.unquote(path.path)
    if not path.path.startswith("/") or path.netloc or path.scheme or path.fragment or "//" in decoded or any(part in (".", "..") for part in decoded.split("/")):
        raise ValueError("Endpoint must be a relative-to-API path without traversal")
    if any(key.lower() in ("token", "access_token", "sudo") for key, _ in urllib.parse.parse_qsl(path.query)):
        raise ValueError("Credential or sudo query parameter refused")
    segments = decoded.split("/")
    if "tokens" in segments or "admin" in segments:
        raise ValueError("Token and admin endpoints are outside this client's scope")
    prefix = url.path.rstrip("/")
    if prefix.endswith("/api/v1"):
        prefix = prefix[:-7]
    return urllib.parse.urlunsplit((url.scheme, url.netloc, prefix + "/api/v1" + endpoint, "", "")) if not path.query else urllib.parse.urlunsplit((url.scheme, url.netloc, prefix + "/api/v1" + path.path, path.query, ""))


def summary(value):
    """Return only typed, non-content metadata; never echo arbitrary API strings."""
    if isinstance(value, list):
        return [summary(item) for item in value]
    if not isinstance(value, dict):
        return {}
    result = {}
    for key in ("id", "index", "number"):
        if type(value.get(key)) is int and value[key] >= 0:
            result[key] = value[key]
    for key in ("private", "merged"):
        if type(value.get(key)) is bool:
            result[key] = value[key]
    if value.get("state") in ("open", "closed", "merged"):
        result["state"] = value["state"]
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("method", choices=["GET", "POST", "PATCH", "PUT", "DELETE"])
    p.add_argument("endpoint", help="path below /api/v1, e.g. /repos/owner/repo")
    p.add_argument("--data-stdin", action="store_true", help="read JSON request body from stdin")
    args = p.parse_args()
    base, token = os.environ.get("GITEA_URL"), os.environ.get("GITEA_TOKEN")
    if not base or not token:
        p.error("GITEA_URL and GITEA_TOKEN must already be set in the process environment")
    if args.data_stdin and args.method == "GET":
        p.error("GET must not include a request body")
    try:
        url = target(base, args.endpoint)
        data = None
        if args.data_stdin:
            data = json.dumps(json.load(sys.stdin)).encode("utf-8")
        req = urllib.request.Request(url, data=data, method=args.method, headers={
            "Authorization": "token " + token, "Accept": "application/json",
            "Content-Type": "application/json", "User-Agent": "hexskills-gitea/0.1",
        })
        with urllib.request.build_opener(NoRedirect).open(req, timeout=20) as response:
            text = response.read().decode("utf-8")
            print(json.dumps({"http_status": response.status, "metadata": summary(json.loads(text))}, indent=2) if text else f"HTTP {response.status}")
    except urllib.error.HTTPError as exc:
        print(f"HTTP {exc.code}: request failed; inspect permissions, endpoint and instance Swagger", file=sys.stderr)
        return 1
    except (ValueError, OSError, json.JSONDecodeError, urllib.error.URLError) as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
