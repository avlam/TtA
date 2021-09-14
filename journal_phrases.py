from parameters import SPACING_CHAR

journal_phrases = {
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
    'aggression': r'(?P<attacker>\w+?) plays (?P<aggression>.*?) against (?P<target>\w+?)',
#     'aggression_resolution': ,
    'war': r'(?P<attacker>\w+?) declares war over (?P<war>.*?) on (?P<target>\w+?)',
#     'war_resolution': ,
    'card_takes': r'(?P<player>\w+?) takes (?P<card>.*?) in hand',
#     'card_plays': ,
    'discovers_technology': fr'(?P<player>\w+?) discovers (?P<technology>\w+?)[{SPACING_CHAR}]+?'\
        r'.+? loses (?P<science>\d+?) science',
    'builds': r'(?P<player>\w+?) builds (?P<worker>\w+?)'\
        r'.+? spends (?P<resources>\d+?) resource',
    'upgrades': r'(?P<player>\w+?) upgrades (?P<worker>\w+?)',
    'event': r'(?P<player>\w+?) plays event.*?scores (?P<event_age>\d+?) culture',
    'tactics': fr'(?P<player>\w+?) (?P<action>.+?) tactics[{SPACING_CHAR}]+?(?P<age>\w+?) / (?P<tactic>.*?)[{SPACING_CHAR}]+?',
    'population': r'(?P<player>\w+?) increases population.*? spends (?P<food>\d+?) food',
#     'destroy': ,
    'treaty': fr'(?P<player>\w+?) proposes (?P<treaty>.*?) to (?P<recipient>\w+?)[{SPACING_CHAR}].*?(?P<a>\w+?) is A',
    'treaty_response': fr'(?P<player>\w+?) (?P<response>\w+?) .*?offer[{SPACING_CHAR}]+?'
    'leader_elects': fr'(?P<player>\w+?) elects (?P<leader>.*?)[{SPACING_CHAR}]+?'
}