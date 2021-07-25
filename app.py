impoty flask
import discord
import os
import aiomysql
import pathlib
import dotenv
from markupsafe import escape
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized


dotenv.load_dotenv()
app = flask.Flask(__name__)
app.secret_key = os.getenv('secret_key')
path = pathlib.PurePath()
root = path / "html"
app.config["DISCORD_CLIENT_ID"] = os.getenv('app_id')   # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = os.getenv('client_secret')
app.config["DISCORD_REDIRECT_URI"] = os.getenv('redirect_uri')
app.config["DISCORD_BOT_TOKEN"] = os.getenv('bot_token')  

discord = DiscordOAuth2Session(app)

def contents(file) -> str:
  with open(root / file) as file:
    return file.read()

@app.route("/<path:path>")
async def serve_old_site(path):
  return flask.send_from_directory('static', path)

@app.route("/jolteon/")
async def root_directory_serv():
  homepage = open(root / "index.html", 'r')
  return homepage.read()


@app.route("/jolteon/<int:guildid>")
async def hello_world(guildid):
    if type(guildid) != int:
        nothere = open(root / "nothere.html", 'r')
        return nothere.read()
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
          complete_factoid_info = f'''<tr>
          <td>{tag[0]}</td>
          <td>{tag[1]}</td>
          </tr>'''
          factoids_and_contents_list.append(complete_factoid_info)
          
        return contents("tagslist-top.html").replace('[[guildid]]', str(guildid)) + "".join(factoids_and_contents_list) + contents("tagslist-bottom.html")

        
    else:
        nothere = open(root / "nothere.html", 'r')
        return nothere.read()

@app.route("/jolteon/invite")
async def bot_invite_redirect():
  redirect = open(root / "invite.html", 'r')
  return redirect.read()

@app.route("/jolteon/login/")
def login():
    return discord.create_session()


@app.route("/jolteon/callback/")
def callback():
    discord.callback()
    user = discord.fetch_user()
    return redirect(url_for(".me"))


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("/login"))


@app.route("/jolteon/me/")
@requires_authorization
def me():
    user = discord.fetch_user()
    return f"""
    <html>
        <head>
            <title>{user.name}</title>
        </head>
        <body>
            <img src='{user.avatar_url}' />
        </body>
    </html>"""

