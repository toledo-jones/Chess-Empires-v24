from Player import Player, AI
from State import *
from Tile import *


class Engine:
    def reset(self):
        self.running = False

    def __init__(self):
        self.running = True
        self.cols = Constant.BOARD_WIDTH_SQ
        self.rows = Constant.BOARD_HEIGHT_SQ
        self.board = [[0 for y in range(self.cols)] for x in range(self.rows)]
        for c in range(self.cols):
            for r in range(self.rows):
                self.board[r][c] = Tile(r, c)
        self.spawn_list = []
        self.turn = None
        self.first = True
        self.first_turn = True
        self.turn_count_display = .5
        self.turn_count_actual = -1
        self.spawn_count = 0
        self.spawn_success = False
        self.spawning = None
        self.ritual = None
        self.mining = False
        self.praying = False
        self.check = False
        self.final_spawn = False
        self.side_bar = None
        self.surrendering = False
        self.stealing = None
        self.menus = []
        self.state = []
        self.protected_tiles = []
        self.pins = []
        self.piece_cost_screen = False
        self.pieces_checking = []
        self.used_and_intercepted_pieces = []
        self.ritual_summon_resource = None
        self.monolith_rituals = []
        self.prayer_stone_rituals = []
        self.line_destroy_selected_range = None
        if Constant.DEBUG_RITUALS:
            self.prayer_stone_rituals.append(Constant.PRAYER_STONE_RITUALS)
            self.monolith_rituals.append(Constant.MONOLITH_RITUALS)
        else:
            self.monolith_rituals.append(self.generate_available_rituals(Constant.MONOLITH_RITUALS,
                                                                         Constant.MAX_MONOLITH_RITUALS_PER_TURN))
            self.prayer_stone_rituals.append(self.generate_available_rituals(Constant.PRAYER_STONE_RITUALS,
                                                                             Constant.MAX_PRAYER_STONE_RITUALS_PER_TURN))
        self.piece_stealing_offsets = []
        self.piece_stealing_offsets.append(self.generate_stealing_offsets(Constant.STEALING_KEY['piece']))

        self.building_stealing_offsets = []
        self.building_stealing_offsets.append(self.generate_stealing_offsets(Constant.STEALING_KEY['building']))

        self.events = []
        self.players = {}
        self.PIECES = {'king': King,
                       'queen': Queen,
                       'rook': Rook,
                       'bishop': Bishop,
                       'knight': Knight,
                       'pawn': Pawn,
                       'castle': Castle,
                       'monk': Monk,
                       'fortress': Fortress,
                       'ram': Ram,
                       'elephant': Elephant,
                       'barracks': Barracks,
                       'jester': Jester,
                       'champion': Champion,
                       'prayer_stone': PrayerStone,
                       'monolith': Monolith,
                       'pikeman': Pikeman,
                       'rogue_rook': RogueRook,
                       'rogue_bishop': RogueBishop,
                       'rogue_knight': RogueKnight,
                       'rogue_pawn': RoguePawn,
                       'builder': Builder,
                       'unicorn': Unicorn,
                       'stable': Stable,
                       'gold_general': GoldGeneral,
                       'duke': Duke,
                       'oxen': Oxen,
                       'wall': Wall,
                       'doe': Doe,
                       'persuader': Persuader,
                       }
        self.STATES = {'playing': Playing,
                       'ai playing': AIPlaying,
                       'mining': Mining,
                       'spawning': Spawning,
                       'starting': Starting,
                       'start spawn': StartingSpawn,
                       'piece cost screen': PieceCost,
                       'building': PreBuilding,
                       'winner': Winner,
                       'surrender': Surrender,
                       'gold_general': SummonGoldGeneral,
                       'smite': PerformSmite,
                       'select starting pieces': SelectStartingPieces,
                       'destroy_resource': PerformDestroyResource,
                       'create_resource': PerformCreateResource,
                       'teleport': PerformTeleport,
                       'swap': PerformSwap,
                       'line_destroy': PerformLineDestroy,
                       'protect': PerformProtect,
                       'main menu': MainMenu,
                       'debug': DebugStart,
                       'ai start spawn': AIStartingSpawn}
        self.RESOURCES = {'tree_tile_1': Wood, 'gold_tile_1': Gold,
                          'quarry_1': Quarry,
                          'tree_tile_2': Wood,
                          'tree_tile_3': Wood, 'tree_tile_4': Wood,
                          'sunken_quarry_1': SunkenQuarry,
                          'depleted_quarry_1': DepletedQuarry}
        self.MENUS = {'stable': StableMenu,
                      'fortress': FortressMenu,
                      'barracks': BarracksMenu,
                      'builder': BuilderMenu,
                      'castle': CastleMenu
                      }
        self.EVENTS = {'pray': Pray, 'steal': Steal, 'mine': Mine, 'spawn': Spawn, 'move': Move, 'capture': Capture}
        self.STEALING_VALUES = {'wood': 0, 'gold': 1, 'stone': 2}
        self.KIND_TO_STEALING_LIST = {'piece': self.piece_stealing_offsets, 'building': self.building_stealing_offsets}

    def stealing_values(self, resource, kind):
        offset_list = self.KIND_TO_STEALING_LIST[kind]
        offset = offset_list[self.turn_count_actual][self.STEALING_VALUES[resource]]
        base_value = Constant.STEALING_KEY[kind][resource]['value']
        value = base_value + offset
        enemy_player = self.players[Constant.TURNS[self.turn]]
        if resource == 'wood':
            if enemy_player.wood - value < 0:
                value = enemy_player.wood
        elif resource == 'gold':
            if enemy_player.gold - value < 0:
                value = enemy_player.gold
        elif resource == 'stone':
            if enemy_player.stone - value < 0:
                value = enemy_player.stone

        return value

    def create_ai(self, color):
        player = AI(color)
        self.players[color] = player

    def create_player(self, color):
        #
        #   Implements player profile which holds all current pieces the player has, has captured, gold, wood, etc
        #   Pulls from this player profile all data which is needed by the engine with regard to the players
        #   Started but incomplete...
        #
        player = Player(color)
        self.players[color] = player

    def set_state(self, state):
        #
        #   Accepts State Object and adds it to State List
        #
        if isinstance(state, State):
            self.state.append(state)

        #
        #   Accepts 'state' string and converts it to state Object. Then adds it to State List
        #
        else:
            new_state = self.STATES[state](self.state[-1].win, self)
            self.set_state(new_state)

        #
        #   Removes the first state in the list if the list reaches length of two
        #
        if len(self.state) == 2:
            del self.state[0]

    def is_start_spawn(self):
        if isinstance(self.state[-1], StartingSpawn):
            return True
        else:
            return False

    def valid_ritual(self, cost):
        #
        #   Check each value in the cost of the piece being spawned against
        #   the amount of that resource the player has
        #
        valid_prayer = self.players[self.turn].prayer - cost >= 0

        #
        #   If all three values are true then the function returns True
        #
        if valid_prayer:
            return True

    def valid_purchase(self, cost):
        #
        #   Check each value in the cost of the piece being spawned against
        #   the amount of that resource the player has
        #
        valid_wood = self.players[self.turn].wood - cost['log'] >= 0
        valid_gold = self.players[self.turn].gold - cost['gold'] >= 0
        valid_stone = self.players[self.turn].stone - cost['stone'] >= 0

        #
        #   If all three values are true then the function returns True
        #
        if valid_wood and valid_gold and valid_stone:
            return True

        #
        #   If all three values are not true the function returns False
        #
        else:
            return False

    def update_stealing_squares(self):
        for player in self.players:
            for piece in self.players[player].pieces:
                piece.update_stealing_squares(self)

    def starting_resources(self):
        #
        #   Gather starting squares from Constant.py
        #   Each is a list of (x,y) coordinates which correspond to the "starting square" of each player
        #   A starting square is a 6x3 box on the left and right side of the board which will always have at least 1
        #   gold resource inside
        #
        w_starting_squares, b_starting_squares = Constant.starting_squares()

        #
        #   Add those lists together into one master list
        #
        starting_squares = w_starting_squares + b_starting_squares

        #
        #   Find the four corners quarters of the board
        #

        top_left, top_right, bottom_left, bottom_right = Constant.quarter_squares()

        gold_list = []
        #
        #   Resource Generating For Loop
        #   Goes through each square on the board and decides what should spawn there
        #
        for r in range(self.rows):
            for c in range(self.cols):
                #
                #   Boolean, True if (row, col) is in Center Squares
                #
                in_center_square = (r, c) in Constant.center_squares()

                #
                #   Boolean, True if (row, col) is in Edge Squares
                #
                in_edge_square = (r, c) in Constant.edge_squares()

                #
                #   Boolean, True if (row, col) is in Starting Squares
                #   (not sure why the reference is different here... )
                #
                in_starting_square = (r, c) in starting_squares

                #
                #   Generate our random number from 0 to 100.
                #   Used to give the maps variation
                #
                rand = random.randint(0, 100)

                #
                #
                #
                if in_starting_square:
                    pass

                elif in_edge_square:
                    if rand in range(10, 100):
                        # edges, trees
                        self.create_resource(r, c, Wood(r, c))
                    if rand in range(80, 100):
                        if len(gold_list) < Constant.TOTAL_GOLD_ON_MAP - 2:
                            pass
                            # edges, gold
                            # temporarily disabled
                            # self.create_resource(r, c, Gold(r, c))
                            # gold_list.append((r, c))
                        else:
                            self.create_resource(r, c, Wood(r, c))
                else:
                    if rand in range(1, 30):
                        # field trees
                        if self.has_no_resource(r, c):
                            self.create_resource(r, c, Wood(r, c))
                            c2 = c + 1
                            if Constant.tile_in_bounds(r, c2):
                                self.create_resource(r, c2, Wood(r, c2))
                            if rand > 5:
                                c2 = c - 1
                                if Constant.tile_in_bounds(r, c2):
                                    self.create_resource(r, c2, Wood(r, c2))

                    if rand in range(80, 100):
                        # field forest
                        self.create_resource(r, c, Wood(r, c))

                        # RIGHT
                        c2 = c + 1
                        if Constant.tile_in_bounds(r, c2):
                            self.create_resource(r, c2, Wood(r, c2))

                        # LEFT
                        c2 = c - 1
                        if Constant.tile_in_bounds(r, c2):
                            self.create_resource(r, c2, Wood(r, c2))

                        # DOWN
                        r2 = r + 1
                        if Constant.tile_in_bounds(r2, c):
                            self.create_resource(r2, c, Wood(r2, c))

                        if rand == 99:
                            # UP
                            r2 = r - 1
                            if Constant.tile_in_bounds(r2, c):
                                self.create_resource(r2, c, Wood(r2, c))

        #
        #   Pick a line near the center destroy all files around it
        #
        rand = random.randint(3, self.rows - 4)
        for c in range(self.cols):
            self.delete_resource(rand, c)

        #
        #   Generate a Gold in each corner
        #

        rand = random.randint(0, len(top_left) - 1)
        r, c = top_left[rand][0], top_left[rand][1]
        self.delete_resource(r, c)
        self.create_resource(r, c, Gold(r, c))

        rand = random.randint(0, len(top_right) - 1)
        r, c = top_right[rand][0], top_right[rand][1]
        self.delete_resource(r, c)
        self.create_resource(r, c, Gold(r, c))

        rand = random.randint(0, len(bottom_left) - 1)
        r, c = bottom_left[rand][0], bottom_left[rand][1]
        self.delete_resource(r, c)
        self.create_resource(r, c, Gold(r, c))

        rand = random.randint(0, len(bottom_right) - 1)
        r, c = bottom_right[rand][0], bottom_right[rand][1]
        self.delete_resource(r, c)
        self.create_resource(r, c, Gold(r, c))

        def play_random_sound_effect():
            i = random.randint(0, len(Constant.generate_resources) - 1)
            Constant.GENERATE_RESOURCES_SOUNDS[i].set_volume(.1)
            Constant.GENERATE_RESOURCES_SOUNDS[i].play()

        play_random_sound_effect()
        # gen 1 gold resource inside each player's starting square
        for sq in range(len(w_starting_squares) - 1):
            rand = random.randint(0, (len(w_starting_squares) - 1))
            r, c = w_starting_squares[rand]
            if self.is_empty(r, c):
                self.create_resource(r, c, Wood(r, c))
                break

        for sq in range(len(b_starting_squares) - 1):
            rand = random.randint(0, (len(b_starting_squares) - 1))
            r, c = b_starting_squares[rand]
            if self.is_empty(r, c):
                self.create_resource(r, c, Wood(r, c))
                break

    def draw(self, win):
        for r in range(self.rows):
            for c in range(self.cols):
                colors = [Constant.DARK_SQUARE_COLOR, Constant.LIGHT_SQUARE_COLOR]
                color = colors[((r + c) % 2)]
                pygame.draw.rect(win, color, pygame.Rect(c * Constant.SQ_SIZE,
                                                         r * Constant.SQ_SIZE,
                                                         Constant.SQ_SIZE,
                                                         Constant.SQ_SIZE))
        for r in range(self.rows):
            for c in range(self.cols):
                self.board[r][c].draw(win)

    def enemy_player_king_does_not_exist(self):
        does_king_exist = False
        for piece in self.players[Constant.TURNS[self.turn]].pieces:
            if isinstance(piece, King):
                does_king_exist = True
        return not does_king_exist

    def update_moves(self):
        for player in self.players:
            for piece in self.players[player].pieces:
                piece.update_move_squares(self)
                piece.update_capture_squares(self)

    def has_prayer_stone(self, row, col):
        if Constant.tile_in_bounds(row, col):
            p = self.board[row][col].get_occupying()
            if isinstance(p, PrayerStone):
                return True

    def piece_is_selected(self, piece):
        selected_list = [piece.selected, piece.mining, piece.pre_selected, piece.purchasing, piece.praying,
                         piece.casting, piece.stealing, piece.mining_stealing, piece.persuading]
        if any(selected_list):
            return True

    def update_previously_selected(self):
        prev = None
        for player in self.players:
            for piece in self.players[player].pieces:
                if self.piece_is_selected(piece):
                    prev = piece

        return prev

    def tick_protected_tiles(self, protected_tiles):
        for tile in protected_tiles:
            tile.tick_protect_timer()

    def untick_protected_tiles(self, protected_tiles):
        for tile in protected_tiles:
            tile.untick_protect_timer(tile.protected_by)

    def generate_stealing_offsets(self, stealing_key):
        variance_list = [stealing_key['wood']['variance'], stealing_key['gold']['variance'],
                         stealing_key['stone']['variance']]

        stealing_offsets = []
        for i in variance_list:
            rand = random.randint(i[0], i[1])
            stealing_offsets.append(rand)

        return stealing_offsets

    def generate_available_rituals(self, potential_rituals, limit):
        length_of_new_ritual_list = random.randint(1, limit)
        available_rituals = []
        random.shuffle(potential_rituals)

        for i in range(length_of_new_ritual_list):
            available_rituals.append(potential_rituals[i])

        return available_rituals

    def update_all_squares(self):
        for player in self.players:
            for piece in self.players[player].pieces:
                piece.update_mining_squares(self)
                piece.update_stealing_squares(self)
                piece.update_praying_squares(self)
                piece.update_move_squares(self)
                piece.update_capture_squares(self)
                piece.update_spawn_squares(self)
                piece.update_persuader_squares(self)

    def update_mining_squares(self):
        for player in self.players:
            for piece in self.players[player].pieces:
                piece.update_mining_squares(self)

    def update_spawn_squares(self):
        for player in self.players:
            for piece in self.players[player].pieces:
                piece.update_spawn_squares(self)

    def set_actions_remaining(self, n):
        for player in self.players:
            for piece in self.players[player].pieces:
                piece.actions_remaining = n

    def reset_piece_limit(self, color):
        self.players[color].reset_piece_limit()

    def update_piece_limit(self):
        for piece in self.players[self.turn].pieces:
            self.players[self.turn].add_additional_piece_limit(piece.get_additional_piece_limit())

    def reset_selected(self):
        for player in self.players:
            for piece in self.players[player].pieces:
                piece.selected = False
                piece.pre_selected = False
                piece.mining = False
                piece.purchasing = False
                piece.praying = False
                piece.casting = False
                piece.stealing = False
                piece.mining_stealing = False
                piece.persuading = False

    def reset_player_actions_remaining(self, color):
        self.players[color].reset_actions_remaining()

    def reset_piece_actions_remaining(self):
        for player in self.players:
            for piece in self.players[player].pieces:
                piece.actions_remaining = 1

    def reset_board(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.board[r][c] = Tile(r, c)

    def reset_unused_piece_highlight(self):
        for player in self.players:
            for piece in self.players[player].pieces:
                piece.unused_piece_highlight = False

    def spawn(self, dest_row, dest_col, spawned):
        #
        #   Create spawned piece object at destination
        #
        spawned_piece = self.PIECES[spawned](dest_row, dest_col, self.turn)

        #
        #   store piece on board at destination address
        #
        self.create_piece(dest_row, dest_col, spawned_piece)

    def capture(self, moving_row, moving_col, dest_row, dest_col):
        #
        #   Remove from captured piece from piece list
        #
        self.players[Constant.TURNS[self.turn]].pieces.remove(self.board[dest_row][dest_col].get_occupying())
        #
        #   Empty captured square
        #
        self.board[dest_row][dest_col].set_occupying(None)

        #
        #   Move piece to newly emptied square
        #
        self.move(moving_row, moving_col, dest_row, dest_col)

    def swap(self, moving_row, moving_col, dest_row, dest_col):
        first_piece_to_swap = self.get_occupying(moving_row, moving_col)
        second_piece_to_swap = self.get_occupying(dest_row, dest_col)

        self.board[moving_row][moving_col].occupying = second_piece_to_swap
        self.board[dest_row][dest_col].occupying = first_piece_to_swap

        first_piece_to_swap.change_pos(dest_row, dest_col)
        second_piece_to_swap.change_pos(moving_row, moving_col)

    def move(self, moving_row, moving_col, dest_row, dest_col):
        piece = self.board[moving_row][moving_col].get_occupying()
        #
        #   Move the piece on the board array
        #
        self.board[dest_row][dest_col].occupying = piece

        #
        #   Change the Row, Col in the Piece object to reflect change
        #

        piece.change_pos(dest_row, dest_col)

        #
        #   Set the position on the board array to where the piece was to None
        #
        self.board[moving_row][moving_col].set_occupying(None)

    def has_gold(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_resource()
            if isinstance(p, Gold):
                return True

    def has_wood(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_resource()
            if isinstance(p, Wood):
                return True

    def has_sunken_quarry(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_resource()
            if isinstance(p, SunkenQuarry):
                return True

    def has_depleted_quarry(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_resource()
            if isinstance(p, DepletedQuarry):
                return True

    def has_fortress(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_occupying()
            if isinstance(p, Fortress):
                return True

    def has_builder(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_occupying()
            if isinstance(p, Builder):
                return True

    def has_player_king(self, r, c):
        p = self.board[r][c].occupying
        if isinstance(p, King):
            if p.color == self.turn or p.occupied == self.turn:
                return True
        else:
            return False

    def has_building(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].occupying
            if isinstance(p, Building):
                return True
            else:
                return False

    def has_resource(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_resource()
            if p is not None:
                return True

    def has_piece(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_occupying()
            if isinstance(p, Piece):
                return True

    def has_elephant(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].occupying
            if isinstance(p, Elephant):
                return True
            else:
                return False

    def has_stable(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_occupying()
            if isinstance(p, Stable):
                return True

    def has_king(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].occupying
            if isinstance(p, King):
                return True
            else:
                return False

    def has_knight(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_occupying()
            if isinstance(p, Knight):
                return True
            else:
                return False

    def has_rogue_pawn(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_occupying()
            if isinstance(p, RoguePawn):
                return True

    def has_pawn(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_occupying()
            if isinstance(p, Pawn):
                return True

    def has_rook(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_occupying()
            if isinstance(p, Rook):
                return True

    def has_bishop(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_occupying()
            if isinstance(p, Bishop):
                return True

    def has_duke(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_occupying()
            if isinstance(p, Duke):
                return True

    def has_castle(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_occupying()
            if isinstance(p, Castle):
                return True
            else:
                return False

    def has_barracks(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_occupying()
            if isinstance(p, Barracks):
                return True
            else:
                return False

    def has_monk(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_occupying()
            if isinstance(p, Monk):
                return True

    def has_gold_general(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_occupying()
            if isinstance(p, GoldGeneral):
                return True

    def has_monolith(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].occupying
            if isinstance(p, Monolith):
                return True
            else:
                return False

    def has_quarry(self, r, c):
        if Constant.tile_in_bounds(r, c):
            p = self.board[r][c].get_resource()
            if isinstance(p, Quarry):
                return True
            else:
                return False

    def has_occupying(self, r, c):
        if Constant.tile_in_bounds(r, c):
            if self.board[r][c].get_occupying():
                return True

    def has_none_occupying(self, r, c):
        if Constant.tile_in_bounds(r, c):
            if self.board[r][c].occupying is None:
                return True

    def has_no_resource(self, r, c):
        if Constant.tile_in_bounds(r, c):
            if self.board[r][c].resource is None:
                return True

    def is_empty(self, r, c):
        if Constant.tile_in_bounds(r, c):
            if self.has_no_resource(r, c) and self.has_none_occupying(r, c):
                return True

    def get_resource(self, r, c):
        return self.board[r][c].get_resource()

    def can_be_legally_occupied(self, r, c):
        if Constant.tile_in_bounds(r, c):
            if self.has_gold(r, c) or self.has_wood(r, c) or self.has_sunken_quarry(r, c):
                return False
            else:
                if self.is_empty(r, c):
                    return True
                elif self.has_quarry(r, c):
                    return True
                elif self.has_depleted_quarry(r, c):
                    return True
                elif self.has_occupying(r, c):
                    return True

    def can_be_legally_occupied_by_rogue(self, r, c):
        if Constant.tile_in_bounds(r, c):
            if self.has_gold(r, c) or self.has_sunken_quarry(r, c):
                return False
            else:
                if self.is_empty(r, c):
                    return True
                elif self.has_quarry(r, c):
                    return True
                elif self.has_depleted_quarry(r, c):
                    return True
                elif self.has_occupying(r, c):
                    return True

    def can_be_legally_occupied_by_gold_general(self, r, c):
        if Constant.tile_in_bounds(r, c):
            if self.is_empty(r, c):
                return True
            elif self.has_quarry(r, c):
                return True
            elif self.has_depleted_quarry(r, c):
                return True
            elif self.has_occupying(r, c):
                return True
            elif self.has_gold(r, c):
                return True
            elif self.has_sunken_quarry(self, r, c):
                return True
            elif self.has_wood(r, c):
                return True

    def can_be_occupied_by_gold_general(self, r, c):
        if Constant.tile_in_bounds(r, c):
            if self.is_empty(r, c):
                return True
            elif self.has_none_occupying(r, c) and self.has_quarry(r, c):
                return True
            elif self.has_none_occupying(r, c) and self.has_depleted_quarry(r, c):
                return True
            elif self.has_none_occupying(r, c) and self.has_wood(r, c):
                return True
            elif self.has_none_occupying(r, c) and self.has_gold(r, c):
                return True
            elif self.has_none_occupying(r, c) and self.has_sunken_quarry(r, c):
                return True

    def can_be_occupied(self, r, c):
        if Constant.tile_in_bounds(r, c):
            if self.has_none_occupying(r, c) and self.has_quarry(r, c):
                return True
            elif self.is_empty(r, c):
                return True
            elif self.has_none_occupying(r, c) and self.has_depleted_quarry(r, c):
                return True
            elif self.has_wood(r, c) or self.has_gold(r, c):
                return False

    def can_be_occupied_by_rogue(self, r, c):
        if Constant.tile_in_bounds(r, c):
            if self.has_none_occupying(r, c) and self.has_quarry(r, c):
                return True
            elif self.is_empty(r, c):
                return True
            elif self.has_none_occupying(r, c) and self.has_depleted_quarry(r, c):
                return True
            elif self.has_none_occupying(r, c) and (self.has_wood(r, c)):
                return True

    def create_resource(self, row, col, resource):
        self.board[row][col].set_resource(resource)

    def delete_piece(self, row, col):
        piece = self.board[row][col].get_occupying()
        pieces = self.players[piece.get_color()].pieces
        del pieces[pieces.index(piece)]
        self.board[row][col].set_occupying(None)

    def create_piece(self, row, col, piece):
        self.board[row][col].set_occupying(piece)
        self.players[piece.get_color()].pieces.append(piece)

    def delete_resource(self, row, col):
        self.board[row][col].set_resource(None)

    def get_occupying(self, row, col):
        if Constant.tile_in_bounds(row, col):
            return self.board[row][col].occupying

    def has_rogue(self, row, col):
        if Constant.tile_in_bounds(row, col):
            if self.get_occupying(row, col).is_rogue:
                return True

    def count_unused_pieces(self):
        unused_pieces = []
        for piece in self.players[self.turn].pieces:
            if piece.actions_remaining == 1:
                unused_pieces.append(piece)
        return unused_pieces

    def count_used_pieces(self):
        used_pieces = []
        for piece in self.players[self.turn].pieces:
            if piece.actions_remaining == 0:
                used_pieces.append(piece)
        return used_pieces

    def count_pieces(self, p, color):
        count = 0
        for piece in self.players[color].pieces:
            if piece == p:
                count += 1
        return count

    def close_menus(self):
        self.menus = []

    def change_turn(self):
        turn_change_event = ChangeTurn(self)
        turn_change_event.complete()
        self.events.append(turn_change_event)
        self.players[self.turn].begin_turn(self)

    def get_occupying_color(self, r, c):
        if Constant.tile_in_bounds(r, c):
            return self.board[r][c].occupying.get_color()

    def set_purchasing(self, row, col, boolean):
        self.board[row][col].occupying.purchasing = boolean

    def set_stealing(self, row, col, boolean):
        self.board[row][col].occupying.stealing = boolean

    def set_mining_stealing(self, row, col, boolean):
        self.board[row][col].occupying.mining_stealing = boolean

    def set_pre_selected(self, row, col, boolean):
        self.board[row][col].occupying.pre_selected = boolean

    def find_player_castle(self):
        for piece in self.players[self.turn].pieces:
            if isinstance(piece, Castle):
                return piece.get_position()

    def player_can_do_action(self, color):
        if self.players[color].can_do_action():
            return True

    def update_additional_actions(self):
        tally_additional_actions = 0
        for piece in self.players[self.turn].pieces:
            self.players[self.turn].add_additional_actions(piece.get_additional_actions())
            tally_additional_actions += piece.get_additional_actions()

        self.players[self.turn].total_additional_actions_this_turn = tally_additional_actions

    def is_legal_ritual(self, ritual):
        ritual_cost = Constant.PRAYER_COSTS[ritual]['prayer']
        if self.valid_ritual(ritual_cost):
            return True

    def player_has_gold_general(self, color):
        for piece in self.players[color].pieces:
            if isinstance(piece, GoldGeneral):
                return True

    def is_legal_spawn(self, spawn):
        piece_cost = Constant.PIECE_COSTS[spawn]
        if self.valid_purchase(piece_cost):
            if self.players[self.turn].can_add_piece(spawn):
                return True
            if self.player_has_gold_general(self.turn):
                if spawn == 'monk':
                    return True

    def has_mineable_resource(self, r, c):
        if Constant.tile_in_bounds(r, c):
            r = self.board[r][c].get_resource()
            if isinstance(r, Wood) or isinstance(r, Quarry) or isinstance(r, Gold) or isinstance(r, SunkenQuarry):
                return True

    def update_persuader_squares(self):
        for piece in self.players[self.turn].pieces:
            piece.update_persuader_squares(self)

    def update_praying_squares(self):
        for piece in self.players[self.turn].pieces:
            piece.update_praying_squares(self)

    def update_interceptor_squares(self):
        for player in self.players:
            for piece in self.players[player].pieces:
                piece.update_interceptor_squares(self)

    def has_prayable_building(self, r, c):
        if Constant.tile_in_bounds(r, c):
            b = self.board[r][c].get_occupying()
            if isinstance(b, PrayerStone) or isinstance(b, Monolith):
                return True

    def get_intercepted_pieces(self):
        intercepted_pieces = []
        for player in self.players:
            for piece in self.players[player].pieces:
                if piece.intercepted and piece.is_effected_by_jester:
                    intercepted_pieces.append(piece)

        return intercepted_pieces

    def find_interceptors(self):
        self.update_interceptor_squares()
        interceptors = []
        for player in self.players:
            for p in self.players[player].pieces:
                if isinstance(p, Jester):
                    interceptors.append(p)
        return interceptors

    def intercept_pieces(self):
        interceptors = self.find_interceptors()
        for i in interceptors:
            for square in i.interceptor_squares_list:
                o = self.board[square[0]][square[1]].get_occupying()
                if o and o.is_effected_by_jester:
                    o.intercepted = True
                    if o.actions_remaining == 0:
                        self.used_and_intercepted_pieces.append(o)
                    o.actions_remaining = 0

    def reset_intercepted(self):
        for player in self.players:
            for piece in self.players[player].pieces:
                if piece.intercepted:
                    piece.intercepted = False

    def correct_interceptions(self):
        intercepted_pieces_original = self.get_intercepted_pieces()
        self.reset_intercepted()
        self.intercept_pieces()
        intercepted_pieces_new = self.get_intercepted_pieces()
        for p in intercepted_pieces_original:
            if p not in intercepted_pieces_new:
                if p not in self.used_and_intercepted_pieces:
                    p.intercepted = False
                    p.actions_remaining = 1

        self.used_and_intercepted_pieces = []

    def transfer_to_stealing_state(self, row, col):
        self.update_stealing_squares()
        stealing_squares = self.board[row][col].get_occupying().stealing_squares_list
        allow_steal = False
        if stealing_squares:
            allow_steal = True
        if allow_steal:
            self.set_stealing(row, col, True)
            new_state = Stealing(self.state[-1].win, self)
            self.menus = []
            self.set_state(new_state)
            return True

    def transfer_to_building_state(self, row, col):
        self.update_spawn_squares()
        spawn_squares = self.board[row][col].get_occupying().spawn_squares_list
        allow_spawn = False
        if spawn_squares:
            allow_spawn = True
        if allow_spawn:
            self.set_pre_selected(row, col, True)
            new_state = PreBuilding(self.state[-1].win, self)
            self.menus = []
            new_state.add_menu_to_menu_queue(str(self.get_occupying(row, col)))
            new_state.spawning_piece = self.get_occupying(row, col)
            self.set_state(new_state)
            return True

    def transfer_to_stealing_mining_state(self, row, col):
        self.update_mining_squares()
        self.update_stealing_squares()
        selectable_squares = self.board[row][col].get_occupying().mining_squares_list + self.board[row][
            col].get_occupying().stealing_squares_list
        allow_state = False
        if selectable_squares:
            allow_state = True
        if allow_state:
            self.set_mining_stealing(row, col, True)
            new_state = MiningStealing(self.state[-1].win, self)
            self.menus = []
            self.set_state(new_state)
            return True

    def transfer_to_piece_cost_screen(self):
        new_state = PieceCost(self.state[-1].win, self)
        self.set_state(new_state)

    def transfer_to_praying_state(self, row, col):
        self.update_praying_squares()
        praying_squares = self.board[row][col].get_occupying().praying_squares_list
        allow_pray = False
        for square in praying_squares:
            if self.has_prayable_building(square[0], square[1]):
                allow_pray = True
        if allow_pray:
            self.board[row][col].get_occupying().praying = True
            new_state = Praying(self.state[-1].win, self)
            self.set_state(new_state)
            self.menus = []
            return True

    def transfer_to_persuading_state(self, row, col):
        self.update_persuader_squares()
        persuader_squares = self.board[row][col].get_occupying().persuader_squares_list
        if persuader_squares:
            self.board[row][col].get_occupying().persuading = True
            new_state = Persuading(self.state[-1].win, self)
            self.set_state(new_state)
            self.menus = []
            return True

    def transfer_to_mining_state(self, row, col):
        self.update_mining_squares()
        mining_squares = self.board[row][col].get_occupying().mining_squares_list
        allow_mine = False
        for m in mining_squares:
            if self.has_mineable_resource(m[0], m[1]):
                allow_mine = True
        if allow_mine:
            self.board[row][col].get_occupying().mining = True
            new_state = Mining(self.state[-1].win, self)
            self.set_state(new_state)
            self.menus = []
            return True

    def transfer_to_surrender_state(self):
        new_state = Surrender(self.state[-1].win, self)
        self.set_state(new_state)
        self.menus = []

    def transfer_to_spawning_state(self, spawning):
        new_state = Spawning(self.state[-1].win, self)
        self.spawning = spawning
        self.set_state(new_state)

    def transfer_to_ritual_state(self, ritual):
        new_state = self.STATES[ritual](self.state[-1].win, self)
        self.menus = []
        self.set_state(new_state)
        return True

    def transfer_to_starting_spawn(self, spawn_list):
        state = StartingSpawn(self.state[-1].win, self)
        self.spawn_list = spawn_list
        self.spawning = self.spawn_list[0]
        self.set_state(state)

    def transfer_to_piece_selection(self):
        state = SelectStartingPieces(self.state[-1].win, self)
        self.set_state(state)

    def create_ritual_menu(self, row, col, ritual_list):
        ritual_menu = RitualMenu(row, col, self.state[-1].win, self, ritual_list)
        self.menus.append(ritual_menu)
        return True

    def create_king_menu(self, row, col):
        king_menu = KingMenu(row, col, self.state[-1].win, self)
        self.menus.append(king_menu)
        self.update_spawn_squares()
        return True

    def is_legal_starting_square(self, row, col):
        player_is_too_close = False
        if not self.can_be_occupied(row, col):
            return False
        if not self.players:
            return True
        for r in range(row - 3, row + 4):
            for c in range(col - 3, col + 4):
                if self.has_castle(r, c):
                    player_is_too_close = True

        return not player_is_too_close
    def is_legal_starting_square(self, row, col):
        player_is_too_close = False
        if not self.can_be_occupied(row, col):
            return False
        if not self.players:
            return True
        for r in range(row - 3, row + 4):
            for c in range(col - 3, col + 4):
                if self.has_castle(r, c):
                    player_is_too_close = True

        return not player_is_too_close
