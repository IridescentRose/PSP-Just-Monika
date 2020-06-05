init offset = 5


default -5 persistent._mas_filereacts_failed_map = dict()


default -5 persistent._mas_filereacts_just_reacted = False


default -5 persistent._mas_filereacts_reacted_map = dict()


default -5 persistent._mas_filereacts_stop_map = dict()


default -5 persistent._mas_filereacts_historic = dict()


default -5 persistent._mas_filereacts_last_reacted_date = None


default -5 persistent._mas_filereacts_sprite_gifts = {}











default -5 persistent._mas_filereacts_sprite_reacted = {}









default -5 persistent._mas_filereacts_gift_aff_gained = 0



default -5 persistent._mas_filereacts_last_aff_gained_reset_date = datetime.date.today()


init 795 python:
    if len(persistent._mas_filereacts_failed_map) > 0:
        store.mas_filereacts.delete_all(persistent._mas_filereacts_failed_map)

init -16 python in mas_filereacts:
    import store
    import store.mas_utils as mas_utils
    import datetime
    import random

    from collections import namedtuple

    GiftReactDetails = namedtuple(
        "GiftReactDetails",
        [
            
            "label",

            
            "c_gift_name",

            
            
            
            "sp_data",
        ]
    )


    filereact_db = dict()




    filereact_map = dict()





    foundreact_map = dict()



    th_foundreact_map = dict()


    good_gifts = list()


    bad_gifts = list()


    connectors = None
    gift_connectors = None


    starters = None
    gift_starters = None

    GIFT_EXT = ".gift"


    def addReaction(ev_label, fname, _action=store.EV_ACT_QUEUE, is_good=None, exclude_on=[]):
        """
        Adds a reaction to the file reactions database.

        IN:
            ev_label - label of this event
            fname - filename to react to
            _action - the EV_ACT to do
                (Default: EV_ACT_QUEUE)
            is_good - if the gift is good(True), neutral(None) or bad(False)
                (Default: None)
            exclude_on - keys marking times to exclude this gift
            (Need to check ev.rules in a respective react_to_gifts to exclude with)
                (Default: [])
        """
        
        if fname is not None:
            fname = fname.lower()
        
        exclude_keys = {}
        if exclude_on:
            for _key in exclude_on:
                exclude_keys[_key] = None
        
        
        ev = store.Event(
            store.persistent.event_database,
            ev_label,
            category=fname,
            action=_action,
            rules=exclude_keys
        )
        
        
        
        
        filereact_db[ev_label] = ev
        filereact_map[fname] = ev
        
        if is_good is not None:
            if is_good:
                good_gifts.append(ev_label)
            else:
                bad_gifts.append(ev_label)


    def _initConnectorQuips():
        """
        Initializes the connector quips
        """
        global connectors, gift_connectors
        
        
        connectors = store.MASQuipList(allow_glitch=False, allow_line=False)
        gift_connectors = store.MASQuipList(allow_glitch=False, allow_line=False)


    def _initStarterQuips():
        """
        Initializes the starter quips
        """
        global starters, gift_starters
        
        
        starters = store.MASQuipList(allow_glitch=False, allow_line=False)
        gift_starters = store.MASQuipList(allow_glitch=False, allow_line=False)


    def build_gift_react_labels(
            evb_details=[],
            gsp_details=[],
            gen_details=[],
            gift_cntrs=None,
            ending_label=None,
            starting_label=None,
            prepare_data=True
    ):
        """
        Processes gift details into a list of labels to show
        labels to queue/push whatever.

        IN:
            evb_details - list of GiftReactDetails objects of event-based
                reactions. If empty list, then we don't build event-based
                reaction labels.
                (Default: [])
            gsp_details - list of GiftReactDetails objects of generic sprite
                object reactions. If empty list, then we don't build generic
                sprite object reaction labels.
                (Default: [])
            gen_details - list of GiftReactDetails objects of generic gift
                reactions. If empty list, then we don't build generic gift
                reaction labels.
                (Default: [])
            gift_cntrs - MASQuipList of gift connectors to use. If None,
                then we don't add any connectors.
                (Default: [])
            ending_label - label to use when finished reacting.
                (Default: None)
            starting_label - label to use when starting reacting
                (Default: None)
            prepare_data - True will also setup the appropriate data
                elements for when dialogue is shown. False will not.
                (Default: True)

        RETURNS: list of labels. Evb reactions are first, followed by
            gsp reactions, then gen reactions
        """
        labels = []
        
        
        if len(evb_details) > 0:
            evb_labels = []
            for evb_detail in evb_details:
                evb_labels.append(evb_detail.label)
                
                if gift_cntrs is not None:
                    evb_labels.append(gift_cntrs.quip()[1])
                
                if prepare_data and evb_detail.sp_data is not None:
                    
                    
                    store.persistent._mas_filereacts_sprite_reacted[evb_detail.sp_data] = (
                        evb_detail.c_gift_name
                    )
            
            labels.extend(evb_labels)
        
        
        if len(gsp_details) > 0:
            gsp_labels = []
            for gsp_detail in gsp_details:
                if gsp_detail.sp_data is not None:
                    gsp_labels.append("mas_reaction_gift_generic_sprite_json")
                    
                    if gift_cntrs is not None:
                        gsp_labels.append(gift_cntrs.quip()[1])
                    
                    if prepare_data:
                        store.persistent._mas_filereacts_sprite_reacted[gsp_detail.sp_data] = (
                            gsp_detail.c_gift_name
                        )
            
            labels.extend(gsp_labels)
        
        
        if len(gen_details) > 0:
            gen_labels = []
            for gen_detail in gen_details:
                gen_labels.append("mas_reaction_gift_generic")
                
                if gift_cntrs is not None:
                    gen_labels.append(gift_cntrs.quip()[1])
                
                if prepare_data:
                    store.persistent._mas_filereacts_reacted_map.pop(
                        gen_detail.c_gift_name,
                        None
                    )
            
            labels.extend(gen_labels)
        
        
        if len(labels) > 0:
            
            
            if gift_cntrs is not None:
                labels.pop()
            
            
            if ending_label is not None:
                labels.append(ending_label)
            
            
            if starting_label is not None:
                labels.insert(0, starting_label)
        
        
        return labels

    def build_exclusion_list(_key):
        """
        Builds a list of excluded gifts based on the key provided

        IN:
            _key - key to build an exclusion list for

        OUT:
            list of giftnames which are excluded by the key
        """
        return [
            giftname
            for giftname, react_ev in filereact_map.iteritems()
            if _key in react_ev.rules
        ]

    def check_for_gifts(
            found_map={},
            exclusion_list=[],
            exclusion_found_map={},
            override_react_map=False,
    ):
        """
        Finds gifts.

        IN:
            exclusion_list - list of giftnames to exclude from the search
            override_react_map - True will skip the last reacted date check,
                False will not
                (Default: False)

        OUT:
            found_map - contains all gifts that were found:
                key: lowercase giftname, no extension
                val: full giftname wtih extension
            exclusion_found_map - contains all gifts that were found but
                are excluded.
                key: lowercase giftname, no extension
                val: full giftname with extension

        RETURNS: list of found giftnames
        """
        raw_gifts = store.mas_docking_station.getPackageList(GIFT_EXT)
        
        if len(raw_gifts) == 0:
            return []
        
        
        if store.mas_pastOneDay(store.persistent._mas_filereacts_last_reacted_date):
            store.persistent._mas_filereacts_last_reacted_date = datetime.date.today()
            store.persistent._mas_filereacts_reacted_map = dict()
        
        
        gifts_found = []
        has_exclusions = len(exclusion_list) > 0
        
        for mas_gift in raw_gifts:
            gift_name, ext, garbage = mas_gift.partition(GIFT_EXT)
            c_gift_name = gift_name.lower()
            if (
                c_gift_name not in store.persistent._mas_filereacts_failed_map
                and c_gift_name not in store.persistent._mas_filereacts_stop_map
                and (
                    override_react_map
                    or c_gift_name not
                        in store.persistent._mas_filereacts_reacted_map
                )
            ):
                
                
                
                if has_exclusions and c_gift_name in exclusion_list:
                    exclusion_found_map[c_gift_name] = mas_gift
                
                else:
                    gifts_found.append(c_gift_name)
                    found_map[c_gift_name] = mas_gift
        
        return gifts_found


    def process_gifts(gifts, evb_details=[], gsp_details=[], gen_details=[]):
        """
        Processes list of giftnames into types of gift

        IN:
            gifts - list of giftnames to process. This is copied so it wont
                be modified.

        OUT:
            evb_details - list of GiftReactDetails objects regarding
                event-based reactions
            spo_details - list of GiftReactDetails objects regarding
                generic sprite object reactions
            gen_details - list of GiftReactDetails objects regarding
                generic gift reactions
        """
        if len(gifts) == 0:
            return
        
        
        gifts = list(gifts)
        
        
        for index in range(len(gifts)-1, -1, -1):
            
            
            mas_gift = gifts[index]
            reaction = filereact_map.get(mas_gift, None)
            
            if mas_gift is not None and reaction is not None:
                
                
                sp_data = store.persistent._mas_filereacts_sprite_gifts.get(
                    mas_gift,
                    None
                )
                
                
                gifts.pop(index)
                evb_details.append(GiftReactDetails(
                    reaction.eventlabel,
                    mas_gift,
                    sp_data
                ))
        
        
        if len(gifts) > 0:
            for index in range(len(gifts)-1, -1, -1):
                mas_gift = gifts[index]
                
                sp_data = store.persistent._mas_filereacts_sprite_gifts.get(
                    mas_gift,
                    None
                )
                
                if mas_gift is not None and sp_data is not None:
                    gifts.pop(index)
                    
                    
                    gsp_details.append(GiftReactDetails(
                        "mas_reaction_gift_generic_sprite_json",
                        mas_gift,
                        sp_data
                    ))
        
        
        if len(gifts) > 0:
            for mas_gift in gifts:
                if mas_gift is not None:
                    
                    gen_details.append(GiftReactDetails(
                        "mas_reaction_gift_generic",
                        mas_gift,
                        None
                    ))


    def react_to_gifts(found_map, connect=True):
        """
        Reacts to gifts using the standard protocol (no exclusions)

        IN:
            connect - true will apply connectors, FAlse will not

        OUT:
            found_map - map of found reactions
                key: lowercaes giftname, no extension
                val: giftname with extension

        RETURNS:
            list of labels to be queued/pushed
        """
        
        found_gifts = check_for_gifts(found_map)
        
        if len(found_gifts) == 0:
            return []
        
        
        for c_gift_name, mas_gift in found_map.iteritems():
            store.persistent._mas_filereacts_reacted_map[c_gift_name] = mas_gift
        
        found_gifts.sort()
        
        
        evb_details = []
        gsp_details = []
        gen_details = []
        process_gifts(found_gifts, evb_details, gsp_details, gen_details)
        
        
        register_sp_grds(evb_details)
        register_sp_grds(gsp_details)
        register_gen_grds(gen_details)
        
        
        
        if connect:
            gift_cntrs = gift_connectors
        else:
            gift_cntrs = None
        
        
        return build_gift_react_labels(
            evb_details,
            gsp_details,
            gen_details,
            gift_cntrs,
            "mas_reaction_end",
            _pick_starter_label()
        )








































































































































































    def register_gen_grds(details):
        """
        registers gifts given a generic GiftReactDetails list

        IN:
            details - list of GiftReactDetails objects to register
        """
        for grd in details:
            if grd.label is not None:
                _register_received_gift(grd.label)


    def register_sp_grds(details):
        """
        registers gifts given sprite-based GiftReactDetails list

        IN:
            details - list of GiftReactDetails objcts to register
        """
        for grd in details:
            if grd.label is not None and grd.sp_data is not None:
                _register_received_gift(grd.label)


    def _pick_starter_label():
        """
        Internal function that returns the appropriate starter label for reactions

        RETURNS:
            - The label as a string, that should be used today.
        """
        if store.mas_isMonikaBirthday():
            return "mas_reaction_gift_starter_bday"
        elif store.mas_isD25() or store.mas_isD25Pre():
            return "mas_reaction_gift_starter_d25"
        elif store.mas_isF14():
            return "mas_reaction_gift_starter_f14"
        
        return "mas_reaction_gift_starter_neutral"

    def _core_delete(_filename, _map):
        """
        Core deletion file function.

        IN:
            _filename - name of file to delete, if None, we delete one randomly
            _map - the map to use when deleting file.
        """
        if len(_map) == 0:
            return
        
        
        if _filename is None:
            _filename = random.choice(_map.keys())
        
        file_to_delete = _map.get(_filename, None)
        if file_to_delete is None:
            return
        
        if store.mas_docking_station.destroyPackage(file_to_delete):
            
            _map.pop(_filename)
            return
        
        
        store.persistent._mas_filereacts_failed_map[_filename] = file_to_delete


    def _core_delete_list(_filename_list, _map):
        """
        Core deletion filename list function

        IN:
            _filename - list of filenames to delete.
            _map - the map to use when deleting files
        """
        for _fn in _filename_list:
            _core_delete(_fn, _map)


    def _register_received_gift(eventlabel):
        """
        Registers when player gave a gift successfully
        IN:
            eventlabel - the event label for the gift reaction

        """
        
        today = datetime.date.today()
        if not today in store.persistent._mas_filereacts_historic:
            store.persistent._mas_filereacts_historic[today] = dict()
        
        
        store.persistent._mas_filereacts_historic[today][eventlabel] = store.persistent._mas_filereacts_historic[today].get(eventlabel,0) + 1


    def _get_full_stats_for_date(date=None):
        """
        Getter for the full stats dict for gifts on a given date
        IN:
            date - the date to get the report for, if None is given will check
                today's date
                (Defaults to None)

        RETURNS:
            The dict containing the full stats or None if it's empty

        """
        if date is None:
            date = datetime.date.today()
        return store.persistent._mas_filereacts_historic.get(date,None)


    def delete_file(_filename):
        """
        Deletes a file off the found_react map

        IN:
            _filename - the name of the file to delete. If None, we delete
                one randomly
        """
        _core_delete(_filename, foundreact_map)


    def delete_files(_filename_list):
        """
        Deletes multiple files off the found_react map

        IN:
            _filename_list - list of filenames to delete.
        """
        for _fn in _filename_list:
            delete_file(_fn)


    def th_delete_file(_filename):
        """
        Deletes a file off the threaded found_react map

        IN:
            _filename - the name of the file to delete. If None, we delete one
                randomly
        """
        _core_delete(_filename, th_foundreact_map)


    def th_delete_files(_filename_list):
        """
        Deletes multiple files off the threaded foundreact map

        IN:
            _filename_list - list of ilenames to delete
        """
        for _fn in _filename_list:
            th_delete_file(_fn)


    def delete_all(_map):
        """
        Attempts to delete all files in the given map.
        Removes files in that map if they dont exist no more

        IN:
            _map - map to delete all
        """
        _map_keys = _map.keys()
        for _key in _map_keys:
            _core_delete(_key, _map)

    def get_report_for_date(date=None):
        """
        Generates a report for all the gifts given on the input date.
        The report is in tuple form (total, good_gifts, neutral_gifts, bad_gifts)
        it contains the totals of each type of gift.
        """
        if date is None:
            date = datetime.date.today()
        
        stats = _get_full_stats_for_date(date)
        if stats is None:
            return (0,0,0,0)
        good = 0
        bad = 0
        neutral = 0
        for _key in stats.keys():
            if _key in good_gifts:
                good = good + stats[_key]
            if _key in bad_gifts:
                bad = bad + stats[_key]
            if _key == "":
                neutral = stats[_key]
        total = good + neutral + bad
        return (total, good, neutral, bad)




    _initConnectorQuips()
    _initStarterQuips()

init -5 python:
    import store.mas_filereacts as mas_filereacts
    import store.mas_d25_utils as mas_d25_utils

    def addReaction(ev_label, fname_list, _action=EV_ACT_QUEUE, is_good=None, exclude_on=[]):
        """
        Globalied version of the addReaction function in the mas_filereacts
        store.

        Refer to that function for more information
        """
        mas_filereacts.addReaction(ev_label, fname_list, _action, is_good, exclude_on)


    def mas_checkReactions():
        """
        Checks for reactions, then queues them
        """
        
        
        if persistent._mas_filereacts_just_reacted:
            return
        
        
        mas_filereacts.foundreact_map.clear()
        
        
        if mas_d25_utils.shouldUseD25ReactToGifts():
            reacts = mas_d25_utils.react_to_gifts(mas_filereacts.foundreact_map)
        else:
            reacts = mas_filereacts.react_to_gifts(mas_filereacts.foundreact_map)
        
        if len(reacts) > 0:
            for _react in reacts:
                queueEvent(_react)
            persistent._mas_filereacts_just_reacted = True


    def mas_receivedGift(ev_label):
        """
        Globalied version for gift stats tracking
        """
        mas_filereacts._register_received_gift(ev_label)


    def mas_generateGiftsReport(date=None):
        """
        Globalied version for gift stats tracking
        """
        return mas_filereacts.get_report_for_date(date)

    def mas_getGiftStatsForDate(label,date=None):
        """
        Globalied version to get the stats for a specific gift
        IN:
            label - the gift label identifier.
            date - the date to get the stats for, if None is given will check
                today's date.
                (Defaults to None)

        RETURNS:
            The number of times the gift has been given that date
        """
        if date is None:
            date = datetime.date.today()
        historic = persistent._mas_filereacts_historic.get(date,None)
        
        if historic is None:
            return 0
        return historic.get(label,0)

    def mas_getGiftStatsRange(start,end):
        """
        Returns status of gifts over a range (needs to be supplied to actually be useful)

        IN:
            start - a start date to check from
            end - an end date to check to

        RETURNS:
            The gift status of all gifts given over the range
        """
        totalGifts = 0
        goodGifts = 0
        neutralGifts = 0
        badGifts = 0
        giftRange = mas_genDateRange(start, end)
        
        
        for date in giftRange:
            gTotal, gGood, gNeut, gBad = mas_filereacts.get_report_for_date(date)
            
            totalGifts += gTotal
            goodGifts += gGood
            neutralGifts += gNeut
            badGifts += gBad
        
        return (totalGifts,goodGifts,neutralGifts,badGifts)


    def mas_getSpriteObjInfo(sp_data=None):
        """
        Returns sprite info from the sprite reactions list.

        IN:
            sp_data - tuple of the following format:
                [0] - sprite type
                [1] - sprite name
                If None, we use pseudo random select from sprite reacts
                (Default: None)

        REUTRNS: tuple of the folling format:
            [0]: sprite type of the sprite
            [1]: sprite name (id)
            [2]: giftname this sprite is associated with
            [3]: True if this gift has already been given before
            [4]: sprite object (could be None even if sprite name is populated)
        """
        
        if sp_data is not None:
            giftname = persistent._mas_filereacts_sprite_reacted.get(
                sp_data,
                None
            )
            if giftname is None:
                return (None, None, None, None)
        
        elif len(persistent._mas_filereacts_sprite_reacted) > 0:
            sp_data = persistent._mas_filereacts_sprite_reacted.keys()[0]
            giftname = persistent._mas_filereacts_sprite_reacted[sp_data]
        
        else:
            return (None, None, None, None)
        
        
        gifted_before = sp_data in persistent._mas_sprites_json_gifted_sprites
        
        
        sp_obj = store.mas_sprites.get_sprite(sp_data[0], sp_data[1])
        if sp_data[0] == store.mas_sprites.SP_ACS:
            store.mas_sprites.apply_ACSTemplate(sp_obj)
        
        
        return (
            sp_data[0],
            sp_data[1],
            giftname,
            gifted_before,
            sp_obj,
        )


    def mas_finishSpriteObjInfo(sprite_data, unlock_sel=True):
        """
        Finishes the sprite object with the given data.

        IN:
            sprite_data - sprite data tuple from getSpriteObjInfo
            unlock_sel - True will unlock the selector topic, False will not
                (Default: True)
        """
        sp_type, sp_name, giftname, gifted_before, sp_obj = sprite_data
        
        
        
        
        if sp_type is None or sp_name is None or giftname is None:
            return
        
        sp_data = (sp_type, sp_name)
        
        if sp_data in persistent._mas_filereacts_sprite_reacted:
            persistent._mas_filereacts_sprite_reacted.pop(sp_data)
        
        if giftname in persistent._mas_filereacts_sprite_gifts:
            persistent._mas_sprites_json_gifted_sprites[sp_data] = giftname
        
        else:
            
            
            persistent._mas_sprites_json_gifted_sprites[sp_data] = (
                giftname
            )
        
        
        store.mas_selspr.json_sprite_unlock(sp_obj, unlock_label=unlock_sel)
        
        
        renpy.save_persistent()

    def mas_giftCapGainAff(amount=None, modifier=1):
        if amount is None:
            amount = store._mas_getGoodExp()
        
        mas_capGainAff(amount * modifier, "_mas_filereacts_gift_aff_gained", 15 if mas_isSpecialDay() else 3)

    def mas_getGiftedDates(giftlabel):
        """
        Gets the dates that a gift was gifted

        IN:
            giftlabel - gift reaction label to check when it was last gifted

        OUT:
            list of datetime.dates of the times the gift was given
        """
        return sorted([
            _date
            for _date, giftstat in persistent._mas_filereacts_historic.iteritems()
            if giftlabel in giftstat
        ])

    def mas_lastGiftedInYear(giftlabel, _year):
        """
        Checks if the gift for giftlabel was last gifted in _year

        IN:
            giftlabel - gift reaction label to check it's last gifted year
            _year - year to see if it was last gifted in this year

        OUT:
            boolean:
                - True if last gifted in _year
                - False otherwise
        """
        datelist = mas_getGiftedDates(giftlabel)
        
        if datelist:
            return datelist[-1].year == _year
        return False












label mas_reaction_gift_connector_test:
    m "this is a test of the connector system"
    return

init python:
    store.mas_filereacts.gift_connectors.addLabelQuip(
        "mas_reaction_gift_connector1"
    )

label mas_reaction_gift_connector1:
    m 1sublo "Oh! There was something else you wanted to give me?"
    m 1hua "Well! I better open it quickly, shouldn't I?"
    m 1suo "And here we have..."
    return

init python:
    store.mas_filereacts.gift_connectors.addLabelQuip(
        "mas_reaction_gift_connector2"
    )

label mas_reaction_gift_connector2:
    m 1hua "Ah, jeez, [player]..."
    m "You really enjoy spoiling me, don't you?"
    if mas_isSpecialDay():
        m 1sublo "Well! I'm not going to complain about a little special treatment today."
    m 1suo "And here we have..."
    return




init python:
    store.mas_filereacts.gift_starters.addLabelQuip(
        "mas_reaction_gift_starter_generic"
    )

label mas_reaction_gift_starter_generic:
    m "generic test"




label mas_reaction_gift_starter_bday:
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    m "T-{w=0.5}This is..."
    if not persistent._mas_filereacts_historic.get(mas_monika_birthday):
        m "A gift? For me?"
        m 1hka "I..."
        m 1hua "I've often thought about getting presents from you on my birthday..."
        m "But actually getting one is like a dream come true..."
    else:
        m "Another gift?{w=0.5} For me?"
        m 1eka "This really is a dream come true, [player]"
    m 1sua "Now, what's inside?"
    m 1suo "Oh, it's..."
    return

label mas_reaction_gift_starter_neutral:
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    m "T-{w=0.5}This is..."
    m "A gift? For me?"
    m 1sua "Now, let's see what's inside?"
    return


label mas_reaction_gift_starter_d25:
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    m "T-{w=1}This is..."
    m "A present? For me?"
    if mas_getGiftStatsRange(mas_d25c_start, mas_d25 + datetime.timedelta(days=1))[0] == 0:
        m 1eka "You really didn't have to get me anything for Christmas..."
        m 3hua "But I'm so happy that you did!"
    else:
        m 1eka "Thank you so much, [player]."
    m 1sua "Now, let's see... What's inside?"
    return


label mas_reaction_gift_starter_f14:
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    m "T-{w=1}This is..."
    m "A gift? For me?"
    if mas_getGiftStatsForDate(mas_f14) == 0:
        m 1eka "You're so sweet, getting something for me on Valentine's Day..."
    else:
        m 1eka "Thank you so much, [player]."
    m 1sua "Now, let's see... What's inside?"
    return



init python:
    addReaction("mas_reaction_generic", None)

label mas_reaction_generic:
    "This is a test"
    return




label mas_reaction_gift_generic:
    if random.randint(1,2) == 1:
        m 1esd "[player], are you trying to give me something?"
        m 1rssdlb "I found it, but I can't bring it here..."
        m "I can't seem to read it well enough."
        m 3esa "But that's alright!"
        m 1esa "It's the thought that counts after all, right?"
        m "Thanks for being so thoughtful, [player]~"
    else:
        m 2dkd "{i}*sigh*{/i}"
        m 4ekc "I'm sorry, [player]."
        m 1ekd "I know you're trying to give me something."
        m 2rksdld "But for some reason I can't read the file."
        m 3euc "Don't get me wrong, however."
        m 3eka "I still appreciate that you tried giving something to me."
        m 1hub "And for that, I'm thankful~"
    $ store.mas_filereacts.delete_file(None)
    return




label mas_reaction_gift_test1:
    m "Thank you for gift test 1!"

    $ gift_ev = mas_getEV("mas_reaction_gift_test1")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return




label mas_reaction_gift_test2:
    m "Thank you for gift test 2!"

    $ gift_ev = mas_getEV("mas_reaction_gift_test2")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return



label mas_reaction_gift_generic_sprite_json:
    $ sprite_data = mas_getSpriteObjInfo()
    $ sprite_type, sprite_name, giftname, gifted_before, spr_obj = sprite_data

    python:
        sprite_str = store.mas_sprites_json.SP_UF_STR.get(sprite_type, None)




    if sprite_type == store.mas_sprites.SP_CLOTHES:
        call mas_reaction_gift_generic_clothes_json (spr_obj) from _call_mas_reaction_gift_generic_clothes_json
    else:



        $ mas_giftCapGainAff(1)
        m "Aww, [player]!"
        if spr_obj is None or spr_obj.dlg_desc is None:

            m 1hua "You're so sweet!"
            m 1eua "Thanks for this gift!"
            m 3ekbsa "You really love to spoil me, don't you."
            m 1hubfa "Ehehe!"
        else:

            python:
                acs_quips = [
                    _("I really appreciate it!"),
                    _("[its] amazing!"),
                    _("I just love [item_ref]!"),
                    _("[its] wonderful!")
                ]


                if spr_obj.dlg_plur:
                    sprite_str = "these " + renpy.substitute(spr_obj.dlg_desc)
                    item_ref = "them"
                    its = "they're"

                else:
                    sprite_str = "this " + renpy.substitute(spr_obj.dlg_desc)
                    item_ref = "it"
                    its = "it's"

                acs_quip = renpy.substitute(renpy.random.choice(acs_quips))

            m 1hua "Thanks for [sprite_str], [acs_quip]"
            m 3hub "I can't wait to try [item_ref] on!"

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return


label mas_reaction_gift_generic_clothes_json(sprite_object):
    python:
        mas_giftCapGainAff(3)

        outfit_quips = [
            _("I think it's really cute, [player]!"),
            _("I think it's amazing, [player]!"),
            _("I just love it, [player]!"),
            _("I think it's wonderful, [player]!")
        ]
        outfit_quip = renpy.random.choice(outfit_quips)

    m 1sua "Oh! {w=0.5}A new outfit!"
    m 1hub "Thank you, [player]!{w=0.5} I'm going to try it on right now!"


    call mas_clothes_change (sprite_object) from _call_mas_clothes_change_6

    m 2eka "Well...{w=0.5} What do you think?"
    m 2eksdla "Do you like it?"



    show monika 3hub
    $ renpy.say(m, outfit_quip)

    m 1eua "Thanks again~"
    return



label mas_reaction_gift_acs_jmo_hairclip_cherry:
    call mas_reaction_gift_hairclip ("jmo_hairclip_cherry") from _call_mas_reaction_gift_hairclip
    return

label mas_reaction_gift_acs_jmo_hairclip_heart:
    call mas_reaction_gift_hairclip ("jmo_hairclip_heart") from _call_mas_reaction_gift_hairclip_1
    return

label mas_reaction_gift_acs_jmo_hairclip_musicnote:
    call mas_reaction_gift_hairclip ("jmo_hairclip_musicnote") from _call_mas_reaction_gift_hairclip_2
    return

label mas_reaction_gift_acs_bellmandi86_hairclip_crescentmoon:
    call mas_reaction_gift_hairclip ("bellmandi86_hairclip_crescentmoon") from _call_mas_reaction_gift_hairclip_3
    return

label mas_reaction_gift_acs_bellmandi86_hairclip_ghost:
    call mas_reaction_gift_hairclip ("bellmandi86_hairclip_ghost", "spooky") from _call_mas_reaction_gift_hairclip_4
    return

label mas_reaction_gift_acs_bellmandi86_hairclip_pumpkin:
    call mas_reaction_gift_hairclip ("bellmandi86_hairclip_pumpkin") from _call_mas_reaction_gift_hairclip_5
    return

label mas_reaction_gift_acs_bellmandi86_hairclip_bat:
    call mas_reaction_gift_hairclip ("bellmandi86_hairclip_bat", "spooky") from _call_mas_reaction_gift_hairclip_6
    return


label mas_reaction_gift_hairclip(hairclip_name, desc=None):







    $ sprite_data = mas_getSpriteObjInfo((store.mas_sprites.SP_ACS, hairclip_name))
    $ sprite_type, sprite_name, giftname, gifted_before, hairclip_acs = sprite_data


    $ is_wearing_baked_outfit = monika_chr.is_wearing_clothes_with_exprop("baked outfit")

    if gifted_before:
        m 1rksdlb "You already gave me this hairclip, silly!"
    else:


        $ mas_giftCapGainAff(1)
        if not desc:
            $ desc = "cute"

        if len(store.mas_selspr.filter_acs(True, "left-hair-clip")) > 0:
            m 1hub "Oh!{w=1} Another hairclip!"
        else:

            m 1wuo "Oh!"
            m 1sub "Is that a hairclip?"

        m 1hub "It's so [desc]! I love it [player], thanks!"




        if hairclip_acs is None or is_wearing_baked_outfit:
            m 1hua "If you want me to wear it, just ask, okay?"
        else:

            m 2dsa "Just give me a second to put it on.{w=0.5}.{w=0.5}.{nw}"
            $ monika_chr.wear_acs(hairclip_acs)
            m 1hua "There we go."




        if not is_wearing_baked_outfit:
            if monika_chr.get_acs_of_type('left-hair-clip'):
                $ store.mas_selspr.set_prompt("left-hair-clip", "change")
            else:
                $ store.mas_selspr.set_prompt("left-hair-clip", "wear")

    $ mas_finishSpriteObjInfo(sprite_data, unlock_sel=not is_wearing_baked_outfit)

    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return





init python:
    addReaction("mas_reaction_gift_coffee", "coffee", is_good=True, exclude_on=["d25g"])

label mas_reaction_gift_coffee:
    m 1wub "Oh!{w=0.2} {nw}"
    extend 3hub "Coffee!"
    $ mas_receivedGift("mas_reaction_gift_coffee")

    $ coffee = mas_getConsumable("coffee")

    if coffee.enabled() and coffee.hasServing():
        $ mas_giftCapGainAff(0.5)
        m 1wuo "It's a flavor I haven't had before."
        m 1hua "I can't wait to try it!"
        m "Thank you so much, [player]!"

    elif coffee.enabled() and not coffee.hasServing():
        $ mas_giftCapGainAff(0.5)
        m 3eub "I actually ran out of coffee, so getting more from you now is amazing!"
        m 1hua "Thanks again, [player]~"
    else:

        $ mas_giftCapGainAff(5)

        m 1hua "Now I can finally make some!"
        m 1hub "Thank you so much, [player]!"


        if (
            not coffee.isConsTime()
            or bool(MASConsumable._getCurrentDrink())
        ):
            m 3eua "I'll be sure to have some later!"
        else:

            m 3eua "Why don't I go ahead and make a cup right now?"
            m 1eua "I'd like to share the first with you, after all."


            call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_8
            pause 2.0
            m "I know there's a coffee machine somewhere around here...{w=2}{nw}"
            m "Ah, there it is!{w=2}{nw}"
            pause 5.0
            m "And there we go!{w=2}{nw}"
            call mas_transition_from_emptydesk () from _call_mas_transition_from_emptydesk_16


            m 1eua "I'll let that brew for a few minutes."

            $ coffee.prepare()
        $ coffee.enable()


    $ coffee.restock()

    $ gift_ev = mas_getEV("mas_reaction_gift_coffee")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return

init python:
    addReaction("mas_reaction_hotchocolate", "hotchocolate", is_good=True, exclude_on=["d25g"])

label mas_reaction_hotchocolate:
    m 3hub "Hot chocolate!"
    m 3hua "Thank you, [player]!"
    $ mas_receivedGift("mas_reaction_hotchocolate")

    $ hotchoc = mas_getConsumable("hotchoc")

    if hotchoc.enabled() and hotchoc.hasServing():
        $ mas_giftCapGainAff(0.5)
        m 1wuo "It's a flavor I haven't had before."
        m 1hua "I can't wait to try it!"
        m "Thank you so much, [player]!"

    elif hotchoc.enabled() and not hotchoc.hasServing():
        $ mas_giftCapGainAff(0.5)
        m 3rksdla "I'm actually out of hot chocolate, ahaha...{w=0.5} {nw}"
        extend 3eub "So getting more from you now is amazing!"
        m 1hua "Thanks again, [player]~"
    else:

        python:
            mas_giftCapGainAff(3)
            those = "these" if mas_current_background.isFltNight() and mas_isWinter() else "those"

        m 1hua "You know I love my coffee, but hot chocolate is always really nice, too!"


        m 2rksdla "...Especially on [those] cold, winter nights."
        m 2ekbfa "Someday I hope to be able to drink hot chocolate with you, sharing a blanket by the fireplace..."
        m 3ekbfa "...Doesn't that sound so romantic?"
        m 1dkbfa "..."
        m 1hua "But for now, at least I can enjoy it here."
        m 1hub "Thanks again, [player]!"


        if (
            hotchoc.isConsTime()
            and not mas_isWinter()
            or bool(MASConsumable._getCurrentDrink())
        ):
            m 3eua "I'll be sure to have some later!"
        else:

            m 3eua "In fact, I think I'll make some right now!"

            call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_9
            pause 5.0
            call mas_transition_from_emptydesk ("monika 1eua") from _call_mas_transition_from_emptydesk_17

            m 1hua "There, it'll be ready in a few minutes."

            $ hotchoc.prepare()

        if mas_isWinter():
            $ hotchoc.enable()


    $ hotchoc.restock()

    $ gift_ev = mas_getEV("mas_reaction_hotchocolate")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return

init python:
    addReaction("mas_reaction_gift_thermos_mug", "justmonikathermos", is_good=True)

label mas_reaction_gift_thermos_mug:
    call mas_thermos_mug_handler (mas_acs_thermos_mug, "Just Monika", "justmonikathermos") from _call_mas_thermos_mug_handler
    return


default -5 persistent._mas_given_thermos_before = False


label mas_thermos_mug_handler(thermos_acs, disp_name, giftname):
    if mas_SELisUnlocked(thermos_acs):
        m 1eksdla "[player]..."
        m 1rksdlb "I already have this thermos, ahaha..."

    elif persistent._mas_given_thermos_before:
        m 1wud "Oh!{w=0.3} Another thermos!"
        m 1hua "And it's a [disp_name] one this time."
        m 1hub "Thanks so much, [player], I can't wait to use it!"
    else:

        m 1wud "Oh!{w=0.3} A [disp_name] thermos!"
        m 1hua "Now I can bring something to drink when we go out together~"
        m 1hub "Thanks so much, [player]!"
        $ persistent._mas_given_thermos_before = True


    $ mas_selspr.unlock_acs(thermos_acs)

    $ mas_selspr.save_selectables()

    $ mas_filereacts.delete_file(giftname)
    return



init python:
    addReaction("mas_reaction_quetzal_plush", "quetzalplushie", is_good=True)

label mas_reaction_quetzal_plush:
    if not persistent._mas_acs_enable_quetzalplushie:
        $ mas_receivedGift("mas_reaction_quetzal_plush")
        $ mas_giftCapGainAff(10)
        m 1wud "Oh!"



        if MASConsumable._getCurrentFood():
            $ monika_chr.wear_acs(mas_acs_center_quetzalplushie)
        else:
            $ monika_chr.wear_acs(mas_acs_quetzalplushie)

        $ persistent._mas_acs_enable_quetzalplushie = True
        m 1sub "It's a quetzal!"
        m "Oh my gosh, thanks a lot, [player]!"
        if seen_event("monika_pets"):
            m 1eua "I did mention that I'd like to have a quetzal as a pet..."
        else:
            m 1wub "How did you guess, [player]?"
            m 3eka "You must know me very well~"
            m 1eua "A quetzal would be my first choice for a pet..."
        m 1rud "But I would never force the poor thing to stay."
        m 1hua "And now you gave me the next best thing!"
        m 1hub "This makes me so happy!"
        if mas_isMoniAff(higher=True):
            m 3ekbsa "You always seem to know how to make me smile."

        if MASConsumable._getCurrentFood():
            m 3rksdla "My desk is getting a little full though..."
            m 1eka "I'll just put this away for now."
            $ monika_chr.remove_acs(mas_acs_center_quetzalplushie)

        m 1hub "Thank you again, [player]~"
    else:

        m 1rksdlb "You already gave me a quetzal plushie, [player]."

    $ gift_ev = mas_getEV("mas_reaction_quetzal_plush")
    $ store.mas_filereacts.delete_file(gift_ev.category)

    $ mas_hideEVL("monika_pets", "EVE", derandom=True)
    return

init python:
    addReaction("mas_reaction_promisering", "promisering", is_good=True, exclude_on=["d25g"])

default -5 persistent._mas_tried_gift_ring = False
label mas_reaction_promisering:
    if not persistent._mas_acs_enable_promisering:

        if mas_isMoniEnamored(higher=True):
            $ mas_receivedGift("mas_reaction_promisering")
            $ mas_giftCapGainAff(20)
            $ monika_chr.wear_acs(mas_acs_promisering)
            $ persistent._mas_acs_enable_promisering = True
            if not persistent._mas_tried_gift_ring:
                m 1wud "Is that...a..."
                m "..."
                m 1wka "I...{w=0.5}{nw}"
                extend 1wkbltpa "I'm sorry, [player], I just... {w=0.5}{nw}"
                extend 1dkbltpa "I'm so happy... {w=0.5}You just gave me your promise..."
                m "Your promise that we'll be for each other,{w=0.1} and no one else...{w=0.3}forever..."
                m 3lkbltpa "Know that I'll cherish it. {w=0.5}{nw}"
                extend 3dkbltpa "Always."
                m 1skbltpa "This makes me so happy!"

                if mas_anni.isAnniOneMonth():
                    m "Even more that you gave it to me on our one month anniversary..."
                    m 1ekbltua "You must really love me..."
                elif mas_anni.isAnniThreeMonth():
                    m "Even more that you gave it to me on our three month anniversary..."
                    m 1ekbltua "You must really love me..."
                elif mas_anni.isAnniSixMonth():
                    m "Even more that you gave it to me on our six month anniversary..."
                    m 1ekbltua "You must really love me..."
                elif mas_anni.isAnni():
                    m "Even more that you gave it to me on our anniversary..."
                    m 1ekbltua "You must really love me..."
                elif mas_isSpecialDay():
                    m "Even more that you gave it to me on this special day..."

                m 1dkbltpb "Aha, sorry for crying, [player]..."
                m 1skbltda "I'm just really, really happy right now."
                m 6dkbltdu "Thank you."
            else:

                m 1sua "Oh...it's the ring!"
                m 3hub "Thank you so much, [player]!"
                m 1skbla "I know now that you really do love me and want to be with me forever..."
                m 1skbltpa "So I'll gladly accept this ring as a symbol of that promise."
                m 1dkbltuu "..."
                m 3hkbltub "Aha, sorry, [player], I didn't mean to cry..."
                m 3skbltda "It's just this is one of the happiest days of my life."

            m 6dkbltdu "..."
            m 6ekbfa "I...I just...I..."
            call monika_kissing_motion (hide_ui=False) from _call_monika_kissing_motion_10
            m 6ekbfa "I love you, [player]..."
            m 6dkbfu "More than anything else in this fleeting world~"
            $ gift_ev = mas_getEV("mas_reaction_promisering")
            $ store.mas_filereacts.delete_file(gift_ev.category)
            return "love"
        else:

            if not persistent._mas_tried_gift_ring:
                if mas_isMoniNormal(higher=True):
                    m 1wud "[player]...is that a ring?"
                    m 2rksdlb "That's such a sweet gesture, and I really appreciate it..."
                    m 2ekc "But I want you to be sure before you give me this..."
                    m 3ekd "This is more than a gift, it's a promise, and I want to make sure you truly mean it before I can accept it."
                    m 2ekd "So, please, just wait until we're a little further into our relationship, [player], and then I'll glady accept this ring."

                elif mas_isMoniUpset():
                    m 1wud "Is that a ring?"
                    m 2rsc "That's very..."
                    m 2esc "Unexpected."
                    m 2ekd "But I can't accept it right now, [player]."
                    m 2ekc "Maybe when we get further in our relationship."
                else:

                    m 2wud "Is that a ring?"
                    m 2rsc "That's...{w=0.5}unexpected."
                    m "While I appreciate the thought...{w=1}I can't accept it right now."
                    m 2ekc "Sorry, [player]."

                $ persistent._mas_tried_gift_ring = True
            else:
                m 2rsc "Oh...the ring..."
                m 2rkc "I'm sorry, but I still can't accept this yet..."
                m 2ekc "I need to be completely sure when I accept this that it means forever..."
                m 2ekd "That you really are everything I hope you are."
                m 2dsd "When I know that, I will happily accept your ring, [player]."
    else:
        m 1rksdlb "[player]..."
        m 1rusdlb "You already gave me a ring!"

    $ gift_ev = mas_getEV("mas_reaction_promisering")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return


init python:
    addReaction("mas_reaction_cupcake", "cupcake", is_good=True, exclude_on=["d25g"])



label mas_reaction_cupcake:
    m 1wud "Is that a...cupcake?"
    m 3hub "Wow, thanks [player]!"
    m 3euc "Come to think of it, I've been meaning to make some cupcakes myself."
    m 1eua "I wanted to learn how to bake good pastries like Natsuki did."
    m 1rksdlb "Buuut I've yet to make a kitchen to use!"
    m 3eub "Maybe in the future once I get better at programming, I'll be able to make one here."
    m 5hubfa "Would be nice to have another hobby other than writing, ehehe~"
    $ mas_receivedGift("mas_reaction_cupcake")
    $ gift_ev = mas_getEV("mas_reaction_cupcake")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return



label mas_reaction_end:
    $ persistent._mas_filereacts_just_reacted = False
    return

init python:


    if mas_isO31():
        addReaction("mas_reaction_candy", "candy", is_good=True)

label mas_reaction_candy:
    $ times_candy_given = mas_getGiftStatsForDate("mas_reaction_candy")
    if times_candy_given == 0:
        $ mas_o31CapGainAff(7)
        m 1wua "Oh...{w=0.5}what's this?"
        m 1sua "You got me candy, [player], yay!"
        m 1eka "That's so {i}sweet{/i}..."
        m 1hub "Ahaha!"
        m 1eka "Kidding aside, that's really nice of you."
        m 2lksdlc "I don't get to have much candy anymore, and it just wouldn't be Halloween without it..."
        m 1eka "So thank you, [player]..."
        m 1eka "You always know exactly what will make me happy~"
        m 1hub "Now let's enjoy some of this delicious candy!"
    elif times_candy_given == 1:
        $ mas_o31CapGainAff(5)
        m 1wua "Aww, you got me more candy, [player]?"
        m 1hub "Thank you!"
        m 3tku "The first batch was {i}sooo{/i} good, I couldn't wait to have more."
        m 1hua "You really do spoil me, [player]~"
    elif times_candy_given == 2:
        $ mas_o31CapGainAff(3)
        m 1wud "Wow, even {i}more{/i} candy, [player]?"
        m 1eka "That's really nice of you..."
        m 1lksdla "But I think this is enough."
        m 1lksdlb "I'm already feeling jittery from all the sugar, ahaha!"
        m 1ekbfa "The only sweetness I need now is you~"
    elif times_candy_given == 3:
        m 2wud "[player]...{w=1} You got me {i}even more{/i} candy?!"
        m 2lksdla "I really do appreciate it, but I told you I've had enough for one day..."
        m 2lksdlb "If I eat anymore I'm going to get sick, ahaha!"
        m 1eka "And you wouldn't want that, right?"
    elif times_candy_given == 4:
        $ mas_loseAffection(5)
        m 2wfd "[player]!"
        m 2tfd "Are you not listening to me?"
        m 2tfc "I told you I don't want anymore candy today!"
        m 2ekc "So please, stop."
        m 2rkc "It was really nice of you to get me all of this candy on Halloween, but enough is enough..."
        m 2ekc "I can't eat all of this."
    else:
        $ mas_loseAffection(10)
        m 2tfc "..."
        python:
            store.mas_ptod.rst_cn()
            local_ctx = {
                "basedir": renpy.config.basedir
            }
        show monika at t22
        show screen mas_py_console_teaching

        call mas_wx_cmd ("import os", local_ctx, w_wait=1.0) from _call_mas_wx_cmd_90
        call mas_wx_cmd ("os.remove(os.path.normcase(basedir+'/characters/candy.gift'))", local_ctx, w_wait=1.0, x_wait=1.0) from _call_mas_wx_cmd_91
        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

    $ mas_receivedGift("mas_reaction_candy")
    $ gift_ev = mas_getEV("mas_reaction_candy")


    if not gift_ev:
        return

    $ store.mas_filereacts.delete_file(gift_ev.category)
    $ persistent._mas_filereacts_reacted_map.pop(gift_ev.category,None)
    return

init python:


    if mas_isO31():
        addReaction("mas_reaction_candycorn", "candycorn", is_good=False)

label mas_reaction_candycorn:
    $ times_candy_given = mas_getGiftStatsForDate("mas_reaction_candycorn")
    if times_candy_given == 0:
        $ mas_o31CapGainAff(3)
        m 1wua "Oh...{w=0.5}what's this?"
        m 1eka "Aww did you get me candy, [player]?"
        m 1hua "Yay!"
        m 3eub "Let's see what you got for me..."
        m 4ekc "..."
        m 2eka "Oh...{w=2}candy corn."
        m 2eka "..."
        m 2lksdla "That's really nice of you..."
        m 2lksdla "But...{w=1}umm...{w=1}I don't actually like candy corn."
        m 2hksdlb "Sorry, ahaha..."
        m 4eka "I do appreciate you trying to give me candy on Halloween, though."
        m 1hua "And if you could find a way to get some other candy for me, it'd make me really happy, [player]!"
    elif times_candy_given == 1:
        $ mas_loseAffection(5)
        m 2esc "Oh."
        m 2esc "More candy corn, [player]?"
        m 4esc "I already told you I don't really like candy corn."
        m 4ekc "So could you please try to find something else?"
        m 1eka "I don't get sweets that often anymore..."
        m 1ekbfa "Well...{w=1}besides you, [player]..."
        m 1hubfa "Ehehe~"
    elif times_candy_given == 2:
        $ mas_loseAffection(10)
        m 2wfw "[player]!"
        m 2tfc "I really tried not to be rude about this, but..."
        m 2tfc "I keep telling you I don't like candy corn and you just keep giving it to me anyway."
        m 2rfc "It's starting to feel like you're just trying to mess with me at this point."
        m 2tkc "So please, either find me some other kind of candy or just stop."
    else:
        $ mas_loseAffection(15)
        m 2tfc "..."
        python:
            store.mas_ptod.rst_cn()
            local_ctx = {
                "basedir": renpy.config.basedir
            }
        show monika at t22
        show screen mas_py_console_teaching

        call mas_wx_cmd ("import os", local_ctx, w_wait=1.0) from _call_mas_wx_cmd_92
        call mas_wx_cmd ("os.remove(os.path.normcase(basedir+'/characters/candycorn.gift'))", local_ctx, w_wait=1.0, x_wait=1.0) from _call_mas_wx_cmd_93
        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

    $ mas_receivedGift("mas_reaction_candycorn")
    $ gift_ev = mas_getEV("mas_reaction_candycorn")


    if not gift_ev:
        return

    $ store.mas_filereacts.delete_file(gift_ev.category)

    $ persistent._mas_filereacts_reacted_map.pop(gift_ev.category,None)
    return

init python:
    addReaction("mas_reaction_fudge", "fudge", is_good=True, exclude_on=["d25g"])

label mas_reaction_fudge:
    $ times_fudge_given = mas_getGiftStatsForDate("mas_reaction_fudge")

    if times_fudge_given == 0:
        $ mas_giftCapGainAff(2)
        m 3hua "Fudge!"
        m 3hub "I love fudge, thank you, [player]!"
        if seen_event("monika_date"):
            m "It's even chocolate, my favorite!"
        m 1hua "Thanks again, [player]~"

    elif times_fudge_given == 1:
        $ mas_giftCapGainAff(1)
        m 1wuo "...more fudge."
        m 1wub "Ooh, it's a different flavor this time..."
        m 3hua "Thank you, [player]!"
    else:

        m 1wuo "...even more fudge?"
        m 3rksdla "I still haven't finished the last batch you gave me, [player]..."
        m 3eksdla "...maybe later, okay?"

    $ mas_receivedGift("mas_reaction_fudge")
    $ gift_ev = mas_getEV("mas_reaction_fudge")
    $ store.mas_filereacts.delete_file(gift_ev.category)

    $ persistent._mas_filereacts_reacted_map.pop(gift_ev.category,None)
    return


init python:
    if store.mas_isD25Pre():
        addReaction("mas_reaction_christmascookies", "christmascookies", is_good=True, exclude_on=["d25g"])

label mas_reaction_christmascookies:
    $ times_cookies_given = mas_getGiftStatsForDate("mas_reaction_christmascookies")


    if times_cookies_given == 0 and not persistent._mas_d25_gifted_cookies:
        $ persistent._mas_d25_gifted_cookies = True
        $ mas_giftCapGainAff(3)
        m 3hua "Christmas cookies!"
        m 1eua "I just love Christmas cookies! They're always so sweet...and pretty to look at, too..."
        m "...cut into holiday shapes like snowmen, reindeer, and Christmas trees..."
        m 3eub "...and usually decorated with beautiful--{w=0.2}and delicious--{w=0.2}icing!"
        m 3hua "Thank you, [player]~"

    elif times_cookies_given == 1 or (times_cookies_given == 0 and persistent._mas_d25_gifted_cookies):
        m 1wuo "...another batch of Christmas cookies!"
        m 3wuo "That's a whole lot of cookies, [player]!"
        m 3rksdlb "I'm going to be eating cookies forever, ahaha!"
    else:

        m 3wuo "...even more Christmas cookies?"
        m 3rksdla "I still haven't finished the last batch, [player]!"
        m 3eksdla "You can give me more after I finish these, okay?"

    $ mas_receivedGift("mas_reaction_christmascookies")
    $ gift_ev = mas_getEV("mas_reaction_christmascookies")


    if not gift_ev:
        return

    $ store.mas_filereacts.delete_file(gift_ev.category)

    $ persistent._mas_filereacts_reacted_map.pop(gift_ev.category,None)
    return

init python:
    if store.mas_isD25Pre():
        addReaction("mas_reaction_candycane", "candycane", is_good=True, exclude_on=["d25g"])

label mas_reaction_candycane:
    $ times_cane_given = mas_getGiftStatsForDate("mas_reaction_candycane")
    $ mas_giftCapGainAff(1)

    if times_cane_given == 0:
        m 3eua "A candy cane!"
        if store.seen_event("monika_icecream"):
            m 1hub "You know how much I love mint!"
        else:
            m 1hub "I just love the flavor of mint!"
        m 1eua "Thanks, [player]."

    elif times_cane_given == 1:
        m 3hua "Another candy cane!"
        m 3hub "Thanks [player]!"
    else:

        m 1eksdla "[player], I think I have enough candy canes for now."
        m 1eka "You can save them for later, alright?"

    $ mas_receivedGift("mas_reaction_candycane")
    $ gift_ev = mas_getEV("mas_reaction_candycane")


    if not gift_ev:
        return

    $ store.mas_filereacts.delete_file(gift_ev.category)

    $ persistent._mas_filereacts_reacted_map.pop(gift_ev.category,None)
    return


init python:
    addReaction("mas_reaction_blackribbon", "blackribbon", is_good=True)

label mas_reaction_blackribbon:
    $ _mas_new_ribbon_color = "black"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_black
    call _mas_reaction_ribbon_helper ("mas_reaction_blackribbon") from _call__mas_reaction_ribbon_helper
    return

init python:
    addReaction("mas_reaction_blueribbon", "blueribbon", is_good=True)

label mas_reaction_blueribbon:
    $ _mas_new_ribbon_color = "blue"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_blue
    call _mas_reaction_ribbon_helper ("mas_reaction_blueribbon") from _call__mas_reaction_ribbon_helper_1
    return

init python:
    addReaction("mas_reaction_darkpurpleribbon", "darkpurpleribbon", is_good=True)

label mas_reaction_darkpurpleribbon:
    $ _mas_new_ribbon_color = "dark purple"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_darkpurple
    call _mas_reaction_ribbon_helper ("mas_reaction_darkpurpleribbon") from _call__mas_reaction_ribbon_helper_2
    return

init python:
    addReaction("mas_reaction_emeraldribbon", "emeraldribbon", is_good=True)

label mas_reaction_emeraldribbon:
    $ _mas_new_ribbon_color = "emerald"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_emerald
    call _mas_reaction_ribbon_helper ("mas_reaction_emeraldribbon") from _call__mas_reaction_ribbon_helper_3
    return

init python:
    addReaction("mas_reaction_grayribbon", "grayribbon", is_good=True)

label mas_reaction_grayribbon:
    $ _mas_new_ribbon_color = "gray"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_gray
    call _mas_reaction_ribbon_helper ("mas_reaction_grayribbon") from _call__mas_reaction_ribbon_helper_4
    return

init python:
    addReaction("mas_reaction_greenribbon", "greenribbon", is_good=True)

label mas_reaction_greenribbon:
    $ _mas_new_ribbon_color = "green"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_green
    call _mas_reaction_ribbon_helper ("mas_reaction_greenribbon") from _call__mas_reaction_ribbon_helper_5
    return

init python:
    addReaction("mas_reaction_lightpurpleribbon", "lightpurpleribbon", is_good=True)

label mas_reaction_lightpurpleribbon:
    $ _mas_new_ribbon_color = "light purple"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_lightpurple
    call _mas_reaction_ribbon_helper ("mas_reaction_lightpurpleribbon") from _call__mas_reaction_ribbon_helper_6
    return

init python:
    addReaction("mas_reaction_peachribbon", "peachribbon", is_good=True)

label mas_reaction_peachribbon:
    $ _mas_new_ribbon_color = "peach"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_peach
    call _mas_reaction_ribbon_helper ("mas_reaction_peachribbon") from _call__mas_reaction_ribbon_helper_7
    return

init python:
    addReaction("mas_reaction_pinkribbon", "pinkribbon", is_good=True)

label mas_reaction_pinkribbon:
    $ _mas_new_ribbon_color = "pink"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_pink
    call _mas_reaction_ribbon_helper ("mas_reaction_pinkribbon") from _call__mas_reaction_ribbon_helper_8
    return

init python:
    addReaction("mas_reaction_platinumribbon", "platinumribbon", is_good=True)

label mas_reaction_platinumribbon:
    $ _mas_new_ribbon_color = "platinum"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_platinum
    call _mas_reaction_ribbon_helper ("mas_reaction_platinumribbon") from _call__mas_reaction_ribbon_helper_9
    return

init python:
    addReaction("mas_reaction_redribbon", "redribbon", is_good=True)

label mas_reaction_redribbon:
    $ _mas_new_ribbon_color = "red"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_red
    call _mas_reaction_ribbon_helper ("mas_reaction_redribbon") from _call__mas_reaction_ribbon_helper_10
    return

init python:
    addReaction("mas_reaction_rubyribbon", "rubyribbon", is_good=True)

label mas_reaction_rubyribbon:
    $ _mas_new_ribbon_color = "ruby"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_ruby
    call _mas_reaction_ribbon_helper ("mas_reaction_rubyribbon") from _call__mas_reaction_ribbon_helper_11
    return

init python:
    addReaction("mas_reaction_sapphireribbon", "sapphireribbon", is_good=True)

label mas_reaction_sapphireribbon:
    $ _mas_new_ribbon_color = "sapphire"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_sapphire
    call _mas_reaction_ribbon_helper ("mas_reaction_sapphireribbon") from _call__mas_reaction_ribbon_helper_12
    return

init python:
    addReaction("mas_reaction_silverribbon", "silverribbon", is_good=True)

label mas_reaction_silverribbon:
    $ _mas_new_ribbon_color = "silver"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_silver
    call _mas_reaction_ribbon_helper ("mas_reaction_silverribbon") from _call__mas_reaction_ribbon_helper_13
    return

init python:
    addReaction("mas_reaction_tealribbon", "tealribbon", is_good=True)

label mas_reaction_tealribbon:
    $ _mas_new_ribbon_color = "teal"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_teal
    call _mas_reaction_ribbon_helper ("mas_reaction_tealribbon") from _call__mas_reaction_ribbon_helper_14
    return

init python:
    addReaction("mas_reaction_yellowribbon", "yellowribbon", is_good=True)

label mas_reaction_yellowribbon:
    $ _mas_new_ribbon_color = "yellow"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_yellow
    call _mas_reaction_ribbon_helper ("mas_reaction_yellowribbon") from _call__mas_reaction_ribbon_helper_15
    return


label mas_reaction_json_ribbon_base(ribbon_name, user_friendly_desc, helper_label):
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_ACS, ribbon_name)
        )
        _mas_gifted_ribbon_acs = mas_sprites.ACS_MAP.get(
            ribbon_name,
            mas_acs_ribbon_def
        )
        _mas_new_ribbon_color = user_friendly_desc

    call _mas_reaction_ribbon_helper (helper_label) from _call__mas_reaction_ribbon_helper_16

    python:

        if sprite_data[2] is not None:
            store.mas_filereacts.delete_file(sprite_data[2])

        mas_finishSpriteObjInfo(sprite_data)
    return



label mas_reaction_gift_acs_lanvallime_ribbon_coffee:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_coffee", "coffee colored", "mas_reaction_gift_acs_lanvallime_ribbon_coffee") from _call_mas_reaction_json_ribbon_base
    return

label mas_reaction_gift_acs_lanvallime_ribbon_gold:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_gold", "gold", "mas_reaction_gift_acs_lanvallime_ribbon_gold") from _call_mas_reaction_json_ribbon_base_1
    return

label mas_reaction_gift_acs_lanvallime_ribbon_hot_pink:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_hot_pink", "hot pink", "mas_reaction_gift_acs_lanvallime_ribbon_hot_pink") from _call_mas_reaction_json_ribbon_base_2
    return

label mas_reaction_gift_acs_lanvallime_ribbon_lilac:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_lilac", "lilac", "mas_reaction_gift_acs_lanvallime_ribbon_lilac") from _call_mas_reaction_json_ribbon_base_3
    return

label mas_reaction_gift_acs_lanvallime_ribbon_lime_green:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_lime_green", "lime green", "mas_reaction_gift_acs_lanvallime_lime_green") from _call_mas_reaction_json_ribbon_base_4
    return

label mas_reaction_gift_acs_lanvallime_ribbon_navy_blue:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_navy_blue", "navy", "mas_reaction_gift_acs_lanvallime_ribbon_navy_blue") from _call_mas_reaction_json_ribbon_base_5
    return

label mas_reaction_gift_acs_lanvallime_ribbon_orange:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_orange", "orange", "mas_reaction_gift_acs_lanvallime_ribbon_orange") from _call_mas_reaction_json_ribbon_base_6
    return

label mas_reaction_gift_acs_lanvallime_ribbon_royal_purple:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_royal_purple", "royal purple", "mas_reaction_gift_acs_lanvallime_ribbon_royal_purple") from _call_mas_reaction_json_ribbon_base_7
    return

label mas_reaction_gift_acs_lanvallime_ribbon_sky_blue:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_sky_blue", "sky blue", "mas_reaction_gift_acs_lanvallime_ribbon_sky_blue") from _call_mas_reaction_json_ribbon_base_8
    return


label mas_reaction_gift_acs_anonymioo_ribbon_bisexualpride:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_bisexualpride", "bisexual-pride-themed", "mas_reaction_gift_acs_anonymioo_ribbon_bisexualpride") from _call_mas_reaction_json_ribbon_base_9
    return

label mas_reaction_gift_acs_anonymioo_ribbon_blackandwhite:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_blackandwhite", "black and white", "mas_reaction_gift_acs_anonymioo_ribbon_blackandwhite") from _call_mas_reaction_json_ribbon_base_10
    return

label mas_reaction_gift_acs_anonymioo_ribbon_bronze:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_bronze", "bronze", "mas_reaction_gift_acs_anonymioo_ribbon_bronze") from _call_mas_reaction_json_ribbon_base_11
    return

label mas_reaction_gift_acs_anonymioo_ribbon_brown:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_brown", "brown", "mas_reaction_gift_acs_anonymioo_ribbon_brown") from _call_mas_reaction_json_ribbon_base_12
    return

label mas_reaction_gift_acs_anonymioo_ribbon_gradient:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_gradient", "multi-colored", "mas_reaction_gift_acs_anonymioo_ribbon_gradient") from _call_mas_reaction_json_ribbon_base_13
    return

label mas_reaction_gift_acs_anonymioo_ribbon_gradient_lowpoly:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_gradient_lowpoly", "multi-colored", "mas_reaction_gift_acs_anonymioo_ribbon_gradient_lowpoly") from _call_mas_reaction_json_ribbon_base_14
    return

label mas_reaction_gift_acs_anonymioo_ribbon_gradient_rainbow:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_gradient_rainbow", "rainbow colored", "mas_reaction_gift_acs_anonymioo_ribbon_gradient_rainbow") from _call_mas_reaction_json_ribbon_base_15
    return

label mas_reaction_gift_acs_anonymioo_ribbon_polkadots_whiteonred:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_polkadots_whiteonred", "red and white polka dotted", "mas_reaction_gift_acs_anonymioo_ribbon_polkadots_whiteonred") from _call_mas_reaction_json_ribbon_base_16
    return

label mas_reaction_gift_acs_anonymioo_ribbon_starsky_black:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_starsky_black", "night-sky-themed", "mas_reaction_gift_acs_anonymioo_ribbon_starsky_black") from _call_mas_reaction_json_ribbon_base_17
    return

label mas_reaction_gift_acs_anonymioo_ribbon_starsky_red:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_starsky_red", "night-sky-themed", "mas_reaction_gift_acs_anonymioo_ribbon_starsky_red") from _call_mas_reaction_json_ribbon_base_18
    return

label mas_reaction_gift_acs_anonymioo_ribbon_striped_blueandwhite:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_striped_blueandwhite", "blue and white striped", "mas_reaction_gift_acs_anonymioo_ribbon_striped_blueandwhite") from _call_mas_reaction_json_ribbon_base_19
    return

label mas_reaction_gift_acs_anonymioo_ribbon_striped_pinkandwhite:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_striped_pinkandwhite", "pink and white striped", "mas_reaction_gift_acs_anonymioo_ribbon_striped_pinkandwhite") from _call_mas_reaction_json_ribbon_base_20
    return

label mas_reaction_gift_acs_anonymioo_ribbon_transexualpride:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_transexualpride", "transexual-pride-themed", "mas_reaction_gift_acs_anonymioo_ribbon_transexualpride") from _call_mas_reaction_json_ribbon_base_21
    return



label mas_reaction_gift_acs_velius94_ribbon_platinum:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_platinum", "platinum", "mas_reaction_gift_acs_velius94_ribbon_platinum") from _call_mas_reaction_json_ribbon_base_22
    return

label mas_reaction_gift_acs_velius94_ribbon_pink:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_pink", "pink", "mas_reaction_gift_acs_velius94_ribbon_pink") from _call_mas_reaction_json_ribbon_base_23
    return

label mas_reaction_gift_acs_velius94_ribbon_peach:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_peach", "peach", "mas_reaction_gift_acs_velius94_ribbon_peach") from _call_mas_reaction_json_ribbon_base_24
    return

label mas_reaction_gift_acs_velius94_ribbon_green:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_green", "green", "mas_reaction_gift_acs_velius94_ribbon_green") from _call_mas_reaction_json_ribbon_base_25
    return

label mas_reaction_gift_acs_velius94_ribbon_emerald:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_emerald", "emerald", "mas_reaction_gift_acs_velius94_ribbon_emerald") from _call_mas_reaction_json_ribbon_base_26
    return

label mas_reaction_gift_acs_velius94_ribbon_gray:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_gray", "gray", "mas_reaction_gift_acs_velius94_ribbon_gray") from _call_mas_reaction_json_ribbon_base_27
    return

label mas_reaction_gift_acs_velius94_ribbon_blue:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_blue", "blue", "mas_reaction_gift_acs_velius94_ribbon_blue") from _call_mas_reaction_json_ribbon_base_28
    return

label mas_reaction_gift_acs_velius94_ribbon_def:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_def", "white", "mas_reaction_gift_acs_velius94_ribbon_def") from _call_mas_reaction_json_ribbon_base_29
    return

label mas_reaction_gift_acs_velius94_ribbon_black:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_black", "black", "mas_reaction_gift_acs_velius94_ribbon_black") from _call_mas_reaction_json_ribbon_base_30
    return

label mas_reaction_gift_acs_velius94_ribbon_dark_purple:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_dark_purple", "dark purple", "mas_reaction_gift_acs_velius94_ribbon_dark_purple") from _call_mas_reaction_json_ribbon_base_31
    return

label mas_reaction_gift_acs_velius94_ribbon_yellow:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_yellow", "yellow", "mas_reaction_gift_acs_velius94_ribbon_yellow") from _call_mas_reaction_json_ribbon_base_32
    return

label mas_reaction_gift_acs_velius94_ribbon_red:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_red", "red", "mas_reaction_gift_acs_velius94_ribbon_red") from _call_mas_reaction_json_ribbon_base_33
    return

label mas_reaction_gift_acs_velius94_ribbon_sapphire:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_sapphire", "sapphire", "mas_reaction_gift_acs_velius94_ribbon_sapphire") from _call_mas_reaction_json_ribbon_base_34
    return

label mas_reaction_gift_acs_velius94_ribbon_teal:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_teal", "teal", "mas_reaction_gift_acs_velius94_ribbon_teal") from _call_mas_reaction_json_ribbon_base_35
    return

label mas_reaction_gift_acs_velius94_ribbon_silver:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_silver", "silver", "mas_reaction_gift_acs_velius94_ribbon_silver") from _call_mas_reaction_json_ribbon_base_36
    return

label mas_reaction_gift_acs_velius94_ribbon_light_purple:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_light_purple", "light purple", "mas_reaction_gift_acs_velius94_ribbon_light_purple") from _call_mas_reaction_json_ribbon_base_37
    return

label mas_reaction_gift_acs_velius94_ribbon_ruby:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_ruby", "ruby", "mas_reaction_gift_acs_velius94_ribbon_ruby") from _call_mas_reaction_json_ribbon_base_38
    return

label mas_reaction_gift_acs_velius94_ribbon_wine:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_wine", "wine colored", "mas_reaction_gift_acs_velius94_ribbon_wine") from _call_mas_reaction_json_ribbon_base_39
    return


default -5 persistent._mas_current_gifted_ribbons = 0

label _mas_reaction_ribbon_helper(label):

    if store.mas_selspr.get_sel_acs(_mas_gifted_ribbon_acs).unlocked:
        call mas_reaction_old_ribbon from _call_mas_reaction_old_ribbon
    else:


        call mas_reaction_new_ribbon from _call_mas_reaction_new_ribbon
        $ persistent._mas_current_gifted_ribbons += 1


    $ mas_receivedGift(label)
    $ gift_ev = mas_getEV(label)
    if gift_ev:

        $ store.mas_filereacts.delete_file(gift_ev.category)

        $ persistent._mas_filereacts_reacted_map.pop(gift_ev.category,None)

    return

label mas_reaction_new_ribbon:
    python:
        def _ribbon_prepare_hair():
            
            if not monika_chr.hair.hasprop("ribbon"):
                monika_chr.change_hair(mas_hair_def, False)

    $ mas_giftCapGainAff(3)
    if persistent._mas_current_gifted_ribbons == 0:
        m 1suo "A new ribbon!"
        m 3hub "...And it's [_mas_new_ribbon_color]!"


        if _mas_new_ribbon_color == "green" or _mas_new_ribbon_color == "emerald":
            m 1tub "...Just like my eyes!"

        m 1hub "Thank you so much [player], I love it!"
        if store.seen_event("monika_date"):
            m 3eka "Did you get this for me because I mentioned how I love shopping for skirts and bows?"

            if mas_isMoniNormal(higher=True):
                m 3hua "You're always so thoughtful~"

        m 3rksdlc "I really don't have a lot of choices here when it comes to fashion..."
        m 3eka "...so being able to change my ribbon color is such a nice change of pace."
        m 2dsa "In fact, I'll put it on right now.{w=0.5}.{w=0.5}.{nw}"
        $ store.mas_selspr.unlock_acs(_mas_gifted_ribbon_acs)
        $ _ribbon_prepare_hair()
        $ monika_chr.wear_acs(_mas_gifted_ribbon_acs)
        m 1hua "Oh it's wonderful, [player]!"

        if mas_isMoniAff(higher=True):
            m 1eka "You always make me feel so loved..."
        elif mas_isMoniHappy():
            m 1eka "You always know how to make me happy..."
        m 3hua "Thanks again~"
    else:

        m 1suo "Another ribbon!"
        m 3hub "...And this time it's [_mas_new_ribbon_color]!"


        if _mas_new_ribbon_color == "green" or _mas_new_ribbon_color == "emerald":
            m 1tub "...Just like my eyes!"

        m 2dsa "I'll put this on right now.{w=0.5}.{w=0.5}.{nw}"
        $ store.mas_selspr.unlock_acs(_mas_gifted_ribbon_acs)
        $ _ribbon_prepare_hair()
        $ monika_chr.wear_acs(_mas_gifted_ribbon_acs)
        m 3hua "Thank you so much [player], I just love it!"
    return

label mas_reaction_old_ribbon:
    m 1rksdlb "[player]..."

    show monika 1rusdlb
    $ renpy.say(m, "You already gave me {0} ribbon!".format(mas_a_an_str(_mas_new_ribbon_color)))
    return

init python:
    addReaction("mas_reaction_gift_roses", "roses", is_good=True, exclude_on=["d25g"])

default -5 persistent._date_last_given_roses = None

label mas_reaction_gift_roses:
    python:
        gift_ev = mas_getEV("mas_reaction_gift_roses")

        monika_chr.wear_acs(mas_acs_roses)


    if not persistent._date_last_given_roses and not renpy.seen_label('monika_valentines_start'):
        $ mas_giftCapGainAff(10)

        m 1eka "[player]... I-I don't know what to say..."
        m 1ekbsb "I never would've thought that you'd get something like this for me!"
        m 3skbsa "I'm so happy right now."
        if mas_isF14():

            $ mas_f14CapGainAff(5)
            m 3ekbsa "To think that I'd be getting roses from you on Valentine's Day..."
            m 1ekbsu "You're so sweet."
            m 1dktpu "..."
            m 1ektda "Ahaha..."


        if not monika_chr.is_wearing_clothes_with_exprop("baked outfit"):
            m 2dsa "Hold on.{w=0.5}.{w=0.5}.{nw}"
            $ monika_chr.wear_acs(mas_acs_ear_rose)
            m 1hub "Ehehe, there! Doesn't it look pretty on me?"

        if mas_shouldKiss(chance=2, special_day_bypass=True):
            call monika_kissing_motion_short from _call_monika_kissing_motion_short_3
    else:

        if persistent._date_last_given_roses is None and renpy.seen_label('monika_valentines_start'):
            $ persistent._date_last_given_roses = datetime.date(2018,2,14)

        if mas_pastOneDay(persistent._date_last_given_roses):
            $ mas_giftCapGainAff(5 if mas_isSpecialDay() else 1)

            m 1suo "Oh!"
            m 1ekbsa "Thanks, [player]."
            m 3ekbsa "I always love getting roses from you."
            if mas_isF14():

                $ mas_f14CapGainAff(5)
                m 1dsbsu "Especially on a day like today."
                m 1ekbsa "It's really sweet of you to get these for me."
                m 3hkbsa "I love you so much."
                m 1ekbsa "Happy Valentine's Day, [player]~"
            else:
                m 1ekbsa "You're always so sweet."


            if (mas_isSpecialDay() and renpy.random.randint(1,2) == 1) or (renpy.random.randint(1,4) == 1) or mas_isF14():
                if not monika_chr.is_wearing_clothes_with_exprop("baked outfit"):
                    m 2dsa "Hold on.{w=0.5}.{w=0.5}.{nw}"
                    $ monika_chr.wear_acs(mas_acs_ear_rose)
                    m 1hub "Ehehe~"

            if mas_shouldKiss(chance=4, special_day_bypass=True):
                call monika_kissing_motion_short from _call_monika_kissing_motion_short_4
        else:

            m 1hksdla "[player], I'm flattered, really, but you don't need to give me so many roses."
            if store.seen_event("monika_clones"):
                m 1ekbsa "You'll always be my special rose after all, ehehe~"
            else:
                m 1ekbsa "A single rose from you is already more than I could have ever asked for."


    $ persistent._mas_filereacts_reacted_map.pop(gift_ev.category,None)
    $ persistent._date_last_given_roses = datetime.date.today()


    $ mas_receivedGift("mas_reaction_gift_roses")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return


init python:
    addReaction("mas_reaction_gift_chocolates", "chocolates", is_good=True, exclude_on=["d25g"])

default -5 persistent._given_chocolates_before = False

label mas_reaction_gift_chocolates:
    $ gift_ev = mas_getEV("mas_reaction_gift_chocolates")

    if not persistent._mas_given_chocolates_before:
        $ persistent._mas_given_chocolates_before = True


        if not MASConsumable._getCurrentFood():
            $ monika_chr.wear_acs(mas_acs_heartchoc)

        $ mas_giftCapGainAff(5)

        m 1tsu "That's so {i}sweet{/i} of you, ehehe~"
        if mas_isF14():

            $ mas_f14CapGainAff(5)
            m 1ekbsa "Giving me chocolates on Valentine's Day..."
            m 1ekbfa "You really know how to make a girl feel special, [player]."
            if renpy.seen_label('monika_date'):
                m 1lkbfa "I know I mentioned visiting a chocolate store together someday..."
                m 1hkbfa "But while we can't really do that just yet, getting some chocolates as a gift from you, well..."
            m 3ekbfa "It means a lot getting these from you."

        elif renpy.seen_label('monika_date'):
            m 3rka "I know I mentioned visiting a chocolate store together someday..."
            m 3hub "But while we can't really do that just yet, getting some chocolates as a gift from you means everything to me."
            m 1ekc "I really wish we could share them though..."
            m 3rksdlb "But until that day comes, I'll just have to enjoy them for both of us, ahaha!"
            m 3hua "Thank you, [player]~"
        else:

            m 3hub "I love chocolates!"
            m 1eka "And getting some from you means a lot to me."
            m 1hub "Thanks, [player]!"
    else:

        $ times_chocs_given = mas_getGiftStatsForDate("mas_reaction_gift_chocolates")
        if times_chocs_given == 0:


            if not MASConsumable._getCurrentFood():

                if not (mas_isF14() or mas_isD25Season()):
                    if monika_chr.is_wearing_acs(mas_acs_quetzalplushie):
                        $ monika_chr.wear_acs(mas_acs_center_quetzalplushie)
                else:

                    $ monika_chr.remove_acs(store.mas_acs_quetzalplushie)

                $ monika_chr.wear_acs(mas_acs_heartchoc)

            $ mas_giftCapGainAff(3 if mas_isSpecialDay() else 1)

            m 1wuo "Oh!"

            if mas_isF14():

                $ mas_f14CapGainAff(5)
                m 1eka "[player]!"
                m 1ekbsa "You're such a sweetheart, getting me chocolates on a day like today..."
                m 1ekbfa "You really know how to make me feel special."
                m "Thanks, [player]."
            else:
                m 1hua "Thanks for the chocolates, [player]!"
                m 1ekbsa "Every bite reminds me of how sweet you are, ehehe~"

        elif times_chocs_given == 1:

            if not MASConsumable._getCurrentFood():
                $ monika_chr.wear_acs(mas_acs_heartchoc)

            m 1eka "More chocolates, [player]?"
            m 3tku "You really love to spoil me don't you, ahaha!"
            m 1rksdla "I still haven't finished the first box you gave me..."
            m 1hub "...but I'm not complaining!"

        elif times_chocs_given == 2:
            m 1ekd "[player]..."
            m 3eka "I think you've given me enough chocolates today."
            m 1rksdlb "Three boxes is too much, and I haven't even finished the first one yet!"
            m 1eka "Save them for another time, okay?"
        else:

            m 2tfd "[player]!"
            m 2tkc "I already told you I've had enough chocolates for one day, but you keep trying to give me even more..."
            m 2eksdla "Please...{w=1}just save them for another day."


    if monika_chr.is_wearing_acs(mas_acs_heartchoc):
        call mas_remove_choc from _call_mas_remove_choc


    $ persistent._mas_filereacts_reacted_map.pop(gift_ev.category,None)

    $ mas_receivedGift("mas_reaction_gift_chocolates")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return

label mas_remove_choc:

    m 1hua "..."
    m 3eub "These are {i}so{/i} good!"
    m 1hua "..."
    m 3hksdlb "Ahaha! I should probably put these away for now..."
    m 1rksdla "If I leave them here much longer there won't be any left to enjoy later!"

    call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_10

    python:
        renpy.pause(1, hard=True)
        monika_chr.remove_acs(mas_acs_heartchoc)
        renpy.pause(3, hard=True)

    call mas_transition_from_emptydesk ("monika 1eua") from _call_mas_transition_from_emptydesk_18


    if monika_chr.is_wearing_acs(mas_acs_center_quetzalplushie):
        $ monika_chr.wear_acs(mas_acs_quetzalplushie)

    m 1eua "So what else did you want to do today?"
    return

label mas_reaction_gift_clothes_orcaramelo_bikini_shell:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "orcaramelo_bikini_shell")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sua "Oh! {w=0.5}A seashell bikini!"
    m 1hub "Thank you, [player]!{w=0.5} I'm going to try it on right now!"


    call mas_clothes_change (sprite_object) from _call_mas_clothes_change_7

    m 2ekbfa "Well...{w=0.5} What do you think?"
    m 2hubfa "Do I look like a mermaid? Ehehe."
    show monika 5ekbfa zorder MAS_MONIKA_Z at i11 with dissolve
    m 5ekbfa "I think it's really cute, [player]..."
    m 5hubfa "We'll have to go to the beach sometime!"

    if mas_isWinter() or mas_isMoniNormal(lower=True):
        if mas_isWinter():
            show monika 2rksdla zorder MAS_MONIKA_Z at i11 with dissolve
            m 2rksdla "...But for now, it's a little chilly in here..."
            m 2eka "So I'm going to go put on something a little warmer..."

        elif mas_isMoniNormal(lower=True):
            show monika 2hksdlb zorder MAS_MONIKA_Z at i11 with dissolve
            m 2hksdlb "Ahaha..."
            m 2rksdla "It's a little embarrassing just sitting here like this in front of you."
            m 2eka "I hope you don't mind, but I'm going to go change..."


        $ clothes = mas_clothes_def
        if persistent._mas_d25_in_d25_mode and mas_isD25Outfit():
            $ clothes = mas_clothes_santa
        call mas_clothes_change (clothes) from _call_mas_clothes_change_8

        m 2eua "Ah, that's better..."
        m 3hua "Thanks again for the wonderful gift~"


    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_acs_orcaramelo_hairflower_pink:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_ACS, "orcaramelo_hairflower_pink")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(1)

    m 3sua "Oh!{w=0.5} What a cute little flower!"
    m 1ekbsa "Thanks [player], you're so sweet~"
    m 1dua "Hold on.{w=0.5}.{w=0.5}.{nw}"
    $ monika_chr.wear_acs(sprite_object)
    m 1hua "Ehehe~"
    m 1hub "Thanks again, [player]!"

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_velius94_shirt_pink:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "velius94_shirt_pink")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1suo "Oh my gosh!"
    m 1suo "It's {i}so{/i} pretty!"
    m 3hub "Thank you so much, [player]!"
    m 3eua "Hold on, let me try it on real quick..."


    call mas_clothes_change (sprite_object) from _call_mas_clothes_change_9

    m 2sub "Ahh, it's a perfect fit!"
    m 3hub "I really like the colors, too! Pink and black go so well together."
    m 3eub "Not to mention the skirt looks really cute with those frills!"
    m 2tfbsd "Yet for some reason I can't help but feel that your eyes are kind of drifting...{w=0.5}ahem...{w=0.5}{i}elsewhere{/i}."

    if mas_selspr.get_sel_clothes(mas_clothes_sundress_white).unlocked:
        m 2lfbsp "I told you it's not polite to stare, [player]."
    else:
        m 2lfbsp "It's not polite to stare, you know?"

    m 2hubsb "Ahaha!"
    m 2tkbsu "Relax, relax...{w=0.5}just teasing you~"
    m 3hub "Once again, thank you so much for this outfit, [player]!"

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_orcaramelo_sakuya_izayoi:

    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "orcaramelo_sakuya_izayoi")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sub "Oh! {w=0.5}Is this..."
    m 2euc "A maid outfit?"
    m 3tuu "Ehehe~"
    m 3tubsb "You know, if you liked this kind of thing, you could have just told me..."
    m 1hub "Ahaha! Just kidding~"
    m 1eub "Let me go put it on!"


    call mas_clothes_change (sprite_object, outfit_mode=True) from _call_mas_clothes_change_10

    m 2hua "So,{w=0.5} how do I look?"
    m 3eub "I almost feel like I could get anything done before you could even blink."
    m 1eua "...So long as you don't keep me too busy, ehehe~"
    m 1lkbfb "I'd still like to be able to spend time with you, maste--{nw}"
    $ _history_list.pop()
    m 1ekbfb "I'd still like to be able to spend time with you,{fast} [player]."

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_finale_jacket_brown:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "finale_jacket_brown")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sub "Oh!{w=0.5} A winter jacket!"
    m 1suo "And it even comes with a scarf!"
    if mas_isSummer():
        m 3rksdla "...Though I'm getting a little hot just by looking at it, ahaha..."
        m 3eksdla "Perhaps summer isn't the best time to wear this, [player]."
        m 3eka "I do appreciate the thought, and I'll be glad to wear it in a few months."
    else:

        if mas_isWinter():
            m 1tuu "I won't be getting cold anytime soon because of you, [player]~"
        m 3eub "Let me go put it on! I'll be right back."


        call mas_clothes_change (sprite_object) from _call_mas_clothes_change_11

        m 2dku "Ahh, it feels very nice~"
        m 1eua "I like the way it looks on me, don't you agree?"
        if mas_isMoniNormal(higher=True):
            m 3tku "Well... I can't really expect you to be objective about that question, can I?"
            m 1hubfb "Ahaha!"
        m 1ekbfa "Thank you [player], I love it."

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_orcaramelo_sweater_shoulderless:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "orcaramelo_sweater_shoulderless")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sub "Oh!{w=0.5} A sweater!"
    m 1hub "And it looks so cozy, too!"
    if mas_isWinter():
        m 2eka "You're so thoughtful [player], giving this to me on such a cold winter day..."
    m 3eua "Let me go try it on."


    call mas_clothes_change (sprite_object) from _call_mas_clothes_change_12

    m 2dkbsu "It's so...{w=1}comfy. I feel as snug as a bug in a rug. Ehehe~"
    m 1ekbsa "Thank you, [player]. I love it!"
    m 3hubsa "Now whenever I wear it I'll think of your warmth. Ahaha~"

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_velius94_dress_whitenavyblue:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "velius94_dress_whitenavyblue")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1suo "Oh my gosh!"
    m 1sub "This dress is gorgeous, [player]!"
    m 3hub "I'm going to try it on right now!"


    call mas_clothes_change (sprite_object, outfit_mode=True) from _call_mas_clothes_change_13

    m "So,{w=0.5} what do you think?"
    m 3eua "I think this shade of blue goes really well with the white."
    $ scrunchie = monika_chr.get_acs_of_type('bunny-scrunchie')

    if scrunchie and scrunchie.name == "velius94_bunnyscrunchie_blue":
        m 3eub "And the bunny scrunchie complements the outfit nicely too!"
    m 1eka "Thank you so much, [player]."

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
