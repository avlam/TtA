from pathlib import Path

root = Path.cwd()
locations = {
    'reports': root.joinpath('reports'),
    'analysis': root.joinpath('analysis'),
    'staging': root.joinpath('staging'),
    'raw': root.joinpath('gamejournals')
    }

manual_files = [
    root.joinpath('game_id_list.csv')
]

generated_files = [
    
]

SPACING_CHAR = '#'