import fortnitepy
import os
import sys
import asyncio
import fortnite_api
import json
import webserver
from fortnitepy.ext import commands

if sys.platform == 'win32':
    asyncio.set_event_loop(asyncio.ProactorEventLoop())
else:
    try:
        import uvloop
    except ModuleNotFoundError:
        pass
    else:
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

api = fortnite_api.FortniteAPI()

with open("config.json", "r") as file:
    config = json.load(file)


email = config["bot"]["email"]
password = config["bot"]["password"]
owner = config["bot"]["owners"]
filename = 'device_auths.json'


def get_device_auth_details():
    if os.path.isfile(filename):
        with open(filename, 'r') as fp:
            return json.load(fp)
    return {}


def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open(filename, 'w') as fp:
        json.dump(existing, fp)


device_auth_details = get_device_auth_details().get(email, {})
client = commands.Bot(
    command_prefix='!',
    auth=fortnitepy.AdvancedAuth(
        email=email,
        prompt_authorization_code=True,
        delete_existing_device_auths=True,
        **device_auth_details
    )
)


@client.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)


@client.event
async def event_ready():
    print(f"""----------------
                Bot ready as
         {client.user.display_name}
              ----------------""")


@client.event
async def event_friend_request(request):
    await request.accept()


@client.event
async def event_party_invite(invitation):
    if invitation.sender.display_name in owner:
        print(f"Joined {invitation.sender.display_name}'s party")
        await invitation.accept()


@client.command()  # This is a test command
async def test(ctx):
    await ctx.send('test')


webserver.run()
if config["bot"]["password"] != "" and config["bot"]["email"] != "":
    client.run()
