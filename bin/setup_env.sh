#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
apt update && apt install -y build-essential python3-dev python3-pip curl libffi-dev libssl-dev
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env
export ANDROID_API_LEVEL=34
export PURE_PYTHON=1
pip install chromadb mempalace --no-cache-dir --break-system-packages
