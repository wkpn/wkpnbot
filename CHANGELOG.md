# Changelog

## 2.3.1 - August 16th, 2024

### Changed

- `DBClient.fetch_many` now always returns a list.
- Small refactoring for dispatcher configuration.

### Fixed

- `/wipe` command not working due to `DBClient.fetch_many` returning `None`.

## 2.3.0 - August 16th, 2024

### Added

- `/wipe` command to delete current forum topic and messages data from the database.
- `DBClient.delete`, `DBClient.delete_many`, `DBClient.fetch_many` methods for database client.
- `CallbackQuery` support for `TopicsManagementMiddleware`.
- Additional `content_type` checks for `FilterMiddleware`.
- Additional database check before constructing `reply_parameters` in `MessagesMiddleware`.
- Support for deleting messages with a special premium reaction (forum only).

### Changed

- Update typings and imports.
- Update `aiogram` to 3.12.0.
- Update `tomlkit` to 0.13.2.
- Update `DBClient` attribute names.

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

- Full support of [aiogram](https://github.com/aiogram/aiogram) v3.
- `pyproject.toml` support.
- Webhook configuration script (`configure_webhook.py`).
- Webhook handler (`wkpnbot/webserver.py`)
- Docker deployment (`nginx` + `supervisor`).
- [Topics](https://telegram.org/blog/topics-in-groups-collectible-usernames#topics-in-groups) support.
- Messages reactions support.
- Replies support.
- Edited messages support.
