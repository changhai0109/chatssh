#!/usr/bin/env python

import os
import sys
import json

if os.geteuid() != 0:
    print("This script must be run as root. Exiting.")
    sys.exit(1)


def install():
    os.system("python -m pip install openai")
    os.system("cp ./chatssh /usr/local/bin && chmod +x /usr/local/bin/chatssh")
    username = input("choose chatbot username: [chat]").strip()
    if username == "":
        username = "chat"
    os.system(f"useradd -m -s /usr/local/bin/chatssh {username} && touch ~{username}/.hushlogin && chown {username}:{username} ~{username}/.hushlogin")
    os.system(f"passwd {username}")
    with open("./config_template.json", "r") as f:
        config = json.load(f)
        config['username'] = username
    openai_key = input("set openai key []").strip()
    config['openai']['api_key'] = openai_key
    deepseek_key = input("set deepseek key []").strip()
    config['deepseek']['api_key'] = deepseek_key
    default_provider = input("default_provider [deepseek]").strip()
    if default_provider == '':
        default_provider = 'deepseek'
    config['provider'] = default_provider
    default_model = input("default_model [deepseek-chat]").strip()
    if default_model == '':
        default_model = 'deepseek-chat'
    config['model'] = default_model
    with open("/etc/chatssh.json", "w") as f:
        json.dump(config, f, indent=4)

def uninstall():
    username = "chat"
    with open("/etc/chatssh.json", "r") as f:
        config = json.load(f)
        username = config['username']
    os.system(f"userdel -r {username}")
    os.system("rm /usr/local/bin/chatssh")
    os.system("rm /etc/chatssh.json")


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in {'install', 'uninstall'}:
        print(f"{sys.argv[0]} <install|uninstall>")
        exit(-1)
    if sys.argv[1] == 'install':
        install()
    elif sys.argv[1] == 'uninstall':
        uninstall()

