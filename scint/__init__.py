from scint.base.settings import Settings

settings = Settings()
settings.load_json("settings/server.json", "library")
settings.load_json("settings/providers.json", "library")
settings.load_json("settings/library.json", "library")
settings.load_json("settings/studio.json", "library")
