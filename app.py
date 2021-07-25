from flask import Flask
import discord
import os
import aiomysql
import pathlib
from markupsafe import escape

app = Flask(__name__)

path = pathlib.PurePath()
root = path / "html"

@app.route("/")
async def lol():
  homepage = open(root / "index.html", 'r')
  return homepage.read()


@app.route("/<int:guildid>")
async def hello_world(guildid):
    conn = await aiomysql.connect(host=os.getenv('SQLserverhost'),
                                      user=os.getenv('SQLusername'),
                                      password=os.getenv('SQLpassword'),
                                      db=os.getenv('SQLdatabase'),
                                      autocommit=True)
    async with conn.cursor() as db:
        await db.execute('''SELECT tagname,tagcontent FROM tags WHERE guildid = %s''', (guildid,))
        factoids = await db.fetchall()
    factoids_and_contents_list = []
    if factoids:
        for tag in factoids:
          complete_factoid_info = f"The tag <code>{escape(tag[0])}</code> has the contents <code>{escape(tag[1])}</code>"
          factoids_and_contents_list.append(complete_factoid_info)
        return "<br>".join(factoids_and_contents_list)

        
    else:
        nothere = open(root / "nothere.html", 'r')
        return nothere.read()