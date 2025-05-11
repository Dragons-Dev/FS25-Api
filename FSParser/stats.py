import requests

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

__all__ = ["fetch_dedi_info", "fetch_dedi_settings"]

last_checked: dict[str, list] = {}


def _utils_guess_type(value: str):
    try:
        if value.isdigit():
            return int(value)
        if "." in value and value.replace(".", "").isdigit():
            return float(value)
        if value.lower() in ["true", "false"]:
            return True if value.lower() == "true" else False
        else:
            return value
    except Exception as e:
        print(f"Error in _utils_guess_type: {e}")
        print(f"Failed guessing type of: {value}")
        return value


def _requester(url: str) -> str | None:
    if url in last_checked:
        if datetime.now() - last_checked[url][0] <= timedelta(seconds=59):
            return last_checked[url][1]
    data = requests.get(url)
    if data.status_code != 200:
        print("Error: Unable to fetch data from the server.")
        return None
    last_checked[url] = [datetime.now(), data.text]
    return data.text


def fetch_dedi_info() -> dict | None:
    data = _requester(
        "http://thedragons.xyz:7999/feed/dedicated-server-stats.xml?code=fea187b4599d71757ff4f3b6e3435852"
    )
    if data is None:
        return None
    info_dict = {}
    root = ET.fromstring(data)
    info_dict["server"] = {}
    info_dict["server"]["game"] = root.get("game")
    info_dict["server"]["version"] = root.get("version")
    info_dict["server"]["name"] = root.get("name")
    info_dict["server"]["mapname"] = root.get("mapName")
    for x in root:
        if x.tag == "Slots":
            info_dict["players"] = {}
            info_dict["players"]["capacity"] = x.get("capacity")
            info_dict["players"]["usage"] = x.get("numUsed")
            for index, y in enumerate(x):
                if True if y.get("isUsed") == "true" else False:
                    info_dict["players"][str(index)] = {}
                    info_dict["players"][str(index)]["name"] = y.text
                    info_dict["players"][str(index)]["admin"] = (
                        True if y.get("isAdmin") == "true" else False
                    )
                    info_dict["players"][str(index)]["uptime"] = int(y.get("uptime"))
                    info_dict["players"][str(index)]["coordinates"] = {}
                    try:
                        info_dict["players"][str(index)]["coordinates"]["x"] = float(
                            y.get("x")
                        )
                        info_dict["players"][str(index)]["coordinates"]["y"] = float(
                            y.get("y")
                        )
                        info_dict["players"][str(index)]["coordinates"]["z"] = float(
                            y.get("z")
                        )
                    except TypeError:
                        pass
                else:
                    pass
        elif x.tag == "Mods":
            info_dict["mods"] = {}
            for index, y in enumerate(x):
                info_dict["mods"][str(index)] = {}
                info_dict["mods"][str(index)]["name"] = y.text
                info_dict["mods"][str(index)]["author"] = y.get("author")
                info_dict["mods"][str(index)]["version"] = y.get("version")
        elif x.tag == "Farmlands":
            info_dict["farmlands"] = {}
            for y in x:
                info_dict["farmlands"][str(y.get("name"))] = {}
                info_dict["farmlands"][str(y.get("name"))]["owner"] = int(
                    y.get("owner")
                )
                info_dict["farmlands"][str(y.get("name"))]["area"] = float(
                    y.get("area")
                )
                info_dict["farmlands"][str(y.get("name"))]["price"] = int(
                    y.get("price")
                )
                info_dict["farmlands"][str(y.get("name"))]["isField"] = False
        elif x.tag == "Fields":
            for y in x:
                info_dict["farmlands"][str(y.get("id"))]["isField"] = True
    return info_dict


def fetch_dedi_settings() -> dict | None:
    data = requests.get(
        "http://thedragons.xyz:7999/feed/dedicated-server-savegame.html?code=fea187b4599d71757ff4f3b6e3435852&file=careerSavegame"
    )
    if data.status_code != 200:
        print("Error: Unable to fetch data from the server.")
        return None

    info_dict = {}
    root = ET.fromstring(data.text)
    for i in root:
        if i.tag == "settings":
            info_dict["settings"] = {}
            for j in i:
                info_dict["settings"][j.tag] = _utils_guess_type(j.text)
        elif i.tag == "statistics":
            info_dict["statistics"] = {}
            for j in i:
                if j.tag == "money":
                    info_dict["statistics"]["money"] = _utils_guess_type(j.text)
                if j.tag == "playTime":
                    info_dict["statistics"]["playTime"] = timedelta(
                        minutes=_utils_guess_type(j.text)
                    ).total_seconds()
    return info_dict


if __name__ == "__main__":
    infos = fetch_dedi_info()
    settings = fetch_dedi_settings()
    import json

    print(json.dumps(infos, indent=4))
    print(json.dumps(settings, indent=4))
    #
    # with open("../info.json", "w") as f:
    #    json.dump(infos, f, indent=4)
