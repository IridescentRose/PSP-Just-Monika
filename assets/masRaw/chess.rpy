


default persistent._mas_chess_stats = {"wins": 0, "losses": 0, "draws": 0}


default persistent._mas_chess_quicksave = ""


default persistent._mas_chess_dlg_actions = {}


default persistent._mas_chess_timed_disable = None


default persistent._mas_chess_3_edit_sorry = False


default persistent._mas_chess_mangle_all = False


default persistent._mas_chess_skip_file_checks = False

define mas_chess.CHESS_SAVE_PATH = "/chess_games/"
define mas_chess.CHESS_SAVE_EXT = ".pgn"
define mas_chess.CHESS_SAVE_NAME = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ-_0123456789"
define mas_chess.CHESS_PROMPT_FORMAT = "{0} | {1} | Turn: {2} | You: {3}"


init 1 python in mas_chess:
    import os
    import chess.pgn


    quit_game = False


    REL_DIR = "chess_games/"


    CHESS_MENU_X = 680
    CHESS_MENU_Y = 40
    CHESS_MENU_W = 560
    CHESS_MENU_H = 640
    CHESS_MENU_XALIGN = -0.05
    CHESS_MENU_AREA = (CHESS_MENU_X, CHESS_MENU_Y, CHESS_MENU_W, CHESS_MENU_H)

    CHESS_MENU_NEW_GAME_VALUE = "NEWGAME"
    CHESS_MENU_NEW_GAME_ITEM = (
        _("Play New Game"),
        CHESS_MENU_NEW_GAME_VALUE,
        True,
        False
    )

    CHESS_MENU_FINAL_VALUE = "NONE"
    CHESS_MENU_FINAL_ITEM = (
        _("Nevermind"),
        CHESS_MENU_FINAL_VALUE,
        False,
        False,
        20
    )

    CHESS_MENU_WAIT_VALUE = "MATTE"
    CHESS_MENU_WAIT_ITEM = (
        _("I can't make this decision right now..."),
        CHESS_MENU_WAIT_VALUE,
        False,
        False,
        20
    )

    CHESS_NO_GAMES_FOUND = "NOGAMES"


    del_files = (
        "chess.rpyc",
    )


    gt_files = (
        "definitions.rpyc",
        "event-handler.rpyc",
        "script-topics.rpyc",
        "script-introduction.rpyc",
        "script-story-events.rpyc",
        "zz_pianokeys.rpyc",
        "zz_music_selector.rpyc"
    )




    chess_strength = (False, 0)



    CHESS_GAME_CONT = "USHO"



    CHESS_GAME_BACKUP = "foundyou"



    CHESS_GAME_FILE = "file"


    loaded_game_filename = None





    QS_LOST = 0




    QF_LOST_OFCN = 1




    QF_LOST_MAYBE = 2




    QF_LOST_ACDNT = 3




    QF_EDIT_YES = 4



    QF_EDIT_NO = 5




    DLG_QF_LOST_OFCN_ENABLE = True
    DLG_QF_LOST_OFCN_CHOICE = _("Of course not!")


    DLG_QF_LOST_MAY_ENABLE = True
    DLG_QF_LOST_MAY_CHOICE = _("Maybe...")


    DLG_QF_LOST_ACDNT_ENABLE = True
    DLG_QF_LOST_ACDNT_CHOICE = _("It was an accident!")


    DLG_CHESS_LOCKED = "mas_chess_dlg_chess_locked"


    DLG_MONIKA_WIN_BASE = "mas_chess_dlg_game_monika_win_{0}"



    DLG_MONIKA_WIN_SURR_BASE = "mas_chess_dlg_game_monika_win_surr_{0}"


    DLG_MONIKA_LOSE_BASE = "mas_chess_dlg_game_monika_lose_{0}"



    monika_loses_mean_quips = None 



    _monika_loses_line_quips = (
        _("Hmph.{w=0.3} You were just lucky today."),
        _("...{w=0.3}I'm just having an off day."),
        _("Ah, so you {i}are{/i} capable of winning..."),
        _("I guess you're not {i}entirely{/i} terrible."),
        _("Tch-"),
        _("Winning isn't everything, you know..."),
        _("Ahaha,{w=0.3} I was just letting you win since you keep losing so much."),
        _("Oh, you won.{w=0.3} I should have taken this game seriously, then.")
        
    )


    _monika_loses_label_quips = (
        "mas_chess_dlg_game_monika_lose_silly",
    )



    monika_wins_mean_quips = None 



    _monika_wins_line_quips = (
        _("Ahaha, do you even know how to play chess?"), 
        _("Are you {i}that{/i} bad? I wasn't even taking this game seriously.")
    )


    _monika_wins_label_quips = (
        "mas_chess_dlg_game_monika_win_rekt",
    )



    monika_wins_surr_mean_quips = None 


    _monika_wins_surr_line_quips = (
        _monika_wins_line_quips[0],
        _("Figures you'd give up. You're not one to see things all the way through."),
    )


    _monika_wins_surr_label_quips = (
        "mas_chess_dlg_game_monika_win_surr_resolve",
        "mas_chess_dlg_game_monika_win_surr_trying"
    )




    def _m1_chess__initDLGActions():
        """
        Initailizes the DLG actions dict and updates the persistent
        appriorpately

        ASSUMES:
            renpy.game.persistent._mas_chess_dlg_actions
        """
        
        
        
        dlg_actions = {
            QS_LOST: 0,
            QF_LOST_OFCN: 0,
            QF_LOST_MAYBE: 0,
            QF_LOST_ACDNT: 0,
            QF_EDIT_YES: 0,
            QF_EDIT_NO: 0
        }
        
        
        if len(dlg_actions) != len(renpy.game.persistent._mas_chess_dlg_actions):
            dlg_actions.update(renpy.game.persistent._mas_chess_dlg_actions)
            renpy.game.persistent._mas_chess_dlg_actions = dlg_actions

    def _initQuipLists(MASQL_class):
        """
        Initializes the mas quiplists.

        IN:
            MASQL_class - the MASQuipList class so we can work with it
                even though we arent global
        """
        
        global monika_loses_mean_quips
        global monika_wins_mean_quips
        global monika_wins_surr_mean_quips
        
        
        monika_loses_mean_quips = MASQL_class()
        
        
        for _line in _monika_loses_line_quips:
            monika_loses_mean_quips.addLineQuip(_line)
        
        
        for _label in _monika_loses_label_quips:
            monika_loses_mean_quips.addLabelQuip(_label)
        
        
        monika_loses_mean_quips.addGlitchQuip(40, 2, 3, True)
        
        
        monika_wins_mean_quips = MASQL_class()
        
        
        for _line in _monika_wins_line_quips:
            monika_wins_mean_quips.addLineQuip(_line)
        
        
        for _label in _monika_wins_label_quips:
            monika_wins_mean_quips.addLabelQuip(_label)
        
        
        monika_wins_surr_mean_quips = MASQL_class()
        
        
        for _line in _monika_wins_surr_line_quips:
            monika_wins_surr_mean_quips.addLineQuip(_line)
        
        
        for _label in _monika_wins_surr_label_quips:
            monika_wins_surr_mean_quips.addLabelQuip(_label)


    def _initMASChess(MASQL_class):
        """
        Initializes mas chess stuff that needs to be initalized

        IN:
            MASQL_class - the MASQuipList class so we can work with it
                even though we arent global
        """
        _m1_chess__initDLGActions()
        
        if renpy.game.persistent._mas_chess_3_edit_sorry:
            _initQuipLists(MASQL_class)


    def _checkInProgressGame(pgn_game, mth):
        """
        Checks if the given pgn game is valid and in progress.

        IN:
            pgn_game - pgn game to check
            mth - monika twitter handle. pass it in since I'm too lazy to
                find context from a store

        RETURNS:
            SEE isInProgressGame
        """
        if pgn_game is None:
            return None
        
        if pgn_game.headers["Result"] != "*":
            return None
        
        
        if pgn_game.headers["White"] == mth:
            the_player = "Black"
        elif pgn_game.headers["Black"] == mth:
            the_player = "White"
        else: 
            return None
        
        
        
        
        board = pgn_game.board()
        for move in pgn_game.main_line():
            board.push(move)
        
        return (
            CHESS_PROMPT_FORMAT.format(
                pgn_game.headers["Date"].replace(".","-"),
                pgn_game.headers["Event"],
                board.fullmove_number,
                the_player
            ),
            pgn_game
        )


    def isInProgressGame(filename, mth):
        """
        Checks if the pgn game with the given filename is valid and
        in progress.

        IN:
            filename - filename of the pgn game
            mth - monika twitter handle. pass it in since I'm too lazy to
                find context from a store

        RETURNS:
            tuple of the following format:
                [0]: Text to display on button
                [1]: chess.pgn.Game of the game
            OR NONE if this is not a valid pgn game
        """
        if filename[-4:] != CHESS_SAVE_EXT:
            return None
        
        pgn_game = None
        with open(
            os.path.normcase(CHESS_SAVE_PATH + filename),
            "r"
        ) as loaded_game:
            pgn_game = chess.pgn.read_game(loaded_game)
        
        return _checkInProgressGame(pgn_game, mth)


init 899 python:

    store.mas_chess._initMASChess(MASQuipList)

init:
    python:
        import chess
        import chess.pgn
        import subprocess
        import platform
        import random
        import pygame
        import threading
        import collections
        import os


        import store.mas_ui as mas_ui

        ON_POSIX = 'posix' in sys.builtin_module_names

        def enqueue_output(out, queue, lock):
            for line in iter(out.readline, b''):
                lock.acquire()
                queue.appendleft(line)
                lock.release()
            out.close()


        class ArchitectureError(RuntimeError):
            pass

        def get_mouse_pos():
            vw = config.screen_width * 10000
            vh = config.screen_height * 10000
            pw, ph = renpy.get_physical_size()
            dw, dh = pygame.display.get_surface().get_size()
            mx, my = pygame.mouse.get_pos()
            
            
            
            mx = (mx * pw) / dw
            my = (my * ph) / dh
            
            r = None
            
            
            if vw / (vh / 10000) > pw * 10000 / ph:
                r = vw / pw
                my -= (ph - vh / r) / 2
            else:
                r = vh / ph
                mx -= (pw - vw / r) / 2
            
            newx = (mx * r) / 10000
            newy = (my * r) / 10000
            
            return (newx, newy)


        class ChessException(Exception):
            def __init__(self, msg):
                self.msg = msg
            def __str__(self):
                return self.msg


        if mas_games.is_platform_good_for_chess():
            
            try:
                file_path = os.path.normcase(
                    config.basedir + mas_chess.CHESS_SAVE_PATH
                )
                if not os.access(file_path, os.F_OK):
                    os.mkdir(file_path)
                mas_chess.CHESS_SAVE_PATH = file_path
            except:
                raise ChessException(
                    "Chess game folder could not be created '{0}'".format(
                        file_path
                    )
                )

        class ChessDisplayable(renpy.Displayable):
            COLOR_WHITE = True
            COLOR_BLACK = False
            MONIKA_WAITTIME = 1500
            MONIKA_OPTIMISM = 33
            MONIKA_THREADS = 1
            
            MOUSE_EVENTS = (
                pygame.MOUSEMOTION,
                pygame.MOUSEBUTTONUP,
                pygame.MOUSEBUTTONDOWN
            )
            
            def __init__(self, player_color, pgn_game=None):
                """
                player_color - player color obvi
                pgn_game - previous game to load (chess.pgn.Game)
                """
                import sys
                
                renpy.Displayable.__init__(self)
                
                
                self.pieces_image = Image("mod_assets/games/chess/chess_pieces.png")
                self.board_image = Image("mod_assets/games/chess/chess_board.png")
                self.piece_highlight_red_image = Image("mod_assets/games/chess/piece_highlight_red.png")
                self.piece_highlight_green_image = Image("mod_assets/games/chess/piece_highlight_green.png")
                self.piece_highlight_yellow_image = Image("mod_assets/games/chess/piece_highlight_yellow.png")
                self.piece_highlight_magenta_image = Image("mod_assets/games/chess/piece_highlight_magenta.png")
                self.move_indicator_player = Image("mod_assets/games/chess/move_indicator_player.png")
                self.move_indicator_monika = Image("mod_assets/games/chess/move_indicator_monika.png")
                self.player_move_prompt = Text(_("It's your turn, [player]!"), size=36)
                self.num_turns = 0
                self.surrendered = False
                
                
                self.VECTOR_PIECE_POS = {
                    'K': 0,
                    'Q': 1,
                    'R': 2,
                    'B': 3,
                    'N': 4,
                    'P': 5
                }
                self.BOARD_BORDER_WIDTH = 15
                self.BOARD_BORDER_HEIGHT = 15
                self.PIECE_WIDTH = 57
                self.PIECE_HEIGHT = 57
                self.BOARD_WIDTH = self.BOARD_BORDER_WIDTH * 2 + self.PIECE_WIDTH * 8
                self.BOARD_HEIGHT = self.BOARD_BORDER_HEIGHT * 2 + self.PIECE_HEIGHT * 8
                self.INDICATOR_WIDTH = 60
                self.INDICATOR_HEIGHT = 96
                self.BUTTON_WIDTH = 120
                self.BUTTON_HEIGHT = 35
                self.BUTTON_X_SPACING = 10
                self.BUTTON_Y_SPACING = 10
                
                
                self.drawn_board_x = int((1280 - self.BOARD_WIDTH) / 2)
                self.drawn_board_y=  int((720 - self.BOARD_HEIGHT) / 2)
                drawn_button_x = (
                    1280 - self.drawn_board_x + self.BUTTON_X_SPACING
                )
                drawn_button_y_top = (
                    720 - (
                        (self.BUTTON_HEIGHT * 2) +
                        self.BUTTON_Y_SPACING +
                        self.drawn_board_y
                    )
                )
                drawn_button_y_bot = (
                    720 - (self.BUTTON_HEIGHT + self.drawn_board_y)
                )
                
                
                self._button_save = MASButtonDisplayable.create_stb(
                    _("Save"),
                    True,
                    drawn_button_x,
                    drawn_button_y_top,
                    self.BUTTON_WIDTH,
                    self.BUTTON_HEIGHT,
                    hover_sound=gui.hover_sound,
                    activate_sound=gui.activate_sound
                )
                self._button_giveup = MASButtonDisplayable.create_stb(
                    _("Give Up"),
                    True,
                    drawn_button_x,
                    drawn_button_y_bot,
                    self.BUTTON_WIDTH,
                    self.BUTTON_HEIGHT,
                    hover_sound=gui.hover_sound,
                    activate_sound=gui.activate_sound
                )
                self._button_done = MASButtonDisplayable.create_stb(
                    _("Done"),
                    False,
                    drawn_button_x,
                    drawn_button_y_bot,
                    self.BUTTON_WIDTH,
                    self.BUTTON_HEIGHT,
                    hover_sound=gui.hover_sound,
                    activate_sound=gui.activate_sound
                )
                
                
                self._visible_buttons = [
                    self._button_save,
                    self._button_giveup
                ]
                self._visible_buttons_winner = [
                    self._button_save,
                    self._button_done
                ]
                
                
                
                if not mas_games.is_platform_good_for_chess():
                    
                    raise ArchitectureError('Your operating system does not support the chess game.')
                
                def open_stockfish(path,startupinfo=None):
                    return subprocess.Popen([renpy.loader.transfn(path)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,startupinfo=startupinfo)
                
                is_64_bit = sys.maxsize > 2**32
                if platform.system() == 'Windows':
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    if is_64_bit:
                        self.stockfish = open_stockfish('mod_assets/games/chess/stockfish_8_windows_x64.exe',startupinfo)
                    else:
                        self.stockfish = open_stockfish('mod_assets/games/chess/stockfish_8_windows_x32.exe',startupinfo)
                
                elif platform.system() == 'Linux' and is_64_bit:
                    os.chmod(config.basedir + '/game/mod_assets/games/chess/stockfish_8_linux_x64',0755)
                    self.stockfish = open_stockfish('mod_assets/games/chess/stockfish_8_linux_x64')
                
                elif platform.system() == 'Darwin' and is_64_bit:
                    os.chmod(config.basedir + '/game/mod_assets/games/chess/stockfish_8_macosx_x64',0755)
                    self.stockfish = open_stockfish('mod_assets/games/chess/stockfish_8_macosx_x64')
                
                
                self.stockfish.stdin.write("setoption name Skill Level value %d\n" % (persistent.chess_strength))
                self.stockfish.stdin.write("setoption name Contempt value %d\n" % (self.MONIKA_OPTIMISM))
                
                
                self.queue = collections.deque()
                self.lock = threading.Lock()
                thrd = threading.Thread(target=enqueue_output, args=(self.stockfish.stdout, self.queue, self.lock))
                thrd.daemon = True
                thrd.start()
                
                
                
                
                
                
                
                
                
                self.promolist = ["q","r","n","b","r","k"]
                
                
                
                self.music_menu_open = False
                
                
                
                
                
                
                
                self.board = None
                
                
                if pgn_game:
                    
                    self.board = pgn_game.board()
                    for move in pgn_game.main_line():
                        self.board.push(move)
                    
                    
                    if self.board.turn == chess.WHITE:
                        self.current_turn = self.COLOR_WHITE
                    else:
                        self.current_turn = self.COLOR_BLACK
                    
                    
                    if pgn_game.headers["White"] == mas_monika_twitter_handle:
                        self.player_color = self.COLOR_BLACK
                    else:
                        self.player_color = self.COLOR_WHITE
                    
                    
                    last_move = self.board.peek().uci()
                    self.last_move_src = (
                        ord(last_move[0]) - ord('a'),
                        ord(last_move[1]) - ord('1')
                    )
                    self.last_move_dst = (
                        ord(last_move[2]) - ord('a'),
                        ord(last_move[3]) - ord('1')
                    )
                    
                    
                    self.num_turns = self.board.fullmove_number
                
                else:
                    
                    self.board = chess.Board()
                    
                    
                    self.today_date = datetime.date.today().strftime("%Y.%m.%d")
                    self.start_fen = self.board.fen()
                    
                    
                    self.current_turn = self.COLOR_WHITE
                    
                    
                    self.player_color = player_color
                    
                    
                    self.last_move_src = None
                    self.last_move_dst = None
                
                self.selected_piece = None
                self.possible_moves = set([])
                self.winner = None
                self.last_clicked_king = 0.0
                
                
                self.drawn_button_x = 0
                self.drawn_button_y_top = 0
                self.drawn_button_y_bot = 0
                
                
                
                self.pgn_game = pgn_game
                
                
                if player_color != self.current_turn:
                    self.start_monika_analysis()
                    self._button_save.disable()
                    self._button_giveup.disable()
                elif self.board.fullmove_number <= 4:
                    self._button_save.disable()
            
            def start_monika_analysis(self):
                self.stockfish.stdin.write("position fen %s" % (self.board.fen()) + '\n')
                self.stockfish.stdin.write("go movetime %d" % self.MONIKA_WAITTIME + '\n')
            
            def poll_monika_move(self):
                self.lock.acquire()
                res = None
                while self.queue:
                    line = self.queue.pop()
                    match = re.match(r"^bestmove (\w+)", line)
                    if match:
                        res = match.group(1)
                self.lock.release()
                return res
            
            def __del__(self):
                self.stockfish.stdin.close()
                self.stockfish.wait()
            
            @staticmethod
            def coords_to_uci(x, y):
                x = chr(x + ord('a'))
                y += 1
                return str(x) + str(y)
            
            def check_winner(self, current_move):
                if self.board.is_game_over():
                    if self.board.result() == '1/2-1/2':
                        self.winner = 'none'
                    else:
                        self.winner = current_move
            
            def _quitPGN(self, giveup):
                """
                Generates a pgn of the board, and depending on if we are
                doing previous game or not, does appropriate header
                setting

                IN:
                    giveup - True if the player surrendered, False otherwise

                RETURNS: tuple of the following format:
                    [0]: chess.pgn.Game object of this game
                    [1]: True if monika won, False if not
                    [2]: True if player gaveup, False otherwise
                    [3]: number of turns of this game
                """
                new_pgn = chess.pgn.Game.from_board(self.board)
                
                if giveup:
                    if self.player_color == self.COLOR_WHITE:
                        new_pgn.headers["Result"] = "0-1"
                    else:
                        new_pgn.headers["Result"] = "1-0"
                
                if self.pgn_game:
                    
                    new_pgn.headers["Site"] = self.pgn_game.headers["Site"]
                    new_pgn.headers["Date"] = self.pgn_game.headers["Date"]
                    new_pgn.headers["White"] = self.pgn_game.headers["White"]
                    new_pgn.headers["Black"] = self.pgn_game.headers["Black"]
                    
                    old_fen = self.pgn_game.headers.get("FEN", None)
                    if old_fen:
                        new_pgn.headers["FEN"] = old_fen
                        new_pgn.headers["SetUp"] = "1"
                
                else:
                    
                    
                    if player_color == self.COLOR_WHITE:
                        new_pgn.headers["White"] = persistent.playername
                        new_pgn.headers["Black"] = mas_monika_twitter_handle
                    else:
                        new_pgn.headers["White"] = mas_monika_twitter_handle
                        new_pgn.headers["Black"] = persistent.playername
                    
                    
                    
                    new_pgn.headers["Site"] = "MAS"
                    new_pgn.headers["Date"] = self.today_date
                    new_pgn.headers["FEN"] = self.start_fen
                    new_pgn.headers["SetUp"] = "1"
                
                return (
                    new_pgn,
                    (
                        (
                            new_pgn.headers["Result"] == "1-0"
                            and new_pgn.headers["White"] == mas_monika_twitter_handle
                        ) or (
                            new_pgn.headers["Result"] == "0-1"
                            and new_pgn.headers["Black"] == mas_monika_twitter_handle
                        )
                    ),
                    giveup,
                    self.board.fullmove_number
                )
            
            
            def _inButton(self, x, y, button_x, button_y):
                """
                Checks if the given mouse coordinates is in the given button's
                area.

                IN:
                    x - x coordinate
                    y - y coordinate
                    button_x - x coordinate of the button
                    button_y - y coordinate of the button

                RETURNS:
                    True if the mouse coords are in the button,
                    False otherwise
                """
                return (
                    button_x <= x <= button_x + self.BUTTON_WIDTH
                    and button_y <= y <= button_y + self.BUTTON_HEIGHT
                )
            
            
            def render(self, width, height, st, at):
                
                
                if self.current_turn != self.player_color and not self.winner:
                    monika_move = self.poll_monika_move()
                    if monika_move is not None:
                        self.last_move_src = (ord(monika_move[0]) - ord('a'), ord(monika_move[1]) - ord('1'))
                        self.last_move_dst = (ord(monika_move[2]) - ord('a'), ord(monika_move[3]) - ord('1'))
                        self.board.push_uci(monika_move)
                        if self.current_turn == self.COLOR_BLACK:
                            self.num_turns += 1
                        self.current_turn = self.player_color
                        self.winner = self.board.is_game_over()
                        
                        
                        
                        if not self.winner:
                            self._button_giveup.enable()
                            
                            
                            if self.num_turns > 4:
                                self._button_save.enable()
                
                
                r = renpy.Render(width, height)
                
                
                board = renpy.render(self.board_image, 1280, 720, st, at)
                
                
                pieces = renpy.render(self.pieces_image, 1280, 720, st, at)
                
                
                highlight_red = renpy.render(self.piece_highlight_red_image, 1280, 720, st, at)
                highlight_green = renpy.render(self.piece_highlight_green_image, 1280, 720, st, at)
                highlight_yellow = renpy.render(self.piece_highlight_yellow_image, 1280, 720, st, at)
                highlight_magenta = renpy.render(self.piece_highlight_magenta_image, 1280, 720, st, at)
                
                
                mx, my = get_mouse_pos()
                
                
                
                
                
                visible_buttons = list()
                if self.winner:
                    
                    
                    visible_buttons = [
                        (b.render(width, height, st, at), b.xpos, b.ypos)
                        for b in self._visible_buttons_winner
                    ]
                
                else:
                    
                    
                    visible_buttons = [
                        (b.render(width, height, st, at), b.xpos, b.ypos)
                        for b in self._visible_buttons
                    ]
                
                
                r.blit(board, (self.drawn_board_x, self.drawn_board_y))
                indicator_position = (int((width - self.INDICATOR_WIDTH) / 2 + self.BOARD_WIDTH / 2 + 50),
                                      int((height - self.INDICATOR_HEIGHT) / 2))
                
                
                if self.current_turn == self.player_color:
                    r.blit(renpy.render(self.move_indicator_player, 1280, 720, st, at), indicator_position)
                else:
                    r.blit(renpy.render(self.move_indicator_monika, 1280, 720, st, at), indicator_position)
                
                
                for b in visible_buttons:
                    r.blit(b[0], (b[1], b[2]))
                
                def get_piece_render_for_letter(letter):
                    jy = 0 if letter.islower() else 1
                    jx = self.VECTOR_PIECE_POS[letter.upper()]
                    return pieces.subsurface((jx * self.PIECE_WIDTH, jy * self.PIECE_HEIGHT,
                                              self.PIECE_WIDTH, self.PIECE_HEIGHT))
                
                
                for ix in range(8):
                    for iy in range(8):
                        iy_orig = iy
                        ix_orig = ix
                        if self.player_color == self.COLOR_WHITE:
                            iy = 7 - iy
                        else: 
                            ix = 7 - ix
                        x = int((width - (self.BOARD_WIDTH - self.BOARD_BORDER_WIDTH * 2)) / 2  + ix * self.PIECE_WIDTH)
                        y = int((height - (self.BOARD_HEIGHT - self.BOARD_BORDER_HEIGHT * 2)) / 2 + iy * self.PIECE_HEIGHT)
                        
                        def render_move(move):
                            if move is not None and ix_orig == move[0] and iy_orig == move[1]:
                                if self.player_color == self.current_turn:
                                    r.blit(highlight_magenta, (x, y))
                                else:
                                    r.blit(highlight_green, (x, y))
                        
                        render_move(self.last_move_src)
                        render_move(self.last_move_dst)
                        
                        
                        if (self.selected_piece is not None and
                            ix_orig == self.selected_piece[0] and
                            iy_orig == self.selected_piece[1]):
                            r.blit(highlight_green, (x, y))
                            continue
                        
                        piece = self.board.piece_at(iy_orig * 8 + ix_orig)
                        
                        possible_move_str = None
                        blit_rendered = False
                        if self.possible_moves:
                            possible_move_str = (ChessDisplayable.coords_to_uci(self.selected_piece[0], self.selected_piece[1]) +
                                                 ChessDisplayable.coords_to_uci(ix_orig, iy_orig))
                            if chess.Move.from_uci(possible_move_str) in self.possible_moves:
                                r.blit(highlight_yellow, (x, y))
                                blit_rendered = True
                            
                            
                            if not blit_rendered and (iy == 0 or iy == 7):
                                index = 0
                                while (not blit_rendered
                                        and index < len(self.promolist)):
                                    
                                    if (chess.Move.from_uci(
                                        possible_move_str + self.promolist[index])
                                        in self.possible_moves):
                                        r.blit(highlight_yellow, (x, y))
                                        blit_rendered = True
                                    
                                    index += 1
                        
                        if piece is None:
                            continue
                        
                        if (mx >= x and mx < x + self.PIECE_WIDTH and
                            my >= y and my < y + self.PIECE_HEIGHT and
                            bool(str(piece).isupper()) == (self.player_color == self.COLOR_WHITE) and
                            self.current_turn == self.player_color and
                            self.selected_piece is None and
                            not self.winner):
                            r.blit(highlight_green, (x, y))
                        
                        if self.winner:
                            result = self.board.result()
                            
                            
                            if str(piece) == "K" and result == "0-1":
                                r.blit(highlight_red, (x, y))
                            
                            
                            elif str(piece) == "k" and result == "1-0":
                                r.blit(highlight_red, (x, y))
                        
                        r.blit(get_piece_render_for_letter(str(piece)), (x, y))
                
                
                if self.current_turn == self.player_color and not self.winner:
                    
                    prompt = renpy.render(self.player_move_prompt, 1280, 720, st, at)
                    pw, ph = prompt.get_size()
                    bh = (height - self.BOARD_HEIGHT) / 2
                    r.blit(prompt, (int((width - pw) / 2), int(self.BOARD_HEIGHT + bh + (bh - ph) / 2)))
                
                if self.selected_piece is not None:
                    
                    piece = self.board.piece_at(self.selected_piece[1] * 8 + self.selected_piece[0])
                    assert piece is not None
                    px, py = get_mouse_pos()
                    px -= self.PIECE_WIDTH / 2
                    py -= self.PIECE_HEIGHT / 2
                    r.blit(get_piece_render_for_letter(str(piece)), (px, py))
                
                
                renpy.redraw(self, 0)
                
                
                
                return r
            
            
            def event(self, ev, x, y, st):
                
                
                if ev.type in self.MOUSE_EVENTS:
                    
                    
                    
                    if self.winner:
                        
                        if self._button_done.event(ev, x, y, st):
                            
                            return self._quitPGN(False)
                    
                    
                    elif self.current_turn == self.player_color:
                        
                        if self._button_save.event(ev, x, y, st):
                            
                            return self._quitPGN(False)
                        
                        elif self._button_giveup.event(ev, x, y, st):
                            renpy.call_in_new_context("mas_chess_confirm_context")
                            if mas_chess.quit_game:
                                
                                return self._quitPGN(True)
                
                def get_piece_pos():
                    mx, my = get_mouse_pos()
                    mx -= (1280 - (self.BOARD_WIDTH - self.BOARD_BORDER_WIDTH * 2)) / 2
                    my -= (720 - (self.BOARD_HEIGHT - self.BOARD_BORDER_HEIGHT * 2)) / 2
                    px = mx / self.PIECE_WIDTH
                    py = my / self.PIECE_HEIGHT
                    if self.player_color == self.COLOR_WHITE:
                        py = 7 - py
                    else: 
                        px = 7 - px
                    if py >= 0 and py < 8 and px >= 0 and px < 8:
                        return (px, py)
                    return (None, None)
                
                
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    px, py = get_piece_pos()
                    if (
                            px is not None
                            and py is not None
                            and self.board.piece_at(py * 8 + px) is not None
                            and bool(str(self.board.piece_at(py * 8 + px)).isupper())
                                == (self.player_color == self.COLOR_WHITE)
                            and self.current_turn == self.player_color
                        ):
                        
                        piece = str(self.board.piece_at(py * 8 + px))
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        self.possible_moves = self.board.legal_moves
                        self.selected_piece = (px, py)
                
                
                if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                    px, py = get_piece_pos()
                    if px is not None and py is not None and self.selected_piece is not None:
                        move_str = self.coords_to_uci(self.selected_piece[0], self.selected_piece[1]) + self.coords_to_uci(px, py)
                        
                        piece = str(
                            self.board.piece_at(
                                self.selected_piece[1] * 8 +
                                self.selected_piece[0]
                            )
                        )
                        
                        if piece.lower() == 'p' and (py == 0 or py == 7):
                            move_str += "q"
                        if chess.Move.from_uci(move_str) in self.possible_moves:
                            self.last_move_src = self.selected_piece
                            self.last_move_dst = (px, py)
                            self.board.push_uci(move_str)
                            
                            self.winner = self.board.is_game_over()
                            if self.current_turn == self.COLOR_BLACK:
                                self.num_turns += 1
                            self.current_turn = not self.current_turn
                            if not self.winner:
                                self.start_monika_analysis()
                            
                            
                            self._button_save.disable()
                            self._button_giveup.disable()
                    
                    self.selected_piece = None
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    self.possible_moves = set([])
                
                
                if ev.type == pygame.KEYUP:
                    
                    
                    if ev.key == pygame.K_m:
                        
                        
                        if ev.mod & pygame.KMOD_SHIFT:
                            mute_music()
                        elif not self.music_menu_open:
                            self.music_menu_open = True
                            select_music()
                        else: 
                            self.music_menu_open = False
                    
                    
                    if (ev.key == pygame.K_PLUS
                            or ev.key == pygame.K_EQUALS
                            or ev.key == pygame.K_KP_PLUS):
                        inc_musicvol()
                    
                    
                    if (ev.key == pygame.K_MINUS
                            or ev.key == pygame.K_UNDERSCORE
                            or ev.key == pygame.K_KP_MINUS):
                        dec_musicvol()
                
                raise renpy.IgnoreEvent()

label game_chess:
    if persistent._mas_chess_timed_disable is not None:
        call mas_chess_dlg_chess_locked from _mas_chess_dclgc
        return

    hide screen keylistener

    m 1eub "You want to play chess? Alright~"


    call demo_minigame_chess from _call_demo_minigame_chess
    return

label demo_minigame_chess:
    $ import store.mas_chess as mas_chess
    $ loaded_game = None
    $ ur_nice_today = True

    if persistent._mas_chess_timed_disable is not None:
        call mas_chess_dlg_chess_locked from _mas_chess_dcldmc
        return

    if not renpy.seen_label("mas_chess_save_selected"):
        call mas_chess_save_migration from _mas_chess_savemg


        if not _return:
            return


        elif _return == mas_chess.CHESS_NO_GAMES_FOUND:
            jump mas_chess_new_game_start


        $ loaded_game = _return




    elif len(persistent._mas_chess_quicksave) > 0:

        python:
            import StringIO 
            import chess.pgn
            import os

            quicksaved_game = chess.pgn.read_game(
                StringIO.StringIO(persistent._mas_chess_quicksave)
            )

            quicksaved_game = mas_chess._checkInProgressGame(
                quicksaved_game,
                mas_monika_twitter_handle
            )


        if quicksaved_game is None:
            $ ur_nice_today = False

            if persistent._mas_chess_3_edit_sorry:
                call mas_chess_dlg_qf_edit_n_3_n_qs from _mas_chess_dlgqfeditn3nqs

                $ persistent._mas_chess_quicksave = ""

                if _return is not None:
                    return
            else:

                python:
                    import os
                    import struct


                    pgn_files = os.listdir(mas_chess.CHESS_SAVE_PATH)
                    if pgn_files:
                        
                        
                        valid_files = list()
                        for filename in pgn_files:
                            in_prog_game = mas_chess.isInProgressGame(
                                filename,
                                mas_monika_twitter_handle
                            )
                            
                            if in_prog_game:
                                valid_files.append((filename, in_prog_game[1]))
                        
                        
                        if len(valid_files) > 0:
                            for filename,pgn_game in valid_files:
                                store._mas_root.mangleFile(
                                    mas_chess.CHESS_SAVE_PATH + filename,
                                    mangle_length=len(str(pgn_game))*2
                                )

                $ persistent._mas_chess_quicksave = ""


                call mas_chess_dlg_qs_lost from _mas_chess_dql_main


                if _return is not None:
                    return

            jump mas_chess_new_game_start


        if persistent._mas_chess_skip_file_checks:
            $ loaded_game = quicksaved_game[1]
            m "Let's continue our unfinished game."
            jump mas_chess_game_load_check


        python:
            quicksaved_game = quicksaved_game[1]

            quicksaved_filename = (
                quicksaved_game.headers["Event"] + mas_chess.CHESS_SAVE_EXT
            )
            quicksaved_filename_clean = (
                mas_chess.CHESS_SAVE_PATH + quicksaved_filename
            ).replace("\\", "/")

            try:
                if os.access(quicksaved_filename_clean, os.R_OK):
                    quicksaved_file = mas_chess.isInProgressGame(
                        quicksaved_filename,
                        mas_monika_twitter_handle
                    )
                else:
                    store.mas_utils.writelog("Failed to access quickfile.\n")
                    quicksaved_file = None
            except Exception as e:
                store.mas_utils.writelog("QUICKFILE: " + str(e) + "\n")
                quicksaved_file = None


        if quicksaved_file is None:
            $ ur_nice_today = False

            python:

                mas_chess.loaded_game_filename = quicksaved_filename_clean

            call mas_chess_dlg_qf_lost from _mas_chess_dql_main2


            if _return == mas_chess.CHESS_GAME_CONT:
                python:
                    try:
                        if os.access(quicksaved_filename_clean, os.R_OK):
                            quicksaved_file = mas_chess.isInProgressGame(
                                quicksaved_filename,
                                mas_monika_twitter_handle
                            )
                        else:
                            store.mas_utils.writelog(
                                "Failed to access quickfile.\n"
                            )
                            quicksaved_file = None
                    except Exception as e:
                        store.mas_utils.writelog(
                            "QUICKFILE: " + str(e) + "\n"
                        )
                        quicksaved_file = None

                if quicksaved_file is None:
                    call mas_chess_dlg_qf_lost_may_removed from _mas_chess_dqlqfr
                    return


            elif _return == mas_chess.CHESS_GAME_BACKUP:
                $ loaded_game = quicksaved_game
                jump mas_chess_game_load_check
            else:



                $ persistent._mas_chess_quicksave = ""


                if _return is not None:
                    return


                jump mas_chess_new_game_start

        python:


            quicksaved_file = quicksaved_file[1]


            is_same = str(quicksaved_game) == str(quicksaved_file)

        if not is_same:

            $ ur_nice_today = False

            call mas_chess_dlg_qf_edit from _mas_chess_dql_main3


            if _return == mas_chess.CHESS_GAME_BACKUP:
                $ loaded_game = quicksaved_game
                jump mas_chess_game_load_check


            elif _return == mas_chess.CHESS_GAME_FILE:
                $ loaded_game = quicksaved_file
                jump mas_chess_game_load_check


            python:
                persistent._mas_chess_quicksave = ""
                try:
                    os.remove(quicksaved_filename_clean)
                except:
                    pass


            if _return is not None:
                return


            jump mas_chess_new_game_start
        else:




            $ loaded_game = quicksaved_game

            if ur_nice_today:


                m 1eua "We still have an unfinished game in progress."
            m "Get ready!"

label mas_chess_game_load_check:

    if loaded_game:

        if loaded_game.headers["White"] == mas_monika_twitter_handle:
            $ player_color = ChessDisplayable.COLOR_BLACK
        else:
            $ player_color = ChessDisplayable.COLOR_WHITE
        jump mas_chess_game_start

label mas_chess_new_game_start:

    if persistent._mas_chess_timed_disable is not None:
        call mas_chess_dlg_chess_locked from _mas_chess_dclngs
        return

    m "What color would suit you?{nw}"
    $ _history_list.pop()
    menu:
        m "What color would suit you?{fast}"
        "White.":

            $ player_color = ChessDisplayable.COLOR_WHITE
        "Black.":
            $ player_color = ChessDisplayable.COLOR_BLACK
        "Let's draw lots!":
            $ choice = random.randint(0, 1) == 0
            if choice:
                $ player_color = ChessDisplayable.COLOR_WHITE
                m 2eua "Oh look, I drew black! Let's begin!"
            else:
                $ player_color = ChessDisplayable.COLOR_BLACK
                m 2eua "Oh look, I drew white! Let's begin!"

label mas_chess_game_start:
    window hide None

    if persistent._mas_chess_timed_disable is not None:
        call mas_chess_dlg_chess_locked from _mas_chess_dclgs
        return

    python:
        ui.add(ChessDisplayable(player_color, pgn_game=loaded_game))
        results = ui.interact(suppress_underlay=True)


        new_pgn_game, is_monika_winner, is_surrender, num_turns = results


        game_result = new_pgn_game.headers["Result"]


        if mas_chess.chess_strength[0]:
            persistent.chess_strength = mas_chess.chess_strength[1]
            mas_chess.chess_strength = (False, 0)






    if game_result == "*":


        call mas_chess_dlg_game_in_progress from _mas_chess_dlggameinprog

        jump mas_chess_savegame

    elif game_result == "1/2-1/2":

        call mas_chess_dlg_game_drawed from _mas_chess_dlggamedrawed
        $ persistent._mas_chess_stats["draws"] += 1

    elif is_monika_winner:
        $ persistent._mas_chess_stats["losses"] += 1
        if is_surrender and num_turns <= 4:


            call mas_chess_dlg_game_monika_win_surr from _mas_chess_dlggmws
        else:


            call mas_chess_dlg_game_monika_win from _mas_chess_dlggmw


        $ persistent.chess_strength -= 1
    else:

        $ persistent._mas_chess_stats["wins"] += 1


        if not persistent.ever_won['chess']:
            $ persistent.ever_won['chess'] = True


        call mas_chess_dlg_game_monika_lose from _mas_chess_dlggml

        $ persistent.chess_strength += 1


    m 1eua "Anyway..."


    if loaded_game:
        jump mas_chess_savegame


    if num_turns > 4:
        m "Would you like to save this game?{nw}"
        $ _history_list.pop()
        menu:
            m "Would you like to save this game?{fast}"
            "Yes.":
                jump mas_chess_savegame
            "No.":

                pass

label mas_chess_playagain:
    m "Do you want to play again?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you want to play again?{fast}"
        "Yes.":

            $ chess_ev = mas_getEV("mas_chess")
            if chess_ev:

                $ chess_ev.shown_count += 1

            jump mas_chess_new_game_start
        "No.":
            pass

label mas_chess_end:
    $ mas_gainAffection(modifier=0.5)

    if is_monika_winner:
        if renpy.seen_label("mas_chess_dlg_game_monika_win_end"):
            call mas_chess_dlg_game_monika_win_end_quick from _mas_chess_dgmwequick
        else:
            call mas_chess_dlg_game_monika_win_end from _mas_chess_dgmwelong


    elif game_result == "*":
        if renpy.seen_label("mas_chess_dlg_game_in_progress_end"):
            call mas_chess_dlg_game_in_progress_end_quick from _mas_chess_dgmipequick
        else:
            call mas_chess_dlg_game_in_progress_end from _mas_chess_dgmipelong
    else:


        if renpy.seen_label("mas_chess_dlg_game_monika_lose_end"):
            call mas_chess_dlg_game_monika_lose_end_quick from _mas_chess_dgmlequick
        else:
            call mas_chess_dlg_game_monika_lose_end from _mas_chess_dgmlelong

    return


label mas_chess_confirm_context:
    call screen mas_chess_confirm
    $ store.mas_chess.quit_game = _return
    return


label mas_chess_save_migration:
    python:
        import chess.pgn
        import os
        import store.mas_chess as mas_chess

        pgn_files = os.listdir(mas_chess.CHESS_SAVE_PATH)
        sel_game = (mas_chess.CHESS_NO_GAMES_FOUND,)

    if pgn_files:
        python:

            pgn_games = list()
            actual_pgn_games = list()
            game_dex = 0
            for filename in pgn_files:
                in_prog_game = mas_chess.isInProgressGame(
                    filename,
                    mas_monika_twitter_handle
                )
                
                if in_prog_game:
                    pgn_games.append((
                        in_prog_game[0],
                        game_dex,
                        False,
                        False
                    ))
                    actual_pgn_games.append((in_prog_game[1], filename))
                    game_dex += 1

            game_count = len(pgn_games)
            pgn_games.sort()
            pgn_games.reverse()


        if game_count > 1:
            if renpy.seen_label("mas_chess_save_multi_dlg"):
                $ pick_text = _("You still need to pick a game to keep.")
            else:
                label mas_chess_save_multi_dlg:
                    m 1m "So I've been thinking, [player]..."
                    m "Most people who leave in the middle of a chess game don't come back to start a new one."
                    m 1n "It makes no sense for me to keep track of more than one unfinished game between us."
                    m 1p "And since we have [game_count] games in progress..."
                    m 1g "I have to ask you to pick only one to keep.{w=0.2} Sorry, [player]."
                    $ pick_text = _("Pick a game you'd like to keep.")
            show monika 1e at t21
            $ renpy.say(m, pick_text, interact=False)

            call screen mas_gen_scrollable_menu(pgn_games, mas_chess.CHESS_MENU_AREA, mas_chess.CHESS_MENU_XALIGN, mas_chess.CHESS_MENU_WAIT_ITEM)

            show monika at t11
            if _return == mas_chess.CHESS_MENU_WAIT_VALUE:

                m 2dsc "I see."
                m 2eua "In that case, please take your time."
                m 1eua "We'll play chess again once you've made your decision."
                return False
            else:

                m 1eua "Alright."
                python:
                    sel_game = actual_pgn_games.pop(_return)
                    for pgn_game in actual_pgn_games:
                        try:
                            os.remove(os.path.normcase(
                                mas_chess.CHESS_SAVE_PATH + pgn_game[1]
                            ))
                        except:
                            pass


        elif game_count == 1:
            $ sel_game = actual_pgn_games[0]


label mas_chess_save_selected:
    return sel_game[0]

label mas_chess_savegame:
    if loaded_game:
        python:
            new_pgn_game.headers["Event"] = (
                loaded_game.headers["Event"]
            )


            save_filename = (
                new_pgn_game.headers["Event"] +
                mas_chess.CHESS_SAVE_EXT
            )


            file_path = mas_chess.CHESS_SAVE_PATH + save_filename


            loaded_game = None
    else:


        python:

            save_name = ""
            while len(save_name) == 0:
                save_name = renpy.input(
                    "Enter a name for this game:",
                    allow=mas_chess.CHESS_SAVE_NAME,
                    length=15
                )
            new_pgn_game.headers["Event"] = save_name


            save_filename = save_name + mas_chess.CHESS_SAVE_EXT

            file_path = mas_chess.CHESS_SAVE_PATH + save_filename


            is_file_exist = os.access(
                os.path.normcase(file_path),
                os.F_OK
            )


        if is_file_exist:
            m 1eka "We already have a game named '[save_name].'"

            m "Should I overwrite it?{nw}"
            $ _history_list.pop()
            menu:
                m "Should I overwrite it?{fast}"
                "Yes.":
                    pass
                "No.":
                    jump mas_chess_savegame

    python:

        with open(file_path, "w") as pgn_file:
            pgn_file.write(str(new_pgn_game))


        if new_pgn_game.headers["Result"] == "*":
            persistent._mas_chess_quicksave = str(new_pgn_game)
        else:
            persistent._mas_chess_quicksave = ""


        display_file_path = mas_chess.REL_DIR + save_filename

    m 1dsc ".{w=0.5}.{w=0.5}.{nw}"
    m 1hua "I've saved our game in '[display_file_path]'!"

    if not renpy.seen_label("mas_chess_pgn_explain"):

        label mas_chess_pgn_explain:
            m 1eua "It's in a format called Portable Game Notation."
            m "You can open this file in PGN viewers."

            if game_result == "*":
                m 1lksdlb "It's possible to edit this file and change the outcome of the game...{w=0.5} {nw}"
                extend 1tsu "but I'm sure you wouldn't do that."

                m 1tku "Right, [player]?{nw}"
                $ _history_list.pop()
                menu:
                    m "Right, [player]?{fast}"
                    "Of course not.":
                        m 1hua "Yay~"

    if game_result == "*":
        jump mas_chess_end

    jump mas_chess_playagain





label mas_chess_dlg_qs_lost:
    python:
        import store.mas_chess as mas_chess
        persistent._mas_chess_dlg_actions[mas_chess.QS_LOST] += 1
        qs_gone_count = persistent._mas_chess_dlg_actions[mas_chess.QS_LOST]

    call mas_chess_dlg_qs_lost_start from _mas_chess_dqsls

    if qs_gone_count == 2:
        call mas_chess_dlg_qs_lost_2 from _mas_chess_dlgqslost2

    elif qs_gone_count == 3:
        call mas_chess_dlg_qs_lost_3 from _mas_chess_dlgqslost3

    elif qs_gone_count % 5 == 0:
        call mas_chess_dlg_qs_lost_5r from _mas_chess_dlgqslost5r

    elif qs_gone_count % 7 == 0:
        call mas_chess_dlg_qs_lost_7r from _mas_chess_dlgqslost7r
    else:

        call mas_chess_dlg_qs_lost_gen from _mas_chess_dlgqslostgen

    return _return


label mas_chess_dlg_qs_lost_start:
    m 2lksdlb "Uh, [player]...{w=0.5} It seems I messed up in saving our last game, and now I can't open it anymore."
    return


label mas_chess_dlg_qs_lost_gen:
    m 1lksdlc "I'm sorry..."
    m 3eksdla "Let's start a new game instead."
    return


label mas_chess_dlg_qs_lost_2:
    m 1lksdld "I'm really, really sorry, [player]."
    m "I hope you can forgive me."
    show monika 1ekc
    pause 1.0
    m 1dsc "I'll make it up to you..."
    m 3eua "...by starting a new game!"
    return


label mas_chess_dlg_qs_lost_3:
    m 1lksdlc "I'm so clumsy, [player]...{w=0.3} I'm sorry."
    m 3eksdla "Let's start a new game instead."
    return


label mas_chess_dlg_qs_lost_5r:
    m 2esc "This has happened [qs_gone_count] times now..."
    m 2tsc "I wonder if this is a side effect of {cps=*0.75}{i}someone{/i}{/cps} trying to edit the saves.{w=1}.{w=1}."
    m 1esd "Anyway..."
    m "Let's start a new game."
    show monika 1esc
    return


label mas_chess_dlg_qs_lost_7r:
    jump mas_chess_dlg_qs_lost_3



label mas_chess_dlg_qf_lost:
    python:
        import store.mas_chess as mas_chess

    call mas_chess_dlg_qf_lost_start from _mas_chess_dqfls

    m "Did you mess with the saves, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Did you mess with the saves, [player]?{fast}"
        "[mas_chess.DLG_QF_LOST_OFCN_CHOICE]" if mas_chess.DLG_QF_LOST_OFCN_ENABLE:
            call mas_chess_dlg_qf_lost_ofcn_start from _mas_chess_dlgqflostofcnstart

        "[mas_chess.DLG_QF_LOST_MAY_CHOICE]" if mas_chess.DLG_QF_LOST_MAY_ENABLE:
            call mas_chess_dlg_qf_lost_may_start from _mas_chess_dlgqflostmaystart

        "[mas_chess.DLG_QF_LOST_ACDNT_CHOICE]" if mas_chess.DLG_QF_LOST_ACDNT_ENABLE:
            call mas_chess_dlg_qf_lost_acdnt_start from _mas_chess_dlgqflostacdntstart

    return _return


label mas_chess_dlg_qf_lost_start:
    m 2lksdla "Well,{w=0.3} this is embarrassing."
    m "I could have sworn that we had an unfinished game, but I can't find the save file."
    return


label mas_chess_dlg_qf_lost_ofcn_start:
    python:
        import store.mas_chess as mas_chess
        persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_OFCN] += 1
        qf_gone_count = persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_OFCN]

    if qf_gone_count == 3:
        call mas_chess_dlg_qf_lost_ofcn_3 from _mas_chess_dlgqflostofcn3

    elif qf_gone_count == 4:
        call mas_chess_dlg_qf_lost_ofcn_4 from _mas_chess_dlgqflostofcn4

    elif qf_gone_count == 5:
        call mas_chess_dlg_qf_lost_ofcn_5 from _mas_chess_dlgqflostofcn5

    elif qf_gone_count >= 6:
        call mas_chess_dlg_qf_lost_ofcn_6 from _mas_chess_dlgqflostofcn6
    else:

        call mas_chess_dlg_qf_lost_ofcn_gen from _mas_chess_dlgqflostofcngen

    return _return


label mas_chess_dlg_qf_lost_ofcn_gen:
    m 1lksdlb "Ah, yeah. You wouldn't do that to me."
    m "I must have misplaced the save files."
    m 1lksdlc "Sorry, [player]."
    m "I'll make it up to you..."
    m 1eua "by starting a new game!"
    return


label mas_chess_dlg_qf_lost_ofcn_3:
    m 2esc "..."
    m "[player],{w=0.2} did you..."
    m 2dsc "Nevermind."
    m 1esc "Let's play a new game."
    return


label mas_chess_dlg_qf_lost_ofcn_4:
    jump mas_chess_dlg_qf_lost_ofcn_3


label mas_chess_dlg_qf_lost_ofcn_5:
    $ mas_loseAffection()
    m 2esc "..."
    m "[player],{w=0.2} this is happening way too much."
    m 2dsc "I really don't believe you this time."
    pause 2.0
    m 2esc "I hope you're not messing with me."
    m "..."
    m 1esc "Whatever.{w=0.5} Let's just play a new game."
    return


label mas_chess_dlg_qf_lost_ofcn_6:






    python:
        mas_loseAffection(modifier=10)

        mas_stripEVL("mas_unlock_chess")

        persistent._seen_ever["mas_unlock_chess"] = True

    m 2dfc "..."
    m 2efc "[player],{w=0.3} I don't believe you."
    m 2efd "If you're just going to throw away our chess games like that..."
    m 6wfw "Then I don't want to play chess with you anymore!"
    return True


label mas_chess_dlg_qf_lost_may_start:
    python:
        import store.mas_chess as mas_chess
        persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_MAYBE] += 1
        qf_gone_count = persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_MAYBE]

    if qf_gone_count == 2:
        call mas_chess_dlg_qf_lost_may_2 from _mas_chess_dlgqflostmay2

    elif qf_gone_count >= 3:
        call mas_chess_dlg_qf_lost_may_3 from _mas_chess_dlgqflostmay3
    else:

        call mas_chess_dlg_qf_lost_may_gen from _mas_chess_dlgqflostmaygen

    return _return



label mas_chess_dlg_qf_lost_may_gen:
    m 2ekd "[player]!{w=0.2} I should have known you were just messing with me!"
    jump mas_chess_dlg_qf_lost_may_filechecker


label mas_chess_dlg_qf_lost_may_gen_found:
    m 2eua "Oh!"
    m 1hua "There's the save.{w=0.2} Thanks for putting it back, [player]."
    m 1eua "Now we can continue our game."
    return store.mas_chess.CHESS_GAME_CONT


label mas_chess_dlg_qf_lost_may_2:
    m 2ekd "[player]!{w=0.2} Stop messing with me!"
    jump mas_chess_dlg_qf_lost_may_filechecker


label mas_chess_dlg_qf_lost_may_2_found:
    jump mas_chess_dlg_qf_lost_may_gen_found


label mas_chess_dlg_qf_lost_may_filechecker:
    $ import os
    $ import store.mas_chess as mas_chess
    $ game_file = mas_chess.loaded_game_filename

    if os.access(game_file, os.F_OK):
        jump mas_chess_dlg_qf_lost_may_gen_found

    m 1eka "Can you put the save back so we can play?"
    if os.access(game_file, os.F_OK):
        jump mas_chess_dlg_qf_lost_may_gen_found

    show monika 1eua


    python:
        renpy.say(m, "I'll wait a minute...", interact=False)
        file_found = False
        seconds = 0
        while not file_found and seconds < 60:
            if os.access(game_file, os.F_OK):
                file_found = True
            else:
                renpy.pause(1.0, hard=True)
                seconds += 1

    if file_found:
        m 1hua "Yay!{w=0.2} Thanks for putting it back, [player]."
        m "Now we can continue our game."
        show monika 1eua
        return mas_chess.CHESS_GAME_CONT


    m 1ekd "[player]..."
    m 1eka "That's okay. Let's just play a new game."
    return


label mas_chess_dlg_qf_lost_may_3:
    $ persistent._mas_chess_skip_file_checks = True

    m 2ekd "[player]! That's--"
    m 2dkc "..."
    m 1esa "...not a problem at all."
    m "I knew you were going to do this again..."
    m 1hub "...so I kept a backup of our save!"

    m 1eua "You can't trick me anymore, [player]."
    m "Now let's continue our game."
    return store.mas_chess.CHESS_GAME_BACKUP


label mas_chess_dlg_qf_lost_may_removed:
    python:
        persistent._mas_chess_timed_disable = datetime.datetime.now()
        mas_loseAffection(modifier=0.5)

    m 2wfw "[player]!"
    m 2wfx "You removed the save again."
    pause 0.7
    m 2rfc "Let's just play chess at another time, then."
    return True


label mas_chess_dlg_qf_lost_acdnt_start:
    python:
        import store.mas_chess as mas_chess
        persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_ACDNT] += 1
        qf_gone_count = persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_ACDNT]

    if qf_gone_count == 2:
        call mas_chess_dlg_qf_lost_acdnt_2 from _mas_chess_dlgqflostacdnt2

    elif qf_gone_count >= 3:
        call mas_chess_dlg_qf_lost_acdnt_3 from _mas_chess_dlgqflostacdnt3
    else:

        call mas_chess_dlg_qf_lost_acdnt_gen from _mas_chess_dlgqflostacdntgen

    return _return


label mas_chess_dlg_qf_lost_acdnt_gen:
    m 1eka "[player]..."
    m "That's okay.{w=0.3} Accidents happen."
    m 1eua "Let's play a new game instead."
    return


label mas_chess_dlg_qf_lost_acdnt_2:
    m 1eka "Again? Don't be so clumsy, [player]."
    m 1hua "But that's okay."
    m "We'll just play a new game instead."
    show monika 1eua
    return


label mas_chess_dlg_qf_lost_acdnt_3:
    $ persistent._mas_chess_skip_file_checks = True

    m 1eka "I had a feeling this would happen again."
    m 3hub "So I kept a backup of our save!"
    m 1eua "Now we can continue our game."
    return store.mas_chess.CHESS_GAME_BACKUP



label mas_chess_dlg_qf_edit:
    python:
        import store.mas_chess as mas_chess

    call mas_chess_dlg_qf_edit_start from _mas_chess_dlgqfeditstart

    m 2ekc "Did you edit the save file?{nw}"
    $ _history_list.pop()
    menu:
        m "Did you edit the save file?{fast}"
        "Yes.":
            call mas_chess_dlg_qf_edit_y_start from _mas_chess_dlgqfeditystart
        "No.":
            call mas_chess_dlg_qf_edit_n_start from _mas_chess_dlgqfeditnstart

    return _return


label mas_chess_dlg_qf_edit_start:
    m 2lksdlc "[player]..."
    return


label mas_chess_dlg_qf_edit_y_start:
    python:
        import store.mas_chess as mas_chess
        persistent._mas_chess_dlg_actions[mas_chess.QF_EDIT_YES] += 1
        qf_edit_count = persistent._mas_chess_dlg_actions[mas_chess.QF_EDIT_YES]

    if qf_edit_count == 1:
        call mas_chess_dlg_qf_edit_y_1 from _mas_chess_dlgqfedity1

    elif qf_edit_count == 2:
        call mas_chess_dlg_qf_edit_y_2 from _mas_chess_dlgqfedity2
    else:

        call mas_chess_dlg_qf_edit_y_3 from _mas_chess_dlgqfedity3

    return _return


label mas_chess_dlg_qf_edit_y_1:
    m 2dsc "I'm disappointed in you."
    m 1euc "But I'm glad that you were honest with me."


    show screen mas_background_timed_jump(5, "mas_chess_dlg_qf_edit_y_1n")
    menu:
        "I'm sorry.":
            hide screen mas_background_timed_jump

            $ mas_gainAffection(modifier=0.5)
            m 1hua "Apology accepted!"
            m 1eua "Luckily, I still remember a little bit of the last game, so we can continue it from there."
            return store.mas_chess.CHESS_GAME_BACKUP
        "...":
            label mas_chess_dlg_qf_edit_y_1n:
                hide screen mas_background_timed_jump
                m 1lfc "Since that game's been ruined, let's just play a new game."
            return
    return


label mas_chess_dlg_qf_edit_y_2:
    python:
        persistent._mas_chess_timed_disable = datetime.datetime.now()
        mas_loseAffection(modifier=0.5)

    m 2dfc "I am incredibly disappointed in you."
    m 2rfc "I don't want to play chess right now."
    return True


label mas_chess_dlg_qf_edit_y_3:
    $ mas_loseAffection()
    $ store.mas_chess.chess_strength = (True, persistent.chess_strength)
    $ persistent.chess_strength = 20
    $ persistent._mas_chess_skip_file_checks = True

    m 2dsc "I'm not surprised..."
    m 2esc "But I am prepared."
    m "I kept a backup of our game just in case you did this again."
    m 1esa "Now let's finish this game."
    return store.mas_chess.CHESS_GAME_BACKUP


label mas_chess_dlg_qf_edit_n_start:
    python:
        import store.mas_chess as mas_chess
        persistent._mas_chess_dlg_actions[mas_chess.QF_EDIT_NO] += 1
        qf_edit_count = persistent._mas_chess_dlg_actions[mas_chess.QF_EDIT_NO]

    if qf_edit_count == 1:
        call mas_chess_dlg_qf_edit_n_1 from _mas_chess_dlgqfeditn1

    elif qf_edit_count == 2:
        call mas_chess_dlg_qf_edit_n_2 from _mas_chess_dlgqfeditn2
    else:

        call mas_chess_dlg_qf_edit_n_3 from _mas_chess_dlgqfeditn3

    return _return


label mas_chess_dlg_qf_edit_n_1:
    $ mas_loseAffection()
    $ store.mas_chess.chess_strength = (True, persistent.chess_strength)
    $ persistent.chess_strength = 20

    m 1ekc "I see."
    m "The save file looks different than how I last remembered it, but maybe that's just my memory failing me."
    m 1eua "Let's continue this game."
    return store.mas_chess.CHESS_GAME_FILE


label mas_chess_dlg_qf_edit_n_2:
    $ mas_loseAffection(modifier=2)
    $ store.mas_chess.chess_strength = (True, persistent.chess_strength)
    $ persistent.chess_strength = 20

    m 1ekc "I see."
    m "..."
    m "Let's just continue this game."
    return store.mas_chess.CHESS_GAME_FILE


label mas_chess_dlg_qf_edit_n_3:
    $ mas_loseAffection(modifier=3)
    m 2dfc "[player]..."
    m 2dftdc "I kept a backup of our game.{w=0.5} I know you edited the save file."
    m 2dftsc "I just-"
    $ _history_list.pop()
    m 6ektsc "I just{fast} can't believe you would cheat and {i}lie{/i} to me."
    m 6rktsc "..."


    show screen mas_background_timed_jump(3, "mas_chess_dlg_qf_edit_n_3n")
    menu:
        "I'm sorry.":
            hide screen mas_background_timed_jump

            $ mas_gainAffection(modifier=0.5)
            call mas_chess_dlg_qf_edit_n_3_s from _mas_chess_dlgqfeditn3s
        "...":

            label mas_chess_dlg_qf_edit_n_3n:
                hide screen mas_background_timed_jump
                call mas_chess_dlg_qf_edit_n_3_n from _mas_chess_dlgqfeditn3n

    return _return


label mas_chess_dlg_qf_edit_n_3_s:
    $ store.mas_chess.chess_strength = (True, persistent.chess_strength)
    $ persistent.chess_strength = 20
    $ persistent._mas_chess_3_edit_sorry = True
    $ persistent._mas_chess_skip_file_checks = True
    $ store.mas_chess._initQuipLists(MASQuipList)

    show monika 6ektsc
    pause 1.0
    show monika 2ektsc
    pause 1.0
    m "I forgive you, [player], but please don't do this to me again."
    m 2lktsc "..."
    return store.mas_chess.CHESS_GAME_BACKUP


label mas_chess_dlg_qf_edit_n_3_n_qs:
    python:
        persistent._mas_chess_timed_disable = datetime.datetime.now()
        mas_loseAffection()

    m 2dfc "[player]..."
    m 2efc "I see you've edited my backup saves."
    m 2lfc "If you want to be like that right now, then we'll play chess some other time."
    return True


label mas_chess_dlg_qf_edit_n_3_n:
    python:

        persistent._mas_chess_mangle_all = True
        persistent.autoload = "mas_chess_go_ham_and_delete_everything"












    m 6ektsc "I can't trust you anymore."
    m "Goodbye, [player].{nw}"


label mas_chess_go_ham_and_delete_everything:
    python:
        import store.mas_chess as mas_chess
        import store._mas_root as mas_root
        import os


        gamedir = os.path.normcase(config.basedir + "/game/")


        for filename in mas_chess.del_files:
            try:
                os.remove(gamedir + filename)
            except:
                pass


        for filename in mas_chess.gt_files:
            mas_root.mangleFile(gamedir + filename)


        try:
            os.remove(
                os.path.normcase(config.basedir + "/characters/monika.chr")
            )
        except:
            pass



        mas_root.resetPlayerData()

    jump _quit



label mas_chess_dlg_chess_locked:

    $ mas_loseAffection(modifier=0.1)
    m 1efc "..."
    m 2lfc "I don't feel like playing chess right now."
    return






label mas_chess_dlg_game_in_progress:
    if persistent._mas_chess_3_edit_sorry:

        pass
    else:

        pass
    return


label mas_chess_dlg_game_drawed:
    if persistent._mas_chess_3_edit_sorry:
        m 1wuo "A draw?"
        m 2lfc "Hmph."
        m 2tfu "I'll beat you next time."
    else:
        m 2tkc "A draw? How boring..."
    return



label mas_chess_dlg_game_monika_win_pre:
    m 1sub "I win!"
    return


label mas_chess_dlg_game_monika_win:
    python:
        import store.mas_chess as mas_chess


    call mas_chess_dlg_game_monika_win_pre from _mas_chess_dlggmwpre


    if persistent._mas_chess_3_edit_sorry:


        $ t_quip, v_quip = mas_chess.monika_wins_mean_quips.quip()


        if t_quip == MASQuipList.TYPE_LABEL:

            call expression v_quip from _mas_chess_dlggmw3esl
        else:


            m 1hub "[v_quip]"
    else:

        python:

            if persistent.chess_strength < 0:
                persistent.chess_strength = 0
            elif persistent.chess_strength > 20:
                persistent.chess_strength = 20

            chess_strength_label = mas_chess.DLG_MONIKA_WIN_BASE.format(
                persistent.chess_strength
            )

        call expression chess_strength_label from _mas_chess_dlggmwcsl

    return


label mas_chess_dlg_game_monika_win_rekt:
    m 1hub "Ahaha~"
    m 1tku "Maybe you should stick to checkers."
    m 1tfu "I doubt you'll ever beat me."
    return


label mas_chess_dlg_game_monika_win_0:
    jump mas_chess_dlg_game_monika_win_2


label mas_chess_dlg_game_monika_win_1:
    jump mas_chess_dlg_game_monika_win_2


label mas_chess_dlg_game_monika_win_2:
    m 1hub "That was really fun, [player]!"
    m 3eka "No matter the outcome, I always enjoy playing chess with you~"
    if renpy.random.randint(1,15) == 1:
        m 3hua "I bet if you keep practicing, you'll be even better than me someday!"
        if renpy.random.randint(1,20) == 1:
            m 3rfu "{cps=*2}...Or at least win occasionally.{/cps}{nw}"
            $ _history_list.pop()
    return


label mas_chess_dlg_game_monika_win_3:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_4:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_5:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_6:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_7:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_8:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_9:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_10:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_11:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_12:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_13:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_14:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_15:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_16:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_17:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_18:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_19:
    jump mas_chess_dlg_game_monika_win_20


label mas_chess_dlg_game_monika_win_20:
    m 1tfu "I'll go a little easier on you next time."
    return



label mas_chess_dlg_game_monika_win_surr_pre:
    m 1eka "Come on, don't give up so easily."
    return


label mas_chess_dlg_game_monika_win_surr:
    python:
        import store.mas_chess as mas_chess


    if persistent._mas_chess_3_edit_sorry:


        $ t_quip, v_quip = mas_chess.monika_wins_surr_mean_quips.quip()


        if t_quip == MASQuipList.TYPE_LABEL:

            call expression v_quip from _mas_chess_dlggmws3esl
        else:


            m 1hub "[v_quip]"
    else:


        call mas_chess_dlg_game_monika_win_surr_pre from _mas_chess_dlggmwspre

        python:

            if persistent.chess_strength < 0:
                persistent.chess_strength = 0
            elif persistent.chess_strength > 20:
                persistent.chess_strength = 20

            chess_strength_label = mas_chess.DLG_MONIKA_WIN_SURR_BASE.format(
                persistent.chess_strength
            )

        call expression chess_strength_label from _mas_chess_dlggmwscsl

    return



label mas_chess_dlg_game_monika_win_surr_resolve:
    m 1tfc "Giving up is a sign of poor resolve..."
    m 1lfc "I don't want a [bf] who has poor resolve."
    return


label mas_chess_dlg_game_monika_win_surr_trying:
    m 1tku "Have you considered {i}actually trying{/i}?"
    m 1tfu "I hear it is beneficial to your mental health."
    return


label mas_chess_dlg_game_monika_win_surr_0:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_1:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_2:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_3:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_4:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_5:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_6:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_7:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_8:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_9:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_10:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_11:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_12:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_13:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_14:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_15:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_16:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_17:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_18:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_19:
    jump mas_chess_dlg_game_monika_win_surr_20


label mas_chess_dlg_game_monika_win_surr_20:

    return



label mas_chess_dlg_game_monika_lose_pre:
    m 2hua "You won! Congratulations."
    return


label mas_chess_dlg_game_monika_lose:
    python:
        import store.mas_chess as mas_chess


    if persistent._mas_chess_3_edit_sorry:


        $ t_quip, v_quip = mas_chess.monika_loses_mean_quips.quip()


        if t_quip == MASQuipList.TYPE_LABEL:

            call expression v_quip from _mas_chess_dlggml3esl
        else:


            m 1dsc "[v_quip]"
    else:


        call mas_chess_dlg_game_monika_lose_pre from _mas_chess_dlggmlp

        python:

            if persistent.chess_strength < 0:
                persistent.chess_strength = 0
            elif persistent.chess_strength > 20:
                persistent.chess_strength = 20

            chess_strength_label = mas_chess.DLG_MONIKA_LOSE_BASE.format(
                persistent.chess_strength
            )

        call expression chess_strength_label from _mas_chess_dlggmlcsl

    return




label mas_chess_dlg_game_monika_lose_silly:
    m 1tku "Surely you don't expect me to believe that you beat me fairly, especially for someone at your skill level."
    m 1tfu "Don't be so silly, [player]."
    return


label mas_chess_dlg_game_monika_lose_0:
    jump mas_chess_dlg_game_monika_lose_2


label mas_chess_dlg_game_monika_lose_1:
    jump mas_chess_dlg_game_monika_lose_2


label mas_chess_dlg_game_monika_lose_2:
    m 1tku "I have to admit, I put less pressure on you than I could have..."
    m 1tsb "I hope you don't mind! I'll be challenging you more as you get better."
    return


label mas_chess_dlg_game_monika_lose_3:
    m 1eua "I'll get you next time for sure!"
    return


label mas_chess_dlg_game_monika_lose_4:
    m 1hua "You played pretty well this game."
    return


label mas_chess_dlg_game_monika_lose_5:
    jump mas_chess_dlg_game_monika_lose_6


label mas_chess_dlg_game_monika_lose_6:
    m 1hua "This game was quite stimulating!"
    return


label mas_chess_dlg_game_monika_lose_7:
    m 3hua "Excellently played, [player]!"
    return


label mas_chess_dlg_game_monika_lose_8:
    jump mas_chess_dlg_game_monika_lose_10


label mas_chess_dlg_game_monika_lose_9:
    jump mas_chess_dlg_game_monika_lose_10


label mas_chess_dlg_game_monika_lose_10:
    m 1wuo "You're quite a strong chess player!"
    return


label mas_chess_dlg_game_monika_lose_11:
    jump mas_chess_dlg_game_monika_lose_12


label mas_chess_dlg_game_monika_lose_12:
    m 1wuo "You're a very challenging opponent, [player]!"
    return


label mas_chess_dlg_game_monika_lose_13:
    jump mas_chess_dlg_game_monika_lose_19


label mas_chess_dlg_game_monika_lose_14:
    jump mas_chess_dlg_game_monika_lose_19


label mas_chess_dlg_game_monika_lose_15:
    jump mas_chess_dlg_game_monika_lose_19


label mas_chess_dlg_game_monika_lose_16:

    m 2lfx "I-{w=1}It's not like I let you win or anything, b-{w=1}baka!"
    return


label mas_chess_dlg_game_monika_lose_17:
    jump mas_chess_dlg_game_monika_lose_19


label mas_chess_dlg_game_monika_lose_18:
    jump mas_chess_dlg_game_monika_lose_19


label mas_chess_dlg_game_monika_lose_19:
    m 1wuo "Wow! You're amazing at chess."
    m 1sub "You could be a professional chess player!"
    return


label mas_chess_dlg_game_monika_lose_20:
    m 1wuo "Wow!"
    m 1tku "Are you sure you're not cheating?"
    return



label mas_chess_dlg_game_monika_win_end:
    m 2eua "Despite its simple rules, chess is a really intricate game."
    m 1eua "It's okay if you find yourself struggling at times."
    m 1hua "Remember, the important thing is to be able to learn from your mistakes."
    return


label mas_chess_dlg_game_monika_win_end_quick:
    m 1eua "Okay, [player], let's play again soon."
    return


label mas_chess_dlg_game_monika_lose_end:
    m 2eub "It's amazing how much more I have to learn even now."
    m 2eua "I really don't mind losing as long as I can learn something."
    m 1hua "After all, the company is good."
    return


label mas_chess_dlg_game_monika_lose_end_quick:
    jump mas_chess_dlg_game_monika_win_end_quick


label mas_chess_dlg_game_in_progress_end:


    jump mas_chess_dlg_game_in_progress_end_quick


label mas_chess_dlg_game_in_progress_end_quick:
    m 1eua "Okay, [player], let's continue this game soon."
    return




screen mas_chess_confirm():


    modal True

    zorder 200

    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:
        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _("Are you sure you want to give up?"):
            style "confirm_prompt"
            text_color mas_globals.button_text_idle_color
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("Yes") action Return(True)
            textbutton _("No") action Return(False)
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
