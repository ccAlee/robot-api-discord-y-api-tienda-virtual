import os
from typing import Callable, TypeVar

from discord.ext import commands

import yaml

from exceptions import *

T = TypeVar("T")


def is_owner() -> Callable[[T], T]:

    async def predicate(context: commands.Context) -> bool:
        with open(f"{os.path.realpath(os.path.dirname(__file__))}/../config.yml") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        permission_ids = data['permissions_ids']
        for permission_id in permission_ids:
            if context.author.id not in data['permissions_ids']:
                raise UserNotOwner
        return True

    return commands.check(predicate)
