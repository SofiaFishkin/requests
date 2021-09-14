import requests
import json

def search_superhero_info(hero_name, access_token="2619421814940190"):
    url = f"https://www.superheroapi.com/api.php/{access_token}/search/"
    response = requests.get(url + hero_name)
    resp_map = json.loads(response.text)
    if resp_map['response'] != "success":
        error_descr = resp_map.get("error")
        print(f"Ошибка: {error_descr}")
        return None
    else:
        search_results = resp_map['results']
        for hero_info in search_results:
            if hero_info['name'].lower() == hero_name.lower():
                simple_info = {
                    "name": hero_info['name'], "intelligence": int(hero_info['powerstats']['intelligence'])
                }
                return simple_info

def measure_intelligence(heroes:list):
    most_intel_hero = ("", 0)
    for hero_name in heroes:
        info = search_superhero_info(hero_name)
        if info == None:
            continue
        if info['intelligence'] > most_intel_hero[1]:
            most_intel_hero = (info['name'], info['intelligence'])
        print(f"{hero_name}'s intelligence is {info['intelligence']}")
    print(f'The most intelligent superhero is {most_intel_hero[0]} with {most_intel_hero[1]} score')

heroes = ["Hulk", "Thanos", "Captain America"]
measure_intelligence(heroes)