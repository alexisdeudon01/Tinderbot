# Tinderbot

A Home Assistant add-on that automates Tinder swiping and messaging.

## Installation

1. Navigate to **Settings → Add-ons → Add-on Store** in Home Assistant.
2. Click the **⋮** menu (top-right) and select **Repositories**.
3. Add this repository URL:
   ```
   https://github.com/alexisdeudon01/Tinderbot
   ```
4. Find **Tinderbot** in the add-on store and click **Install**.

## Configuration

| Option | Type | Default | Description |
|---|---|---|---|
| `auth_token` | `str` | *(required)* | Your Tinder API authentication token. |
| `auto_like` | `bool` | `true` | Automatically like (swipe right on) recommended profiles. |
| `daily_like_limit` | `int` | `100` | Maximum number of likes to send per run. |
| `send_message` | `bool` | `false` | Send a message automatically when a match is made. |
| `default_message` | `str` | `"Hey! 👋"` | The message to send on a new match (only used when `send_message` is `true`). |

### How to get your Tinder auth token

1. Open Tinder in a browser and log in.
2. Open the browser developer tools (F12) and go to the **Network** tab.
3. Look for any request to `api.gotinder.com` and copy the value of the `X-Auth-Token` header.
4. Paste that value into the `auth_token` option.

## Usage

1. Set your `auth_token` in the add-on **Configuration** tab.
2. Adjust `daily_like_limit` and other options as desired.
3. Start the add-on from the **Info** tab.

The add-on will run through your Tinder recommendations, like profiles up to the daily limit, and optionally send your configured message to new matches.

## Support

For issues or feature requests, open an issue on [GitHub](https://github.com/alexisdeudon01/Tinderbot/issues).
