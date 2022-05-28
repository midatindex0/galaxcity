from motor.motor_asyncio import AsyncIOMotorClient

import discord

from .models import User


class Utils:
    @staticmethod
    def create_user(
        id: int,
        level: int = 1,
        tries: int = 0,
        score: int = 0,
        user: discord.User = None,
    ):
        return User(id=id, level=level, tries=tries, score=score, user=user)


class Database:
    def __init__(self, URI: str) -> None:
        self.URI = URI
        self.client = AsyncIOMotorClient(URI)
        self.db = self.client.main

    async def init_user(self, user: User):
        collection = self.db.users
        return await collection.insert_one(user.__dict__)

    async def update_user(self, user: User):
        collection = self.db.users
        return await collection.update_one({"id": user.id}, {"$set": user.__dict__})

    async def fetch_user(self, id: int):
        collection = self.db.users
        user = await collection.find_one({"id": id})
        if not user:
            return user
        return User(
            id=user["id"],
            level=user["level"],
            tries=user["tries"],
            score=user["score"],
            user=user["user"],
        )
