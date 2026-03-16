#!/usr/bin/env python3
"""Tinderbot - Home Assistant Add-on for automated Tinder interactions."""

import argparse
import logging
import time
import sys

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

TINDER_API_BASE = "https://api.gotinder.com"
HEADERS_TEMPLATE = {
    "X-Auth-Token": "",
    "Content-Type": "application/json",
    "User-Agent": "Tinder/11.4.0 (iPhone; iOS 12.4.1; Scale/2.00)",
}


def get_headers(auth_token: str) -> dict:
    headers = HEADERS_TEMPLATE.copy()
    headers["X-Auth-Token"] = auth_token
    return headers


def get_recommendations(auth_token: str) -> list:
    """Fetch a batch of profile recommendations from Tinder."""
    url = f"{TINDER_API_BASE}/v2/recs/core"
    try:
        response = requests.get(url, headers=get_headers(auth_token), timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("results", [])
    except requests.exceptions.HTTPError as exc:
        logger.error("Failed to fetch recommendations: %s", exc)
        return []


def like_profile(auth_token: str, user_id: str) -> dict:
    """Like (swipe right on) a profile by user ID."""
    url = f"{TINDER_API_BASE}/like/{user_id}"
    try:
        response = requests.get(url, headers=get_headers(auth_token), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as exc:
        logger.error("Failed to like profile %s: %s", user_id, exc)
        return {}


def send_message(auth_token: str, match_id: str, message: str) -> bool:
    """Send a message to a match."""
    url = f"{TINDER_API_BASE}/v2/matches/{match_id}/messages"
    payload = {"message": message}
    try:
        response = requests.post(
            url, json=payload, headers=get_headers(auth_token), timeout=10
        )
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as exc:
        logger.error("Failed to send message to match %s: %s", match_id, exc)
        return False


def run_bot(
    auth_token: str,
    auto_like: bool,
    daily_like_limit: int,
    should_message: bool,
    default_message: str,
) -> None:
    """Main bot loop."""
    likes_sent = 0
    logger.info("Tinderbot is running. Daily like limit: %d", daily_like_limit)

    while likes_sent < daily_like_limit:
        recommendations = get_recommendations(auth_token)

        if not recommendations:
            logger.info("No recommendations available. Waiting 60 seconds...")
            time.sleep(60)
            continue

        for rec in recommendations:
            if likes_sent >= daily_like_limit:
                logger.info("Daily like limit (%d) reached.", daily_like_limit)
                break

            user = rec.get("user", {})
            user_id = user.get("_id")
            name = user.get("name", "Unknown")

            if not user_id:
                continue

            if auto_like:
                result = like_profile(auth_token, user_id)
                likes_sent += 1
                logger.info("Liked profile: %s (%s) [%d/%d]", name, user_id, likes_sent, daily_like_limit)

                match_id = result.get("match", {}).get("_id")
                if should_message and match_id:
                    if send_message(auth_token, match_id, default_message):
                        logger.info("Sent message to match: %s", name)

                # Respect Tinder rate limiting (≥1 s between likes)
                time.sleep(1)

    logger.info("Tinderbot finished. Total likes sent today: %d", likes_sent)


def parse_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() in ("true", "1", "yes")


def main() -> None:
    parser = argparse.ArgumentParser(description="Tinderbot Home Assistant Add-on")
    parser.add_argument("--auth-token", required=True, help="Tinder API auth token")
    parser.add_argument("--auto-like", default="true", help="Automatically like profiles")
    parser.add_argument("--daily-like-limit", type=int, default=100, help="Maximum likes per day")
    parser.add_argument("--send-message", default="false", help="Send a message on match")
    parser.add_argument("--default-message", default="Hey! 👋", help="Default message to send on match")
    args = parser.parse_args()

    run_bot(
        auth_token=args.auth_token,
        auto_like=parse_bool(args.auto_like),
        daily_like_limit=args.daily_like_limit,
        should_message=parse_bool(args.send_message),
        default_message=args.default_message,
    )


if __name__ == "__main__":
    main()
