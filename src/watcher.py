# Updated
import discord

from commonbot.user import UserLookup

import db
from client import client


class Watcher:
    def __init__(self):
        self.watchlist = [x[0] for x in db.get_watch_list()]
        self.ul = UserLookup()

    def should_note(self, id: int) -> bool:
        return id in self.watchlist

    def remove_user(self, id: int):
        if id in self.watchlist:
            db.del_watch(id)
            self.watchlist.remove(id)

    async def watch_user(self, mes: discord.Message, _):
        userid = self.ul.parse_id(mes)
        if not userid:
            await mes.channel.send("Мені не вдалося знайти користувача в цьому повідомленні")
            return

        db.add_watch(userid)
        self.watchlist.append(userid)

        username = self.ul.fetch_username(client, userid)
        await mes.channel.send(f"{username} додано до списку відстеження. :spy:")

    async def unwatch_user(self, mes: discord.Message, _):
        userid = self.ul.parse_id(mes)
        if not userid:
            await mes.channel.send("Мені не вдалося знайти користувача в цьому повідомленні")
            return
        elif userid not in self.watchlist:
            await mes.channel.send("...Цього користувача не відстежують")
            return

        self.remove_user(userid)

        username = self.ul.fetch_username(client, userid)
        await mes.channel.send(f"{username} видалено зі списку відстежування.")

    async def get_watchlist(self, mes: discord.Message, _):
        if len(self.watchlist) == 0:
            await mes.channel.send("Немає відстежуваних користувачів")
            return

        output = "```"
        for userid in self.watchlist:
            username = self.ul.fetch_username(client, userid)
            if username:
                output += f"{username} ({userid})\n"
            else:
                # If we couldn't find them, just prune them
                self.remove_user(userid)

        output += "```"

        await mes.channel.send(output)
