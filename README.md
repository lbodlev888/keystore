# Custom Keyring – A Simple GPG-Encrypted Password Manager

A lightweight, file-based credential store that encrypts each password individually with GPG.  
No extra dependencies — just Python 3 and `gpg`.

Perfect for storing API keys, SSH/PGP private keys, tokens, or any sensitive text you want encrypted at rest.

## Features

- One `.gpg` file per credential
- Single recipient set once during `init`
- Works everywhere GPG is available (servers, containers, CI, etc.)
- Pure files → easy to backup, sync, or version control
- Simple and auditable code

## Files

```
custom_keyring.py  → core library
keystore.py        → CLI frontend (install as `keystore`)
```

## Installation

```bash
git clone https://github.com/yourname/custom-keyring.git
cd custom-keyring

# Recommended: make the CLI globally available
sudo ln -s "$(pwd)/keystore.py" /usr/local/bin/keystore
```

(Or just use an alias / add the folder to your PATH)

## Requirements

- Python 3.6+
- GnuPG (`gpg`) in `$PATH`
- A personal GPG key pair

## Usage

```bash
# 1. Initialize (only once)
keystore init me@example.com
# or use key ID / fingerprint
keystore init 0xDEADBEEF12345678

# 2. Store credentials
keystore new --service github --username alice --password SuperSecret123!

# Store an SSH key, API token, etc.
keystore new --service aws --username AKIA... --password wJalrXUtnFEMI/...

# 3. Retrieve
keystore get --service github --username alice
# → SuperSecret123!

# 4. Update
keystore update --service github --username alice --new-password EvenBetter456!

# 5. Remove
keystore remove --service github --username alice
```

### In scripts

```bash
export DB_PASS=$(keystore get --service prod-db --username postgres)
export GH_TOKEN=$(keystore get --service github --username git-bot)
```

## Storage

Everything lives in `~/.custom_keyring/`:
- `data.json` → only stores the recipient GPG ID
- One `<service>_<username>.gpg` file per credential

Safe to back up or sync with any tool (Syncthing, git, Dropbox, etc.).

## Use as a Python library

```python
from custom_keyring import Keyring

kr = Keyring()
kr.save_password("openai", "sk-", "sk-XXXXXXXXXXXXXXXXXXXX")
token = kr.get_password("openai", "sk-")
```

## Security notes

- Plaintext never touches disk
- Each credential encrypted separately
- Only you (with your private key + passphrase) can decrypt
- Minimal attack surface

## Missing on purpose (feel free to contribute!)

- `list` command
- Built-in password generator
- Symmetric encryption fallback

---

**License**: MIT  
Feel free to use, modify, and distribute. Enjoy your tiny, trustworthy vault!
