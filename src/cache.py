import os
import json
import requests
from datetime import datetime

class Cache:
    def __init__(self, filepath, refresh_cache_url, cache_lifetime):
        self.__filepath = filepath
        self.__refresh_cache_url = refresh_cache_url
        self.__cache_lifetime = cache_lifetime

        self.data = dict()
        print("Getting token info...")
        self.load_cache()

    def load_cache(self):
        if not os.path.exists(self.__filepath):
            self.refresh_cache()
        else:
            ok = False
            with open(self.__filepath, "r", encoding="utf-8") as file:
                buffer = file.read().strip()
                if buffer != "":
                    self.data = json.loads(buffer)
                    ok = True

            if (not ok) or ("last_update" not in self.data) or self.data["last_update"] + self.__cache_lifetime < int(datetime.now().timestamp()):
                self.refresh_cache()

    def refresh_cache(self):
        resp = requests.get(self.__refresh_cache_url)
        # Only write if the response is valid
        if resp.ok:
            ustr =  resp.content.decode("latin-1")
            self.data = json.loads(ustr)
            self.write_cache()

    def write_cache(self):
        with open(self.__filepath, "w") as file:
            self.data["last_update"] = int(datetime.now().timestamp())
            file.write(json.dumps(self.data))