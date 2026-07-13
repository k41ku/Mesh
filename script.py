local_version = "0.0.1"
from instagrapi import Client
from instagrapi import exceptions
import getpass

# --- arguments ---
import argparse
parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description="Mesh by k41ku\nOSINT tool made to discover social circles of people of interest based of Instagram \"friends\" (mutual follow between multiple people)")

parser.add_argument("-V", "--verbose", action="store_true", help="enable verbose output (currently does nothing)")
parser.add_argument("-v", "--version", action="store_true", help="show version")
parser.add_argument("-L", "--level", type=int, default=1, help="Set how deep this tool will go [1]")
parser.add_argument("-mx", "--max-follows", type=int, default=100, help="Max followers/following before target is skipped [100]")
parser.add_argument("--country", default="US", help="Account's country code [US]")
parser.add_argument("--locale", default="en_US", help="Account's locale [en_US]")

args = parser.parse_args()

# version + mismatch check
import requests
if args.version:
  print(f"Version: {local_version}\nMade by: k41ku\nGithub repo: https://github.com/k41ku/Mesh")
  exit()

r = requests.get("https://raw.githubusercontent.com/k41ku/Mesh/master/script.py")
newest_version = r.text.splitlines()[0].split('"')[1]
if local_version != newest_version:
  print(f"Your installed version ({local_version}) does not match the newest version ({newest_version}). If something doesnt work, try updating first - run: git pull")

# level
if args.level < 1:
  print("Invalid level. Level must be more or equal to 1!")
  exit()

# --- debug mode --- (will get removed in final ?)
debug_mode = input("do you want to enable debug mode? (y/n) ")
if debug_mode != "y":
  import sys
  import os

  sys.stderr = open(os.devnull, 'w')
else:
  print("debug mode enabled")

# verbose
def log(msg):
  if args.verbose:
    print(msg)

# --- login ---
cl = Client()
cl.set_country(args.country)
cl.set_locale(args.locale)
cl.delay_range = [2, 5]
username = input("Enter your username: \n")
password = getpass.getpass("Enter your password: ")

log("> Trying to log in...")
while True:
  try:
    cl.login(username, password)
    cl.get_timeline_feed()
    log("> Login succesful.")
    break
  except exceptions.BadPassword:
    log("> Login failed.")
    log(cl.last_json)
    password = getpass.getpass("Invalid password. try again: \n")
  except exceptions.UnknownError:
    log("> Login failed.")
    username = input("A account with this username doesnt exist. Try again: \n")
  except exceptions.ChallengeRequired:
    log("> Login failed.")
    input("In the app, confirm \"I tried to log in\" then press Enter to continue")
    cl.challenge_resolve(cl.last_json)
    break

print("logged in! \n")
target = input("Enter target username:\n")
log(f"> Fetching user ID for {target}...")
target_id = cl.user_id_from_username(target)
log(f"> Fetching info for {target} ({target_id})...")
user = cl.user_info(target_id)
if user.following_count > args.max_follows or user.follower_count > args.max_follows:
  print("Target has more than maximum limit followers or following. To increase this limit, use the --max_follows flag.")
  exit()
  
log(f"> Fetching {target} followers...")
followers = cl.user_followers(target_id)
follower_usernames = [user.username for user in followers.values()]
log(f"> Fetching {target} following...")
following = cl.user_following(target_id)
following_usernames = [user.username for user in following.values()]
log("> Checking target profile private status...")
if user.is_private:
  print(f"{target} profile is private and you dont follow it.")
  exit()

print(f"Profile info: {target}\n({user.full_name})\n\nfollower count:  {user.follower_count}\nfollowing count: {user.following_count}\nfriends:")
log(f"> Creating {target} friends list...")
friends = list(set(following_usernames) & set(follower_usernames))
print("\n".join(friends))
circles = {}
for secondary in friends:
  if secondary == target:
    continue
  sec_id = cl.user_id_from_username(secondary)
  sec_followers = [u.username for u in cl.user_followers(sec_id).values()]
  sec_following = [u.username for u in cl.user_following(sec_id).values()]
  circles[secondary] = list(set(sec_followers) & set(sec_following))
