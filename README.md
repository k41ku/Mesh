# Mesh

![Python](https://img.shields.io/badge/python-3.x-blue)

Maps social circles from Instagram mutual follows.

Two people who follow each other are "friends." A group where everyone is friends with everyone else is a circle. Mesh finds those circles around a target account and shows you the overlapping social structure that isn't visible from a follower list alone.

> [!NOTE]
> Everything is subject to change. Nothing is final. This tool is in active development.

## Example output

Target: target_user

```
Profile info: target_user (Target User)
follower count:  87
following count: 94
friends:
alice
bob
carol
dave

Circle 1:
target_user
alice
bob
carol

Circle 2:
target_user
dave
erin
```

Alice, bob and carol all follow each other and the target - one circle.
Dave and erin form a separate cluster.

## Install

```bash
git clone https://github.com/k41ku/Mesh
cd Mesh
pip install -r requirements.txt
```

## Usage

```bash
python script.py
```

Use -h if you need any help.

> [!CAUTION]
> It is currently reccomended to log in with sessionID (--sessionid).
> How? Pull the sessionid cookie from instagram.com in a logged-in browser (DevTools > Application > Cookies)

| Flag | Description |
|------|-------------|
| `-V`, `--verbose` | Show progress for every request |
| `-v`, `--version` | Show version and check for updates |
| `-L`, `--level` | How deep to traverse [1] |
| `-mx`, `--max-follows` | Skip targets above this follower/following count [100] |
| `--country` | Account's country code [US] |
| `--locale` | Account's locale [en_US] |
| `--sessionid` | Log in with a session ID instead of a password |

> [!NOTE]
> As of now, -L / --level flag does nothing. Will fix soon.

## Known limitations

**Login is unreliable.** Instagram frequently rejects username/password logins from unrecognised devices, returning a misleading "incorrect password" error. --sessionid is more likely to work.

**Rate limits are aggressive.** Each friend costs three API calls with delays between them. A target with 30 friends takes several minutes.

Private accounts can't be analysed unless you follow them.

## Roadmap

- [x] Mutual follow detection
- [x] Circle detection
- [ ] non-mutual-follow based circles + Confidence levels
- [ ] SVG output
- [ ] Multi-account rotation 

## Disclaimer

For educational and research purposes. Only analyse accounts you have permission to analyse. Automated access violates Instagram's Terms of Service - use at your own risk.


