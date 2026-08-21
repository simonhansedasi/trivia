#!/bin/bash
set -e

DO="root@68.183.130.60"
DEST="$DO:/home/simonhans/coding/trivia"
SSH="ssh -i $HOME/.ssh/id_ed25519"

echo "Syncing to DO..."
rsync -av --checksum \
  -e "ssh -i $HOME/.ssh/id_ed25519" \
  --exclude='.git/' \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  --exclude='venv/' \
  ./ "$DEST"

echo "Installing dependencies..."
$SSH $DO "cd /home/simonhans/coding/trivia && python3 -m venv venv && venv/bin/pip install -q -r requirements.txt"

echo "Installing service..."
$SSH $DO "cp /home/simonhans/coding/trivia/trivia.service /etc/systemd/system/trivia.service && systemctl daemon-reload && systemctl enable trivia && systemctl restart trivia && systemctl is-active trivia"

echo "Done. If first deploy, run on DO:"
echo "  cp /home/simonhans/coding/trivia/nginx_trivia.conf /etc/nginx/sites-enabled/trivia"
echo "  nginx -t && systemctl reload nginx"
