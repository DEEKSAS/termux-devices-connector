#!/usr/bin/env bash
# Termux agent prototype (improved)
# Configure these variables or export them in environment before running
SERVER_URL="${RDCR_SERVER:-http://YOUR_SERVER:8080/submit}"
JWT="${RDCR_JWT:-REPLACE_WITH_JWT}"
PUBLIC_KEY_PATH="${RDCR_PUBKEY:-/data/data/com.termux/files/home/public.pem}"
WORKDIR="${RDCR_WORKDIR:-/data/data/com.termux/files/home/rdcr}"
mkdir -p "$WORKDIR"

log() { echo "[rdcr]" "$@"; }

download_pubkey() {
  if [ -n "$RDCR_PUBKEY_URL" ]; then
    curl -sSf "$RDCR_PUBKEY_URL" -o "$PUBLIC_KEY_PATH" || return 1
    log "Downloaded public key"
  fi
}

upload_bundle() {
  bundle="$1"
  sig="$1.sig"
  if [ ! -f "$sig" ]; then
    log "Missing signature: $sig"
    return 1
  fi
  curl -s -X POST -H "Authorization: Bearer $JWT" \
    -F "bundle=@$bundle" -F "signature=$(xxd -p -c 9999 $sig)" \
    "$SERVER_URL"
}

verify_signature() {
  sigfile="$1.sig"
  bundle="$1"
  if command -v python3 >/dev/null 2>&1; then
    python3 "$(dirname "$0")/verify_signature.py" "$PUBLIC_KEY_PATH" "$bundle" "$sigfile"
    return $?
  elif command -v openssl >/dev/null 2>&1; then
    openssl dgst -sha256 -verify "$PUBLIC_KEY_PATH" -signature "$sigfile" "$bundle"
    return $?
  else
    log "No verification tool (python3 or openssl) available"
    return 2
  fi
}

run_in_sandbox() {
  bundle_zip="$1"
  tmpdir="$WORKDIR/tmp"
  rm -rf "$tmpdir" && mkdir -p "$tmpdir"
  unzip -q "$bundle_zip" -d "$tmpdir"
  if [ -x "$tmpdir/run.sh" ]; then
    # Use proot to isolate if available
    if command -v proot >/dev/null 2>&1; then
      log "Running in proot sandbox"
      proot -q qemu-aarch64 -R "$tmpdir" /bin/sh -c "cd / && ./run.sh"
    else
      log "Running without proot (no isolation)"
      (cd "$tmpdir" && ./run.sh)
    fi
  else
    log "No run.sh in bundle"
    return 3
  fi
}

usage() { cat <<EOF
Usage: agent.sh command [args]
Commands:
  verify <bundle.zip>    - verify signature
  run <bundle.zip>       - verify then run in sandbox
  upload <bundle.zip>    - upload bundle to server
  fetchpub                - download public key if RDCR_PUBKEY_URL set
EOF
}

case "$1" in
  verify) download_pubkey; verify_signature "$2" ;; 
  run) download_pubkey; verify_signature "$2" && run_in_sandbox "$2" ;; 
  upload) upload_bundle "$2" ;; 
  fetchpub) download_pubkey ;; 
  *) usage ;; 
esac

