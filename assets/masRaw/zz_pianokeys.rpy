

















































































default persistent._mas_pnml_data = []


default persistent._mas_piano_keymaps = {}





transform mas_piano_lyric_label:
    xalign 0.5 yalign 0.5



define xp.ZZPK_FULLCOMBO = 40

define xp.ZZPK_PRACTICE = 15


label mas_piano_start:


    $ import store.mas_piano_keys as mas_piano_keys

    $ pnmlLoadTuples()


    m 1hua "You want to play the piano?"

label mas_piano_loopstart:


    $ song_list,final_item = mas_piano_keys.getSongChoices()
    $ song_list.sort()
    $ play_mode = PianoDisplayable.MODE_FREE

label mas_piano_songchoice:

    $ pnml = None

    if len(song_list) > 0:
        m 1eua "Did you want to play a song or play on your own, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "Did you want to play a song or play on your own, [player]?{fast}"
            "Play a song.":
                m "Which song?"
                show monika at t21
                call screen mas_gen_scrollable_menu(song_list, mas_piano_keys.MENU_AREA, mas_piano_keys.MENU_XALIGN, final_item)
                show monika at t11

                $ pnml = _return


                if pnml != "None":


                    m 1hua "I'm so excited to hear you play, [player]!"




                    if pnml.launch_label:
                        call expression pnml.launch_label from _zzpk_ssll


                    $ play_mode = PianoDisplayable.MODE_SONG

                    jump mas_piano_setupstart
                else:


                    jump mas_piano_songchoice
            "On my own.":

                pass
            "Nevermind.":

                jump mas_piano_loopend


    m 1eua "Then play for me, [player]~"

label mas_piano_setupstart:

    show monika 1eua at t22


    python:
        disable_esc()
        mas_MUMURaiseShield()
    stop music



    $ ui.add(PianoDisplayable(play_mode, pnml=pnml))
    $ full_combo,is_win,is_practice,post_piano = ui.interact()



    $ mas_MUMUDropShield()
    $ enable_esc()
    $ mas_startup_song()
    $ pnmlSaveTuples()

    show monika 1hua at t11



    if full_combo and not persistent.ever_won['piano']:
        $ persistent.ever_won['piano']=True


    call expression post_piano from _zzpk_ppel


    if post_piano != "mas_piano_result_none":
        m 1eua "Would you like to play again?{nw}"
        $ _history_list.pop()
        menu:
            m "Would you like to play again?{fast}"
            "Yes.":
                jump mas_piano_loopstart
            "No.":
                pass

label mas_piano_loopend:
    return




label mas_piano_result_default:
    $ mas_gainAffection(modifier=0.2)
    m 1eua "All done, [player]?"
    return


label mas_piano_result_none:
    m 1lksdla "Uhhh [player]..."
    m 1hksdlb "I thought you wanted to play the piano?"
    m 1eka "I really enjoy hearing you play."
    m 1hua "Promise to play for me next time?"
    return



label mas_piano_def_win:
    m 1eua "Wow! You almost got it!"
    m 2eub "Good job, [player]."
    return


label mas_piano_def_fail:
    m 1lksdla "..."
    m 1lksdlb "You did your best, [player]..."
    return


label mas_piano_def_fc:
    m 1eua "Great job!"
    m 1hub "Maybe we should play together sometime!"
    return


label mas_piano_def_prac:
    m 1eua "That was nice, [player]!"
    m 1eka "Make sure to practice often!"
    return



label mas_piano_hb_win:
    $ mas_gainAffection()
    m 1eua "Wow! You almost got it!"
    if mas_isMonikaBirthday():
        if mas_isplayer_bday():
            m 3hub "That's so cool being able to sing along while you play that on our birthday, [player]!"
        else:
            m 1hua "Thanks for playing that for me on my birthday, [player]."
            m 1hubfb "I'm so happy we can spend this special day sharing our love of music!"
    elif mas_isplayer_bday():
        m 3hub "Ahaha! That was really neat, [player]!"
        m 1hua "It's always nice to have a little music to sing along with!"
    else:
        m 2eub "Good job, [player]."
    m 3eub "Make sure you keep practicing. I'm sure you'll play it perfectly next time!"
    return

label mas_piano_hb_fail:
    if mas_isMonikaBirthday():
        if mas_isMoniUpset(lower=True):
            if mas_isplayer_bday():
                $ our = "our"
            else:
                $ our = "my"
            m 1dsd "Well, if you wanted to play this on [our] birthday..."
            m 3tsd "You should have practiced sooner."
        elif mas_isplayer_bday():
            m 1eka "Aw, that's okay, [player]..."
            m 3hub "It was a neat idea to try to play that on our birthday!"
            m 1hua "I'm sure if you keep practicing you'll be able to do it perfectly!"
        else:
            m 1lksdla "I appreciate the thought, [player]."
            m 3eka "Even if you can't get it by the end of the day, I'm sure you'll do better next year."
    elif mas_isplayer_bday():
        m 1eka "That's okay, [player]!"
        m 3hub "It was a neat idea to play that on your birthday while I sung along!"
        m 1hua "I'm sure if you keep practicing you'll be able to do it perfectly!"
    else:
        m 1lksdla "..."
        m 1lksdlb "You did your best, [player]..."
        m "Even a simple song takes time to learn."
    return

label mas_piano_hb_fc:
    $ mas_gainAffection(modifier=1.5)
    if mas_isMonikaBirthday():
        if mas_isplayer_bday():
            m 3hub "Ahaha! That was {i}so{/i} cool!"
            m 1eka "Singing the Birthday Song while you play it on the piano on our birthday..."
            m 1hua "I can't imagine a better way of sharing our special day~"
        else:
            m 1rusdlb "Ahaha! It feels weird to sing the Birthday Song for myself..."
            m 1hub "But you did such a great job playing it!"
            m 1ekbfa "You must have practiced really hard for me..."
            m 1hub "I'm happy that I got to enjoy this with you~"
            m 1hubfb "Thanks for this gift, [player]!"
            if mas_isMoniAff(higher=True):
                m 1ekbfa "You always make me feel special~"
    elif mas_isplayer_bday():
        m 3hub "Ahaha! That was really neat, [player]!"
        m 1hua "It's always nice to have a little music to sing along with!"
    else:
        m 1eua "Hehe, great job!"
        m 2eub "I know that's an easy one, but you did great."
        m 1hub "Are you going to play that for me on my Birthday?"
    return

label mas_piano_hb_prac:
    if mas_isMonikaBirthday():
        if mas_isplayer_bday():
            m 1eka "Aww, you're trying the Birthday Song on our birthday, [player]!"
            m 3hua "Keep trying, I know you can do it!"
        else:
            m 1eua "Thanks for trying to play this one on my birthday!"
            m 1hub "I appreciate your effort!"
    elif mas_isplayer_bday():
        m 1eksdla "Ehehe, trying the Birthday Song on your birthday, [player]?"
        m 3hua "Keep trying, I know you can do it!"
    else:
        m 1eua "You're practicing the Birthday Song?"
        m 3hua "I know you can do it, [player]!"
    return





label mas_piano_yr_win:
    $ mas_gainAffection()
    m 1lksdla "That was nice, [player]."
    m "But..."
    m 1lksdlb "You could do better with some more practice..."
    m 1hksdlb "Ehehe~"
    return


label mas_piano_yr_fc:
    $ mas_gainAffection(modifier=1.5)
    m 1sub "That was wonderful, [player]!"
    m 1eub "I didn't know you can play the piano so well."
    m 1hub "Maybe we should play together sometime!"
    return


label mas_piano_yr_fail:
    m 1lksdlc "..."
    m 1eka "That's okay, [player]."
    m 1hua "At least you tried your best."
    return


label mas_piano_yr_prac:
    m 1hua "That was really cool, [player]!"
    m 3eua "With some more practice, you'll be able to play my song perfectly."
    m 1eka "Make sure to practice everyday for me, okay?~"
    return






init -3 python in mas_piano_keys:
    import pygame 
    import os
    log = renpy.store.mas_utils.getMASLog("log/pnm")

    from store.mas_utils import tryparseint, tryparsefloat


    pnml_basedir = os.path.normcase(
        renpy.config.basedir + "/piano_songs/"
    )
    stock_pnml_basedir = os.path.normcase(
        renpy.config.basedir + "/game/mod_assets/games/piano/songs/"
    )
    no_pnml_basedir = False
    try:
        if not os.access(pnml_basedir, os.F_OK):
            os.mkdir(pnml_basedir)
    except:
        no_pnml_basedir = True


    MENU_X = 680
    MENU_Y = 40
    MENU_W = 560
    MENU_H = 640
    MENU_XALIGN = -0.05
    MENU_AREA = (MENU_X, MENU_Y, MENU_W, MENU_H)


    MISS_KEY = "key '{0}' is missing."
    NOTE_BAD = "bad note list."
    PNOTE_BAD = "bad post note list."
    EXP_BAD = "expression '{0}' not found."
    EVT_BAD = "ev timeout '{0}' is invalid."
    VIST_BAD = "vis timeout '{0}' is invalid."
    VERSE_BAD = "verse '{0}' is invalid."
    PTEXT_BAD = "bad posttext value."
    EXTRA_BAD = "extra key '{0}' found."

    NOTES_BAD = "pnm list cannot be empty."
    VERSES_BAD = "verse list cannot be empty."
    NAME_BAD = "name must be unique."
    LABEL_BAD = "label '{0}' does not exist."
    WAIT_BAD = "wait time '{0}' is invalid."
    L_VERSE_BAD = "verse '{0}' out of bounds."

    LOAD_TRY = "Attempting to load '{0}'..."
    LOAD_SUCC = "'{0}' loaded successfully."
    LOAD_FAILED = "Load failed."

    PNM_LOAD_TRY = "Loading PNM '{0}'..."
    PNM_LOAD_SUCC = "PNM '{0}' loaded successfully!"
    PNM_LOAD_FAILED = "PNM '{0}' load failed."

    JSON_LOAD_FAILED = "Failed to load json at '{0}'."
    FILE_LOAD_FAILED = "Failed to load file at '{0}'. | {1}\n"


    MSG_INFO = "[info]: {0}\n"
    MSG_WARN = "[Warning!]: {0}\n"
    MSG_ERR = "[!ERROR!]: {0}\n"

    MSG_INFO_ID = "    [info]: {0}\n"
    MSG_WARN_ID = "    [Warning!]: {0}\n"
    MSG_ERR_ID = "    [!ERROR!]: {0}\n"


    pnml_db = dict()
    pnml_bk_db = dict() 



    NOTE_SIZE = 5




    QUIT = pygame.K_z
    F4 = pygame.K_q
    F4SH = pygame.K_2
    G4 = pygame.K_w
    G4SH = pygame.K_3
    A4 = pygame.K_e
    A4SH = pygame.K_4
    B4 = pygame.K_r
    C5 = pygame.K_t
    C5SH = pygame.K_6
    D5 = pygame.K_y
    D5SH = pygame.K_7
    E5 = pygame.K_u
    F5 = pygame.K_i
    F5SH = pygame.K_9
    G5 = pygame.K_o
    G5SH = pygame.K_0
    A5 = pygame.K_p
    A5SH = pygame.K_MINUS
    B5 = pygame.K_LEFTBRACKET
    C6 = pygame.K_RIGHTBRACKET
    ESC = pygame.K_ESCAPE


    KEYORDER = [
        F4,
        F4SH,
        G4,
        G4SH,
        A4,
        A4SH,
        B4,
        C5,
        C5SH,
        D5,
        D5SH,
        E5,
        F5,
        F5SH,
        G5,
        G5SH,
        A5,
        A5SH,
        B5,
        C6
    ]


    KEYMAP = {
        F4: F4,
        F4SH: F4SH,
        G4: G4,
        G4SH: G4SH,
        A4: A4,
        A4SH: A4SH,
        B4: B4,
        C5: C5,
        C5SH: C5SH,
        D5: D5,
        D5SH: D5SH,
        E5: E5,
        F5: F5,
        F5SH: F5SH,
        G5: G5,
        G5SH: G5SH,
        A5: A5,
        A5SH: A5SH,
        B5: B5,
        C6: C6
    }


    BLACKLIST = (
        ESC,
        pygame.K_MODE,
        pygame.K_HELP,
        pygame.K_PRINT,
        pygame.K_SYSREQ,
        pygame.K_BREAK,
        pygame.K_MENU,
        pygame.K_POWER,
        pygame.K_EURO

    )


    NONCHAR_TEXT = {
        pygame.K_LEFTBRACKET: "[[",
        123: "{{", 
        pygame.K_BACKSPACE: "\\b",
        pygame.K_TAB: "\\t",
        pygame.K_CLEAR: "Cr",
        pygame.K_RETURN: "\\r",
        pygame.K_PAUSE: "Pa",
        pygame.K_DELETE: "Dl",
        pygame.K_KP0: "K0",
        pygame.K_KP1: "K1",
        pygame.K_KP2: "K2",
        pygame.K_KP3: "K3",
        pygame.K_KP4: "K4",
        pygame.K_KP5: "K5",
        pygame.K_KP6: "K6",
        pygame.K_KP7: "K7",
        pygame.K_KP8: "K8",
        pygame.K_KP9: "K9",
        pygame.K_KP_PERIOD: "K.",
        pygame.K_KP_DIVIDE: "K/",
        pygame.K_KP_MULTIPLY: "K*",
        pygame.K_KP_MINUS: "K-",
        pygame.K_KP_PLUS: "K+",
        pygame.K_KP_ENTER: "Kr",
        pygame.K_KP_EQUALS: "K=",
        pygame.K_UP: "Up",
        pygame.K_DOWN: "Dn",
        pygame.K_RIGHT: "Rg",
        pygame.K_LEFT: "Lf",
        pygame.K_INSERT: "In",
        pygame.K_HOME: "Hm",
        pygame.K_END: "En",
        pygame.K_PAGEUP: "PU",
        pygame.K_PAGEDOWN: "PD",
        pygame.K_F1: "F1",
        pygame.K_F2: "F2",
        pygame.K_F3: "F3",
        pygame.K_F4: "F4",
        pygame.K_F5: "F5",
        pygame.K_F6: "F6",
        pygame.K_F7: "F7",
        pygame.K_F8: "F8",
        pygame.K_F9: "F9",
        pygame.K_F10: "10",
        pygame.K_F11: "11",
        pygame.K_F12: "12",
        pygame.K_F13: "13",
        pygame.K_F14: "14",
        pygame.K_F15: "15",
        pygame.K_NUMLOCK: "NL",
        pygame.K_CAPSLOCK: "CL",
        pygame.K_SCROLLOCK: "SL",
        pygame.K_RSHIFT: "RS",
        pygame.K_LSHIFT: "LS",
        pygame.K_RCTRL: "RC",
        pygame.K_LCTRL: "LC",
        pygame.K_RALT: "RA",
        pygame.K_LALT: "LA",
        pygame.K_RMETA: "RM",
        pygame.K_LMETA: "LM",
        pygame.K_RSUPER: "RW",
        pygame.K_LSUPER: "LW"
    }


    JSON_KEYMAP = {
        "F4": F4,
        "F4SH": F4SH,
        "G4": G4,
        "G4SH": G4SH,
        "A4": A4,
        "A4SH": A4SH,
        "B4": B4,
        "C5": C5,
        "C5SH": C5SH,
        "D5": D5,
        "D5SH": D5SH,
        "E5": E5,
        "F5": F5,
        "F5SH": F5SH,
        "G5": G5,
        "G5SH": G5SH,
        "A5": A5,
        "A5SH": A5SH,
        "B5": B5,
        "C6": C6
    }


    KEYMAP_TO_STR = dict()
    for k in JSON_KEYMAP:
        KEYMAP_TO_STR[JSON_KEYMAP[k]] = k





    def _findKeymap(value):
        """
        Finds the key that points to value in the keymap. Effectively a dict
        value search

        IN:
            value - value to find

        RETURNS:
            key in persistent._mas_piano_keymaps that returns value, or None
            if value not found

        ASSUMES:
            persistent._mas_piano_keymaps
        """
        for k in renpy.game.persistent._mas_piano_keymaps:
            if renpy.game.persistent._mas_piano_keymaps[k] == value:
                return k
        
        return None


    def _setKeymap(key, new):
        """
        Sets a keymap. Checks for existing keymap and will remove it.
        Will NOT set the keymap if key == new

        IN:
            key - the key we are mapping
            new - the new key item to map to

        RETURNS: tuple of the following format:
            [0] - new key that was set (could be None)
            [1] - old key that was originally set (could be None)

        ASSUMES:
            persistent._mas_piano_keymaps
        """
        old_key = _findKeymap(key)
        
        if old_key:
            
            renpy.game.persistent._mas_piano_keymaps.pop(old_key)
        
        
        if key != new:
            renpy.game.persistent._mas_piano_keymaps[new] = key
            return (new, old_key)
        
        return (None, old_key)


    def _strtoN(note):
        """
        Converts a stringified note to a regular note

        IN:
            note - note string to convert

        RETURNS:
            piano note version, or None if this wasnt a real ntoe
        """
        return JSON_KEYMAP.get(note, None)


    def _strtoN_list(note_list):
        """
        Versin of strtoN that can handle a full list

        IN:
            note_list - list of notes to convert

        RETURNS:
            list of piano notes. or None if at least note wasnt real
        """
        real_note_list = []
        for _note in note_list:
            r_note = _strtoN(_note)
            if r_note is None:
                return None
            
            
            real_note_list.append(r_note)
        
        return real_note_list


    def _labelCheck(key, _params, jobj, islogopen):
        """
        specialized json label checking function
        NOTE: only use this for optional params

        IN:
            key - key of label to check
            _params - params dict, also using key
            jobj - json object, also using key
            islogopen - True if log is open, false othrewise
        """
        if key not in jobj:
            return
        
        
        _label = jobj.pop(key)
        if not renpy.has_label(_label):
            if islogopen:
                log.write(MSG_WARN_ID.format(LABEL_BAD.format(_label)))
            return
        
        _params[key] = _label


    def _intCheck_nl(key, _params, jobj, warn_msg, islogopen):
        """
        Specialized json int checking function
        NOTE: only use this for optinal params
        NOTE: non warning list varient of _intCheck

        IN:
            key - key of the integer to check
            _params - params dict, also using key
            jobj - json object, also using key
            warn_msg - warning message
            islogopen - True if log is open, otherwise false
        """
        _warns = list()
        _intCheck(key, _params, _warns, jobj, warn_msg)
        if len(_warns) > 0 and islogopen:
            log.write(MSG_WARN_ID.format(_warns[0]))


    def _noteCheck(key, _params, _warns, jobj, warn_msg):
        """
        Specialized json note list checking function
        NOTE: only use this for optional params

        IN:
            key - key of notes to check
            _params - params dict, also using key
            _warns - warnings list
            jobj - json object, also using key
            warn_msg - message to use for warning
        """
        if key not in jobj:
            return
        
        _notes = _strtoN_list(jobj.pop(key))
        if _notes is None:
            _warns.append(warn_msg)
            return
        
        
        _params[key] = _notes


    def _scCheck(key, _params, _warns, jobj, warn_msg):
        """
        Specialized json spritecode / expression checking function
        NOTE: only use this for optional params

        IN:
            key - key of sprite code to check
            _params - params dict, also using key
            _warns - warning list
            jobj - json object, also using key
            warn_msg - message to use for warning
        """
        if key not in jobj:
            return
        
        _exp = jobj.pop(key)
        if not renpy.image_exists("monika " + _exp):
            _warns.append(warn_msg.format(_exp))
            return
        
        
        _params[key] = _exp


    def _floatCheck(key, _params, _warns, jobj, warn_msg):
        """
        Specialized json float checking function
        NOTE: only use this for optional params

        IN:
            key - key of the float to check
            _params - params dict, also using key
            _warns - warning list
            jobj - json object also using keuy
            warn_msg - message to use for warning
        """
        if key not in jobj:
            return
        
        _m1_zz_pianokeys__num = jobj.pop(key)
        _num = tryparsefloat(_m1_zz_pianokeys__num, -1.0)
        if _num < 0:
            _warns.append(warn_msg.format(_m1_zz_pianokeys__num))
            return
        
        
        _params[key] = _num


    def _intCheck(key, _params, _warns, jobj, warn_msg):
        """
        Specialized json int checking function
        NOTE: only use this for optional params

        IN:
            key - key of the int to check
            _params - params dict, also using key
            _warns - warning list
            jobj - json object also using keuy
            warn_msg - message to use for warning
        """
        if key not in jobj:
            return
        
        _m1_zz_pianokeys__num = jobj.pop(key)
        _num = tryparseint(_m1_zz_pianokeys__num, -1)
        if _num < 0:
            _warns.append(warn_msg.format(_m1_zz_pianokeys__num))
            return
        
        
        _params[key] = _num


    def _boolCheck(key, _params, _warns, jobj, warn_msg):
        """
        Specialized json bool checking function
        NOTE: only use this for optional params

        IN:
            key - key of the bool to check
            _params - params dict, also using key
            _warns - warning list
            jobj - json object also using keuy
            warn_msg - message to use for warning
        """
        if key not in jobj:
            return
        
        _bool = jobj.pop(key)
        if bool != type(_bool):
            _warns.append(warn_msg.format(_bool))
            return
        
        
        _params[key] = _bool




    class PianoException(Exception):
        def __init__(self, msg):
            self.msg = msg
        def __str__(self):
            return "PianoException: " + self.msg



































    class PianoNoteMatch(object):
        
        
        REQ_ARG = [
            "text",
            "style",
            "notes"
        ]
        
        def __init__(self,
                say,
                notes=None,
                postnotes=None,
                express="1eub",
                postexpress="1eua",
                ev_timeout=None,
                vis_timeout=None,
                verse=0,
                copynotes=None,
                posttext=False
            ):
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            if notes is None or len(notes) == 0:
                raise PianoException("Notes list must exist")
            if verse < 0:
                raise PianoException("Verse must be positive number")
            if copynotes is not None and copynotes < 0:
                raise PianoException("copyntoes must be positive number")
            if type(say) is not renpy.text.text.Text:
                raise PianoException("say must be of type Text")
            if not renpy.image_exists("monika " + express):
                raise PianoException("Given expression does not exist")
            if not renpy.image_exists("monika " + postexpress):
                raise PianoException("Given post expression does not exist")
            
            
            
            
            
            
            
            
            
            self.say = say
            self.notes = notes
            self.notestr = "".join([chr(x) for x in notes])
            self.express = "monika " + express
            self.ev_timeout = ev_timeout
            self.vis_timeout = vis_timeout
            self.postnotes = postnotes
            self.postexpress = "monika " + postexpress
            self.verse = verse
            self.copynotes = copynotes
            self.posttext = posttext
            
            
            self.reset()
        
        def isNoteMatch(self, new_key, index=None):
            
            
            
            
            
            
            
            
            
            
            
            
            
            return self._is_match(new_key, self.notes, index=index)
        
        def isPostMatch(self, new_key, index=None):
            
            
            
            
            
            
            
            
            
            
            
            
            
            return self._is_match(new_key, self.postnotes, index=index)
        
        def _is_match(self, new_key, notes, index=None):
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            if index is None:
                index = self.matchdex
            
            if index >= len(notes):
                return -2
            
            if new_key == notes[index]:
                self.matchdex = index + 1
                return 1
            
            return -1
        
        
        def is_single(self):
            """
            RETURNS True if this notematch consists of a single note
            """
            return len(self.notes) == 1
        
        
        def reset(self):
            """
            Resets this piano note match to its default values.

            NOTE: this only clears the following values:
                misses - 0
                fails - 0
                passes - 0
                matchdex - 0
                matched - False
            """
            self.misses = 0
            self.matchdex = 0
            self.fails = 0
            self.passes = 0
            self.matched = False
        
        
        @staticmethod
        def fromJSON(jobj):
            """
            Creates a PianoNoteMatch from a given json object (which is just
            a dict)

            May add warnings to log file

            IN:
                jobj - JSON object (as a dict)

            RETURNS:
                Tuple of the following format:
                [0]: PianoNoteMatch associated with the given json object
                    Or NONE if the Json object is missing required information
                [1]: List of warning strings
                    Or error message string if fatal error occurs
            """
            
            for required in PianoNoteMatch.REQ_ARG:
                if required not in jobj:
                    return (None, MISS_KEY.format(required))
            
            
            _params = dict()
            _warn = list()
            
            
            
            _params["say"] = renpy.text.text.Text(
                jobj.pop("text"),
                style=jobj.pop("style")
            )
            
            
            _notes = _strtoN_list(jobj.pop("notes"))
            if _notes is None:
                return (None, NOTE_BAD)
            _params["notes"] = _notes
            
            
            _noteCheck("postnotes", _params, _warn, jobj, PNOTE_BAD)
            _scCheck("express", _params, _warn, jobj, EXP_BAD)
            _scCheck("postexpress", _params, _warn, jobj, EXP_BAD)
            _floatCheck("ev_timeout", _params, _warn, jobj, EVT_BAD)
            _floatCheck("vis_timeout", _params, _warn, jobj, VIST_BAD)
            _intCheck("verse", _params, _warn, jobj, VERSE_BAD)
            _boolCheck("posttext", _params, _warn, jobj, PTEXT_BAD)
            
            if "copynotes" in jobj:
                
                jobj.pop("copynotes")
            
            if "_comment" in jobj:
                jobj.pop("_comment")
            
            
            if len(jobj) > 0:
                for extra in jobj:
                    _warn.append(EXTRA_BAD.format(extra))
            
            return (PianoNoteMatch(**_params), _warn)


    class PianoNoteMatchList(object):
        """
        This a wrapper for a list of note matches. WE do this so we can
        easily group note matches with other information.

        PROPERTIES:
            pnm_list - list of piano note matches
            verse_list - list of verse indexes (must be in order)
            name - song name (displayed to user in song selection mode)
            full_combos - number of times the song has been played with no
                no mistakes
            wins - number of times the song has been completed
            losses - number of the times the song has been attempted but not
                completed
            win_label - labelt o call to if we played the song well
            fc_label - label to call to if we full comboed
            fail_label - label to call to if we failed the song
            prac_label - label to call if we are practicing
            end_wait - seconds to wait before continuing to quit phase
            launch_label - label to call to prepare song launch
        """
        
        
        REQ_ARG = [
            "pnm_list",
            "verse_list",
            "name"
        ]
        
        def __init__(self,
                pnm_list,
                verse_list,
                name,
                win_label,
                fc_label,
                fail_label,
                prac_label,
                end_wait=0,
                launch_label=None,
                ):
            """
            Creates a PianoNoteMatchList

            IN:
                pnm_list - list of piano note matches
                verse_list - list of verse indexes (must be in order)
                name - song name (displayed to user in song selection mode)
                win_label - label to call to if we played the song well
                fc_label - label to call to if we full comboed the song
                fail_label - label to call to if we failed the song
                prac_label - label to call if we are practicing
                end_wait - number of seoncds to wait before actually quitting
                    (Integers pleaes)
                    (Default: 0)
                launch_label - label to call to prepare this song for play
                    (Default: None)
            """
            if not renpy.has_label(win_label):
                raise PianoException(
                    "label '" + win_label + "' does not exist"
                )
            if not renpy.has_label(fc_label):
                raise PianoException(
                    "label '" + fc_label + "' does not exist"
                )
            if not renpy.has_label(fail_label):
                raise PianoException(
                    "label '" + fail_label + "' does not exist"
                )
            if not renpy.has_label(prac_label):
                raise PianoException(
                    "label '" + prac_label + "' does not exist"
                )
            if launch_label and not renpy.has_label(launch_label):
                raise PianoException(
                    "label '" + launch_label + "' does not exist"
                )
            
            self.pnm_list = pnm_list
            self.verse_list = verse_list
            self.name = name
            self.win_label = win_label
            self.fc_label = fc_label
            self.fail_label = fail_label
            self.prac_label = prac_label
            self.launch_label = launch_label
            self.end_wait = end_wait
            self.full_combos = 0
            self.wins = 0
            self.losses = 0
        
        def resetPNM(self):
            """
            Resets the piano note matches in this Piano Note Match List
            """
            for pnm in self.pnm_list:
                pnm.reset()
        
        def _loadTuple(self, data_tup):
            """
            Fills in the data of this PianoNoteMatchList using the given data
            tup. (which was probably pickeled)

            IN:
                data_tup - tuple of the following format:
                    [0] -> name
                    [1] -> full_combos
                    [2] -> wins
                    [3] -> losses
            """
            if len(data_tup) == 4:
                
                self.name, self.full_combos, self.wins, self.losses = data_tup
        
        def _saveTuple(self):
            """
            Generates a tuple of key data in this PianoNoteMatchList for
            pickling

            RETURNS:
                a tuple of the following format:
                    See _loadTuple
            """
            return (self.name, self.full_combos, self.wins, self.losses)
        
        
        @staticmethod
        def fromJSON(jobj):
            """
            Creats a PianoNoteMatchList from a given JSON object (which is
            just a dict)

            May add warnings to logg file

            IN:
                jobj - JSON object (As a dict)

            RETURNS:
                PianoNoteMatchList associated with given JSON object, or
                None if JSON object is missing required information
            """
            islogopen = log.open()
            log.raw_write = True
            
            
            for required in PianoNoteMatchList.REQ_ARG:
                if required not in jobj:
                    if islogopen:
                        log.write(MSG_ERR.format(MISS_KEY.format(required)))
                        log.write(MSG_ERR.format(LOAD_FAILED))
                    return None
            
            
            _params = dict()
            
            
            _name = jobj.pop("name")
            if islogopen:
                log.write(MSG_INFO.format(LOAD_TRY.format(_name)))
            
            if len(_name) <= 0:
                
                if islogopen:
                    log.write(MSG_ERR_ID.format(NAME_BAD.format(_name)))
                    log.write(MSG_ERR.format(LOAD_FAILED))
                return None
            
            if _name in pnml_bk_db:
                
                if islogopen:
                    log.write(MSG_ERR_ID.format(NAME_BAD.format(_name)))
                    log.write(MSG_ERR.format(LOAD_FAILED))
                return None
            
            _params["name"] = _name
            
            
            _m1_zz_pianokeys__pnm_list = jobj.pop("pnm_list")
            
            if len(_m1_zz_pianokeys__pnm_list) <= 0:
                if islogopen:
                    log.write(MSG_ERR_ID.format(NOTES_BAD))
                    log.write(MSG_ERR.format(LOAD_FAILED))
                return None
            
            _pnm_list = list()
            index = 0
            for _pnm in _m1_zz_pianokeys__pnm_list:
                if islogopen:
                    log.write(MSG_INFO_ID.format(PNM_LOAD_TRY.format(index)))
                
                real_pnm, _msg = PianoNoteMatch.fromJSON(_pnm)
                
                if real_pnm is None:
                    
                    if islogopen:
                        log.write(MSG_ERR_ID.format(_msg))
                        log.write(
                            MSG_ERR_ID.format(PNM_LOAD_FAILED.format(index))
                        )
                        log.write(MSG_ERR.format(LOAD_FAILED))
                    return None
                
                
                _pnm_list.append(real_pnm)
                
                
                if islogopen:
                    for _warn in _msg:
                        log.write(MSG_WARN_ID.format(_warn))
                
                
                if real_pnm.verse < 0 or real_pnm.verse >= len(_pnm_list):
                    if islogopen:
                        log.write(MSG_ERR_ID.format(
                            L_VERSE_BAD.format(real_pnm.verse)
                        ))
                        log.write(
                            MSG_ERR_ID.format(PNM_LOAD_FAILED.format(index))
                        )
                        log.write(MSG_ERR.format(LOAD_FAILED))
                    return None
                
                
                if islogopen:
                    log.write(MSG_INFO_ID.format(PNM_LOAD_SUCC.format(index)))
                index += 1
            _params["pnm_list"] = _pnm_list
            
            
            _verse_list = jobj.pop("verse_list")
            
            if len(_verse_list) <= 0:
                if islogopen:
                    log.write(MSG_ERR_ID.format(VERSES_BAD))
                    log.write(MSG_ERR.format(LOAD_FAILED))
                return None
            
            for _verse in _verse_list:
                if _verse < 0 or _verse >= len(_pnm_list):
                    if islogopen:
                        log.write(MSG_ERR_ID.format(L_VERSE_BAD.format(_verse)))
                        log.write(MSG_ERR.format(LOAD_FAILED))
                    return None
            
            
            _params["verse_list"] = _verse_list
            
            
            _params["win_label"] = "mas_piano_def_win"
            _params["fc_label"] = "mas_piano_def_fc"
            _params["fail_label"] = "mas_piano_def_fail"
            _params["prac_label"] = "mas_piano_def_prac"
            
            
            _labelCheck("win_label", _params, jobj, islogopen)
            _labelCheck("fc_label", _params, jobj, islogopen)
            _labelCheck("fail_label", _params, jobj, islogopen)
            _labelCheck("prac_label", _params, jobj, islogopen)
            _labelCheck("launch_label", _params, jobj, islogopen)
            _intCheck_nl("end_wait", _params, jobj, WAIT_BAD, islogopen)
            
            
            if "_comment" in jobj:
                jobj.pop("_comment")
            
            
            if len(jobj) > 0 and islogopen:
                for extra in jobj:
                    log.write(MSG_WARN_ID.format(EXTRA_BAD.format(extra)))
            
            
            if islogopen:
                log.write(MSG_INFO.format(LOAD_SUCC.format(_name)))
            return PianoNoteMatchList(**_params)



init 790 python in mas_piano_keys:
    import json


    def addSong(filepath, add_main=False):
        """
        Adds a song to the pnml db, given its json filepath

        NOTE: may raise exceptions

        IN:
            filepath - filepath to the JSON we want to load in
                - Assumed to be clean and ready to go
            add_main - True means we should add this to the main pnml db too
                (Default: False)
        """
        islogopen = log.open()
        
        
        with open(filepath, "r") as jsonfile:
            
            
            jobj = json.load(jsonfile)
        
        
        if jobj is None:
            if islogopen:
                log.write(
                    MSG_ERR.format(JSON_LOAD_FAILED.format(filepath))
                )
            return
        
        
        pnml = PianoNoteMatchList.fromJSON(jobj)
        if pnml is None:
            
            return
        
        
        pnml_bk_db[pnml.name] = pnml
        
        
        if add_main:
            pnml_db[pnml.name] = pnml


    def addCustomSongs():
        """
        Adds the custom songs (if we find any) to the game
        """
        if no_pnml_basedir:
            return
        
        
        json_files = [
            j_file
            for j_file in os.listdir(pnml_basedir)
            if j_file.endswith(".json")
        ]
        
        if len(json_files) < 1:
            return
        
        
        for j_song in json_files:
            j_path = pnml_basedir + j_song
            try:
                addSong(j_path, True)
            except Exception as e:
                log.write(
                    MSG_ERR.format(
                        FILE_LOAD_FAILED.format(j_path, repr(e))
                    )
                )


    def addStockSongs():
        """
        Adds the stock songs to the game
        """
        stock_songs = [
            "happybirthday.json",
            "yourreality.json",
            "d__p_c__o.json"
        ]
        
        for song in stock_songs:
            song_path = stock_pnml_basedir + song
            try:
                addSong(song_path)
            except:
                log.write(MSG_ERR.format(FILE_LOAD_FAILED.format(song_path, "")))











































label mas_piano_dpco_win:
    m 2dsc "I can't believe you've done this."
    m 1eka "Not bad, though."
    return

label mas_piano_dpco_fc:

    jump mas_piano_dpco_win


label mas_piano_dpco_fail:
    m 1lksdla "I think it's okay to not learn this one..."
    return


label mas_piano_dpco_prac:
    m 1eka "Do you really want to learn this?"
    return


init 800 python in mas_piano_keys:



    _pnm_dpco_v1l1 = PianoNoteMatch(
        renpy.text.text.Text(
            "Sí, sabes que ya llevo un rato mirándote",
            style="monika_credits_text"
        ),
        [
            D5,
            C5SH,
            B4,
            F4SH,
            B4,
            C5SH,
            D5,
            E5,
            D5,
            C5SH,
            B4,
            A4,
            G4,
            D5,
            D5
        ],
        express="1eua",
        postexpress="1eua",
        verse=0
    )
    _pnm_dpco_v1l2 = PianoNoteMatch(
        renpy.text.text.Text(
            "Tengo que bailar contigo hoy",
            style="monika_credits_text"
        ),
        [
            D5,
            A4,
            D5,
            A4,
            D5,
            A4,
            D5,
            E5,
            C5SH
        ],
        express="1eua",
        postexpress="1eua",
        verse=0
    )
    _pnm_dpco_v1l3 = PianoNoteMatch(
        renpy.text.text.Text(
            "Vi que tu mirada ya estaba llamándome",
            style="monika_credits_text"
        ),
        [
            D5,
            C5SH,
            B4,
            F4SH,
            B4,
            C5SH,
            D5,
            E5,
            D5,
            C5SH,
            B4,
            A4,
            G4,
            D5,
            E5
        ],
        express="1eub",
        postexpress="1eua",
        verse=0
    )
    _pnm_dpco_v1l4 = PianoNoteMatch(
        renpy.text.text.Text(
            "Muéstrame el camino que yo voy",
            style="monika_credits_text"
        ),
        _pnm_dpco_v1l2.notes,
        postnotes=[
            D5,
            C5SH
        ],
        express="1eua",
        postexpress="1eua",
        verse=0,
        copynotes=1
    )


    _pnm_dpco_v2l1 = PianoNoteMatch(
        renpy.text.text.Text(
            "Tú",
            style="monika_credits_text"
        ),
        [B4],
        express="1eua",
        postexpress="1eua",
        verse=4,
        vis_timeout=2.0,
        posttext=True
    )
    _pnm_dpco_v2l2 = PianoNoteMatch(
        renpy.text.text.Text(
            "Tú eres el imán y yo soy el metal",
            style="monika_credits_text"
        ),
        [
            F4SH,
            B4,
            C5SH,
            D5,
            C5SH,
            D5,
            C5SH,
            D5,
            C5SH,
            B4
        ],
        express="1eua",
        postexpress="1eua",
        verse=4,
    )
    _pnm_dpco_v2l3 = PianoNoteMatch(
        renpy.text.text.Text(
            "Me voy acercando y voy armando el plan",
            style="monika_credits_text"
        ),
        [
            G4,
            B4,
            C5SH,
            D5,
            C5SH,
            D5,
            C5SH,
            D5,
            E5,
            A4
        ],
        express="1eua",
        postexpress="1eua",
        verse=4
    )
    _pnm_dpco_v2l4 = PianoNoteMatch(
        renpy.text.text.Text(
            "Solo con pensarlo se acelera el pulso",
            style="monika_credits_text"
        ),
        [
            A4,
            A4,
            A4,
            A4,
            D5,
            C5SH,
            D5,
            C5SH,
            D5,
            E5,
            E5,
            C5SH
        ],
        express="1eua",
        postexpress="1eka",
        verse=4
    )


    _pnm_dpco_v3l1 = PianoNoteMatch(
        renpy.text.text.Text(
            "Ya",
            style="monika_credits_text"
        ),
        _pnm_dpco_v2l1.notes,
        express="1eua",
        postexpress="1eua",
        copynotes=4,
        verse=8,
        ev_timeout=5.0,
        vis_timeout=2.0,
        posttext=True
    )
    _pnm_dpco_v3l2 = PianoNoteMatch(
        renpy.text.text.Text(
            "Ya me está gustando más de lo normal",
            style="monika_credits_text"
        ),
        _pnm_dpco_v2l2.notes,
        copynotes=5,
        verse=8,
        express="1eua",
        postexpress="1eua"
    )
    _pnm_dpco_v3l3 = PianoNoteMatch(
        renpy.text.text.Text(
            "Todos mis sentidos van pidiendo más",
            style="monika_credits_text"
        ),
        _pnm_dpco_v2l3.notes,
        express="1eua",
        postexpress="1eua",
        copynotes=6,
        verse=8
    )
    _pnm_dpco_v3l4 = PianoNoteMatch(
        renpy.text.text.Text(
            "Esto hay que tomarlo sin ningún apuro",
            style="monika_credits_text"
        ),
        _pnm_dpco_v2l4.notes,
        express="1eua",
        postexpress="1eka",
        copynotes=7,
        verse=8
    )



    _pnm_dpco_v4l1 = PianoNoteMatch(
         renpy.text.text.Text(
            "Des-",
            style="monika_credits_text"
        ),
        [D5],
        express="1dsc",
        postexpress="1dsc",
        verse=12,
        ev_timeout=3.0,
        vis_timeout=2.0,
        posttext=True
    )
    _pnm_dpco_v4l2 = PianoNoteMatch(
         renpy.text.text.Text(
            "-pa-",
            style="monika_credits_text"
        ),
        [C5SH],
        express="1dsc",
        postexpress="1dsc",
        ev_timeout=3.0,
        vis_timeout=2.0,
        posttext=True,
        verse=12
    )
    _pnm_dpco_v4l3 = PianoNoteMatch(
         renpy.text.text.Text(
            "-cito",
            style="monika_credits_text"
        ),
        [
            B4,
            F4SH
        ],
        express="1eub",
        postexpress="1eub",
        ev_timeout=3.0,
        vis_timeout=2.0,
        verse=12
    )
    _pnm_dpco_v4l4 = PianoNoteMatch(
         renpy.text.text.Text(
            "Quiero respirar tu cuello despacito",
            style="monika_credits_text"
        ),
        [
            F4SH,
            F4SH,
            F4SH,
            F4SH,
            B4,
            B4,
            B4,
            B4,
            B4,
            A4,
            B4,
            G4
        ],
        express="1eub",
        postexpress="1eub",
        verse=12
    )


    pnml_dpco = PianoNoteMatchList(
        [
            _pnm_dpco_v1l1,
            _pnm_dpco_v1l2,
            _pnm_dpco_v1l3,
            _pnm_dpco_v1l4,
            _pnm_dpco_v2l1,
            _pnm_dpco_v2l2,
            _pnm_dpco_v2l3,
            _pnm_dpco_v2l4,
            _pnm_dpco_v3l1,
            _pnm_dpco_v3l2,
            _pnm_dpco_v3l3,
            _pnm_dpco_v3l4,
            _pnm_dpco_v4l1,
            _pnm_dpco_v4l2,
            _pnm_dpco_v4l3,
            _pnm_dpco_v4l4
        ],
        [0, 4, 8, 12],
        "D--p-c--o",
        "mas_piano_dpco_win",
        "mas_piano_dpco_fc",
        "mas_piano_dpco_fail",
        "mas_piano_dpco_prac",
        5.0

    )








    addStockSongs()


    _m1_zz_pianokeys__stock_song_names = [
        "Happy Birthday",
        "Your Reality"

    ]
    for _song in _m1_zz_pianokeys__stock_song_names:
        if _song in pnml_bk_db:
            pnml_db[_song] = pnml_bk_db[_song]






    addCustomSongs()


    def getSongChoices():
        """
        Creates a list of tuples appropriate to display as a piano song
        selection menu.

        RETURNS:
            Tuple of the following format:
            [0]: list of tuples for song selection. May be an empty list
            [1]: Last item (the nvm) for the song selection

        ASSUMES:
            pnml_db
        """
        song_list = list()
        
        for k in pnml_db:
            pnml = pnml_db.get(k)
            if pnml.wins > 0:
                song_list.append((pnml.name, pnml, False, False))
        
        return song_list, ("Nevermind", "None", False, False, 10)


init 810 python:
    import store.mas_piano_keys as mas_piano_keys


    def pnmlLoadTuples():
        """
        Loads piano note match lists from the saved data, wich is assumed to
        be in the proper format. No checking is done.

        ASSUMES:
            persistent._mas_pnml_data
            mas_piano_keys.pnml_bk_db
        """
        for data_row in persistent._mas_pnml_data:
            db_data = mas_piano_keys.pnml_bk_db.get(data_row[0], None)
            if db_data:
                db_data._loadTuple(data_row)

    def pnmlSaveTuples():
        """
        Saves piano not match list into a pickleable format.

        ASSUMES:
            persistent._mas_pnml_data
            mas_piano_keys.pnml_bk_db
        """
        persistent._mas_pnml_data = [
            mas_piano_keys.pnml_bk_db[k]._saveTuple()
            for k in mas_piano_keys.pnml_bk_db
        ]


    class PianoDisplayable(renpy.Displayable):
        import pygame 
        
        
        
        TIMEOUT = 1.5 
        SONG_TIMEOUT = 3.0 
        SONG_VIS_TIMEOUT = 4.0 
        
        
        
        VIS_TIMEOUT = 2.5 
        
        
        
        
        AT_LIST = [i22]
        TEXT_AT_LIST = [mas_piano_lyric_label]
        
        
        DEFAULT = "monika 1a"
        AWKWARD = "monika 1l"
        HAPPY = "monika 1j"
        FAILED = "monika 1m"
        CONFIGGING = "monika 3a"
        
        
        
        TEXT_TAG = "piano_text"
        
        
        
        
        
        STATE_LISTEN = 0
        
        
        
        
        STATE_JMATCH = 1
        
        
        
        
        
        STATE_MATCH = 2
        
        
        
        
        STATE_MISS = 3
        
        
        
        
        
        
        STATE_FAIL = 4
        
        
        
        
        
        
        
        STATE_JPOST = 5
        
        
        
        
        
        STATE_POST = 6
        
        
        
        
        
        
        
        STATE_VPOST = 7
        
        
        
        
        
        
        STATE_CPOST = 8
        
        
        
        
        
        
        
        STATE_WPOST = 9
        
        
        
        
        
        STATE_CLEAN = 10 
        
        
        
        
        STATE_DONE = 11
        
        
        
        
        STATE_DJPOST = 12
        
        
        
        
        STATE_DPOST = 13
        
        
        
        
        STATE_WDONE = 14
        
        
        
        
        
        
        STATE_CONFIG_WAIT = 15
        
        
        
        
        STATE_CONFIG_CHANGE = 16
        
        
        
        
        STATE_CONFIG_ENTRY = 17
        
        
        
        DONE_STATES = (
            STATE_DPOST,
            STATE_WDONE,
            STATE_DJPOST,
            STATE_DONE
        )
        
        
        POST_STATES = (
            STATE_POST,
            STATE_JPOST,
            STATE_DPOST,
            STATE_DJPOST
        )
        
        
        TRANS_POST_STATES = (
            STATE_WPOST,
            STATE_CPOST,
            STATE_VPOST
        )
        
        
        MATCH_STATES = (
            STATE_MATCH,
            STATE_MISS,
            STATE_JMATCH
        )
        
        
        TOUT_MATCH_STATES = (
            STATE_MATCH,
            STATE_MISS,
            STATE_JMATCH,
            STATE_FAIL
        )
        
        
        TOUT_POST_STATES = (
            STATE_POST,
            STATE_JPOST
        )
        
        
        REND_DONE_STATES = (
            STATE_WDONE,
            STATE_DPOST,
            STATE_DONE
        )
        
        
        FINAL_DONE_STATES = (
            STATE_DONE,
            STATE_WDONE
        )
        
        
        CONFIG_STATES = (
            STATE_CONFIG_WAIT,
            STATE_CONFIG_CHANGE,
            STATE_CONFIG_ENTRY
        )
        
        
        STATE_TO_STRING = {
            STATE_LISTEN: "Listening",
            STATE_JMATCH: "Just matched",
            STATE_MATCH: "In match",
            STATE_MISS: "Missed",
            STATE_FAIL: "Failed",
            STATE_JPOST: "Just Post",
            STATE_POST: "In Post",
            STATE_VPOST: "Visual post",
            STATE_CPOST: "Clean post",
            STATE_WPOST: "Wait post",
            STATE_CLEAN: "Cleaning",
            STATE_DONE: "Done",
            STATE_DJPOST: "Just doned",
            STATE_DPOST: "Done Post",
            STATE_WDONE: "Wait Done",
            STATE_CONFIG_WAIT: "Config wait",
            STATE_CONFIG_CHANGE: "Config change",
            STATE_CONFIG_ENTRY: "Config entry"
        }
        
        
        KEY_LIMIT = 100
        
        
        
        ZZFP_F4 =  "mod_assets/sounds/piano_keys/F4.ogg"
        ZZFP_F4SH = "mod_assets/sounds/piano_keys/F4sh.ogg"
        ZZFP_G4 = "mod_assets/sounds/piano_keys/G4.ogg"
        ZZFP_G4SH = "mod_assets/sounds/piano_keys/G4sh.ogg"
        ZZFP_A4 = "mod_assets/sounds/piano_keys/A4.ogg"
        ZZFP_A4SH = "mod_assets/sounds/piano_keys/A4sh.ogg"
        ZZFP_B4 = "mod_assets/sounds/piano_keys/B4.ogg"
        ZZFP_C5 = "mod_assets/sounds/piano_keys/C5.ogg"
        ZZFP_C5SH = "mod_assets/sounds/piano_keys/C5sh.ogg"
        ZZFP_D5 = "mod_assets/sounds/piano_keys/D5.ogg"
        ZZFP_D5SH = "mod_assets/sounds/piano_keys/D5sh.ogg"
        ZZFP_E5 = "mod_assets/sounds/piano_keys/E5.ogg"
        ZZFP_F5 = "mod_assets/sounds/piano_keys/F5.ogg"
        ZZFP_F5SH = "mod_assets/sounds/piano_keys/F5sh.ogg"
        ZZFP_G5 = "mod_assets/sounds/piano_keys/G5.ogg"
        ZZFP_G5SH = "mod_assets/sounds/piano_keys/G5sh.ogg"
        ZZFP_A5 = "mod_assets/sounds/piano_keys/A5.ogg"
        ZZFP_A5SH = "mod_assets/sounds/piano_keys/A5sh.ogg"
        ZZFP_B5 = "mod_assets/sounds/piano_keys/B5.ogg"
        ZZFP_C6 = "mod_assets/sounds/piano_keys/C6.ogg"
        
        
        ZZPK_IMG_BACK = "mod_assets/games/piano/board.png"
        ZZPK_IMG_KEYS = "mod_assets/games/piano/piano.png"
        
        
        ZZPK_LYR_BAR = "mod_assets/games/piano/lyrical_bar.png"
        
        
        ZZPK_W_OVL_LEFT = "mod_assets/games/piano/ovl/ivory_left.png"
        ZZPK_W_OVL_RIGHT = "mod_assets/games/piano/ovl/ivory_right.png"
        ZZPK_W_OVL_CENTER = "mod_assets/games/piano/ovl/ivory_center.png"
        ZZPK_W_OVL_PLAIN = "mod_assets/games/piano/ovl/ivory_plain.png"
        
        
        ZZPK_B_OVL_PLAIN = "mod_assets/games/piano/ovl/ebony.png"
        
        
        ZZPK_IMG_BACK_X = 5
        ZZPK_IMG_BACK_Y = 10
        ZZPK_IMG_KEYS_X = 51
        ZZPK_IMG_KEYS_Y = 50
        ZZPK_LYR_BAR_YOFF = -50
        
        
        ZZPK_IMG_IKEY_YOFF = 152
        
        
        ZZPK_IMG_IKEY_WIDTH = 36
        ZZPK_IMG_IKEY_HEIGHT = 214
        ZZPK_IMG_EKEY_WIDTH = 29
        ZZPK_IMG_EKEY_HEIGHT = 152
        
        
        MODE_SETUP = -1 
        MODE_FREE = 0
        MODE_SONG = 1 
        
        
        BUTTON_SPACING = 10
        BUTTON_WIDTH = 120
        BUTTON_HEIGHT = 35
        
        
        MOUSE_EVENTS = (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEBUTTONUP
        )
        
        
        
        
        
        
        KMP_TXT_OVL_B_Y = ZZPK_IMG_BACK_Y
        KMP_TXT_OVL_B_W = ZZPK_IMG_EKEY_WIDTH
        KMP_TXT_OVL_B_H = 47
        KMP_TXT_OVL_B_BGCLR = "#4D4154"
        KMP_TXT_OVL_B_FGCLR = "#14001E"
        
        
        KMP_TXT_OVL_W_X = ZZPK_IMG_KEYS_X
        KMP_TXT_OVL_W_Y = ZZPK_IMG_BACK_Y + 281
        KMP_TXT_OVL_W_W = ZZPK_IMG_IKEY_WIDTH
        KMP_TXT_OVL_W_H = 41
        KMP_TXT_OVL_W_BGCLR = "#14001E"
        KMP_TXT_OVL_W_FGCLR = "#4D4154"
        
        KMP_TXT_OVL_FONT = "gui/font/Halogen.ttf"
        
        def __init__(self, mode, pnml=None):
            """
            Creates the piano displablable

            IN:
                mode - the mode we want to be in
                pnml - the piano note match list we want to use
                    (Default: None)
            """
            super(renpy.Displayable,self).__init__()
            
            
            self.mode = mode
            
            
            
            
            self.piano_back = Image(self.ZZPK_IMG_BACK)
            self.piano_keys = Image(self.ZZPK_IMG_KEYS)
            self.PIANO_BACK_WIDTH = 545
            self.PIANO_BACK_HEIGHT = 322
            
            
            self.lyrical_bar = Image(self.ZZPK_LYR_BAR)
            
            
            
            cbutton_x_start = (
                int((self.PIANO_BACK_WIDTH - (
                    (self.BUTTON_WIDTH * 3) + (self.BUTTON_SPACING * 2)
                )) / 2) + self.ZZPK_IMG_BACK_X
            )
            cbutton_y_start = (
                self.ZZPK_IMG_BACK_Y +
                self.PIANO_BACK_HEIGHT +
                self.BUTTON_SPACING
            )
            pbutton_x_start = (
                int((self.PIANO_BACK_WIDTH - (
                    (self.BUTTON_WIDTH * 2) + self.BUTTON_SPACING
                )) / 2) + self.ZZPK_IMG_BACK_X
            )
            pbutton_y_start = cbutton_y_start
            
            
            self._button_done = MASButtonDisplayable.create_stb(
                _("Done"),
                True,
                cbutton_x_start,
                cbutton_y_start,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )
            self._button_cancel = MASButtonDisplayable.create_stb(
                _("Cancel"),
                True,
                cbutton_x_start + self.BUTTON_WIDTH + self.BUTTON_SPACING,
                cbutton_y_start,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )
            self._button_reset = MASButtonDisplayable.create_stb(
                _("Reset"),
                True,
                cbutton_x_start + ((self.BUTTON_WIDTH + self.BUTTON_SPACING) * 2),
                cbutton_y_start,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )
            self._button_resetall = MASButtonDisplayable.create_stb(
                _("Reset All"),
                True,
                cbutton_x_start + ((self.BUTTON_WIDTH + self.BUTTON_SPACING) * 2),
                cbutton_y_start,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )
            
            
            self._button_config = MASButtonDisplayable.create_stb(
                _("Config"),
                True,
                pbutton_x_start,
                pbutton_y_start,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )
            self._button_quit = MASButtonDisplayable.create_stb(
                _("Quit"),
                False,
                pbutton_x_start + self.BUTTON_WIDTH + self.BUTTON_SPACING,
                pbutton_y_start,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )
            
            
            self._always_visible_config = [
                self._button_done,
                self._button_cancel
            ]
            self._always_visible_play = [
                self._button_config,
                self._button_quit
            ]
            
            
            self._config_wait_help = Text(
                _("Click on a pink area to change the keymap for that piano key"),
                font=gui.default_font,
                size=gui.text_size,
                color="#fff",
                outlines=[]
            )
            self._config_change_help = Text(
                _("Press the key you'd like to set this piano key to"),
                font=gui.default_font,
                size=gui.text_size,
                color="#fff",
                outlines=[]
            )
            
            
            
            self.pkeys = {
                mas_piano_keys.F4: self.ZZFP_F4,
                mas_piano_keys.F4SH: self.ZZFP_F4SH,
                mas_piano_keys.G4: self.ZZFP_G4,
                mas_piano_keys.G4SH: self.ZZFP_G4SH,
                mas_piano_keys.A4: self.ZZFP_A4,
                mas_piano_keys.A4SH: self.ZZFP_A4SH,
                mas_piano_keys.B4: self.ZZFP_B4,
                mas_piano_keys.C5: self.ZZFP_C5,
                mas_piano_keys.C5SH: self.ZZFP_C5SH,
                mas_piano_keys.D5: self.ZZFP_D5,
                mas_piano_keys.D5SH: self.ZZFP_D5SH,
                mas_piano_keys.E5: self.ZZFP_E5,
                mas_piano_keys.F5: self.ZZFP_F5,
                mas_piano_keys.F5SH: self.ZZFP_F5SH,
                mas_piano_keys.G5: self.ZZFP_G5,
                mas_piano_keys.G5SH: self.ZZFP_G5SH,
                mas_piano_keys.A5: self.ZZFP_A5,
                mas_piano_keys.A5SH: self.ZZFP_A5SH,
                mas_piano_keys.B5: self.ZZFP_B5,
                mas_piano_keys.C6: self.ZZFP_C6
            }
            
            
            self.pressed = {
                mas_piano_keys.F4: False,
                mas_piano_keys.F4SH: False,
                mas_piano_keys.G4: False,
                mas_piano_keys.G4SH: False,
                mas_piano_keys.A4: False,
                mas_piano_keys.A4SH: False,
                mas_piano_keys.B4: False,
                mas_piano_keys.C5: False,
                mas_piano_keys.C5SH: False,
                mas_piano_keys.D5: False,
                mas_piano_keys.D5SH: False,
                mas_piano_keys.E5: False,
                mas_piano_keys.F5: False,
                mas_piano_keys.F5SH: False,
                mas_piano_keys.G5: False,
                mas_piano_keys.G5SH: False,
                mas_piano_keys.A5: False,
                mas_piano_keys.A5SH: False,
                mas_piano_keys.B5: False,
                mas_piano_keys.C6: False
            }
            
            
            blank_text = Text("")
            
            
            mouse_w_ovl_idle = Solid(

                "#ffe6f4bb",
                xsize=self.ZZPK_IMG_IKEY_WIDTH,
                ysize=self.ZZPK_IMG_IKEY_HEIGHT - self.ZZPK_IMG_IKEY_YOFF
            )
            mouse_w_ovl_hover = Solid(

                "#ffaa99aa",
                xsize=self.ZZPK_IMG_IKEY_WIDTH,
                ysize=self.ZZPK_IMG_IKEY_HEIGHT - self.ZZPK_IMG_IKEY_YOFF
            )
            left = Image(self.ZZPK_W_OVL_LEFT)
            right = Image(self.ZZPK_W_OVL_RIGHT)
            center = Image(self.ZZPK_W_OVL_CENTER)
            w_plain = Image(self.ZZPK_W_OVL_PLAIN)
            whites = [
                (mas_piano_keys.F4, left),
                (mas_piano_keys.G4, center),
                (mas_piano_keys.A4, center),
                (mas_piano_keys.B4, right),
                (mas_piano_keys.C5, left),
                (mas_piano_keys.D5, center),
                (mas_piano_keys.E5, right),
                (mas_piano_keys.F5, left),
                (mas_piano_keys.G5, center),
                (mas_piano_keys.A5, center),
                (mas_piano_keys.B5, right),
                (mas_piano_keys.C6, w_plain),
            ]
            
            
            
            
            mouse_b_ovl_idle = Solid(
                "#ffe6f4bb",
                xsize=self.ZZPK_IMG_EKEY_WIDTH,
                ysize=self.ZZPK_IMG_EKEY_HEIGHT
            )
            mouse_b_ovl_hover = Solid(
                "#ffaa99aa",
                xsize=self.ZZPK_IMG_EKEY_WIDTH,
                ysize=self.ZZPK_IMG_EKEY_HEIGHT
            )
            b_plain = Image(self.ZZPK_B_OVL_PLAIN)
            blacks = [
                (mas_piano_keys.F4SH, 73),
                (mas_piano_keys.G4SH, 110),
                (mas_piano_keys.A4SH, 147),
                (mas_piano_keys.C5SH, 221),
                (mas_piano_keys.D5SH, 258),
                (mas_piano_keys.F5SH, 332),
                (mas_piano_keys.G5SH, 369),
                (mas_piano_keys.A5SH, 406)
            ]
            
            
            self._kmp_txt_ovl_b_bg = Solid(
                self.KMP_TXT_OVL_B_BGCLR,
                xsize=self.KMP_TXT_OVL_B_W,
                ysize=self.KMP_TXT_OVL_B_H
            )
            self._kmp_txt_ovl_w_bg = Solid(
                self.KMP_TXT_OVL_W_BGCLR,
                xsize=self.KMP_TXT_OVL_W_W,
                ysize=self.KMP_TXT_OVL_W_H
            )
            
            
            
            self._keymap_overlays = dict()
            
            
            
            
            
            self.overlays = dict()
            
            
            self._config_overlays = dict()
            
            
            self._config_overlays_list = list()
            
            
            for i in range(0,len(whites)):
                k,img = whites[i]
                top_left_x = (
                    self.ZZPK_IMG_KEYS_X + (i * (self.ZZPK_IMG_IKEY_WIDTH + 1))
                )
                self.overlays[k] = (
                    img,
                    top_left_x,
                    self.ZZPK_IMG_KEYS_Y
                )
                new_button = MASButtonDisplayable(
                    blank_text,
                    blank_text,
                    blank_text,
                    mouse_w_ovl_idle,
                    mouse_w_ovl_hover,
                    mouse_w_ovl_idle,
                    top_left_x + self.ZZPK_IMG_BACK_X,
                    (
                        self.ZZPK_IMG_KEYS_Y +
                        self.ZZPK_IMG_IKEY_YOFF +
                        self.ZZPK_IMG_BACK_Y
                    ),
                    self.ZZPK_IMG_IKEY_WIDTH,
                    self.ZZPK_IMG_IKEY_HEIGHT - self.ZZPK_IMG_IKEY_YOFF,
                    hover_sound=gui.hover_sound,
                    activate_sound=self.pkeys[k],
                    return_value=k
                )
                self._config_overlays[k] = new_button
                self._config_overlays_list.append(new_button)
            
            
            for k,x in blacks:
                self.overlays[k] = (
                    b_plain,
                    x,
                    self.ZZPK_IMG_KEYS_Y
                )
                new_button = MASButtonDisplayable(
                    blank_text,
                    blank_text,
                    blank_text,
                    mouse_b_ovl_idle,
                    mouse_b_ovl_hover,
                    mouse_b_ovl_idle,
                    x + self.ZZPK_IMG_BACK_X,
                    self.ZZPK_IMG_KEYS_Y + self.ZZPK_IMG_BACK_Y,
                    self.ZZPK_IMG_EKEY_WIDTH,
                    self.ZZPK_IMG_EKEY_HEIGHT,
                    hover_sound=gui.hover_sound,
                    activate_sound=self.pkeys[k],
                    return_value=k
                )
                self._config_overlays[k] = new_button
                self._config_overlays_list.append(new_button)
            
            
            
            
            
            self.pnml_list = []
            if self.mode == self.MODE_FREE:
                self.pnml_list = [
                    mas_piano_keys.pnml_db[k] for k in mas_piano_keys.pnml_db
                    if mas_piano_keys.pnml_db[k].wins == 0
                ]
            
            
            self.played = list()
            self.prev_time = 0
            self.drawn_time = 0
            
            
            self.match = None
            
            
            self.justmatched = False
            
            
            self.missed_one = False
            
            
            self.lastmatch = None
            
            
            
            self.failed = False
            
            
            self.state = self.STATE_LISTEN
            
            
            self.lyric = None
            
            
            self.pnm_index = 0
            
            
            self.ev_timeout = self.TIMEOUT
            self.vis_timeout = self.VIS_TIMEOUT
            
            
            self.versedex = 0
            
            
            self.pnml = pnml
            
            
            if self.mode == self.MODE_SONG:
                self.pnml.resetPNM()
                self.match = self.pnml.pnm_list[0]
                self.setsongmode(True)
            
            
            self.note_hit = False
            
            
            self._sel_ovl = None
            
            
            self.live_keymap = None
            
            
            if len(persistent._mas_piano_keymaps) == 0:
                self._button_resetall.disable()
                self.live_keymap = dict(mas_piano_keys.KEYMAP)
            else:
                self._initKeymap()
                for key in persistent._mas_piano_keymaps:
                    self._keymap_overlays[key] = self._buildKeyTextOverlay(key)
            
            
            self._button_cancel.disable()
            self._button_reset.disable()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        def _buildKeyTextOverlay(self, key):
            """
            Builds a keytext overlay for a key. This will check the keymaps
            for the associated actual key and set everything up approptiately.
            Assumes the given key has a keymap

            IN:
                key - the key to build a keytextoverlay for (the key user will
                    press)

            RETURNS:
                MASButtonDisplayable of the text overlay. All states of this
                button will be the same.
            """
            
            real_key = self.live_keymap[key]
            config_ovl_button = self._config_overlays[real_key]
            if key in mas_piano_keys.NONCHAR_TEXT:
                text_key = mas_piano_keys.NONCHAR_TEXT[key]
            else:
                text_key = chr(key).upper()
            
            if config_ovl_button.height == self.ZZPK_IMG_EKEY_HEIGHT:
                
                ovl_text = Text(
                    text_key,
                    font=self.KMP_TXT_OVL_FONT,
                    size=gui.text_size,
                    color=self.KMP_TXT_OVL_B_FGCLR,
                    outlines=[]
                )
                return MASButtonDisplayable(
                    ovl_text,
                    ovl_text,
                    ovl_text,
                    self._kmp_txt_ovl_b_bg,
                    self._kmp_txt_ovl_b_bg,
                    self._kmp_txt_ovl_b_bg,
                    config_ovl_button.xpos,
                    self.KMP_TXT_OVL_B_Y,
                    self.KMP_TXT_OVL_B_W,
                    self.KMP_TXT_OVL_B_H
                )
            
            else:
                
                ovl_text = Text(
                    text_key,
                    font=self.KMP_TXT_OVL_FONT,
                    size=gui.text_size,
                    color=self.KMP_TXT_OVL_W_FGCLR,
                    outlines=[]
                )
                return MASButtonDisplayable(
                    ovl_text,
                    ovl_text,
                    ovl_text,
                    self._kmp_txt_ovl_w_bg,
                    self._kmp_txt_ovl_w_bg,
                    self._kmp_txt_ovl_w_bg,
                    config_ovl_button.xpos,
                    self.KMP_TXT_OVL_W_Y,
                    self.KMP_TXT_OVL_W_W,
                    self.KMP_TXT_OVL_W_H
                )
        
        
        def _initKeymap(self):
            """
            Initalizes the keymap, applying persistent adjustments.

            ASSUMES:
                persistent._mas_piano_keymaps
                mas_piano_keys.KEYMAP - the defaults keymap
                self.live_keymap - the keymap we use
            """
            
            self.live_keymap = dict(mas_piano_keys.KEYMAP)
            
            
            for key,real_key in persistent._mas_piano_keymaps.iteritems():
                if (
                        real_key in self.live_keymap
                        and real_key == self.live_keymap[real_key]
                    ):
                    self.live_keymap.pop(real_key)
                self.live_keymap[key] = real_key
        
        
        def _sendEventsToOverlays(self, ev, x, y, st):
            """
            Sends event overlays to the list of config overlays.
            NOTE: massively assumes that only one clicked event can occur at a
                time.

            IN:
                ev - pygame event
                x - x coord of event
                y - y coord of event
                st - same as st in event

            RETURNS:
                the MASButtonDisplayable that returned a non None value, or
                None if all of them returned None
            """
            for ovl in self._config_overlays_list:
                clicked_ev = ovl.event(ev, x, y, st)
                if clicked_ev is not None:
                    return ovl
            
            return None
        
        
        def _singleFlow(self, ev, key):
            """
            Special workflow for notematches that only have a single note

            IN:
                ev - pygame event
                key - key that was pressed (post map)

            ASSUMES: self.match.is_single is True
            """
            self.match.matchdex = 0
            self.lyric = self.match.say
            self.stateMatch(ev, key)
        
        
        def _timeoutFlow(self):
            """
            Runs flow for timeout cases.
            """
            self.played = list()
            
            
            
            
            
            
            
            
            
            
            
            if self.state in self.DONE_STATES:
                return self.quitflow()
            
            
            
            elif self.state in self.TOUT_MATCH_STATES:
                self.resetVerse()
                self.state = self.STATE_LISTEN
            
            
            
            elif self.state in self.TOUT_POST_STATES:
                next_pnm = self.getnotematch()
                
                if next_pnm:
                    self.setsongmode(
                        ev_tout=next_pnm.ev_timeout,
                        vis_tout=self.match.vis_timeout
                    )
                    self.state = self.STATE_WPOST
                    self.match = next_pnm
                    self.match.matchdex = 0
                
                
                else:
                    self.state = self.STATE_WDONE
                    self._button_config.disable()
            
            
            elif self.state == self.STATE_CLEAN:
                self.state = self.STATE_LISTEN
        
        
        def findnotematch(self, notes):
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            notestr = "".join([chr(x) for x in notes])
            
            
            for pnml in self.pnml_list:
                pnm = pnml.pnm_list[0]
                
                
                findex = pnm.notestr.find(notestr)
                if findex >= 0:
                    pnm.matchdex = findex + len(notestr)
                    pnm.matched = True
                    self.pnm_index = 0
                    self.pnml = pnml 
                    self.mode = self.MODE_SONG 
                    return pnm
            
            return None
        
        def getnotematch(self, index=None):
            
            
            
            
            
            
            
            
            
            
            
            
            if index is None:
                self.pnm_index += 1
                index = self.pnm_index
            
            if index >= len(self.pnml.pnm_list):
                return None
            
            new_pnm = self.pnml.pnm_list[index]
            
            
            
            
            
            return new_pnm
        
        def quitflow(self):
            """
            Quits the game and does the appropriate processing.

            RETURNS:
                tuple of the following format:
                    [0]: true if full_combo, False if not
                    [1]: true if won, false if not
                    [2]: true if both passes and misses are greater than 0
                        (which is like practicing)
                    [3]: label to call next (like post game dialogue)
            """
            
            passes = 0
            fails = 0
            misses = 0
            full_combo = False
            is_win = False
            is_prac = False
            end_label = None
            completed_pnms = 0
            
            if not self.note_hit:
                end_label = "mas_piano_result_none"
            
            elif self.pnml:
                full_combo = True
                
                
                for pnm  in self.pnml.pnm_list:
                    passes += pnm.passes
                    fails += pnm.fails
                    misses += pnm.misses
                    
                    if pnm.passes > 0:
                        completed_pnms += 1
                    
                    if pnm.misses > 0 or pnm.fails > 0 or pnm.passes == 0:
                        full_combo = False
                
                if full_combo:
                    end_label = self.pnml.fc_label
                    self.pnml.full_combos += 1
                    self.pnml.wins += 1
                    is_win = True
                
                
                elif (completed_pnms != len(self.pnml.pnm_list)
                        and fails > passes
                    ):
                    end_label = self.pnml.fail_label
                    self.pnml.losses += 1
                
                
                elif completed_pnms == len(self.pnml.pnm_list):
                    end_label = self.pnml.win_label
                    self.pnml.wins += 1
                    is_win = True
                
                
                else:
                    end_label = self.pnml.prac_label
                    is_prac = True
            
            else:
                end_label = "mas_piano_result_default"
            
            
            return (
                full_combo,
                is_win,
                is_prac,
                end_label
            )
        
        
        def resetVerse(self):
            """
            Resets the current match back to its verse start.
            """
            
            if self.match:
                self.pnm_index = self.match.verse
                self.match = self.getnotematch(self.pnm_index)
        
        
        def setsongmode(self, songmode=True, ev_tout=None, vis_tout=None):
            
            
            
            
            
            
            
            
            
            
            
            if songmode:
                
                if ev_tout:
                    self.ev_timeout = ev_tout
                else:
                    self.ev_timeout = self.SONG_TIMEOUT
                
                if vis_tout:
                    self.vis_timeout = vis_tout
                else:
                    self.vis_timeout = self.SONG_VIS_TIMEOUT
            else:
                self.ev_timeout = self.TIMEOUT
                self.vis_timeout = self.VIS_TIMEOUT
        
        
        def stateListen(self, ev, key):
            """
            Flow that occurs when we in listen state

            IN:
                ev - pygame event that occured
                key - key that was pressed (post map)

            STATES:
                STATE_LISTEN
            """
            
            if self.mode == self.MODE_SONG:
                
                
                findex = self.match.isNoteMatch(key, 0)
                
                if findex >= 0:
                    self.state = self.STATE_JMATCH
                    
                    if self.match.is_single():
                        self._singleFlow(ev, key)
            
            
            
            elif len(self.played) >= mas_piano_keys.NOTE_SIZE:
                
                
                self.match = self.findnotematch(self.played)
                
                
                if self.match:
                    self.state = self.STATE_JMATCH
                    
                    if self.match.is_single():
                        self._singleFlow(ev, key)
        
        
        def stateMatch(self, ev, key):
            """
            Flow that occurs when we are matching notes

            IN:
                ev - pygame event that occured
                key - key that was pressed (post map)

            STATES:
                STATE_MATCH
                STATE_MISS
                STATE_JMATCH
            """
            
            
            findex = self.match.isNoteMatch(key)
            
            
            if findex < 0:
                
                
                if findex == -1:
                    
                    
                    
                    if self.state == self.STATE_MISS:
                        self.match.fails += 1
                        self.state = self.STATE_FAIL
                        
                        
                        
                        
                        self.played = list()
                    
                    
                    
                    
                    
                    
                    else:
                        self.match.misses += 1
                        self.state = self.STATE_MISS
            
            
            else:
                
                
                if self.match.matchdex == len(self.match.notes):
                    
                    
                    self.match.passes += 1
                    
                    
                    if self.match.postnotes:
                        
                        
                        if self.getnotematch(self.pnm_index+1):
                            self.state = self.STATE_JPOST
                        else:
                            self.state = self.STATE_DJPOST
                            self._button_config.disable()
                        
                        self.match.matchdex = 0
                        self.played = list()
                    
                    
                    else:
                        next_pnm = self.getnotematch()
                        
                        if next_pnm:
                            
                            self.lastmatch = self.match
                            self.match = next_pnm
                            self.state = self.STATE_VPOST
                            self.setsongmode(
                                ev_tout=next_pnm.ev_timeout,
                                vis_tout=self.lastmatch.vis_timeout
                            )
                            self.match.matchdex = 0
                            self.played = list()
                        
                        
                        else:
                            self.state = self.STATE_WDONE
                            self._button_config.disable()
                else:
                    self.state = self.STATE_MATCH
        
        
        def statePost(self, ev, key):
            """
            Flow that occurs when we are post matching notes

            IN:
                ev - pygame event that occured
                key - key that was pressed (post map)

            STATES:
                STATE_POST
                STATE_JPOST
                STATE_DPOST
                STATE_DJPOST
            """
            
            findex = self.match.isPostMatch(key)
            
            
            if findex == -1:
                
                next_pnm = self.getnotematch()
                
                
                if next_pnm:
                    
                    if next_pnm.isNoteMatch(key, 0) >= 0:
                        
                        self.state = self.STATE_JMATCH
                        self.match = next_pnm
                        self.played = [key]
                        
                        if self.match.is_single():
                            
                            self._singleFlow(ev, key)
                    
                    else:
                        
                        
                        self.state = self.STATE_WPOST
                        next_pnm.matchdex = 0
                        self.setsongmode(
                            ev_tout=next_pnm.ev_timeout,
                            vis_tout=self.match.vis_timeout
                        )
                        self.match = next_pnm
                        self.played = [key]
                
                
                else:
                    self.state = self.STATE_WDONE
                    self._button_config.disable()
            
            
            elif self.match.matchdex == len(self.match.postnotes):
                
                next_pnm = self.getnotematch()
                
                
                if next_pnm:
                    
                    self.played = list()
                    next_pnm.matchdex = 0
                    self.setsongmode(
                        ev_tout=next_pnm.ev_timeout,
                        vis_tout=self.match.vis_timeout
                    )
                    self.match = next_pnm
                    self.state = self.STATE_WPOST
                
                
                
                else:
                    self.state = self.STATE_WDONE
                    self._button_config.disable()
        
        
        def stateWaitPost(self, ev, key):
            """
            Flow that occurs when we are in a transitional phase from a note
            match to another

            IN:
                ev - pygame event that occured
                key - key that was pressed (post map)

            STATES:
                STATE_WPOST
                STATE_CPOST
                STATE_VPOST
            """
            
            findex = self.match.isNoteMatch(key, index=0)
            
            if findex > 0:
                self.state = self.STATE_JMATCH
                if self.match.is_single():
                    self._singleFlow(ev, key)
            
            else:
                
                
                self.state = self.STATE_CLEAN
                self.played = [key]
        
        
        def render(self, width, height, st, at):
            
            
            
            r = renpy.Render(width, height)
            
            
            back = renpy.render(self.piano_back, 1280, 720, st, at)
            piano = renpy.render(self.piano_keys, 1280, 720, st, at)
            
            
            overlays = list()
            for k in self.pressed:
                if self.pressed[k]:
                    overlays.append(
                        (
                            renpy.render(self.overlays[k][0], 1280, 720, st, at),
                            self.overlays[k][1],
                            self.overlays[k][2]
                        )
                    )
            
            
            keytext_overlays = [
                (
                    self._keymap_overlays[key].render(
                        width, height, st, at
                    ),
                    self._keymap_overlays[key].xpos,
                    self._keymap_overlays[key].ypos
                )
                for key in self._keymap_overlays
            ]
            
            
            r.blit(
                back,
                (
                    self.ZZPK_IMG_BACK_X,
                    self.ZZPK_IMG_BACK_Y
                )
            )
            r.blit(
                piano,
                (
                    self.ZZPK_IMG_KEYS_X + self.ZZPK_IMG_BACK_X,
                    self.ZZPK_IMG_KEYS_Y + self.ZZPK_IMG_BACK_Y
                )
            )
            
            
            for ovl in overlays:
                r.blit(
                    ovl[0],
                    (
                        self.ZZPK_IMG_BACK_X + ovl[1],
                        self.ZZPK_IMG_BACK_Y + ovl[2]
                    )
                )
            
            
            for ovl,x,y in keytext_overlays:
                r.blit(ovl, (x, y))
            
            
            restart_int = False
            
            if self.state in self.CONFIG_STATES:
                
                
                if self.state == self.STATE_CONFIG_ENTRY:
                    
                    
                    renpy.show(self.CONFIGGING)
                    
                    restart_int = True
                    self.state = self.STATE_CONFIG_WAIT
                
                
                
                
                
                visible_overlays = list()
                
                
                visible_buttons = [
                    (
                        b.render(width, height, st, at),
    
                        b.xpos,
                        b.ypos
                    )
                    for b in self._always_visible_config
                ]
                
                
                if self.state == self.STATE_CONFIG_WAIT:
                    visible_buttons.append((
                        self._button_resetall.render(width, height, st, at),
                        self._button_resetall.xpos,
                        self._button_resetall.ypos
                    ))
                    
                    
                    visible_overlays = [
                        (
                            ovl.render(width, height, st, at),
                            ovl.xpos,
                            ovl.ypos
                        )
                        for ovl in self._config_overlays_list
                    ]
                    
                    
                    self.lyric = self._config_wait_help
                
                elif self.state == self.STATE_CONFIG_CHANGE:
                    visible_buttons.append((
                        self._button_reset.render(width, height, st, at),
                        self._button_reset.xpos,
                        self._button_reset.ypos
                    ))
                    
                    
                    
                    
                    self.lyric = self._config_change_help
                
                
                
                
                for ovl,x,y in visible_overlays:
                    r.blit(ovl, (x, y))
            
            else:
                
                
                visible_buttons = [
                    (
                        b.render(width, height, st, at),
                        b.xpos,
                        b.ypos
                    )
                    for b in self._always_visible_play
                ]
                
                
                redrawn = False
                
                
                
                
                
                
                
                
                
                
                if self.state in self.DONE_STATES:
                    
                    if self.state == self.STATE_DJPOST:
                        
                        renpy.show(self.match.postexpress)
                        
                        
                        if not self.match.posttext:
                            self.lyric = None
                        
                        restart_int = True
                        
                        
                        self.state = self.STATE_DPOST
                        
                        
                        renpy.redraw(self, self.vis_timeout)
                    
                    
                    elif st-self.prev_time >= self.vis_timeout:
                        
                        
                        self.state = self.STATE_DONE
                        renpy.timeout(1.0)
                    
                    
                    
                    
                    
                    else:
                        renpy.redraw(self, self.vis_timeout)
                
                
                elif (
                        self.state == self.STATE_CLEAN
                        or st-self.prev_time >= self.ev_timeout
                    ):
                    
                    
                    renpy.show(self.DEFAULT)
                    
                    
                    self.lyric = None
                    
                    restart_int = True
                    
                    if self.state not in self.DONE_STATES:
                        self.state = self.STATE_LISTEN
                        self.resetVerse()
                    self.setsongmode(False)
                
                elif self.state != self.STATE_LISTEN:
                    
                    if self.state == self.STATE_JMATCH:
                        
                        
                        renpy.show(self.match.express)
                        
                        
                        self.lyric = self.match.say
                        
                        
                        self.setsongmode(vis_tout=self.match.vis_timeout)
                        
                        restart_int = True
                        self.state = self.STATE_MATCH
                    
                    elif self.state == self.STATE_MISS:
                        
                        
                        renpy.show(self.AWKWARD)
                        restart_int = True
                    
                    elif self.state == self.STATE_VPOST:
                        
                        
                        renpy.show(self.lastmatch.postexpress)
                        restart_int = True
                        
                        
                        if not self.lastmatch.posttext:
                            self.lyric = None
                        
                        
                        if self.lastmatch.vis_timeout:
                            
                            
                            
                            
                            renpy.redraw(self, self.lastmatch.vis_timeout)
                            self.drawn_time = st
                            self.state = self.STATE_CPOST
                            redrawn = True
                        
                        else:
                            self.state = self.STATE_WPOST
                    
                    elif self.state == self.STATE_CPOST:
                        
                        
                        if st-self.drawn_time >= self.lastmatch.vis_timeout:
                            
                            
                            renpy.show(self.DEFAULT)
                            
                            
                            self.lyric = None
                            
                            restart_int = True
                            self.state = self.STATE_WPOST
                        
                        
                        else:
                            
                            renpy.redraw(self, 1.0)
                            redrawn = True
                    
                    elif self.state == self.STATE_JPOST:
                        
                        
                        renpy.show(self.match.postexpress)
                        
                        
                        if not self.match.posttext:
                            self.lyric = None
                        
                        restart_int = True
                        self.state = self.STATE_POST
                    
                    elif self.state == self.STATE_FAIL:
                        
                        
                        renpy.show(self.FAILED)
                        
                        
                        self.lyric = None
                        
                        restart_int = True
                        self.state = self.STATE_CLEAN
                    
                    
                    if not redrawn:
                        renpy.redraw(self, self.vis_timeout)
            
            
            
            if self.lyric:
                lyric_bar = renpy.render(self.lyrical_bar, 1280, 720, st, at)
                lyric = renpy.render(self.lyric, 1280, 720, st, at)
                pw, ph = lyric.get_size()
                
                
                r.blit(
                    lyric_bar,
                    (
                        0,
                        int((height - 50) /2) - self.ZZPK_LYR_BAR_YOFF
                    )
                )
                r.blit(
                    lyric,
                    (
                        int((width - pw) / 2),
                        int((height - ph) / 2) - self.ZZPK_LYR_BAR_YOFF
                    )
                )
            
            
            if config.developer:
                match_str = ""
                if self.match is not None:
                    match_str = str(self.match.matchdex)
                state_text = renpy.render(
                    renpy.text.text.Text(
                        self.STATE_TO_STRING.get(self.state, "No state") +
                        "| " + match_str
                    ),
                    1280,
                    720,
                    st,
                    at
                )
                stw, sth = state_text.get_size()
                r.blit(
                    state_text,
                    (
                        int((width - stw) / 2),
                        670
                    )
                )
                
                if len(self.played) > 0:
                    played_text = renpy.render(
                        renpy.text.text.Text(
                            "[[" + ", ".join([
                                store.mas_piano_keys.KEYMAP_TO_STR.get(x,"")
                                for x in self.played
                            ]) + "]"
                        ),
                        1280,
                        720,
                        st,
                        at
                    )
                    rtw, rth = played_text.get_size()
                    r.blit(
                        played_text,
                        (
                            int((width - rtw) / 2),
                            645
                        )
                    )
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            for vis_b in visible_buttons:
                r.blit(vis_b[0], (vis_b[1], vis_b[2]))
            
            if restart_int:
                renpy.restart_interaction()
            
            
            
            
            
            return r
        
        def event(self, ev, x, y, st):
            
            
            
            
            if self.state in self.FINAL_DONE_STATES:
                return self.quitflow()
            
            
            if ev.type in self.MOUSE_EVENTS:
                
                
                if self.state == self.STATE_CONFIG_WAIT:
                    
                    
                    clicked_done = self._button_done.event(ev, x, y, st)
                    clicked_resetall = self._button_resetall.event(ev, x, y, st)
                    
                    
                    clicked_ovl = self._sendEventsToOverlays(ev, x, y, st)
                    
                    if clicked_done is not None:
                        
                        self.state = self.STATE_CLEAN
                    
                    elif clicked_resetall is not None:
                        
                        
                        persistent._mas_piano_keymaps = dict()
                        self._initKeymap()
                        self._button_resetall.disable()
                        self._keymap_overlays = dict()
                    
                    elif clicked_ovl is not None:
                        
                        
                        self._sel_ovl = clicked_ovl
                        self._sel_ovl.ground() 
                        self.pressed[clicked_ovl.return_value] = True
                        self.state = self.STATE_CONFIG_CHANGE
                        self._button_done.disable()
                        self._button_cancel.enable()
                        
                        
                        if mas_piano_keys._findKeymap(clicked_ovl.return_value):
                            self._button_reset.enable()
                
                
                elif self.state == self.STATE_CONFIG_CHANGE:
                    
                    
                    clicked_cancel = self._button_cancel.event(ev, x, y, st)
                    clicked_reset = self._button_reset.event(ev, x, y, st)
                    
                    if clicked_cancel is not None:
                        
                        self.state = self.STATE_CONFIG_WAIT
                        self._button_done.enable()
                        self._button_cancel.disable()
                        self._button_reset.disable()
                        self.pressed[self._sel_ovl.return_value] = False
                        
                        if len(persistent._mas_piano_keymaps) > 0:
                            self._button_resetall.enable()
                    
                    elif clicked_reset is not None:
                        
                        old_key = mas_piano_keys._findKeymap(
                            self._sel_ovl.return_value
                        )
                        
                        if old_key:
                            persistent._mas_piano_keymaps.pop(old_key)
                            self._keymap_overlays.pop(old_key)
                        
                        self.state = self.STATE_CONFIG_WAIT
                        self._button_done.enable()
                        self._button_cancel.disable()
                        self._button_reset.disable()
                        self.pressed[self._sel_ovl.return_value] = False
                        self._initKeymap()
                
                
                else:
                    
                    clicked_config = self._button_config.event(ev, x, y, st)
                    clicked_quit = self._button_quit.event(ev, x, y, st)
                    
                    
                    if clicked_quit is not None:
                        return self.quitflow()
                    
                    elif clicked_config is not None:
                        self.state = self.STATE_CONFIG_ENTRY
                        
                        
                        self.resetVerse()
                        self.setsongmode(False)
                        self.played = list()
                
                renpy.redraw(self, 0)
            
            
            elif ev.type == pygame.KEYDOWN:
                
                if self.state == self.STATE_CONFIG_CHANGE:
                    
                    if (
                            ev.key not in mas_piano_keys.BLACKLIST
                            and (ev.key in mas_piano_keys.NONCHAR_TEXT
                                or 0 <= ev.key <= 255
                            )
                        ):
                        
                        
                        new_key, old_key = mas_piano_keys._setKeymap(
                            self._sel_ovl.return_value,
                            ev.key
                        )
                        
                        
                        self.state = self.STATE_CONFIG_WAIT
                        self._button_done.enable()
                        self._button_cancel.disable()
                        self._button_reset.disable()
                        self.pressed[self._sel_ovl.return_value] = False
                        self._initKeymap()
                        
                        
                        if len(persistent._mas_piano_keymaps) > 0:
                            self._button_resetall.enable()
                        else:
                            self._button_resetall.disable()
                        
                        
                        if old_key in self._keymap_overlays:
                            self._keymap_overlays.pop(old_key)
                        if new_key:
                            self._keymap_overlays[new_key] = (
                                self._buildKeyTextOverlay(new_key)
                            )
                        
                        renpy.play(
                            self.pkeys[self._sel_ovl.return_value],
                            channel="audio"
                        )
                        
                        renpy.redraw(self, 0)
                
                else:
                    
                    key = self.live_keymap.get(ev.key, None)
                    
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                    
                    
                    if not self.pressed.get(key, True):
                        
                        
                        self.pressed[key] = True
                        
                        
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(key)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, key)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, key)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, key)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, key)
                        
                        
                        renpy.play(self.pkeys[key], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)
            
            
            elif ev.type == pygame.KEYUP:
                
                
                key = self.live_keymap.get(ev.key, None)
                
                
                if self.pressed.get(key, False):
                    
                    
                    self.pressed[key] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            
            
            elif ev.type == renpy.display.core.TIMEEVENT:
                
                renpy.redraw(self, 0)
            
            
            raise renpy.IgnoreEvent()
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
