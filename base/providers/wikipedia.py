import requests, wikipediaapi


url = "https://example/..."
headers = {
    "User-Agent": "CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)"
}

response = requests.get(url, headers=headers)
wiki_wiki = wikipediaapi.Wikipedia("MyProjectName (merlin@example.com)", "en")
page_py = wiki_wiki.page("Python_(programming_language)")
print("Page - Exists: %s" % page_py.exists())
page_missing = wiki_wiki.page("NonExistingPageWithStrangeName")
print("Page - Exists: %s" % page_missing.exists())
page_py = wiki_wiki.page("Python_(programming_language)")
print(page_py.fullurl)
