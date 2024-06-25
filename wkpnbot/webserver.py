import argparse
import sys

from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application
)
from aiohttp import web

from wkpnbot.db import DBClient
from wkpnbot.dispatcher import create_bot_and_dispatcher


if sys.version_info < (3, 11):
    import tomlkit as toml
else:
    # python3.11+ has a builtin tomllib module
    import tomllib as toml


def build_app(config_file: str, env: str) -> web.Application:
    with open(config_file, mode="rb") as f:
        config = toml.load(f)

    bot_conf = config["bot"]
    db_conf = config["database"]
    wh_conf = config["webhook"]

    db = DBClient.from_project_key(
        base_url=db_conf["base_url"],
        project_key=db_conf[env]["project_key"]
    )

    bot, dp = create_bot_and_dispatcher(
        bot_token=bot_conf[env]["bot_token"],
        db=db,
        forum_id=bot_conf[env]["forum_id"],
        messages_table=db_conf["messages"],
        topics_table=db_conf["topics"]
    )

    app = web.Application()

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=wh_conf["secret_token"]
    ).register(app, path=wh_conf["path"])

    setup_application(app, dp, bot=bot)

    return app


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--config-file", type=str, required=True)
    parser.add_argument("--env", type=str, required=False, default="prod")
    parser.add_argument("--path", type=str, required=True)

    args = parser.parse_args()

    web.run_app(build_app(args.config_file, args.env), path=args.path, access_log=None)


if __name__ == "__main__":
    main()
