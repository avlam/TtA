from pathlib import Path

root = Path.cwd()
locations = {
    'reports': root.joinpath('reports'),
    'analysis': root.joinpath('analysis'),
    'staging': root.joinpath('staging'),
    'raw': root.joinpath('gamejournals')
    }

SPACING_CHAR = '#'