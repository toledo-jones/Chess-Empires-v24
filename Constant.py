import os
import random
import time

import pygame

#
#   INIT LOGIC
#
#
#   COLORS
#
GOLD = pygame.Color('gold')
DARK_ORANGE = pygame.Color('dark orange')
WHITE = pygame.Color('white')
BLACK = pygame.Color('black')
BLUE = pygame.Color('blue')
RED = pygame.Color('red')

MENU_COLOR = pygame.Color((72, 61, 139))
LIGHT_SQUARE_COLOR = pygame.Color((238, 232, 170))
DARK_SQUARE_COLOR = pygame.Color((222, 184, 135))

UNUSED_PIECE_HIGHLIGHT_COLOR = pygame.Color((248, 127, 0))
SELF_SQUARE_HIGHLIGHT_COLOR = BLUE
MOVE_SQUARE_HIGHLIGHT_COLOR = pygame.Color((72, 61, 139))

ICON_COLORS = {0: 'w', 1: 'b'}
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
win.fill(MENU_COLOR)
LOGO_COLOR = ICON_COLORS[random.randint(0, 1)]
MAIN_MENU_LOGO = pygame.transform.scale(
    pygame.image.load(os.path.join("files/images", LOGO_COLOR + "_game_name.png")), (400, 400))
LOGO_POSITION = (pygame.display.Info().current_w // 2 - 200, pygame.display.Info().current_h // 2 - 400)
win.blit(MAIN_MENU_LOGO, LOGO_POSITION)
pygame.display.update()
time.sleep(2)
VERSION = "a"
NUMBER = "v0.024"
MAX_FPS = 120
BOARD_HEIGHT_PX = pygame.display.Info().current_h
SQ_SIZE = BOARD_HEIGHT_PX // 10
BOARD_HEIGHT_SQ = BOARD_HEIGHT_PX // SQ_SIZE
BOARD_WIDTH_SQ = 12
BOARD_WIDTH_PX = BOARD_WIDTH_SQ * SQ_SIZE
SIDE_MENU_WIDTH = pygame.display.Info().current_w - BOARD_WIDTH_PX

#
#   GAMEPLAY MECHANIC SETTINGS
#


DEBUG_START = False
DEBUG_STARTING_PRAYER = 12
DEBUG_STARTING_WOOD = 99
DEBUG_STARTING_GOLD = 99
DEBUG_STARTING_STONE = 99
DEBUG_STARTING_PIECES = ['castle', 'rogue_rook', 'king']
DEBUG_RITUALS = False
PLAY_AGAINST_AI = False
BOARD_STARTS_WITH_RESOURCES = True

'DEFAULT START'
STARTING_PRAYER = 0
STARTING_WOOD = 0
STARTING_GOLD = 0
STARTING_STONE = 0
STARTING_PIECES = ['castle', 'king']

SELECTABLE_STARTING_PIECES = ['pawn', 'builder', 'monk', 'pikeman', 'rogue_pawn', 'wall']
NUMBER_OF_STARTING_PIECES = 5
MONOLITH_RITUALS = ['gold_general', 'create_resource', 'smite', 'swap', 'destroy_resource', 'teleport', 'line_destroy', 'protect', ]
PRAYER_STONE_RITUALS = ['destroy_resource', 'create_resource', 'teleport', 'swap', 'protect']
STEALING_KEY = {'building': {
    'wood': {'variance': (-2, 2), 'value': 4},
    'gold': {'variance': (-2, 2), 'value': 4},
    'stone': {'variance': (-2, 2), 'value': 4}},
    'piece': {
        'wood': {'variance': (-2, 2), 'value': 4},
        'gold': {'variance': (-2, 2), 'value': 4},
        'stone': {'variance': (-2, 2), 'value': 4}}}

MAX_MONOLITH_RITUALS_PER_TURN = 3
MAX_PRAYER_STONE_RITUALS_PER_TURN = 3

STABLE_SPAWN_LIST = ['doe', 'oxen', 'unicorn', 'ram', 'elephant', 'knight']
FORTRESS_SPAWN_LIST = ['rogue_rook', 'rogue_bishop', 'rogue_knight', 'rogue_pawn']
CASTLE_SPAWN_LIST = ['pawn', 'builder', 'pikeman', 'monk', 'persuader', 'jester']
BUILDER_SPAWN_LIST = ['quarry_1', 'wall', 'stable', 'monolith', 'castle', 'barracks', 'fortress']
BARRACKS_SPAWN_LIST = ['duke', 'queen', 'champion', 'rook', 'bishop']

SPAWN_LISTS = {'stable': STABLE_SPAWN_LIST, 'fortress': FORTRESS_SPAWN_LIST, 'castle': CASTLE_SPAWN_LIST,
               'builder': BUILDER_SPAWN_LIST, 'barracks': BARRACKS_SPAWN_LIST, }

DEFAULT_ACTIONS_REMAINING = 1
ACTIONS_UPDATE_ON_SPAWN = False
MINING_COSTS_ACTION = False
PRAYING_COSTS_ACTION = False
STEALING_COSTS_ACTION = False
PERSUADE_COSTS_ACTION = True


CASTLE_ADDITIONAL_ACTIONS = 0
BARRACKS_ADDITIONAL_ACTIONS = 0
FORTRESS_ADDITIONAL_ACTIONS = 0
STABLE_ADDITIONAL_ACTIONS = 0
MONOLITH_ADDITIONAL_ACTIONS = 0
PRAYER_STONE_ADDITIONAL_ACTIONS = 0

DEFAULT_PIECE_LIMIT = 3
PIECE_COSTS = {'king': {'log': 999, 'gold': 999, 'stone': 999},
               'gold_general': {'log': 0, 'gold': 0, 'stone': 0},
               'quarry_1': {'log': 3, 'gold': 0, 'stone': 0},
               'pawn': {'log': 6, 'gold': 0, 'stone': 0},
               'builder': {'log': 6, 'gold': 0, 'stone': 0},
               'monk': {'log': 6, 'gold': 0, 'stone': 1},
               'pikeman': {'log': 0, 'gold': 4, 'stone': 4},
               'castle': {'log': 10, 'gold': 0, 'stone': 0},
               'stable': {'log': 10, 'gold': 0, 'stone': 10},
               'barracks': {'log': 0, 'gold': 10, 'stone': 0},
               'fortress': {'log': 0, 'gold': 12, 'stone': 12},
               'queen': {'log': 0, 'gold': 14, 'stone': 14},
               'rook': {'log': 0, 'gold': 6, 'stone': 6},
               'bishop': {'log': 6, 'gold': 6, 'stone': 0},
               'knight': {'log': 1, 'gold': 0, 'stone': 3},
               'jester': {'log': 0, 'gold': 12, 'stone': 0},
               'rogue_rook': {'log': 0, 'gold': 14, 'stone': 14},
               'rogue_bishop': {'log': 9, 'gold': 9, 'stone': 0},
               'rogue_knight': {'log': 0, 'gold': 9, 'stone': 0},
               'rogue_pawn': {'log': 6, 'gold': 0, 'stone': 0},
               'elephant': {'log': 6, 'gold': 0, 'stone': 6},
               'ram': {'log': 6, 'gold': 0, 'stone': 6},
               'unicorn': {'log': 12, 'gold': 0, 'stone': 12},
               'monolith': {'log': 0, 'gold': 0, 'stone': 15},
               'prayer_stone': {'log': 0, 'gold': 0, 'stone': 4},
               'duke': {'log': 6, 'gold': 14, 'stone': 15},
               'oxen': {'log': 12, 'gold': 0, 'stone': 12},
               'champion': {'log': 0, 'gold': 9, 'stone': 9},
               'wall': {'log': 0, 'gold': 0, 'stone': 3},
               'persuader': {'log': 0, 'gold': 20, 'stone': 0},
               'doe': {'log': 14, 'gold': 0, 'stone': 14},
               }
# HOW TO ACCESS:
# for line in Constant.DESCRIPTIONS['piece']
# print(line)
# Constant.DESCRIPTIONS['piece'][description_line_index]
DESCRIPTIONS = {'king': ['every player gets one', 'capture your opponent\'s to win'],
                'gold_general': ['summons the strongest piece imaginable'],
                'quarry_1': ['can be mined for stone', 'may cave in and begin to yield less stone',
                             'cannot be dug onto a depleted quarry'],
                'pawn': ['can mine resources'],
                'builder': ['can create buildings'],
                'monk': ['can pray at monoliths and prayer Stones'],
                'pikeman': ['attacks and defends all surrounding squares', 'a useful defender'],
                'castle': ['creates basic pieces, such as pawns'],
                'stable': ['creates leapers, such as the knight'],
                'barracks': ['creates basic attacking pieces', 'a staple in any good kingdom'],
                'fortress': ['creates rogue pieces who', 'can move through forest tiles and',
                             'steal from enemy pieces'],
                'queen': ['attacks in all directions as far as the eye can see'],
                'rook': ['attacks orthogonally and has the', 'ability to pray'],
                'bishop': ['attacks diagonally and has the', 'ability to pray'],
                'knight': ['a simple leaper who moves up two and over one'],
                'jester': ['cannot capture but', 'moves like a queen and any piece or', 'building nearby cannot act'],
                'rogue_rook': ['a rook who can move through the forest', 'and can steal from enemy pieces'],
                'rogue_bishop': ['a bishop who can move through the forest', 'and can steal from enemy pieces'],
                'rogue_knight': ['a knight who can move through the forest', 'and can steal from enemy pieces'],
                'rogue_pawn': ['a pawn who can move through the forest', 'and can steal from nearby pieces'],
                'oxen': ['moves like a knight, then like a rook'],
                'champion': ['moves diagonally one square', 'then like a rook in that same direction'],
                'elephant': ['a leaper who moves up three and over one', 'and who also moves like a knight'],
                'ram': ['a leaper who moves like a knight, then like a bishop'],
                'unicorn': ['a leaper who moves like a knight ', 'and can double jump'],
                'monolith': ['a strange, powerful prayer site'],
                'prayer_stone': ['a strange prayer site'],
                'duke': ['moves like a queen', 'but has the ability to pray'],
                'smite': ['select one piece or building to be destroyed'],
                'destroy_resource': ['select one resource to be destroyed'],
                'create_resource': ['create a resource'],
                'wall': ['blocks pieces from passing through', 'can be destroyed by units in the stable or pikeman'],
                'teleport': ['teleport a piece anywhere else on the board'],
                'swap': ['trade places with another piece'],
                'line_destroy': ['destroys everything in it\'s path'],
                'protect': ['protects a square from capture or destruction'],
                'doe': ['moves like a knight and a bishop'],
                'persuader': ['can convert the color of nearby pieces']
                }

PIECE_POPULATION = {'king': 1,
                    'queen': 2,
                    'rook': 1,
                    'bishop': 1,
                    'knight': 1,
                    'pawn': 1,
                    'castle': 0,
                    'duke': 1,
                    'rogue_bishop': 1,
                    'jester': 1,
                    'rogue_rook': 1,
                    'war_tower': 0,
                    'elephant': 1,
                    'pikeman': 1,
                    'champion': 1,
                    'gold_general': 6,
                    'silver_general': 1,
                    'elephant_cart': 1,
                    'flag': 0,
                    'barracks': 0,
                    'rogue_pawn': 1,
                    'monolith': 0,
                    'prayer_stone': 0,
                    'monk': 1,
                    'fortress': 0,
                    'rogue_knight': 1,
                    'builder': 1,
                    'quarry_1': 0,
                    'stable': 0,
                    'unicorn': 1,
                    'ram': 1,
                    'oxen': 1,
                    'wall': 0,
                    'doe': 1,
                    'persuader': 1}

PRAYER_COSTS = {'gold_general': {'prayer': 12, 'monk': 3},
                'smite': {'prayer': 8, 'monk': 1},
                'destroy_resource': {'prayer': 8, 'monk': 0},
                'create_resource': {'prayer': 4, 'monk': 0},
                'teleport': {'prayer': 4, 'monk': 0},
                'swap': {'prayer': 2, 'monk': 0},
                'line_destroy': {'prayer': 8, 'monk': 1},
                'protect': {'prayer': 1, 'monk': 0}}

ADDITIONAL_PIECE_LIMIT = {'castle': 5, 'barracks': 3, 'fortress': 3, 'stable': 3,
                          'king': 0,
                          'queen': 0,
                          'rook': 0,
                          'bishop': 0,
                          'knight': 0,
                          'pawn': 0,
                          'monk': 0,
                          'jester': 0,
                          'silver_general': 0,
                          'gold_general': 0,
                          'pikeman': 0,
                          'champion': 0,
                          'rogue_rook': 0,
                          'rogue_bishop': 0,
                          'rogue_knight': 0,
                          'rogue_pawn': 0,
                          'elephant': 0,
                          'elephant_cart': 0,
                          'monolith': 2,
                          'prayer_stone': 1,
                          'wall': 0,
                          'flag': 0,
                          'duke': 0,
                          'war_tower': 0,
                          'quarry_1': 0,
                          'builder': 0,
                          'unicorn': 0,
                          'ram': 0,
                          'oxen': 0,
                          'doe': 0,
                          'persuader': 0}
TOTAL_GOLD_ON_MAP = 6

WOOD_TOTAL_MINED = 1
GOLD_TOTAL_MINED = 6
QUARRY_TOTAL_MINED = 6
DEPLETED_QUARRY_TOTAL_MINED = 0
SUNKEN_QUARRY_TOTAL_MINED = 1

WOOD_VARIANCE = (-2, 2)
GOLD_VARIANCE = (-3, 1)
STONE_VARIANCE = (-2, 2)

WOOD_YIELD_PER_HARVEST = 7
GOLD_YIELD_PER_HARVEST = 9
STONE_YIELD_PER_HARVEST = 8
SUNKEN_QUARRY_YIELD_PER_HARVEST = 1
DEPLETED_QUARRY_YIELD_PER_HARVEST = 0

PRAYER_STONE_YIELD = 1
MONOLITH_YIELD = 2
ADDITIONAL_PRAYER_FROM_MONK = 2
ADDITIONAL_MINING_FROM_ROGUE = {'wood': -2, 'stone': -3, 'gold': -2}

RESOURCE_KEY = {'gold_tile_1': 'gold', 'quarry_1': 'stone',
                'sunken_quarry_1': 'stone', 'tree_tile_1': 'wood',
                'tree_tile_2': 'wood', 'tree_tile_3': 'wood',
                'tree_tile_4': 'wood', 'log': 'wood', 'gold': 'gold', 'stone': 'stone'}

MASTER_COST_LIST = ['builder', 'castle', 'stable', 'barracks', 'fortress', 'monolith']

FACTION_NAMES = ['clique', 'coterie', 'cabal', 'bloc', 'camp', 'grouping',
                 'side', 'division', 'wing', 'section', 'countrymen', 'squad', 'faction',
                 'company', 'troupe', 'set', 'army', 'party', 'gang', 'selection', 'crew',
                 'corps', 'lineup', 'sect', 'band', 'color']
rand = random.randint(0, len(FACTION_NAMES) - 1)
FACTION = FACTION_NAMES[rand]
rand = random.randint(0, 2)

#
#   INTRO TEXT COLOR
#
if rand == 0:
    INTRO_TEXT_COLOR = WHITE
else:
    INTRO_TEXT_COLOR = BLACK
turn_to_color = {'w': WHITE, 'b': BLACK}
TURNS = {'w': 'b', 'b': 'w'}

#
#   MOVES
#


RIGHT = (0, 1)
LEFT = (0, -1)
UP = (-1, 0)
DOWN = (1, 0)
TWO_RIGHT = (0, 2)
TWO_LEFT = (0, -2)
TWO_UP = (-2, 0)
TWO_DOWN = (2, 0)
THREE_RIGHT = (0, 3)
THREE_LEFT = (0, -3)
THREE_UP = (-3, 0)
THREE_DOWN = (3, 0)
UP_RIGHT = (-1, 1)
DOWN_LEFT = (1, -1)
DOWN_RIGHT = (1, 1)
UP_LEFT = (-1, -1)
TWO_UP_LEFT = (-2, -1)
TWO_LEFT_UP = (-1, -2)
TWO_UP_RIGHT = (-2, 1)
TWO_RIGHT_UP = (-1, 2)
TWO_DOWN_RIGHT = (2, 1)
TWO_RIGHT_DOWN = (1, 2)
TWO_DOWN_LEFT = (2, -1)
TWO_LEFT_DOWN = (1, -2)
THREE_UP_LEFT = (-3, -1)
THREE_LEFT_UP = (-1, -3)
THREE_UP_RIGHT = (-3, 1)
THREE_RIGHT_UP = (-1, 3)
THREE_DOWN_RIGHT = (3, 1)
THREE_RIGHT_DOWN = (1, 3)
THREE_DOWN_LEFT = (3, -1)
THREE_LEFT_DOWN = (1, -3)


#
#   GRAPHICS / UX
#
DEFAULT_PIECE_SCALE = (SQ_SIZE, SQ_SIZE)
HIGHLIGHT_ALPHA = 110

SPAWNING_MENU_WIDTH = round(SQ_SIZE * 5.5)
SPAWNING_MENU_HEIGHT_BUFFER = SQ_SIZE * 1.3
SIDE_MENU_HEIGHT = BOARD_HEIGHT_PX
GAME_NAME_SCALE = (round(SQ_SIZE * 2.2), round(SQ_SIZE * 2.2))
PICKAXE_SCALE = (SQ_SIZE * 2, SQ_SIZE * 2)
CENTER_X = BOARD_WIDTH_SQ * SQ_SIZE // 2 + SQ_SIZE // 2
CENTER_Y = BOARD_HEIGHT_SQ * SQ_SIZE // 2
START_MENU_WIDTH = round(SQ_SIZE * 6.5)
START_MENU_HEIGHT = round(SQ_SIZE * 3.5)
PRAYER_BAR_WIDTH = round(SQ_SIZE // 64)
PRAYER_BAR_END_WIDTH = round(SQ_SIZE // 6)
PRAYER_BAR_HEIGHT = round(SQ_SIZE // 2.8)
PRAYER_BAR_SCALE = (PRAYER_BAR_WIDTH, PRAYER_BAR_HEIGHT)
PRAYER_BAR_END_SCALE = (PRAYER_BAR_END_WIDTH, PRAYER_BAR_HEIGHT)
TREE_SCALE_1 = (round(SQ_SIZE * 1.3), round(SQ_SIZE * 1.3))
TREE_SCALE_2 = (round(SQ_SIZE * 1.38), round(SQ_SIZE * 1.38))
TREE_SCALE_3 = (round(SQ_SIZE * 1.35), round(SQ_SIZE * 1.35))
TREE_SCALE_4 = (round(SQ_SIZE * 1.38), round(SQ_SIZE * 1.38))
GOLD_SCALE = (round(SQ_SIZE * 1.1), round(SQ_SIZE * 1.1))
QUARRY_SCALE = (round(SQ_SIZE * 1.1), round(SQ_SIZE * 1.1))
TREE_OFFSET = (round(SQ_SIZE // -5.5), round(SQ_SIZE // -3.5))
GOLD_OFFSET = (round(SQ_SIZE // -10), round(SQ_SIZE // -10))
CASTLE_SCALE = round(SQ_SIZE * 1.1), round(SQ_SIZE * 1.1)
CASTLE_OFFSET = (0, -10)
MENU_ICON_DEFAULT_SCALE = (SQ_SIZE // 2, SQ_SIZE // 2)
BARRACKS_SCALE = (round(SQ_SIZE * 1.2), round(SQ_SIZE * 1.2))
BARRACKS_OFFSET = (0, -10)
PAWN_MENU_ICON_SCALE = (100, 100)
FORTRESS_SCALE = (round(SQ_SIZE * 1.15), round(SQ_SIZE * 1.15))
FORTRESS_OFFSET = (0, -10)
WALL_OFFSET = (-10, -10)
PRAYER_RITUAL_SCALE = (round(SQ_SIZE * 1.5), round(SQ_SIZE * 1.5))
BOAT_PIECE_SCALE = round(SQ_SIZE * 1.5), round(SQ_SIZE * 1.5)
RESOURCES_BUTTON_SCALE = (SIDE_MENU_WIDTH, 2 * SQ_SIZE)
YES_BUTTON_SCALE = (round(SQ_SIZE * .8), round(SQ_SIZE * .8))
NO_BUTTON_SCALE = (round(SQ_SIZE * .8), round(SQ_SIZE * .8))
PROTECT_SQUARE_SCALE = (SQ_SIZE, SQ_SIZE)
PROTECT_SQUARE_OFFSET = (SQ_SIZE // 2 - PROTECT_SQUARE_SCALE[0] // 2, SQ_SIZE // 2 - PROTECT_SQUARE_SCALE[1] // 2)
#
#   IMAGES / FILES
#
w_pieces = ['w_king',
            'w_queen',
            'w_rook',
            'w_bishop',
            'w_knight',
            'w_pawn',
            'w_monk',
            'w_duke',
            'w_rogue_bishop',
            'w_jester',
            'w_pikeman',
            'w_gold_general',
            'w_silver_general',
            'w_rogue_rook',
            'w_elephant',
            'w_elephant_cart',
            'w_champion',
            'w_rogue_pawn',
            'w_rogue_knight',
            'w_builder',
            'w_unicorn',
            'w_ram',
            'w_oxen',
            'w_persuader',
            'w_doe']
w_buildings = ['w_castle',
               'w_fortress',
               'w_barracks',
               'w_wall',
               'w_monolith',
               'w_prayer_stone',
               'w_flag',
               'w_barracks',
               'w_war_tower',
               'w_stable']
b_pieces = ['b_king', 'b_queen', 'b_rook', 'b_bishop',
            'b_knight', 'b_pawn', 'b_monk', 'b_duke',
            'b_rogue_bishop', 'b_jester', 'b_pikeman',
            'b_gold_general', 'b_silver_general',
            'b_rogue_rook', 'b_elephant', 'b_elephant_cart',
            'b_champion', 'b_rogue_pawn', 'b_rogue_knight',
            'b_builder', 'b_unicorn', 'b_ram', 'b_oxen',
            'b_persuader', 'b_doe']
b_buildings = ['b_castle', 'b_fortress', 'b_barracks',
               'b_wall', 'b_monolith', 'b_prayer_stone',
               'b_flag', 'b_barracks', 'b_war_tower', 'b_stable']
w_prayer_rituals = ['w_gold_general', 'w_smite', 'w_destroy_resource', 'w_create_resource', 'w_teleport',
                    'w_swap', 'w_line_destroy', 'w_protect']
b_prayer_rituals = ['b_gold_general', 'b_smite', 'b_destroy_resource', 'b_create_resource', 'b_teleport', 'b_swap',
                    'b_line_destroy', 'b_protect']
images = ['icon', 'pickaxe', 'w_game_name', 'b_game_name', 'prayer', 'gold_coin', 'log', 'action', 'prayer_bar_end',
          'units', 'prayer', 'prayer_bar', 'stone', 'w_boat', 'b_boat', 'hour_glass', 'hammer', 'axe',
          'resources_button',
          'b_no', 'b_yes', 'w_no', 'w_yes', 'b_protect', 'w_protect', 'steal', 'persuade']
music = ['music']
resources = ['gold_tile_1',
             'tree_tile_1',
             'tree_tile_2',
             'tree_tile_3',
             'tree_tile_4',
             'quarry_1',
             'sunken_quarry_1',
             'depleted_quarry_1']
menu_icons = ['gold_coin',
              'log',
              'stone',
              'prayer']
sounds = []
RITUAL_IMAGE_MODIFY = {'gold_general': {'SCALE': PRAYER_RITUAL_SCALE, 'OFFSET': (0, 0)},
                       'smite': {'SCALE': PRAYER_RITUAL_SCALE, 'OFFSET': (0, 0)},
                       'destroy_resource': {'SCALE': PRAYER_RITUAL_SCALE, 'OFFSET': (0, 0)},
                       'create_resource': {'SCALE': PRAYER_RITUAL_SCALE, 'OFFSET': (0, 0)},
                       'teleport': {'SCALE': PRAYER_RITUAL_SCALE, 'OFFSET': (0, 0)},
                       'swap': {'SCALE': PRAYER_RITUAL_SCALE, 'OFFSET': (0, 0)},
                       'line_destroy': {'SCALE': PRAYER_RITUAL_SCALE, 'OFFSET': (0, 0)},
                       'protect': {'SCALE': PRAYER_RITUAL_SCALE, 'OFFSET': (0, 0)}}

PIECE_IMAGE_MODIFY = {'king': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'queen': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'rook': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'bishop': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'knight': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'pawn': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'monk': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'duke': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'rogue_bishop': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'jester': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'pikeman': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'gold_general': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'silver_general': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'rogue_rook': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'elephant': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'elephant_cart': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'champion': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'rogue_pawn': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'rogue_knight': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'castle': {'SCALE': CASTLE_SCALE, 'OFFSET': CASTLE_OFFSET},
                      'fortress': {'SCALE': FORTRESS_SCALE, 'OFFSET': FORTRESS_OFFSET},
                      'wall': {'SCALE': FORTRESS_SCALE, 'OFFSET': WALL_OFFSET},
                      'monolith': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'prayer_stone': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'flag': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'barracks': {'SCALE': BARRACKS_SCALE, 'OFFSET': BARRACKS_OFFSET},
                      'war_tower': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'builder': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'unicorn': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'ram': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'stable': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'oxen': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'doe': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      'persuader': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                      }

IMAGES_IMAGE_MODIFY = {'icon': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                       'pickaxe': {'SCALE': PICKAXE_SCALE, 'OFFSET': (0, 0)},
                       'w_game_name': {'SCALE': GAME_NAME_SCALE, 'OFFSET': (0, 0)},
                       'b_game_name': {'SCALE': GAME_NAME_SCALE, 'OFFSET': (0, 0)},
                       'prayer': {'SCALE': PICKAXE_SCALE, 'OFFSET': (0, 0)},
                       'gold_coin': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                       'log': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                       'action': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                       'prayer_bar_end': {'SCALE': PRAYER_BAR_END_SCALE, 'OFFSET': (0, 0)},
                       'units': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                       'prayer_bar': {'SCALE': PRAYER_BAR_SCALE, 'OFFSET': (0, 0)},
                       'hour_glass': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                       'stone': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)},
                       'w_boat': {'SCALE': BOAT_PIECE_SCALE, 'OFFSET': (0, 0)},
                       'hammer': {'SCALE': PICKAXE_SCALE, 'OFFSET': (0, 0)},
                       'axe': {'SCALE': PICKAXE_SCALE, 'OFFSET': (0, 0)},
                       'b_boat': {'SCALE': BOAT_PIECE_SCALE, 'OFFSET': (0, 0)},
                       'resources_button': {'SCALE': RESOURCES_BUTTON_SCALE, 'OFFSET': (0, 0)},
                       'b_no': {'SCALE': NO_BUTTON_SCALE, 'OFFSET': (0, 0)},
                       'b_yes': {'SCALE': YES_BUTTON_SCALE, 'OFFSET': (0, 0)},
                       'w_no': {'SCALE': NO_BUTTON_SCALE, 'OFFSET': (0, 0)},
                       'w_yes': {'SCALE': YES_BUTTON_SCALE, 'OFFSET': (0, 0)},
                       'w_protect': {'SCALE': PROTECT_SQUARE_SCALE, 'OFFSET': PROTECT_SQUARE_OFFSET},
                       'b_protect': {'SCALE': PROTECT_SQUARE_SCALE, 'OFFSET': PROTECT_SQUARE_OFFSET},
                       'persuade': {'SCALE': PICKAXE_SCALE, 'OFFSET': (0,0)},
                       'steal': {'SCALE': PICKAXE_SCALE, 'OFFSET': (0, 0)}}

RESOURCES_IMAGE_MODIFY = {'gold_tile_1': {'SCALE': GOLD_SCALE, 'OFFSET': GOLD_OFFSET},
                          'tree_tile_1': {'SCALE': TREE_SCALE_1, 'OFFSET': TREE_OFFSET},
                          'tree_tile_2': {'SCALE': TREE_SCALE_2, 'OFFSET': TREE_OFFSET},
                          'tree_tile_3': {'SCALE': TREE_SCALE_3, 'OFFSET': TREE_OFFSET},
                          'tree_tile_4': {'SCALE': TREE_SCALE_4, 'OFFSET': TREE_OFFSET},
                          'quarry_1': {'SCALE': QUARRY_SCALE, 'OFFSET': (0, 0)},
                          'sunken_quarry_1': {'SCALE': QUARRY_SCALE, 'OFFSET': (0, 0)},
                          'depleted_quarry_1': {'SCALE': QUARRY_SCALE, 'OFFSET': (0, 0)}}

MENU_ICONS_IMAGE_MODIFY = {'gold_coin': {'SCALE': MENU_ICON_DEFAULT_SCALE, 'OFFSET': (0, 0)},
                           'log': {'SCALE': MENU_ICON_DEFAULT_SCALE, 'OFFSET': (0, 0)},
                           'stone': {'SCALE': MENU_ICON_DEFAULT_SCALE, 'OFFSET': (0, 0)},
                           'prayer': {'SCALE': DEFAULT_PIECE_SCALE, 'OFFSET': (0, 0)}}
PRAYER_RITUALS = {}
IMAGES = {}
RESOURCES = {}
MENU_ICONS = {}
W_PIECES = {}
W_BUILDINGS = {}
B_PIECES = {}
B_BUILDINGS = {}
MUSIC = {}

ambience = []
for i in range(6):
    ambience.append(i)
building_spawning = []
for i in range(6):
    building_spawning.append(i)
captures = []
for i in range(62):
    captures.append(i)
harvesting_rock = []
for i in range(63):
    harvesting_rock.append(i)
harvesting_wood = []
for i in range(36):
    harvesting_wood.append(i)
moves = []
for i in range(118):
    moves.append(i)
piece_spawning = []
for i in range(16):
    piece_spawning.append(i)
purchase = []
for i in range(25):
    purchase.append(i)
rituals = []
for i in range(54):
    rituals.append(i)

generate_resources = []
for i in range(12):
    generate_resources.append(i)

pray = []
for i in range(19):
    pray.append(i)

change_turn = []
for i in range(8):
    change_turn.append(i)

start_game = []
for i in range(4):
    start_game.append(i)
BUILDING_SPAWNING_SOUNDS = {}
CAPTURE_SOUNDS = {}
HARVESTING_ROCK_SOUNDS = {}
HARVESTING_WOOD_SOUNDS = {}
MOVE_SOUNDS = {}
PIECE_SPAWNING_SOUNDS = {}
PURCHASE_SOUNDS = {}
PRAYER_RITUAL_SOUNDS = {}
GENERATE_RESOURCES_SOUNDS = {}
PRAY_SOUNDS = {}
CHANGE_TURN_SOUNDS = {}
START_GAME_SOUNDS = {}


def load_sounds():
    for i in building_spawning:
        filename = str(0) + str(building_spawning[i])
        BUILDING_SPAWNING_SOUNDS[i] = pygame.mixer.Sound(
            os.path.join("files/sounds/building_spawning", filename + '.wav'))

    for i in captures:
        filename = str(0) + str(captures[i])
        CAPTURE_SOUNDS[i] = pygame.mixer.Sound(os.path.join("files/sounds/captures", filename + '.wav'))

    for i in harvesting_rock:
        filename = str(0) + str(harvesting_rock[i])
        HARVESTING_ROCK_SOUNDS[i] = pygame.mixer.Sound(
            os.path.join("files/sounds/harvesting_rock", filename + '.wav'))

    for i in harvesting_wood:
        filename = str(0) + str(harvesting_wood[i])
        HARVESTING_WOOD_SOUNDS[i] = pygame.mixer.Sound(
            os.path.join("files/sounds/harvesting_wood", filename + '.wav'))

    for i in moves:
        filename = str(0) + str(moves[i])
        MOVE_SOUNDS[i] = pygame.mixer.Sound(
            os.path.join("files/sounds/moves", filename + '.wav'))

    for i in piece_spawning:
        filename = str(0) + str(piece_spawning[i])
        PIECE_SPAWNING_SOUNDS[i] = pygame.mixer.Sound(
            os.path.join("files/sounds/piece_spawning", filename + '.wav'))

    for i in purchase:
        filename = str(0) + str(purchase[i])
        PURCHASE_SOUNDS[i] = pygame.mixer.Sound(
            os.path.join("files/sounds/purchase", filename + '.wav'))

    for i in generate_resources:
        filename = str(0) + str(generate_resources[i])
        GENERATE_RESOURCES_SOUNDS[i] = pygame.mixer.Sound(
            os.path.join("files/sounds/generate_resources", filename + '.wav'))

    for i in pray:
        filename = str(0) + str(pray[i])
        PRAY_SOUNDS[i] = pygame.mixer.Sound(
            os.path.join("files/sounds/pray", filename + '.wav'))

    for i in change_turn:
        filename = str(0) + str(change_turn[i])
        CHANGE_TURN_SOUNDS[i] = pygame.mixer.Sound(
            os.path.join("files/sounds/change_turn", filename + '.wav'))

    for i in start_game:
        filename = str(0) + str(start_game[i])
        START_GAME_SOUNDS[i] = pygame.mixer.Sound(
            os.path.join("files/sounds/start_game", filename + '.wav'))

    for i in rituals:
        filename = str(0) + str(rituals[i])
        PRAYER_RITUAL_SOUNDS[i] = pygame.mixer.Sound(
            os.path.join("files/sounds/rituals", filename + '.wav'))


def load_music():
    i = random.randint(0, len(ambience))
    filename = str(0) + str(i)
    pygame.mixer.music.load(os.path.join("files/music/ambience", filename + '.wav'))
    pygame.mixer.music.play()


def load_images():
    for image in images:
        scale = IMAGES_IMAGE_MODIFY[image]['SCALE']
        IMAGES[image] = pygame.transform.scale(pygame.image.load(os.path.join("files/images", image + ".png")),
                                               (scale[0], scale[1])).convert_alpha()
    for resource in resources:
        scale = RESOURCES_IMAGE_MODIFY[resource]['SCALE']
        RESOURCES[resource] = pygame.transform.scale(
            pygame.image.load(os.path.join("files/resources", resource + ".png")),
            (scale[0], scale[1])).convert_alpha()
    for menu_icon in menu_icons:
        scale = MENU_ICONS_IMAGE_MODIFY[menu_icon]['SCALE']
        MENU_ICONS[menu_icon] = pygame.transform.scale(
            pygame.image.load(os.path.join("files/menu_icons", menu_icon + ".png")),
            (scale[0], scale[1])).convert_alpha()

    for piece in w_pieces:
        scale = PIECE_IMAGE_MODIFY[piece_color_to_type(piece)]['SCALE']
        W_PIECES[piece] = pygame.transform.scale(pygame.image.load(os.path.join("files/pieces", piece + ".png")),
                                                 (scale[0], scale[1])).convert_alpha()
    for piece in w_buildings:
        scale = PIECE_IMAGE_MODIFY[piece_color_to_type(piece)]['SCALE']
        W_BUILDINGS[piece] = pygame.transform.scale(pygame.image.load(os.path.join("files/pieces", piece + ".png")),
                                                    (scale[0], scale[1])).convert_alpha()
    for piece in b_pieces:
        scale = PIECE_IMAGE_MODIFY[piece_color_to_type(piece)]['SCALE']
        B_PIECES[piece] = pygame.transform.scale(pygame.image.load(os.path.join("files/pieces", piece + ".png")),
                                                 (scale[0], scale[1])).convert_alpha()
    for piece in b_buildings:
        scale = PIECE_IMAGE_MODIFY[piece_color_to_type(piece)]['SCALE']
        B_BUILDINGS[piece] = pygame.transform.scale(pygame.image.load(os.path.join("files/pieces", piece + ".png")),
                                                    (scale[0], scale[1])).convert_alpha()

    for ritual in w_prayer_rituals:
        scale = RITUAL_IMAGE_MODIFY[piece_color_to_type(ritual)]['SCALE']
        PRAYER_RITUALS[ritual] = pygame.transform.scale(
            pygame.image.load(os.path.join("files/prayer_rituals", ritual + ".png")),
            (scale[0], scale[1])).convert_alpha()

    for ritual in b_prayer_rituals:
        scale = RITUAL_IMAGE_MODIFY[piece_color_to_type(ritual)]['SCALE']
        PRAYER_RITUALS[ritual] = pygame.transform.scale(
            pygame.image.load(os.path.join("files/prayer_rituals", ritual + ".png")),
            (scale[0], scale[1])).convert_alpha()


def piece_color_to_type(color_piece):
    return color_piece[2:]


def quarter_squares():
    top_left = []
    top_right = []
    bottom_left = []
    bottom_right = []
    x, y = board_max_index()
    minimum_row = 2
    maximum_row = y - 1
    for c in range(x + 1):
        for r in range(minimum_row, maximum_row):
            if c > x // 2 and r > y // 2:
                bottom_right.append((r, c))
            elif c < x // 2 and r > y // 2:
                bottom_left.append((r, c))
            elif c > x // 2 and r < y // 2:
                top_right.append((r, c))
            elif c < x // 2 and r < y // 2:
                top_left.append((r, c))

    return top_left, top_right, bottom_left, bottom_right


def center_squares():
    squares = []
    # x, y equal max val col, row
    x, y = board_max_index()

    for c in range(x // 2 + 1, x // 2 + 2):
        for r in range(y // 2, x // 2 + 2):
            square = (r, c)
            squares.append(square)
    return squares


def edge_squares():
    squares = []
    # x, y equal max val col, row
    x, y = board_max_index()
    for c in range(0, x + 1):
        for r in range(0, 3):
            square = (r, c)
            squares.append(square)
        for r in range(y - 2, y + 1):
            square = (r, c)
            squares.append(square)
    return squares


def starting_squares():
    w_starting_squares, b_starting_squares = [], []
    x, y = board_max_index()
    y_center = y // 2
    for c in range(0, 5):
        for r in range(y_center - 2, y_center + 4):
            square = (r, c)
            w_starting_squares.append(square)
    for c in range(x - 4, x + 1):
        for r in range(y_center - 2, y_center + 4):
            square = (r, c)
            b_starting_squares.append(square)
    return w_starting_squares, b_starting_squares


def board_max_index():
    x = BOARD_WIDTH_SQ - 1
    y = BOARD_HEIGHT_SQ - 1
    return x, y


def pos_in_bounds(pos):
    if BOARD_WIDTH_PX > pos[0] > 0 and BOARD_HEIGHT_PX > pos[1] > 0:
        return True
    else:
        return False


def tile_in_bounds(r, c):
    x, y = board_max_index()
    if c <= x and r <= y:
        if c >= 0 and r >= 0:
            return True
    else:
        return False


def convert_pos(pos):
    row = pos[1] // SQ_SIZE
    col = pos[0] // SQ_SIZE
    return row, col
