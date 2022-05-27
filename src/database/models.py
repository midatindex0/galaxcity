from dataclasses import dataclass
from typing import Optional

import discord

@dataclass()
class User:
    id: int
    level: int
    tries: int
    score: int
    user: Optional[discord.User] = None