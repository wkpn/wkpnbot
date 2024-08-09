# Changelog

## 2.2.0 - August 9th, 2024

### Changed

- Update typings and imports.
- Update `aiogram` to 3.11.0.
- Update `cachetools` to 5.4.0.
- Update `orjson` to 3.10.7.
- Update `tomlkit` to 0.13.0.

## 2.1.0 - July 8th, 2024

### Added

- Additional checks for `my_chat_member` updates.
- Inline button for `edited_message` that shows on what date the message was edited.
- `/privacy` command that shows a link to the Privacy Policy.
- `supervisor` config (`configs/supervisor.conf`).

### Changed

- Update typings and imports.
- Update `aiogram` to 3.10.0.
- Update `orjson` to 3.10.6.

### Removed

- `DEFAULT_EMOJI` for new forum topics.

## 2.0.0 - June 24th, 2024

### Added

- Full support of [aiogram](https://github.com/aiogram) v3.
- `pyproject.toml` support.
- Webhook configuration script (`configure_webhook.py`).
- Webhook handler (`wkpnbot/webserver.py`)
- Docker deployment (`nginx` + `supervisor`).
- [Topics](https://telegram.org/blog/topics-in-groups-collectible-usernames#topics-in-groups) support.
- Messages reactions support.
- Replies support.
- Edited messages support.
