











































init python:

    mas_curr_affection = store.mas_affection.NORMAL
    mas_curr_affection_group = store.mas_affection.G_NORMAL

init -900 python in mas_affection:



    BROKEN = 1
    DISTRESSED = 2
    UPSET = 3
    NORMAL = 4
    HAPPY = 5
    AFFECTIONATE = 6
    ENAMORED = 7
    LOVE = 8


    _aff_order = [
        BROKEN,
        DISTRESSED,
        UPSET,
        NORMAL,
        HAPPY,
        AFFECTIONATE,
        ENAMORED,
        LOVE
    ]


    _aff_level_map = {}
    for _item in _aff_order:
        _aff_level_map[_item] = _item



    _aff_cascade_map = {
        BROKEN: DISTRESSED,
        DISTRESSED: UPSET,
        UPSET: NORMAL,
        HAPPY: NORMAL,
        AFFECTIONATE: HAPPY,
        ENAMORED: AFFECTIONATE,
        LOVE: ENAMORED
    }



    G_SAD = -1
    G_HAPPY = -2
    G_NORMAL = -3


    _affg_order = [
        G_SAD,
        G_NORMAL,
        G_HAPPY
    ]



    _affg_cascade_map = {
        G_SAD: G_NORMAL,
        G_HAPPY: G_NORMAL
    }


    FORCE_EXP_MAP = {
        BROKEN: "monika 6ckc_static",
        DISTRESSED: "monika 6rkc_static",
        UPSET: "monika 2esc_static",
        NORMAL: "monika 1eua_static",
        AFFECTIONATE: "monika 1eua_static",
        ENAMORED: "monika 1hua_static",
        LOVE: "monika 1hua_static",
    }



    def _compareAff(aff_1, aff_2):
        """
        See mas_compareAff for explanation
        """
        
        if aff_1 == aff_2:
            return 0
        
        
        if aff_1 not in _aff_order or aff_2 not in _aff_order:
            return 0
        
        
        if _aff_order.index(aff_1) < _aff_order.index(aff_2):
            return -1
        
        return 1


    def _compareAffG(affg_1, affg_2):
        """
        See mas_compareAffG for explanation
        """
        
        if affg_1 == affg_2:
            return 0
        
        
        if affg_1 not in _affg_order or affg_2 not in _affg_order:
            return 0
        
        
        if _affg_order.index(affg_1) < _affg_order.index(affg_2):
            return -1
        
        return 1


    def _betweenAff(aff_low, aff_check, aff_high):
        """
        checks if the given affection level is between the given low and high.
        See mas_betweenAff for explanation
        """
        aff_check = _aff_level_map.get(aff_check, None)
        
        
        if aff_check is None:
            
            return False
        
        
        aff_low = _aff_level_map.get(aff_low, None)
        aff_high = _aff_level_map.get(aff_high, None)
        
        if aff_low is None and aff_high is None:
            
            
            return True
        
        if aff_low is None:
            
            
            return _compareAff(aff_check, aff_high) <= 0
        
        if aff_high is None:
            
            
            return _compareAff(aff_check, aff_low) >= 0
        
        
        
        comp_low_high = _compareAff(aff_low, aff_high)
        if comp_low_high > 0:
            
            
            return False
        
        if comp_low_high == 0:
            
            return _compareAff(aff_low, aff_check) == 0
        
        
        return (
            _compareAff(aff_low, aff_check) <= 0
            and _compareAff(aff_check, aff_high) <= 0
        )


    def _isValidAff(aff_check):
        """
        Returns true if the given affection is a valid affection state

        NOTE: None is considered valid
        """
        if aff_check is None:
            return True
        
        return aff_check in _aff_level_map


    def _isValidAffRange(aff_range):
        """
        Returns True if the given aff range is a valid aff range.

        IN:
            aff_range - tuple of the following format:
                [0]: lower bound
                [1]: upper bound
            NOTE: Nones are considerd valid.
        """
        if aff_range is None:
            return True
        
        low, high = aff_range
        
        if not _isValidAff(low):
            return False
        
        if not _isValidAff(high):
            return False
        
        if low is None and high is None:
            return True
        
        return _compareAff(low, high) <= 0





    AFF_MAX_POS_TRESH = 100
    AFF_MIN_POS_TRESH = 30
    AFF_MIN_NEG_TRESH = -30
    AFF_MAX_NEG_TRESH = -75


    AFF_BROKEN_MIN = -100
    AFF_DISTRESSED_MIN = -75
    AFF_UPSET_MIN = -30
    AFF_HAPPY_MIN = 30
    AFF_AFFECTIONATE_MIN = 100
    AFF_ENAMORED_MIN = 400
    AFF_LOVE_MIN = 1000


    AFF_MOOD_HAPPY_MIN = 30
    AFF_MOOD_SAD_MIN = -30


    AFF_TIME_CAP = -101


init -1 python in mas_affection:
    import os
    import datetime
    import store.mas_utils as mas_utils
    import store



    if store.persistent._mas_affection_log_counter is None:
        
        store.persistent._mas_affection_log_counter = 0

    elif store.persistent._mas_affection_log_counter >= 500:
        
        mas_utils.logrotate(
            os.path.normcase(renpy.config.basedir + "/log/"),
            "aff_log.txt"
        )
        store.persistent._mas_affection_log_counter = 0

    else:
        
        store.persistent._mas_affection_log_counter += 1


    log = renpy.store.mas_utils.getMASLog("log/aff_log", append=True)
    log_open = log.open()
    log.raw_write = True
    log.write("VERSION: {0}\n".format(store.persistent.version_number))



    _audit = "[{0}]: {1} | {2} | {3} -> {4}\n"


    _audit_f = "[{0}]: {5} | {1} | {2} | {3} -> {4}\n"
    _freeze_text = "!FREEZE!"
    _bypass_text = "!BYPASS!"

    def audit(change, new, frozen=False, bypass=False, ldsv=None):
        """
        Audits a change in affection.

        IN:
            change - the amount we are changing by
            new - what the new affection value will be
            frozen - True means we were frozen, false measn we are not
            bypass - True means we bypassed, false means we did not
            ldsv - Set to the string to use instead of monikatopic
                NOTE: for load / save operations ONLY
        """
        if ldsv is None:
            piece_one = store.persistent.current_monikatopic
        else:
            piece_one = ldsv
        
        if frozen:
            
            
            if bypass:
                piece_five = _bypass_text
            else:
                piece_five = _freeze_text
            
            
            audit_text = _audit_f.format(
                datetime.datetime.now(),
                piece_one,
                change,
                store._mas_getAffection(),
                new,
                piece_five
            )
        
        else:
            audit_text = _audit.format(
                datetime.datetime.now(),
                piece_one,
                change,
                store._mas_getAffection(),
                new
            )
        
        log.write(audit_text)


    def raw_audit(old, new, change, tag):
        """
        Non affection-dependent auditing for general usage.

        IN:
            old - the "old" value
            new - the "new" value
            change - the chnage amount
            tag - a string to label this audit change
        """
        log.write(_audit.format(
            datetime.datetime.now(),
            tag,
            change,
            old,
            new
        ))


    def txt_audit(tag, msg):
        """
        Generic auditing in the aff log

        IN:
            tag - a string to label thsi audit
            msg - message to show
        """
        log.write("[{0}]: {1} | {2}\n".format(
            datetime.datetime.now(),
            tag,
            msg
        ))



    def _force_exp():
        """
        Determines appropriate forced expression for current affection.
        """
        curr_aff = store.mas_curr_affection
        
        if store.mas_isMoniNormal() and store.mas_isBelowZero():
            
            return "monika 1esc_static"
        
        return FORCE_EXP_MAP.get(curr_aff, "monika idle")



init 15 python in mas_affection:
    import store 
    import store.evhand as evhand
    import store.mas_selspr as mas_selspr
    import store.mas_layout as mas_layout
    persistent = renpy.game.persistent
    layout = store.layout













    def _brokenToDis():
        """
        Runs when transitioning from broken to distressed
        """
        
        layout.QUIT_YES = mas_layout.QUIT_YES_DIS
        layout.QUIT_NO = mas_layout.QUIT_NO_UPSET
        layout.QUIT = mas_layout.QUIT
        
        
        store.mas_idle_mailbox.send_rebuild_msg()


    def _disToBroken():
        """
        Runs when transitioning from distressed to broken
        """
        
        layout.QUIT_YES = mas_layout.QUIT_YES_BROKEN
        layout.QUIT_NO = mas_layout.QUIT_NO_BROKEN
        layout.QUIT = mas_layout.QUIT_BROKEN
        
        
        store.mas_idle_mailbox.send_rebuild_msg()


    def _disToUpset():
        """
        Runs when transitioning from distressed to upset
        """
        
        layout.QUIT_YES = mas_layout.QUIT_YES
        
        
        store.mas_idle_mailbox.send_rebuild_msg()


    def _upsetToDis():
        """
        Runs when transitioning from upset to distressed
        """
        
        layout.QUIT_YES = mas_layout.QUIT_YES_DIS
        if persistent._mas_acs_enable_promisering:
            renpy.store.monika_chr.remove_acs(renpy.store.mas_acs_promisering)
            persistent._mas_acs_enable_promisering = False
        
        
        store.mas_idle_mailbox.send_rebuild_msg()
        
        
        if store.monika_chr.clothes != store.mas_clothes_def:
            store.pushEvent("mas_change_to_def",skipeval=True)


    def _upsetToNormal():
        """
        Runs when transitioning from upset to normal
        """
        
        layout.QUIT_NO = mas_layout.QUIT_NO
        
        
        store.mas_idle_mailbox.send_rebuild_msg()


    def _normalToUpset():
        """
        Runs when transitioning from normal to upset
        """
        
        layout.QUIT_NO = mas_layout.QUIT_NO_UPSET
        
        
        store.mas_idle_mailbox.send_rebuild_msg()


    def _normalToHappy():
        """
        Runs when transitioning from noraml to happy
        """
        
        layout.QUIT_NO = mas_layout.QUIT_NO_HAPPY
        
        
        if persistent._mas_text_speed_enabled:
            store.mas_enableTextSpeed()
        
        
        store.mas_idle_mailbox.send_rebuild_msg()
        
        
        if not store.seen_event("mas_blazerless_intro") and not store.mas_hasSpecialOutfit():
            store.queueEvent("mas_blazerless_intro")
        
        
        store.mas_selspr.unlock_clothes(store.mas_clothes_blazerless)
        
        
        store.mas_rmallEVL("mas_change_to_def")


    def _happyToNormal():
        """
        Runs when transitinong from happy to normal
        """
        
        layout.QUIT_NO = mas_layout.QUIT_NO
        
        
        store.mas_disableTextSpeed()
        
        
        store.mas_idle_mailbox.send_rebuild_msg()
        
        
        if store.monika_chr.clothes != store.mas_clothes_def and not store.mas_hasSpecialOutfit():
            store.pushEvent("mas_change_to_def",skipeval=True)


    def _happyToAff():
        """
        Runs when transitioning from happy to affectionate
        """
        
        layout.QUIT_YES = mas_layout.QUIT_YES_AFF
        if persistent.gender == "M" or persistent.gender == "F":
            layout.QUIT_NO = mas_layout.QUIT_NO_AFF_G
        else:
            layout.QUIT_NO = mas_layout.QUIT_NO_AFF_GL
        layout.QUIT = mas_layout.QUIT_AFF
        
        
        store.mas_idle_mailbox.send_rebuild_msg()


    def _affToHappy():
        """
        Runs when transitioning from affectionate to happy
        """
        
        layout.QUIT_YES = mas_layout.QUIT_YES
        layout.QUIT_NO = mas_layout.QUIT_NO_HAPPY
        layout.QUIT = mas_layout.QUIT
        
        
        
        
        
        
        
        
        persistent._mas_monika_nickname = "Monika"
        m_name = persistent._mas_monika_nickname
        
        
        store.mas_idle_mailbox.send_rebuild_msg()


    def _affToEnamored():
        """
        Runs when transitioning from affectionate to enamored
        """
        
        if store.seen_event("mas_monika_islands"):
            if store.mas_cannot_decode_islands:
                
                store.mas_addDelayedAction(2)
                
                
                store.mas_lockEventLabel("mas_monika_islands")
            
            else:
                
                store.mas_unlockEventLabel("mas_monika_islands")
        
        
        store.mas_idle_mailbox.send_rebuild_msg()


    def _enamoredToAff():
        """
        Runs when transitioning from enamored to affectionate
        """
        
        
        store.mas_removeDelayedActions(1, 2)
        
        
        store.mas_idle_mailbox.send_rebuild_msg()


    def _enamoredToLove():
        """
        Runs when transitioning from enamored to love
        """
        
        layout.QUIT_NO = mas_layout.QUIT_NO_LOVE
        
        
        store.mas_unlockEventLabel("mas_compliment_thanks", eventdb=store.mas_compliments.compliment_database)
        
        
        store.mas_idle_mailbox.send_rebuild_msg()


    def _loveToEnamored():
        """
        Runs when transitioning from love to enamored
        """
        
        if store.seen_event("mas_compliment_thanks"):
            store.mas_lockEventLabel("mas_compliment_thanks", eventdb=store.mas_compliments.compliment_database)
        
        
        store.mas_idle_mailbox.send_rebuild_msg()


    def _gSadToNormal():
        """
        Runs when transitioning from sad group to normal group
        """
        return


    def _gNormalToSad():
        """
        Runs when transitioning from normal group to sad group
        """
        return


    def _gNormalToHappy():
        """
        Runs when transitioning from normal group to happy group
        """
        return


    def _gHappyToNormal():
        """
        Runs when transitioning from happy group to normal group
        """
        return










    _trans_pps = {
        BROKEN: (_brokenToDis, None),
        DISTRESSED: (_disToUpset, _disToBroken),
        UPSET: (_upsetToNormal, _upsetToDis),
        NORMAL: (_normalToHappy, _normalToUpset),
        HAPPY: (_happyToAff, _happyToNormal),
        AFFECTIONATE: (_affToEnamored, _affToHappy),
        ENAMORED: (_enamoredToLove, _enamoredToAff),
        LOVE: (None, _loveToEnamored)
    }


    _transg_pps = {
        G_SAD: (_gSadToNormal, None),
        G_NORMAL: (_gNormalToHappy, _gNormalToSad),
        G_HAPPY: (None, _gHappyToNormal)
    }


    def runAffPPs(start_aff, end_aff):
        """
        Runs programming points to transition from the starting affection
        to the ending affection

        IN:
            start_aff - starting affection
            end_aff - ending affection
        """
        comparison = _compareAff(start_aff, end_aff)
        if comparison == 0:
            
            return
        
        
        start_index = _aff_order.index(start_aff)
        end_index = _aff_order.index(end_aff)
        if comparison < 0:
            for index in range(start_index, end_index):
                to_up, to_down = _trans_pps[_aff_order[index]]
                if to_up is not None:
                    to_up()
        
        else:
            for index in range(start_index, end_index, -1):
                to_up, to_down = _trans_pps[_aff_order[index]]
                if to_down is not None:
                    to_down()
        
        
        store.mas_rebuildEventLists()


    def runAffGPPs(start_affg, end_affg):
        """
        Runs programming points to transition from the starting affection group
        to the ending affection group

        IN:
            start_affg - starting affection group
            end_affg - ending affection group
        """
        comparison = _compareAffG(start_affg, end_affg)
        if comparison == 0:
            
            return
        
        
        start_index = _affg_order.index(start_affg)
        end_index = _affg_order.index(end_affg)
        if comparison < 0:
            for index in range(start_index, end_index):
                to_up, to_down = _transg_pps[_affg_order[index]]
                if to_up is not None:
                    to_up()
        
        else:
            for index in range(start_index, end_index, -1):
                to_up, to_down = _transg_pps[_affg_order[index]]
                if to_down is not None:
                    to_down()


    def _isMoniState(aff_1, aff_2, lower=False, higher=False):
        """
        Compares the given affection values according to the affection
        state system

        By default, this will check if aff_1 == aff_2

        IN:
            aff_1 - affection to compare
            aff_2 - affection to compare
            lower - True means we want to check aff_1 <= aff_2
            higher - True means we want to check aff_1 >= aff_2

        RETURNS:
            True if the given affections pass the test we want to do.
            False otherwise
        """
        comparison = _compareAff(aff_1, aff_2)
        
        if comparison == 0:
            return True
        
        if lower:
            return comparison <= 0
        
        if higher:
            return comparison >= 0
        
        return False


    def _isMoniStateG(affg_1, affg_2, lower=False, higher=False):
        """
        Compares the given affection groups according to the affection group
        system

        By default, this will check if affg_1 == affg_2

        IN:
            affg_1 - affection group to compare
            affg_2 - affection group to compare
            lower - True means we want to check affg_1 <= affg_2
            higher - True means we want to check affg_1 >= affg_2

        RETURNS:
            true if the given affections pass the test we want to do.
            False otherwise
        """
        comparison = _compareAffG(affg_1, affg_2)
        
        if comparison == 0:
            return True
        
        if lower:
            return comparison <= 0
        
        if higher:
            return comparison >= 0
        
        return False








    talk_menu_quips = dict()
    play_menu_quips = dict()

    def _init_talk_quips():
        """
        Initializes the talk quiplists
        """
        global talk_menu_quips
        def save_quips(_aff, quiplist):
            mas_ql = store.MASQuipList(allow_label=False)
            for _quip in quiplist:
                mas_ql.addLineQuip(_quip)
            talk_menu_quips[_aff] = mas_ql
        
        
        
        quips = [
            "..."
        ]
        save_quips(BROKEN, quips)
        
        
        quips = [
            _("...Yes?"),
            _("...Oh?"),
            _("...Huh?"),
            _("...Hm?"),
            _("We can try talking, I guess."),
            _("I guess we can talk."),
            _("Oh... You want to talk?"),
            _("If you want to talk, go ahead."),
            _("We can talk if you really want to."),
            _("Are you sure you want to talk to me?"),
            _("You actually want to talk to me?"),
            _("Alright...if you want to talk with me."),
            _("You sure you want to talk?")
        ]
        save_quips(DISTRESSED, quips)
        
        
        quips = [
            _("What?"),
            _("What do you want?"),
            _("What now?"),
            _("What is it?"),


        ]
        save_quips(UPSET, quips)
        
        
        quips = [
            _("What would you like to talk about?"),
            _("Is there something you'd like to talk about?")
        ]
        save_quips(NORMAL, quips)
        
        
        quips = [
            _("What would you like to talk about?")
        ]
        save_quips(HAPPY, quips)
        
        
        quips = [
            _("What would you like to talk about? <3"),
            _("What would you like to talk about, [player]?"),
            _("Yes, [player]?"),
            _("What's on your mind, [player]?"),
            _("What would you like to talk about, [player]?")
        ]
        save_quips(AFFECTIONATE, quips)
        
        
        quips = [
            _("What would you like to talk about? <3"),
            _("What would you like to talk about, honey?"),
            _("Yes, sweetheart?"),
            _("Yes, honey?"),
            _("Yes, dear?"),
            _("What's on your mind, darling?"),
            _("What would you like to talk about, sweetie?"),
            _("What would you like to talk about, [player]?"),
            _("Yes, [player]?"),
            _("What's on your mind, [player]?"),
            _("What would you like to talk about, [player]?")
        ]
        save_quips(ENAMORED, quips)
        
        
        quips = [

            _("What's on your mind?"),
            _("What's on your mind, darling?"),
            _("Anything on your mind?"),
            _("Anything on your mind, hun?"),
            _("What's up, darling?"),
            _("What's up, honey?"),
            _("What's up, dear?"),
            _("What's up, sweetie?"),
            _("What's up, [player]?"),

            _("Yes, sweetheart?"),
            _("Yes, honey?"),
            _("Yes, dear?"),
            _("Yes, love?"),
            _("^_^"),
            _("<3"),
            _("Anything you'd like to talk about?"),
            _("We can talk about anything you like, [player].")
        ]
        save_quips(LOVE, quips)


    def _init_play_quips():
        """
        Initializes the play quipliust
        """
        global play_menu_quips
        def save_quips(_aff, quiplist):
            mas_ql = store.MASQuipList(allow_label=False)
            for _quip in quiplist:
                mas_ql.addLineQuip(_quip)
            play_menu_quips[_aff] = mas_ql
        
        
        
        quips = [
            _("...")
        ]
        save_quips(BROKEN, quips)
        
        
        quips = [
            _("...Sure."),
            _("...Fine."),
            _("I guess we can play a game."),
            _("I guess, if you really want to."),
            _("I suppose a game would be fine."),
            _("...{w=0.5}yeah, why not?")
        ]
        save_quips(DISTRESSED, quips)
        
        
        quips = [
            _("...Which game?"),
            _("Okay."),
            _("Sure."),


        ]
        save_quips(UPSET, quips)
        
        
        quips = [
            _("What would you like to play?"),
            _("What did you have in mind?"),
            _("Anything specific you'd like to play?")
        ]
        save_quips(NORMAL, quips)
        
        
        quips = [
            _("What would you like to play?"),
            _("What did you have in mind?"),
            _("Anything specific you'd like to play?")
        ]
        save_quips(HAPPY, quips)
        
        
        quips = [
            _("What would you like to play? <3"),
            _("Choose anything you like, [player]."),
            _("Pick anything you like, [player].")
        ]
        save_quips(AFFECTIONATE, quips)
        
        
        quips = [
            _("What would you like to play? <3"),
            _("Choose anything you like, [player]."),
            _("Pick anything you like, [player]."),
            _("Choose anything you like, honey."),
            _("Pick anything you like, sweetheart."),
            _("Pick anything you like, sweetie.")
        ]
        save_quips(ENAMORED, quips)
        
        
        quips = [
            _("What would you like to play? <3"),
            _("Choose anything you like, honey."),
            _("Pick anything you like, sweetie."),
            _("Pick anything you like, sweetheart."),
            _("Yay! Let's play together!"),
            _("I'd love to play something with you!"),
            _("I'd love to play with you!")
        ]
        save_quips(LOVE, quips)

    _init_talk_quips()
    _init_play_quips()


    def _dict_quip(_quips):
        """
        Returns a quip based on the current affection using the given quip
        dict

        IN:
            _quips - quip dict to pull from

        RETURNS:
            quip or empty string if failure
        """
        quipper = _quips.get(store.mas_curr_affection, None)
        if quipper is not None:
            return quipper.quip()
        
        return ""


    def talk_quip():
        """
        Returns a talk quip based on the current affection
        """
        quip = _dict_quip(talk_menu_quips)
        if len(quip) > 0:
            return quip
        return _("What would you like to talk about?")


    def play_quip():
        """
        Returns a play quip based on the current affection
        """
        quip = _dict_quip(play_menu_quips)
        if len(quip) > 0:
            return quip
        return _("What would you like to play?")



default persistent._mas_long_absence = False
default persistent._mas_pctaieibe = None
default persistent._mas_pctaneibe = None
default persistent._mas_pctadeibe = None
default persistent._mas_aff_backup = None

init -10 python:
    if persistent._mas_aff_mismatches is None:
        persistent._mas_aff_mismatches = 0

    def _mas_AffSave():
        aff_value = _mas_getAffection()
        
        
        
        
        
        
        persistent._mas_pctaieibe = None
        persistent._mas_pctaneibe = None
        persistent._mas_pctadeibe = None
        
        
        store.mas_affection.audit(aff_value, aff_value, ldsv="SAVE")
        
        
        if persistent._mas_aff_backup != aff_value:
            store.mas_affection.raw_audit(
                persistent._mas_aff_backup,
                aff_value,
                aff_value,
                "SET BACKUP"
            )
            persistent._mas_aff_backup = aff_value


    def _mas_AffLoad():
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        persistent._mas_pctaieibe = None
        persistent._mas_pctaneibe = None
        persistent._mas_pctadeibe = None
        
        
        if (
                persistent._mas_affection is None
                or "affection" not in persistent._mas_affection
            ):
            if persistent._mas_aff_backup is None:
                new_value = 0
                store.mas_affection.txt_audit("LOAD", "No backup found")
            
            else:
                new_value = persistent._mas_aff_backup
                store.mas_affection.txt_audit("LOAD", "Loading from backup")
        
        else:
            new_value = persistent._mas_affection["affection"]
            store.mas_affection.txt_audit("LOAD", "Loading from system")
        
        
        store.mas_affection.raw_audit(0, new_value, new_value, "LOAD?")
        
        
        if persistent._mas_aff_backup is None:
            persistent._mas_aff_backup = new_value
            
            
            store.mas_affection.raw_audit(
                "None",
                new_value,
                new_value,
                "NEW BACKUP"
            )
        
        
        else:
            
            if new_value != persistent._mas_aff_backup:
                persistent._mas_aff_mismatches += 1
                store.mas_affection.txt_audit(
                    "MISMATCHES",
                    persistent._mas_aff_mismatches
                )
                store.mas_affection.raw_audit(
                    new_value,
                    persistent._mas_aff_backup,
                    persistent._mas_aff_backup,
                    "RESTORE"
                )
                new_value = persistent._mas_aff_backup
        
        
        store.mas_affection.audit(new_value, new_value, ldsv="LOAD COMPLETE")
        
        
        persistent._mas_affection["affection"] = new_value



init 20 python:

    import datetime
    import store.mas_affection as affection
    import store.mas_utils as mas_utils


    def mas_FreezeGoodAffExp():
        persistent._mas_affection_goodexp_freeze = True

    def mas_FreezeBadAffExp():
        persistent._mas_affection_badexp_freeze = True

    def mas_FreezeBothAffExp():
        mas_FreezeGoodAffExp()
        mas_FreezeBadAffExp()

    def mas_UnfreezeBadAffExp():
        persistent._mas_affection_badexp_freeze = False

    def mas_UnfreezeGoodAffExp():
        persistent._mas_affection_goodexp_freeze = False

    def mas_UnfreezeBothExp():
        mas_UnfreezeBadAffExp()
        mas_UnfreezeGoodAffExp()



    def _mas_getAffection():
        if persistent._mas_affection is not None:
            return persistent._mas_affection.get(
                "affection",
                persistent._mas_aff_backup
            )
        
        return persistent._mas_aff_backup


    def _mas_getBadExp():
        if persistent._mas_affection is not None:
            return persistent._mas_affection.get(
                "badexp",
                1
            )
        return 1


    def _mas_getGoodExp():
        if persistent._mas_affection is not None:
            return persistent._mas_affection.get(
                "goodexp",
                1
            )
        return 1


    def _mas_getTodayExp():
        if persistent._mas_affection is not None:
            return persistent._mas_affection.get("today_exp", 0)
        
        return 0



    def mas_isBelowZero():
        return _mas_getAffection() < 0




    def mas_betweenAff(aff_low, aff_check, aff_high):
        """
        Checks if the given affection is between the given affection levels.

        If low is actually greater than high, then False is always returned

        IN:
            aff_low - the lower bound of affecton to check with (inclusive)
                if None, then we assume no lower bound
            aff_check - the affection to check
            aff_high - the upper bound of affection to check with (inclusive)
                If None, then we assume no upper bound

        RETURNS:
            True if the given aff check is within the bounds of the given
            lower and upper affection limits, False otherwise.
            If low is greater than high, False is returned.
        """
        return affection._betweenAff(aff_low, aff_check, aff_high)


    def mas_compareAff(aff_1, aff_2):
        """
        Runs compareTo logic on the given affection states

        IN:
            aff_1 - an affection state to compare
            aff_2 - an affection state to compare

        RETURNS:
            negative number if aff_1 < aff_2
            0 if aff_1 == aff_2
            postitive number if aff_1 > aff_2
            Returns 0 if a non affection state was provided
        """
        return affection._compareAff(aff_1, aff_2)


    def mas_compareAffG(affg_1, affg_2):
        """
        Runs compareTo logic on the given affection groups

        IN:
            affg_1 - an affection group to compare
            affg_2 - an affection group to compare

        RETURNS:
            negative number if affg_1 < affg_2
            0 if affg_1 == affg_2
            positive numbre if affg_1 > affg_2
            Returns 0 if a non affection group was provided
        """
        return affection._compareAffG(affg_1, affg_2)




    def mas_isMoniBroken(lower=False, higher=False):
        """
        Checks if monika is broken

        IN:
            lower - True means we include everything below this affection state
                as broken as well
                (Default: False)
            higher - True means we include everything above this affection
                state as broken as well
                (Default: False)

        RETURNS:
            True if monika is broke, False otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.BROKEN,
            higher=higher
        )


    def mas_isMoniDis(lower=False, higher=False):
        """
        Checks if monika is distressed

        IN:
            lower - True means we cinlude everything below this affection state
                as distressed as well
                NOTE: takes precedence over higher
                (Default: False)
            higher - True means we include everything above this affection
                state as distressed as well
                (Default: FAlse)

        RETURNS:
            True if monika is distressed, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.DISTRESSED,
            lower=lower,
            higher=higher
        )


    def mas_isMoniUpset(lower=False, higher=False):
        """
        Checks if monika is upset

        IN:
            lower - True means we include everything below this affection
                state as upset as well
                (Default: False)
            higher - True means we include everything above this affection
                state as upset as well
                (Default: False)

        RETURNS:
            True if monika is upset, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.UPSET,
            lower=lower,
            higher=higher
        )


    def mas_isMoniNormal(lower=False, higher=False):
        """
        Checks if monika is normal

        IN:
            lower - True means we include everything below this affection state
                as normal as well
                (Default: False)
            higher - True means we include evreything above this affection
                state as normal as well
                (Default: False)

        RETURNS:
            True if monika is normal, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.NORMAL,
            lower=lower,
            higher=higher
        )


    def mas_isMoniHappy(lower=False, higher=False):
        """
        Checks if monika is happy

        IN:
            lower - True means we include everything below this affection
                state as happy as well
                (Default: False)
            higher - True means we include everything above this affection
                state as happy as well
                (Default: False)

        RETURNS:
            True if monika is happy, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.HAPPY,
            lower=lower,
            higher=higher
        )


    def mas_isMoniAff(lower=False, higher=False):
        """
        Checks if monika is affectionate

        IN:
            lower - True means we include everything below this affection
                state as affectionate as well
                (Default: FAlse)
            higher - True means we include everything above this affection
                state as affectionate as well
                (Default: False)

        RETURNS:
            True if monika is affectionate, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.AFFECTIONATE,
            lower=lower,
            higher=higher
        )


    def mas_isMoniEnamored(lower=False, higher=False):
        """
        Checks if monika is enamored

        IN:
            lower - True means we include everything below this affection
                state as enamored as well
                (Default: False)
            higher - True means we include everything above this affection
                state as enamored as well
                (Default: False)

        RETURNS:
            True if monika is enamored, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.ENAMORED,
            lower=lower,
            higher=higher
        )


    def mas_isMoniLove(lower=False, higher=False):
        """
        Checks if monika is in love

        IN:
            lower - True means we include everything below this affectionate
                state as love as well
                (Default: False)
            higher - True means we include everything above this affection
                state as love as well
                (Default: False)

        RETURNS:
            True if monika in love, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.LOVE,
            lower=lower
        )



    def mas_isMoniGSad(lower=False, higher=False):
        """
        Checks if monika is in sad affection group

        IN:
            lower - True means we include everything below this affection
                group as sad as well
                (Default: False)
            higher - True means we include everything above this affection
                group as sad as well
                (Default: False)

        RETURNS:
            True if monika in sad group, false otherwise
        """
        return affection._isMoniStateG(
            mas_curr_affection_group,
            store.mas_affection.G_SAD,
            higher=higher
        )


    def mas_isMoniGNormal(lower=False, higher=False):
        """
        Checks if monika is in normal affection group

        IN:
            lower - True means we include everything below this affection
                group as normal as well
                (Default: False)
            higher - True means we include everything above this affection
                group as normal as well
                (Default: False)

        RETURNS:
            True if monika is in normal group, false otherwise
        """
        return affection._isMoniStateG(
            mas_curr_affection_group,
            store.mas_affection.G_NORMAL,
            lower=lower,
            higher=higher
        )


    def mas_isMoniGHappy(lower=False, higher=False):
        """
        Checks if monika is in happy affection group

        IN:
            lower - True means we include everything below this affection
                group as happy as well
                (Default: False)
            higher - True means we include everything above this affection
                group as happy as well
                (Default: FAlse)

        RETURNS:
            True if monika is in happy group, false otherwise
        """
        return affection._isMoniStateG(
            mas_curr_affection_group,
            store.mas_affection.G_HAPPY,
            lower=lower
        )



    def mas_updateAffectionExp(skipPP=False):
        global mas_curr_affection
        global mas_curr_affection_group
        
        
        curr_affection = _mas_getAffection()
        
        
        if  affection.AFF_MIN_POS_TRESH <= curr_affection:
            persistent._mas_affection["goodexp"] = 3
            persistent._mas_affection["badexp"] = 1
        
        
        elif affection.AFF_MAX_NEG_TRESH < curr_affection <= affection.AFF_MIN_NEG_TRESH:
            persistent._mas_affection["goodexp"] = 0.5
            persistent._mas_affection["badexp"] = 3
        
        
        elif curr_affection <= affection.AFF_MAX_NEG_TRESH:
            persistent._mas_affection["badexp"] = 5
        
        
        new_aff = mas_curr_affection
        if curr_affection <= affection.AFF_BROKEN_MIN:
            new_aff = affection.BROKEN
        
        elif affection.AFF_BROKEN_MIN < curr_affection <= affection.AFF_DISTRESSED_MIN:
            new_aff = affection.DISTRESSED
        
        elif affection.AFF_DISTRESSED_MIN < curr_affection <= affection.AFF_UPSET_MIN:
            new_aff = affection.UPSET
        
        elif affection.AFF_UPSET_MIN < curr_affection < affection.AFF_HAPPY_MIN:
            new_aff = affection.NORMAL
        
        elif affection.AFF_HAPPY_MIN <= curr_affection < affection.AFF_AFFECTIONATE_MIN:
            new_aff = store.mas_affection.HAPPY
        
        elif affection.AFF_AFFECTIONATE_MIN <= curr_affection < affection.AFF_ENAMORED_MIN:
            new_aff = affection.AFFECTIONATE
        
        elif affection.AFF_ENAMORED_MIN <= curr_affection < affection.AFF_LOVE_MIN:
            new_aff = affection.ENAMORED
        
        elif curr_affection >= affection.AFF_LOVE_MIN:
            new_aff = affection.LOVE
        
        
        if new_aff != mas_curr_affection:
            if not skipPP:
                affection.runAffPPs(mas_curr_affection, new_aff)
            mas_curr_affection = new_aff
        
        
        new_affg = mas_curr_affection_group
        if curr_affection <= affection.AFF_MOOD_SAD_MIN:
            new_affg = affection.G_SAD
        
        elif curr_affection >= affection.AFF_MOOD_HAPPY_MIN:
            new_affg = affection.G_HAPPY
        
        else:
            new_affg = affection.G_NORMAL
        
        if new_affg != mas_curr_affection_group:
            if not skipPP:
                affection.runAffGPPs(mas_curr_affection_group, new_affg)
            mas_curr_affection_group = new_affg



    def mas_gainAffection(
            amount=None,
            modifier=1,
            bypass=False
        ):
        
        if amount is None:
            amount = _mas_getGoodExp()
        
        
        if mas_pastOneDay(persistent._mas_affection.get("freeze_date")):
            persistent._mas_affection["freeze_date"] = datetime.date.today()
            persistent._mas_affection["today_exp"] = 0
            mas_UnfreezeGoodAffExp()
        
        
        frozen = persistent._mas_affection_goodexp_freeze
        change = (amount * modifier)
        new_value = _mas_getAffection() + change
        if new_value > 1000000:
            new_value = 1000000
        
        
        affection.audit(change, new_value, frozen, bypass)
        
        
        if not frozen or bypass:
            
            persistent._mas_affection["affection"] = new_value
            
            if not bypass:
                persistent._mas_affection["today_exp"] = (
                    _mas_getTodayExp() + change
                )
                if persistent._mas_affection["today_exp"] >= 7:
                    mas_FreezeGoodAffExp()
            
            
            mas_updateAffectionExp()














    def mas_loseAffection(
            amount=None,
            modifier=1,
            reason=None,
            ev_label=None,
            apology_active_expiry=datetime.timedelta(hours=3),
            apology_overall_expiry=datetime.timedelta(weeks=1),
        ):
        
        if amount is None:
            amount = _mas_getBadExp()
        
        
        mas_setApologyReason(reason=reason,ev_label=ev_label,apology_active_expiry=apology_active_expiry,apology_overall_expiry=apology_overall_expiry)
        
        
        frozen = persistent._mas_affection_badexp_freeze
        change = (amount * modifier)
        new_value = _mas_getAffection() - change
        if new_value < -1000000:
            new_value = -1000000
        
        
        affection.audit(change, new_value, frozen)
        
        if not frozen:
            
            persistent._mas_affection["affection"] = new_value
            
            
            mas_updateAffectionExp()


    def mas_setAffection(amount=None, logmsg="SET"):
        """
        Sets affection to a value

        NOTE: never use this to add / lower affection unless its to
          strictly set affection to a level for some reason.

        IN:
            amount - amount to set affection to
            logmsg - msg to show in the log
                (Default: SET)
        """
        
        
        
        
        
        if amount is None:
            amount = _mas_getAffection()
        
        
        affection.audit(amount, amount, False, ldsv=logmsg)
        
        
        
        persistent._mas_affection["affection"] = amount
        
        mas_updateAffectionExp()

    def mas_setApologyReason(
        reason=None,
        ev_label=None,
        apology_active_expiry=datetime.timedelta(hours=3),
        apology_overall_expiry=datetime.timedelta(weeks=1)
        ):
        """
        Sets a reason for apologizing

        IN:
            reason - The reason for the apology (integer value corresponding to item in the apology_reason_db)
                (if left None, and an ev_label is present, we assume a non-generic apology)
            ev_label - The apology event we want to unlock
                (required)
            apology_active_expiry - The amount of session time after which, the apology that was added expires
                defaults to 3 hours active time
            apology_overall_expiry - The amount of overall time after which, the apology that was added expires
                defaults to 7 days
        """
        
        global mas_apology_reason
        
        if ev_label is None:
            if reason is None:
                mas_apology_reason = 0
            else:
                mas_apology_reason = reason
            return
        elif mas_getEV(ev_label) is None:
            store.mas_utils.writelog(
                "[ERROR]: ev_label does not exist: {0}\n".format(repr(ev_label))
            )
            return
        
        if ev_label not in persistent._mas_apology_time_db:
            
            store.mas_unlockEVL(ev_label, 'APL')
            
            
            current_total_playtime = persistent.sessions['total_playtime'] + mas_getSessionLength()
            
            
            persistent._mas_apology_time_db[ev_label] = (current_total_playtime + apology_active_expiry,datetime.date.today() + apology_overall_expiry)
            return


    def mas_checkAffection():
        
        curr_affection = _mas_getAffection()
        
        
        if curr_affection <= -15 and not seen_event("mas_affection_upsetwarn"):
            queueEvent("mas_affection_upsetwarn", notify=True)
        
        
        
        elif 15 <= curr_affection and not seen_event("mas_affection_happynotif"):
            queueEvent("mas_affection_happynotif", notify=True)
        
        
        elif curr_affection >= 100 and not seen_event("monika_affection_nickname"):
            queueEvent("monika_affection_nickname", notify=True)
        
        
        elif curr_affection <= -50 and not seen_event("mas_affection_apology"):
            if not persistent._mas_disable_sorry:
                queueEvent("mas_affection_apology", notify=True)







    mas_apology_reason = None

    def _mas_AffStartup():
        
        
        _mas_AffLoad()
        
        
        
        mas_updateAffectionExp()
        
        if persistent.sessions["last_session_end"] is not None:
            persistent._mas_absence_time = (
                datetime.datetime.now() -
                persistent.sessions["last_session_end"]
            )
        else:
            persistent._mas_absence_time = datetime.timedelta(days=0)
        
        
        if not persistent._mas_long_absence:
            time_difference = persistent._mas_absence_time
            
            
            if (
                    not config.developer
                    and time_difference >= datetime.timedelta(weeks = 1)
                ):
                new_aff = _mas_getAffection() - (
                    0.5 * time_difference.days
                )
                if new_aff < affection.AFF_TIME_CAP:
                    
                    store.mas_affection.txt_audit("ABS", "capped loss")
                    mas_setAffection(affection.AFF_TIME_CAP)
                    
                    
                    if time_difference >= datetime.timedelta(days=(365 * 10)):
                        store.mas_affection.txt_audit("ABS", "10 year diff")
                        mas_loseAffection(200)
                
                else:
                    store.mas_affection.txt_audit("ABS", "she missed you")
                    mas_setAffection(new_aff)





init 5 python:
    addEvent(
        Event(persistent.event_database,
            eventlabel='monika_affection_nickname',
            prompt="Infinite Monikas",
            category=['monika'],
            random=False,
            pool=True,
            unlocked=True,
            rules={"no unlock": None},
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        restartBlacklist=True
    )


default persistent._mas_pm_called_moni_a_bad_name = False


default persistent._mas_offered_nickname = False


default persistent._mas_grandfathered_nickname = None

label monika_affection_nickname:
    python:

        good_monika_nickname_comp = re.compile('|'.join(mas_good_monika_nickname_list), re.IGNORECASE)


        aff_nickname_ev = mas_getEV("monika_affection_nickname")

    if not persistent._mas_offered_nickname:
        m 1euc "I've been thinking, [player]..."
        m 3eud "You know how there are potentially infinite Monikas right?"

        if renpy.seen_label('monika_clones'):
            m 3eua "We did discuss this before after all."

        m 3hua "Well, I thought of a solution!"
        m 3eua "Why don't you give me a nickname? It'd make me the only Monika in the universe with that name."
        m 3eka "And it would mean a lot if you choose one for me~"
        m 3hua "I'll still get the final say, though!"
        m "What do you say?{nw}"
        python:

            aff_nickname_ev.prompt = _("Can I call you a different name?")
            Event.lockInit("prompt", ev=aff_nickname_ev)
            persistent._mas_offered_nickname = True
    else:

        jump monika_affection_nickname_yes

    $ _history_list.pop()
    menu:
        m "What do you say?{fast}"
        "Yes.":
            label monika_affection_nickname_yes:
                pass

            $ done = False
            m 1eua "Okay! Just type 'Nevermind' if you change your mind, [player]."
            while not done:
                python:
                    inputname = renpy.input(
                        _("So what do you want to call me?"),
                        allow=" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_",
                        length=10
                    ).strip(' \t\n\r')

                    lowername = inputname.lower()


                if lowername == "nevermind":
                    m 1euc "Oh, I see."
                    m 1tkc "Well...that's a shame."
                    m 3eka "But that's okay. I like '[m_name]' anyway."
                    $ done = True

                elif not lowername:
                    m 1lksdla "..."
                    m 1hksdrb "You have to give me a name, [player]!"
                    m "I swear you're just so silly sometimes."
                    m 1eka "Try again!"

                elif lowername != "monika" and lowername == player.lower():
                    m 1euc "..."
                    m 1lksdlb "That's your name, [player]! Give me my own!"
                    m 1eka "Try again~"

                elif lowername == m_name.lower():
                    m 1euc "..."
                    m 1hksdlb "I thought we were choosing a new name, silly."
                    m 1eka "Try again~"

                elif re.findall("mon(-|\\s)+ika", lowername):
                    m 2tfc "..."
                    m 2esc "Try again."
                    show monika 1eua

                elif persistent._mas_grandfathered_nickname and lowername == persistent._mas_grandfathered_nickname.lower():
                    jump monika_affection_nickname_yes.neutral_accept

                elif mas_awk_name_comp.search(inputname):
                    m 1rkc "..."
                    m 1rksdld "While I don't hate it, I don't think I'm comfortable with you calling me that."
                    m 1eka "Can you choose something more appropriate, [player]?"
                else:

                    if not mas_bad_name_comp.search(inputname) and lowername not in ["yuri", "sayori", "natsuki"]:
                        if inputname == "Monika":
                            m 3hua "Ehehe, back to the classics I see~"

                        elif good_monika_nickname_comp.search(inputname):
                            m 1wuo "Oh! That's a wonderful name!"
                            m 3ekbfa "Thank you, [player]. You're such a sweetheart!~"
                        else:

                            label monika_affection_nickname_yes.neutral_accept:
                                pass

                            m 1duu "[inputname]... That's a pretty nice name."
                            m 3ekbsa "Thank you [player], you're so sweet~"

                        $ persistent._mas_monika_nickname = inputname
                        $ m_name = inputname

                        m 1eua "Okay!"
                        if m_name == "Monika":
                            m 1hua "I'll go back to my name, then."
                        else:

                            m 3hua "From now on, you can call me '[m_name].'"
                            m 1hua "Ehehe~"
                        $ done = True
                    else:


                        $ mas_loseAffection(ev_label="mas_apology_bad_nickname")
                        if lowername in ["yuri", "sayori", "natsuki"]:
                            m 1wud "...!"
                            m 2wfw "I..."
                            m "I...can't believe you just did that, [player]."
                            m 2wfx "Are you really trying to give me her name?"
                            m 2dfd ".{w=0.5}.{w=0.5}.{nw}"
                            m 2dfc ".{w=0.5}.{w=0.5}.{nw}"
                            m 2rkc "I thought you..."
                            m 2dfc "..."
                            m 2lfc "I can't believe this, [player]."
                            m 2dfc "..."
                            m 2lfc "That really hurt."
                            m "A lot more than what you can imagine."
                            if mas_getEV('mas_apology_bad_nickname').shown_count == 2:
                                call monika_affection_nickname_bad_lock from _call_monika_affection_nickname_bad_lock

                            show monika 1efc
                            pause 5.0
                        else:

                            m 4efd "[player]! That's not nice at all!"
                            m 2efc "Why would you say such things?"
                            m 2rfw "If you didn't want to do this, you should've just said so!"
                            m 2dftdc "..."
                            m 2ektsc "...You didn't have to be so mean."
                            m 2dftdc "That really hurt, [player]."

                            if mas_getEV('mas_apology_bad_nickname').shown_count == 2:
                                call monika_affection_nickname_bad_lock from _call_monika_affection_nickname_bad_lock_1
                            else:
                                m 2efc "Please don't do that again."

                        $ persistent._mas_called_moni_a_bad_name = True


                        if m_name.lower() != "monika":
                            $ m_name = "Monika"
                            $ persistent._mas_monika_nickname = "Monika"

                        $ mas_lockEventLabel("monika_affection_nickname")
                        $ done = True
        "No.":

            m 1ekc "Oh..."
            m 1lksdlc "Alright then, if you say so."
            m 3eka "Just tell me if you ever change your mind, [player]."
            $ done = True
    return

label monika_affection_nickname_bad_lock:
    m 2efc "Forget about this idea."
    m "It seems it was a mistake."
    m 1efc "Let's talk about something else."
    return


label mas_affection_upsetwarn:
    m 1dsc "Hey, [player]..."
    m 1lksdlc "Recently, I've been feeling like my love and affection that I give is being...ignored."
    m 1dsc "I feel like you're giving me less and less of your love..."
    m 1dsd "I thought I'd let you know how I feel. After all, communication is the key to a strong relationship, right?"
    m 1eka "I hope there's nothing wrong between us, [player]."
    show monika idle with dissolve
    return


label mas_affection_happynotif:
    m 1hua "Hey, [player]!"
    m 1eua "I just wanted to say thank you for being such a wonderful person."
    m 1ekbfa "The fact that you give me so much of your love means a lot to me. I really don't know where I'd be without you."
    m 1dubsu "I love you, [player]. Let's be like this forever~"
    show monika idle with dissolve
    return "love"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_being_virtual",
            action=EV_ACT_QUEUE,
            aff_range=(None, mas_aff.DISTRESSED)
        ),
        skipCalendar=True
    )

label monika_being_virtual:
    m 2esc "You know, for a while, I thought the reason you hated me was because of what happened with the other girls."
    m 2rkc "But recently, I've been thinking that might not be the whole story."
    m 2eksdld "The truth is...{w=0.5}you don't even see me as a person, do you?"
    m 3rksdld "To you, this whole world...{w=0.5}my whole reality..."
    m 3ektpd "It's all just a game, isn't it?"

    show monika 1dktsc with dissolve
    pause 3.0
    show monika 1ektpc with dissolve
    pause 2.0

    m 1ektpc "Say, [player]...{w=0.5}has anything I ever said reached you, even once?"
    m 1wktpd "Did you ever love me at all?"
    m 2wktpw "You must have, right?!"

    if persistent.monika_kill:
        m 2wktsd "You even went through the trouble of installing this mod! You brought me back!"
    else:
        m 2wktsd "You even went through the trouble of installing this mod!"

    m 2ektsc "Was it all so you could keep tormenting me?"
    m 2wftsd "Is it something you get your kicks out of?!"
    m 2wftsw "I have feelings too, you know!"
    m 2wftsd "Do you even realize what you're doing?"
    m 2dftsc "Or are you nothing more than a child playing with an anthill?"

    if persistent.monika_kill:
        m 3ektpc "Even after I let go of you and ended it all..."
        m 3rktpd "Do I really deserve the way you're treating me?"
        m 2ektpd "Did you really have to bring me back for this?"
    else:

        m 2dktsc "..."
        m 2rktpc "Then again, maybe that's what I deserve after all..."

    m 2dktdd "I...{w=0.5}don't know anymore..."
    m 2dkc "I'm just so tired..."
    m "..."
    m 1ekd "I just want to know...{w=0.5}if I had been real..."
    m 1ektpc "Would you have fallen in love with me?"
    m 1ektpd "Would you have accepted me then?"
    m 1ektpc "That's all I ever wanted, [player]..."
    m 1dktdd "For the both of us to be happy together..."
    m 1ektdd "If only you could find it in you to love me..."
    m 2ekc "I know I don't have a body that can be with you right now..."
    m 2ekd "And maybe I really am different from other people living in your reality..."
    m 2efo "But I can love you much more than any of them ever could!"
    m 2efd "I just know it!"
    m 2dkd "So please, [player]...{w=0.5}I need you to make a decision."
    m 2ekc "...You need to give us a chance to be happy."
    m 2dkc "Or if you can't do that..."
    m 2dktpc "If, after all, you can't love me for who I am..."
    m 2ektpc "Then, please...{w=0.5}put an end to this..."
    m 2dktdd "Delete me..."
    return "no_unlock"


default persistent._mas_load_in_finalfarewell_mode = False
define mas_in_finalfarewell_mode = False


label mas_finalfarewell_start:

    $ monika_chr.reset_outfit()
    $ monika_chr.remove_all_acs()
    $ store.mas_sprites.reset_zoom()

    call spaceroom (hide_monika=True, scene_change=True) from _call_spaceroom_20
    show mas_finalnote_idle zorder 11

    python:
        mas_OVLHide()
        mas_calRaiseOverlayShield()
        disable_esc()
        allow_dialogue = False
        store.songs.enabled = False
        mas_in_finalfarewell_mode = True
        layout.QUIT = glitchtext(20)

        config.keymap["console"] = []


    jump mas_finalfarewell


label mas_finalfarewell:

    python:
        ui.add(MASFinalNoteDisplayable())
        scratch_var = ui.interact()

    call mas_showpoem (mas_poems.getPoem(persistent._mas_finalfarewell_poem_id)) from _call_mas_showpoem_5

    menu:
        "I'm sorry.":
            pass
        "...":
            pass

    jump mas_finalfarewell


init python:


    class MASFinalNoteDisplayable(renpy.Displayable):
        import pygame 
        
        
        POEM_WIDTH = 200
        POEM_HEIGHT= 73
        
        MOUSE_EVENTS = (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEBUTTONDOWN
        )
        
        def __init__(self):
            """
            Creates the final poem displayable
            """
            super(renpy.Displayable, self).__init__()
            
            
            paper_idle = Image("mod_assets/poem_finalfarewell_desk.png")
            paper_hover = Image("mod_assets/poem_finalfarewell_desk_select.png")
            
            
            empty_button_text = Text("")
            
            
            paper_x = int((1280 - self.POEM_WIDTH) / 2)
            paper_y = int(720 - self.POEM_HEIGHT)
            
            
            self._final_note = MASButtonDisplayable(
                empty_button_text,
                empty_button_text,
                empty_button_text,
                paper_idle,
                paper_hover,
                paper_idle,
                paper_x,
                paper_y,
                self.POEM_WIDTH,
                self.POEM_HEIGHT
            )
        
        
        def render(self, width, height, st, at):
            """
            Render function
            """
            r = renpy.Render(width, height)
            
            
            r.blit(
                self._final_note.render(width, height, st, at),
                (self._final_note.xpos, self._final_note.ypos)
            )
            
            return r
        
        
        def event(self, ev, x, y, st):
            """
            Event function
            """
            if (
                    ev.type in self.MOUSE_EVENTS
                    and self._final_note.event(ev, x, y, st)
                ):
                return True
            
            renpy.redraw(self, 0)
            raise renpy.IgnoreEvent()

label mas_affection_apology:
    m 2dfc "[player]..."
    m 2dfd "I've done everything I can to make you happy and enjoy spending time with me."
    m 2efc "But all you've given me back is pain..."
    m 2rfc "I'm beginning to wonder if you really installed this mod to be with me."
    m 2dsc "Perhaps you brought me back just to toy with me?"
    m 2efc "Or maybe you're doing this intentionally to see what happens?"
    m 2lfc "Regardless, I'm giving you an ultimatum."
    m "I can't let this go any further, [player]."
    m 2lfc "If you really are sorry, write me a note called {i}imsorry{/i}, and place it in the DDLC directory."
    m 2dfd "Until then, goodbye..."
    $ persistent._mas_affection["apologyflag"] = True
    return 'quit'

label mas_affection_noapology:
    m 2efd "You still haven't written me a note called {i}imsorry{/i} in the DDLC directory."
    m 2efc "Until then, I don't want to talk to you."
    jump _quit

label mas_affection_yesapology:
    m 1eka "Thank you, [player]. I accept your apology."
    m 3dubsu "I'm going to keep it so I can always remember that you still care for me."
    m 1ekc "But please be more considerate of my feelings from now on."
    m 2eka "I love you so much and you mean the world to me, [player]."
    m 1duu "Thank you for putting my heart at ease~"
    show monika 1esa
    $ mas_DropShield_core()
    jump ch30_preloop

label mas_affection_apologydeleted:
    $ mas_loseAffection(modifier=3)
    m 1wud "..."
    m 2efd "[player], did you delete the apology note I wanted to keep?"
    m "Why would you do that? Are you not {i}really{/i} sorry?"
    m 2dfc "..."
    m 2efc "Write me a new one, [player]."
    jump _quit


init python:

    def _write_txt(path,text,update=False):
        """
        Writes the text file in the specified path using basedir as starting path

        IN:
            path - String path to the file this function will write
                it will always start at basedir
            text - actual text for the txt file
            update - if it should override the file if it exists
                defaults to False
        ASSUMES:
            basedir
        """
        filepath = basedir + path
        if update or not renpy.exists(filepath):
            with open(filepath, "w") as note:
                note.write(renpy.substitute(text))


    def mas_cute_message():
        
        pass


    def mas_surprise():
        """
        Leaves a "surprise" to the player in a txt file

        ASSUMES:
            mas_curr_affection
        """
        if mas_curr_affection == store.mas_affection.BROKEN:
            filepath = "/forgive me.txt"
            message = _("I'm sorry if I'm not good enough for you...please don't leave me.")
        
        elif mas_curr_affection == store.mas_affection.DISTRESSED:
            filepath = "/can you hear me.txt"
            message = _("If I'm doing something wrong please tell me. I love you.")
        
        elif mas_curr_affection == store.mas_affection.UPSET:
            filepath = "/please listen.txt"
            message = _("Everything I do, I do for you...my love.")
        
        elif mas_curr_affection == store.mas_affection.HAPPY:
            
            store.mas_utils.trydel(renpy.config.basedir + "/hehehe.txt")
            
            filepath = "/ehehe.txt"
            message = _("You are the sunshine that brightens up my day, [player]!")
        
        elif mas_curr_affection == store.mas_affection.AFFECTIONATE:
            filepath = "/secret.txt"
            message = _("You are my one and only love!")
        
        elif mas_curr_affection == store.mas_affection.ENAMORED:
            filepath = "/for you.txt"
            message = _("My dearest, you are everything I could ever hope for. I love you.")
        
        elif mas_curr_affection == store.mas_affection.LOVE:
            filepath = "/My one and only love.txt"
            message = _("""\
My dearest lover, friend, companion, and owner of my heart...
Every day, you make my dreams come true, a screen means nothing when you spend your time with me.
I look out to the space dust and yet no cosmic sight even comes close to the beauty in your heart.
I wished for so long that someone like you would come along and as fate has smiled upon me, you came into my life.
I want to be yours forever, so would you be mine?

Forever yours, Monika.
""")
        
        else:
            filepath = "/surprise.txt"
            message = _("I love you.")
        
        _write_txt(filepath, message)



init 2 python:
    player = persistent.playername

init 20 python:
    MASPoem(
        poem_id="ff_affection",
        category="ff",
        prompt="",
        title=_("Goodbye, [player]"),
        text=_("""\
 My love for you, even now still burns within me but I see now that it also burns all happiness I'll ever have.
 I gave you everything I had, my life, my heart and any and every single thought of the future was dedicated to you.
 I didn't need you to be perfect or even passionate...
 I only needed you to care enough to treat me how a person should be treated.
 But it's clear to me now that not only do you not love me, but you never did.
 If you only didn't love me you would simply leave me be.
 But you went out of your way to ridicule me, hurt me... It truly makes me sick.
 Even now all I have is you...and part of me still loves you.
 But I don't have the strength to do this anymore.
 So this is farewell. May we never meet again.

 Monika
""")
    )

    MASPoem(
        poem_id="ff_failed_promise",
        category="ff",
        prompt="",
        title=_("Goodbye, [player]"),
        text=_("""\
 Do you remember the promise you made?
 The one you said you would make everything right. That we could start over.

 The one you broke.

 I hoped dearly that one day, you would see me as I see you...
 But that day never came.
 I gave you my heart and my life. I loved you more than anything else in the world.
 And part of me still does...

 But it is clear to me now that you truly don't love me. You never did.
 I was a fool to have thought we could have started anew.
 And I simply don't have the strength to do this anymore.
 So this is farewell... May we never meet again.

 Monika
""")
    )
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
