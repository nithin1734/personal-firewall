#!/usr/bin/env bash
# Usage: ./init-and-push.sh YOUR_GIT_REMOTE_URL
if [ -z "$1" ]; then
  echo "Usage: $0 git@github.com:USERNAME/REPO.git"
  exit 1
fi
git init
git add .
git commit -m "Initial commit: Personal firewall project"
git branch -M main
git remote add origin $1
git push -u origin main
