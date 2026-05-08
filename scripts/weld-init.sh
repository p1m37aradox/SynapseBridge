#!/bin/bash
# 🌉 Synapse Bridge Environment Initializer
# This script applies the proven "Monolithic Weld" aliases.

case "$1" in
    "host")
        echo "🔧 Applying Termux Host Aliases..."
        # We use a unique marker to avoid double-entry if run twice
        sed -i '/# <SYNAPSE-BRIDGE-HOST>/,/# <\/SYNAPSE-BRIDGE-HOST>/d' ~/.bashrc
        cat <<EOM >> ~/.bashrc
# <SYNAPSE-BRIDGE-HOST>
alias synapse='proot-distro login debian --bind \$HOME/storage/shared/SynapseBridge:/mnt/SynapseBridge'
alias synapse-ui='bash \$HOME/storage/shared/SynapseBridge/scripts/UI_main.sh'
alias g-gem='cd \$HOME/storage/shared/SynapseBridge && git checkout geminiCLI'
alias g-main='cd \$HOME/storage/shared/SynapseBridge && git checkout main'
# </SYNAPSE-BRIDGE-HOST>
EOM
        echo "✅ Host aliases added."
        ;;
    "guest")
        echo "🧪 Applying Debian Guest Aliases..."
        sed -i '/# <SYNAPSE-BRIDGE-GUEST>/,/# <\/SYNAPSE-BRIDGE-GUEST>/d' ~/.bashrc
        cat <<EOM >> ~/.bashrc
# <SYNAPSE-BRIDGE-GUEST>
alias sb-venv='source ~/SynapseBridge_Root/venv/bin/activate && cd /mnt/SynapseBridge'
alias sbc='cd /mnt/SynapseBridge'
alias synapse-mempalace-mcp='mempalace-mcp'
# </SYNAPSE-BRIDGE-GUEST>
EOM
        echo "✅ Guest aliases added."
        ;;
    *)
        echo "Usage: bash weld-init.sh [host|guest]"
        exit 1
        ;;
esac
