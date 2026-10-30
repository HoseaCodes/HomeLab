"""Generate user-specific launchd plists; run as the Mac account, without sudo.

This writes staging files only. Review and install them using the runbook.
"""
from pathlib import Path
import getpass
import os
import plistlib

if os.getuid() == 0:
    raise SystemExit('Run as the Mac account without sudo.')

home = Path.home()
base = home / 'homelab-assistant'
(base / 'launchd').mkdir(parents=True, exist_ok=True)
(base / 'logs').mkdir(parents=True, exist_ok=True)
commands = {
    'model': [
        str(base / 'llama.cpp/build/bin/llama-server'),
        '--model', str(base / 'models/qwen-1.5b.gguf'),
        '--host', '127.0.0.1', '--port', '8081',
        '--ctx-size', '2048', '--threads', '2',
        '--parallel', '1', '--n-gpu-layers', '0',
    ],
    'assistant': [str(base / '.venv/bin/python'), str(base / 'assistant.py')],
}
for name, arguments in commands.items():
    label = f'com.hosea.homelab.{name}'
    config = {
        'Label': label,
        'UserName': getpass.getuser(),
        'ProgramArguments': arguments,
        'WorkingDirectory': str(base),
        'EnvironmentVariables': {'HOME': str(home), 'PYTHONUNBUFFERED': '1'},
        'RunAtLoad': True,
        'KeepAlive': True,
        'ThrottleInterval': 15,
        'StandardOutPath': str(base / f'logs/{name}.out.log'),
        'StandardErrorPath': str(base / f'logs/{name}.err.log'),
    }
    destination = base / f'launchd/{label}.plist'
    with destination.open('wb') as stream:
        plistlib.dump(config, stream)
    print(destination)
