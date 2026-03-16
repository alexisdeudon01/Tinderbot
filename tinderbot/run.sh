#!/usr/bin/env bash
set -e

CONFIG_PATH=/data/options.json

AUTH_TOKEN=$(jq --raw-output '.auth_token // ""' "$CONFIG_PATH")
AUTO_LIKE=$(jq --raw-output '(.auto_like // true) | tostring' "$CONFIG_PATH")
DAILY_LIKE_LIMIT=$(jq --raw-output '.daily_like_limit // 100' "$CONFIG_PATH")
SEND_MESSAGE=$(jq --raw-output '(.send_message // false) | tostring' "$CONFIG_PATH")
DEFAULT_MESSAGE=$(jq --raw-output '.default_message // "Hey! 👋"' "$CONFIG_PATH")

if [ -z "$AUTH_TOKEN" ]; then
    echo "[ERROR] auth_token is not set. Please configure your Tinder API token in the add-on options."
    exit 1
fi

echo "[INFO] Starting Tinderbot..."
echo "[INFO] Auto-like: $AUTO_LIKE"
echo "[INFO] Daily like limit: $DAILY_LIKE_LIMIT"
echo "[INFO] Send message on match: $SEND_MESSAGE"

exec python3 /tinderbot.py \
    --auth-token "$AUTH_TOKEN" \
    --auto-like "$AUTO_LIKE" \
    --daily-like-limit "$DAILY_LIKE_LIMIT" \
    --send-message "$SEND_MESSAGE" \
    --default-message "$DEFAULT_MESSAGE"
