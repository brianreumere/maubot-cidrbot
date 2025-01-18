import os
import yaml

with open("maubot.yaml") as f:
    maubot = yaml.safe_load(f)
maubot["version"] = os.environ["BOT_VERSION"]
with open("maubot.yaml", "w") as f:
    yaml.safe_dump(maubot, f)
