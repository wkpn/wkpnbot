import asyncio
import argparse
import sys

from aiogram import Bot


if sys.version_info < (3, 11):
    import tomlkit as toml
else:
    # python3.11+ has a builtin tomllib module
    import tomllib as toml


async def configure(config_file: str, env: str) -> None:
    with open(config_file, mode="rb") as f:
        config = toml.load(f)

    bot_conf = config["bot"]
    bot_token = bot_conf[env]["bot_token"]

    wh_conf = config["webhook"]
    webhook_url = f"{wh_conf['host']}/{wh_conf['path']}"
    secret_token = wh_conf["secret_token"]
    allowed_updates = wh_conf["allowed_updates"]

    async with Bot(token=bot_token) as bot:
        bot_info = await bot.me()

        print(
            f"ID: {bot_info.id}",
            f"Name: {bot_info.first_name}",
            f"Username: {bot_info.username}",
            sep="\n"
        )

        assert await bot.set_webhook(
            url=webhook_url,
            allowed_updates=allowed_updates,
            secret_token=secret_token
        )

        await asyncio.sleep(1.0)

        webhook_info = await bot.get_webhook_info()

        assert webhook_info.url == webhook_url
        assert sorted(webhook_info.allowed_updates) == sorted(allowed_updates)

        print(
            f"Webhook URL: {webhook_info.url}",
            f"Webhook IP: {webhook_info.ip_address}",
            sep="\n"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--config-file", type=str, required=True)
    parser.add_argument("--env", type=str, required=False, default="prod")

    args = parser.parse_args()

    asyncio.run(configure(args.config_file, args.env))
