from parameters import SPACING_CHAR

"""
Make sure not to use the following token names or downstream issues will occur:
'time'
'age'
'round'
'game_id''text'
"""
places = ['first','second','third','fourth']
end_result_template = r'.*?is (?P<{place}>.*?) as (?P<{place}_seat>\w+?) \((?P<{place}_score>\d+?) pts\)'

journal_phrases = {
    'game_name': r'game (?P<game_name>.*?) created',
    'game_end': ''.join([end_result_template.format(place=place) for place in places]),
    'impact': r'impact of (?P<impact_name>\w+)',
#     'production': fr'end turn[{SPACING_CHAR}]+?.*?(?P<player>\w+?) scores:'\
#         r'.*?(?P<food_gen>\d+?) food - consumption: (?P<consumption>\d+?) \(now (?P<food>\d+?)\)'\
#         r'.*?(?P<resource_gen>\d+?) resources \(now (?P<resource>\d+?)\)'\
#         r'.*?(?P<culture_gen>\d+?) culture \(now (?P<culture>\d+?)\)'\
#         r'.*?(?P<science_gen>\d+?) science \(now (?P<science>\d+?)\)'\
#         f'[{SPACING_CHAR}]+?',
    'production_food': fr'end turn[{SPACING_CHAR}]+?.*?(?P<player>\w+?) scores:'\
        r'.*?(?P<food_gen>\d+?) food - consumption: (?P<consumption>\d+?) \(now (?P<food>\d+?)\)'\
        fr'.*?[{SPACING_CHAR}]+?',
    'production_resources': fr'end turn[{SPACING_CHAR}]+?.*?(?P<player>\w+?) scores:'\
        r'.*?(?P<resource_gen>\d+?) resources \(now (?P<resource>\d+?)\)'\
        fr'.*?[{SPACING_CHAR}]+?',
    'production_culture': fr'end turn[{SPACING_CHAR}]+?.*?(?P<player>\w+?) scores:'\
        r'.*?(?P<culture_gen>\d+?) culture \(now (?P<culture>\d+?)\)'\
        fr'.*?[{SPACING_CHAR}]+?',
    'production_science': fr'end turn[{SPACING_CHAR}]+?.*?(?P<player>\w+?) scores:'\
        r'.*?(?P<science_gen>\d+?) science \(now (?P<science>\d+?)\)'\
        fr'.*?[{SPACING_CHAR}]+?',
    'aggression': r'(?P<attacker>\w+) plays (?P<aggression>.*?) against (?P<target>\w+)',
    'aggression_success': 'concedes defeat',
    'aggression_fail' : r'(?P<target>.*?) defends',
    'war': r'(?P<attacker>\w+) declares war over (?P<war>.*?) on (?P<target>\w+)',
    'war_resolution': fr'(?P<player>\w+?) wins (?P<war>.*?)[{SPACING_CHAR}]'\
        r'attacker.s strength: (?P<attack>\d+) defender.s strength: (?P<defense>\d+)',
    'territory': fr'(?P<player>\w+) wins (?P<territory>.*?)[{SPACING_CHAR}]'\
        r'winning bid is (?P<bid>\d+)',
    'card_takes': r'(?P<player>\w+) takes (?P<card>.*?) in hand',
    'discovers_technology': fr'(?P<player>\w+) discovers (?P<technology>\w+?)[{SPACING_CHAR}]+?'\
        r'.+? loses (?P<science>\d+) science',
    'builds': r'(?P<player>\w+) builds (?P<worker>\w+?)'\
        r'.+? spends (?P<resources>\d+) resource',
    'upgrades': fr'(?P<player>\w+) upgrades (?P<worker>\w+?)[{SPACING_CHAR}]',
    'event': r'(?P<player>\w+?) plays event.*?scores (?P<event_age>\d+?) culture',
    'tactics': fr'(?P<player>\w+?) (?P<action>.+?) tactics[{SPACING_CHAR}]+?'\
        fr'(?P<tactic_age>\w+?) / (?P<tactic>.*?)[{SPACING_CHAR}]+?',
    'population': r'(?P<player>\w+?) increases population.*? spends (?P<food>\d+?) food',
    'destroys': fr'(?P<player>\w+?) destroys (?P<unit>.*?)[{SPACING_CHAR}]+?',
    'disbands': fr'(?P<player>\w+?) disbands (?P<unit>.*?)[{SPACING_CHAR}]+?',
    'treaty': fr'(?P<player>\w+?) proposes (?P<treaty>.*?) to (?P<recipient>\w+?)[{SPACING_CHAR}].*?(?P<a>\w+?) is A',
    'treaty_response': fr'(?P<player>\w+?) (?P<response>\w+?) .*?offer[{SPACING_CHAR}]+?',
    'leader_elects': fr'(?P<player>\w+?) elects (?P<leader>.*?)[{SPACING_CHAR}]+?'
}