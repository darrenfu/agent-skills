#!/bin/bash
set -euo pipefail

keychain="${1:-$HOME/Library/Keychains/login.keychain-db}"

if [[ ! -f "$keychain" ]]; then
  printf 'Keychain not found: %s\n' "$keychain" >&2
  exit 2
fi

if ! security show-keychain-info "$keychain" >/dev/null 2>&1; then
  printf 'The keychain is locked. Enter the Mac login password in the secure prompt.\n' >&2
  security unlock-keychain "$keychain"
fi

security set-keychain-settings "$keychain"
info="$(security show-keychain-info "$keychain" 2>&1)"
printf '%s\n' "$info"

if [[ "$info" != *"no-timeout"* ]]; then
  printf 'No-timeout verification failed.\n' >&2
  exit 3
fi

security find-identity -v -p codesigning "$keychain"
