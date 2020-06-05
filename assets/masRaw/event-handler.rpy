






image monika_waiting_img:
    "monika 1eua"
    1.0
    "monika 1euc"
    1.0
    "monika 1esc"
    1.0
    "monika 1lksdlc"
    1.0
    "monika 1ekd"
    1.0
    repeat


transform prompt_monika:
    tcommon(950,z=0.8)


init -999 python in mas_ev_data_ver:



    import __builtin__


    import datetime



    def _verify_bool(val, allow_none=True):
        return _verify_item(val, bool, allow_none)


    def _verify_dict(val, allow_none=True):
        return _verify_item(val, __builtin__.dict, allow_none)


    def _verify_list(val, allow_none=True):
        return _verify_item(val, __builtin__.list, allow_none)


    def _verify_dt(val, allow_none=True):
        if (
                isinstance(val, datetime.datetime)
                and val.year < 1900
            ):
            return False
        return _verify_item(val, datetime.datetime, allow_none)


    def _verify_dt_nn(val):
        return _verify_dt(val, False)


    def _verify_evact(val, allow_none=True):
        if val is None:
            return allow_none
        
        return val in store.EV_ACTIONS


    def _verify_int(val, allow_none=True):
        return _verify_item(val, int, allow_none)


    def _verify_int_nn(val):
        return _verify_int(val, False)


    def _verify_str(val, allow_none=True):
        if val is None:
            return allow_none
        
        return isinstance(val, str) or isinstance(val, unicode)


    def _verify_td(val, allow_none=True):
        if val is None:
            return allow_none
        return _verify_item(val, datetime.timedelta, allow_none)


    def _verify_td_nn(val):
        return _verify_td(val, False)


    def _verify_tuli(val, allow_none=True):
        if val is None:
            return allow_none
        
        return isinstance(val, __builtin__.list) or isinstance(val, tuple)


    def _verify_tuli_aff(val, allow_none=True):
        if val is None:
            return allow_none
        
        return isinstance(val, tuple) and len(val) == 2


    def _verify_item(val, _type, allow_none=True):
        """
        Verifies the given value has the given type/instance

        IN:
            val - value to verify
            _type - type to check
            allow_none - If True, None should be considered good value,
                false means bad value
                (Default: True)

        RETURNS: True if the given value has the given type/instance,
            false otherwise
        """
        if val is None:
            return allow_none
        
        
        return isinstance(val, _type)


    class MASCurriedVerify(object):
        """
        Allows for currying of a verification function
        """
        
        def __init__(self, verifier, allow_none):
            """
            Constructor

            IN:
                verifier - the verification function we want to use
                allow_none - True if we should pass True for allow_none,
                    false for False
            """
            self.verifier = verifier
            self.allow_none = allow_none
        
        
        def __call__(self, value):
            """
            Callable override

            IN:
                value - the value we want to verify

            RETURNS: True if the value passes verification, False otherwise
            """
            return self.verifier(value, self.allow_none)


init -950 python in mas_ev_data_ver:
    import store


    _verify_map = {
        0: MASCurriedVerify(_verify_str, False), 
        1: MASCurriedVerify(_verify_str, True), 
        2: MASCurriedVerify(_verify_str, True), 
        

        4: MASCurriedVerify(_verify_bool, True), 
        5: MASCurriedVerify(_verify_bool, True), 
        6: MASCurriedVerify(_verify_bool, True), 
        7: MASCurriedVerify(_verify_str, True), 
        8: MASCurriedVerify(_verify_evact, True), 
        9: MASCurriedVerify(_verify_dt, True), 
        10: MASCurriedVerify(_verify_dt, True), 
        11: MASCurriedVerify(_verify_dt, True), 
        12: MASCurriedVerify(_verify_int, False), 
        
        14: MASCurriedVerify(_verify_dt, True), 
        15: MASCurriedVerify(_verify_tuli, True), 
        16: MASCurriedVerify(_verify_bool, True), 
        17: MASCurriedVerify(_verify_tuli_aff, True), 
        18: MASCurriedVerify(_verify_bool, True), 
    }


    def _verify_data_line(ev_line):
        """
        Verifies event data for a single tuple of data.

        IN:
            ev_line - single line of data to verify

        RETURNS:
            True if passed verification, False if not
        """
        
        for index in range(len(ev_line)):
            
            verify = _verify_map.get(index, None)
            if verify is not None and not verify(ev_line[index]):
                
                return False
        
        return True


    def verify_event_data(per_db):
        """
        Verifies event data of the given persistent data. Entries that are
        invalid are removed. We only check the bits of data that we have, so
        data lines with smaller sizes are only validated for what they have.

        IN:
            per_db - persistent database to verify
        """
        if per_db is None:
            return
        
        for ev_label in per_db.keys():
            
            ev_line = per_db[ev_label]
            
            if not _verify_data_line(ev_line):
                
                store.mas_utils.writelog(
                    "bad data found in {0}\n".format(ev_label)
                )
                per_db.pop(ev_label)


init -895 python in mas_ev_data_ver:



    for _dm_db in store._mas_dm_dm.per_dbs:
        verify_event_data(_dm_db)

    _dm_db = None









init -500 python:





    mas_init_lockdb_template = (
        True, 
        False, 
        False, 
        False, 
        True, 
        True, 
        True, 
        True, 
        True, 
        True, 
        True, 
        True, 
        True, 
        False, 
        True, 
        False, 
        False, 
        False, 
        False, 
    )













    if persistent._mas_event_init_lockdb is None:
        persistent._mas_event_init_lockdb = dict()

    for ev_key in persistent._mas_event_init_lockdb:
        stored_lock_row = persistent._mas_event_init_lockdb[ev_key]
        
        if len(mas_init_lockdb_template) != len(stored_lock_row):
            
            lock_row = list(mas_init_lockdb_template)
            lock_row[0:len(stored_lock_row)] = list(stored_lock_row)
            persistent._mas_event_init_lockdb[ev_key] = tuple(lock_row)


    persistent._mas_event_init_lockdb_template = mas_init_lockdb_template






    Event.INIT_LOCKDB = persistent._mas_event_init_lockdb



init 4 python:











    mas_all_ev_db_map = {
        "EVE": store.evhand.event_database,
        "BYE": store.evhand.farewell_database,
        "GRE": store.evhand.greeting_database,
        "MOO": store.mas_moods.mood_db,
        "STY": store.mas_stories.story_database,
        "CMP": store.mas_compliments.compliment_database,
        "FLR": store.mas_filereacts.filereact_db,
        "APL": store.mas_apology.apology_db,
        "WRS": store.mas_windowreacts.windowreact_db,
        "FFF": store.mas_fun_facts.fun_fact_db,
        "SNG": store.mas_songs.song_db,
        "GME": store.mas_games.game_db
    }


init 6 python:




    mas_all_ev_db = {}
    for code,ev_db in mas_all_ev_db_map.iteritems():
        mas_all_ev_db.update(ev_db)

    del code, ev_db

    def mas_getEV(ev_label):
        """
        Global get function that retreives an event given the label

        Designed to be used as a wrapper around the mas_all_ev_db dict
        NOTE: only available at RUNTIME

        IN:
            ev_label - eventlabel to find event for

        RETURNS:
            the event object you were looking for, or None if not found
        """
        return mas_all_ev_db.get(ev_label, None)


    def mas_getEVCL(ev_label):
        """
        Global get function that retrieves the calendar label for an event
        given the eventlabel. This is mainly to help with calendar.

        IN:
            ev_label - eventlabel to find calendar label for

        RETURNS:
            the calendar label you were looking for, or "Unknown Event" if
            not found.
        """
        ev = mas_getEV(ev_label)
        if ev is None:
            return "Unknown Event"
        else:
            return ev.label


    def mas_hideEVL(
            ev_label,
            code,
            lock=False,
            derandom=False,
            depool=False,
            decond=False
        ):
        """
        Hides an event given label and code.

        IN:
            ev_label - label of event to hide
            code - string code of the db this ev_label belongs to
            lock - True if we want to lock this event
                (Default: False)
            derandom - True if we want to de random this event
                (Default: False)
            depool - True if we want to de pool this event
                (Default: False)
            decond - True if we want to remove conditoinal for this event
                (Default: False)
        """
        store.evhand._hideEvent(
            mas_all_ev_db_map.get(code, {}).get(ev_label, None),
            lock=lock,
            derandom=derandom,
            depool=depool,
            decond=decond
        )


    def mas_showEVL(
            ev_label,
            code,
            unlock=False,
            _random=False,
            _pool=False,
        ):
        """
        Shows an event given label and code.

        IN:
            ev_label - label of event to show
            code - string code of the db this ev_label belongs to
            unlock - True if we want to unlock this Event
                (Default: False)
            _random - True if we want to random this event
                (Default: False)
            _pool - True if we want to random thsi event
                (Default: False)
        """
        store.mas_showEvent(
            mas_all_ev_db_map.get(code, {}).get(ev_label, None),
            unlock=unlock,
            _random=_random,
            _pool=_pool
        )


    def mas_lockEVL(ev_label, code):
        """
        Locks an event given label and code.

        IN:
            ev_label - label of event to show
            code - string code of the db this ev_label belongs to
        """
        mas_hideEVL(ev_label, code, lock=True)


    def mas_unlockEVL(ev_label, code):
        """
        Unlocks an event given label and code.

        IN:
            ev_label - label of event to show
            code - string code of the db this ev_label belongs to
        """
        mas_showEVL(ev_label, code, unlock=True)


    def mas_stripEVL(ev_label, list_pop=False):
        """
        Strips the conditional and action from an event given the label
        Also removes the event from the event list if present (optional)

        IN:
            ev_label - label of event to strip
            list_pop - True if we want to remove the event from the event list
                (Default: False)
        """
        ev = mas_getEV(ev_label)
        if ev is not None:
            ev.conditional = None
            ev.action = None
            
            if list_pop:
                mas_rmEVL(ev_label)

init 4 python:
    def mas_lastSeenInYear(ev_label, year=None):
        """
        Checks whether or not the even was last seen in the year provided

        IN:
            ev_label - label of the event we want to check
            year - the year we want to check if it's been last seen in

        OUT:
            boolean - True if last seen this year, False otherwise

        NOTE: if no year provided, we assume this year
        """
        
        try:
            
            ev = mas_getEV(ev_label)
        except:
            ev = None
        
        
        if not ev or not ev.last_seen:
            return False
        
        
        if year is None:
            year = datetime.date.today().year
        
        
        return ev.last_seen.year == year

    def mas_lastSeenLastYear(ev_label):
        """
        Checks if the event corresponding to ev_label was last seen last year
        """
        return mas_lastSeenInYear(ev_label, datetime.date.today().year-1)


    store.evhand.cleanYearsetBlacklist()


python early:







    MAS_FC_INIT = 1


    MAS_FC_START = 2


    MAS_FC_END = 4


    MAS_FC_IDLE_ROUTINE = 8



    MAS_FC_IDLE_ONCE = 16


    MAS_FC_IDLE_HOUR = 32


    MAS_FC_IDLE_DAY = 64

    MAS_FC_CONSTANTS = [
        MAS_FC_INIT,
        MAS_FC_START,
        MAS_FC_END,
        MAS_FC_IDLE_ROUTINE,
        MAS_FC_IDLE_ONCE,
        MAS_FC_IDLE_HOUR,
        MAS_FC_IDLE_DAY,
    ]


init -880 python:





    if persistent._mas_delayed_action_list is None:
        
        
        
        persistent._mas_delayed_action_list = list()




    mas_delayed_action_map = dict()

    class MASDelayedAction(object):
        """
        A Delayed action consists of the following:

        All exceptions are logged

        id - the unique ID of this DelayedAction
        ev - the event this action is associated with
        conditional - the logical conditional we want to check before performing
            action
            NOTE: this is not checked for correctness
            If cond_is_callable is True, then this is called instead of eval'd.
            In that case, the event object in question is passed into the
            callable.
        action - EV_ACTION constant this delayed action will perform
            NOTE: this is not checked for existence
            NOTE: this can also be a callable
                the event would be passd in as ev
                if callable, make this return True upon success and false
                    othrewise
        flowcheck - FC constant saying when this delayed action should be
            checked
            NOTE: this is not checked for existence
        been_checked - True if this action has been checked this game session
        executed - True if this delayed action has been executed
            - Delayed actions that have been executed CANNOT be executed again
        cond_is_callable - True if the conditional is a callable instead of
            a eval check.
            NOTE: we do not check callable for correctness
        """
        import store.mas_utils as m_util
        
        ERR_COND = "[ERROR] delayed action has bad conditional '{0}' | {1}\n"
        
        
        def __init__(self,
                _id,
                ev,
                conditional,
                action,
                flowcheck,
                cond_is_callable=False
            ):
            """
            Constructor

            NOTE: MAY raise exceptions
            NOTE: also logs exceptions.

            IN:
                _id - id of this delayedAction
                ev - event this action is related to
                conditional - conditional to check to do this action
                    NOTE: if this is a callable, then event is passed in
                action - EV_ACTION constant for this delayed action
                    NOTE: this can also be a callable
                        ev would be passed in as ev
                    If callable, make this return True on success, False
                        otherwise
                flowcheck - FC constant saying when this delaeyd action should
                    be checked
                cond_is_callable - True if the conditional is actually a
                    callable.
                    If this True and None is passed into the conditional, then
                    we just return False (aka never run the delayedaction)
                    (Default: False)
            """
            if not cond_is_callable:
                try:
                    eval(conditional)
                except Exception as e:
                    self.m_util.writelog(self.ERR_COND.format(
                        conditional,
                        str(e)
                    ))
                    raise e
            
            self.cond_is_callable = cond_is_callable
            self.conditional = conditional
            self.action = action
            self.flowcheck = flowcheck
            self.been_checked = False
            self.executed = False
            self.ev = ev
            self.id = _id
        
        
        def __call__(self):
            """
            Checks if the conditional passes then performs the action

            NOTE: logs exceptions

            RETURNS:
                True on successful action performed, False otherwise
            """
            
            if self.ev is None or self.executed or self.action is None:
                return False
            
            
            try:
                
                
                if self.cond_is_callable:
                    
                    if self.conditional is None:
                        
                        return False
                    
                    condition_passed = self.conditional(ev=self.ev)
                
                else:
                    condition_passed = eval(self.conditional)
                
                
                if condition_passed:
                    if self.action in Event.ACTION_MAP:
                        Event.ACTION_MAP[self.action](
                            self.ev, unlock_time=datetime.datetime.now()
                        )
                        self.executed = True
                    
                    else:
                        
                        self.executed = self.action(ev=self.ev)
            
            except Exception as e:
                self.m_util.writelog(self.ERR_COND.format(
                    self.conditional,
                    str(e)
                ))
            
            
            return self.executed
        
        
        @staticmethod
        def makeWithLabel(
                _id,
                ev_label,
                conditional,
                action,
                flowcheck,
                cond_is_callable=False
            ):
            """
            Makes a MASDelayedAction using an eventlabel instead of an event

            IN:
                _id - id of this delayedAction
                ev_label - label of the event this action is related to
                conditional - conditional to check to do to tihs action
                action - EV_ACTION constant for this delayed action
                    NOTE: this can also be a cllable
                        ev would be passed in as ev
                    If callable, make this return True on success, False
                        otherwise
                flowcheck - FC constant saying when this delayed action should
                    be checked
                cond_is_callable - True if the conditional is actually a
                    callable.
                    If this True and None is passed into the conditional, then
                    we just return False (aka never run the delayedaction)
                    (Default: False)
            """
            return MASDelayedAction(
                _id,
                mas_getEV(ev_label),
                conditional,
                action,
                flowcheck,
                cond_is_callable
            )



    def mas_removeDelayedAction(_id):
        """
        Removes a delayed action with the given ID

        NOTE: this removes from both persistent and the runtime lists

        IN:
            _id - id of the delayed action to remove
        """
        if _id in persistent._mas_delayed_action_list:
            persistent._mas_delayed_action_list.remove(_id)
        
        if _id in mas_delayed_action_map:
            mas_delayed_action_map.pop(_id)


    def mas_removeDelayedActions_list(_ids):
        """
        Removes a list of delayed actions with given Ids

        IN:
            _ids - list of Ids to remove
        """
        for _id in _ids:
            mas_removeDelayedAction(_id)


    def mas_removeDelayedActions(*args):
        """
        Multiple argument delayed action removal

        Assumes all given args are IDS
        """
        mas_removeDelayedActions_list(args)


    def mas_runDelayedActions(flow):
        """
        Attempts to run currently held delayed actions for the given flow mode

        Delayed actions that are successfully completed are removed from the
        list

        IN:
            flow - FC constant for the current flow
        """
        if flow not in MAS_FC_CONSTANTS:
            return
        
        
        for action_id in list(mas_delayed_action_map):
            action = mas_delayed_action_map[action_id]
            
            
            if (action.flowcheck & flow) > 0:
                if action():
                    
                    mas_removeDelayedAction(action_id)
                
                
                action.been_checked = True


    def mas_addDelayedAction(_id):
        """
        Creates a delayed action with the given ID and adds it to the delayed
        action map (runtime)

        NOTE: this handles duplicates, so its better to use this

        NOTE: this also adds to persistent, just in case

        IN:
            _id - id of the delayed action to create
        """
        if _id in mas_delayed_action_map:
            return
        
        
        make_action = store.mas_delact.MAP.get(_id, None)
        if make_action is None:
            return
        
        
        mas_delayed_action_map[_id] = make_action()
        
        
        if _id not in persistent._mas_delayed_action_list:
            persistent._mas_delayed_action_list.append(_id)


    def mas_addDelayedActions_list(_ids):
        """
        Creates delayed actions given a list of Ids

        IN:
            _ids - list of IDS to add
        """
        for _id in _ids:
            mas_addDelayedAction(_id)


    def mas_addDelayedActions(*args):
        """
        Creates delayed actions given ids as args

        assumes each arg is a valid id
        """
        mas_addDelayedActions_list(args)


init 995 python:

    mas_runDelayedActions(MAS_FC_INIT)

init -880 python in mas_delact:

    import store

    def _MDA_safeadd(*ids):
        """
        Adds MASDelayedAction ids to the persistent mas delayed action list.

        NOTE: this is only meant for code that runs super early yet needs to
        add MASDelayedActions.

        NOTE: This will NOT add duplicates.

        IN:
            ids - ids to add to the delayed action list
        """
        for _id in ids:
            if _id not in store.persistent._mas_delayed_action_list:
                store.persistent._mas_delayed_action_list.append(_id)


    def _MDA_saferm(*ids):
        """
        Removes MASDelayedActions from the persistent mas delayed action list.

        NOTE: this is only meant for code that runs super early yet needs to
        remove MASDelayedActions

        NOTE: this will check for existence before removing

        IN:
            ids - ids to remove from the delayed action list
        """
        for _id in ids:
            if _id in store.persistent._mas_delayed_action_list:
                store.persistent._mas_delayed_action_list.remove(_id)


init -875 python in mas_delact:

    import datetime 






    MAP = {
        

        2: _mas_monika_islands_unlock,













        16: _mas_birthdate_bad_year_fix,
    }


init 994 python in mas_delact:


    def loadDelayedActionMap():
        """
        Checks the persistent delayed action list and generates the
        runtime map of delayed actions
        """
        store.mas_addDelayedActions_list(
            store.persistent._mas_delayed_action_list
        )


    def saveDelayedActionMap():
        """
        Checks the runtime map of delayed actions and saves them into the
        persistent value.

        NOTE: this does not ADD to the persistent's list. This recreates it
            entirely.
        """
        store.persistent._mas_delayed_action_list = [
            action_id for action_id in store.mas_delayed_action_map
        ]



    loadDelayedActionMap()


default persistent._mas_ev_yearset_blacklist = {}




init -1 python in evhand:
    import store


    event_database = dict()
    farewell_database = dict()
    greeting_database = dict()


    from collections import namedtuple




    _NT_CAT_PANE = namedtuple("_NT_CAT_PANE", "menu cats")



    RIGHT_X = 1020

    RIGHT_Y = 40

    RIGHT_W = 250
    RIGHT_H = 640

    RIGHT_XALIGN = -0.10
    RIGHT_AREA = (RIGHT_X, RIGHT_Y, RIGHT_W, RIGHT_H)



    LEFT_X = 735

    LEFT_Y = RIGHT_Y

    LEFT_W = RIGHT_W
    LEFT_H = RIGHT_H

    LEFT_XALIGN = -0.10
    LEFT_AREA = (LEFT_X, LEFT_Y, LEFT_W, LEFT_H)

    UNSE_X = 680
    UNSE_Y = 40
    UNSE_W = 560
    UNSE_H = 640
    UNSE_XALIGN = -0.05
    UNSE_AREA = (UNSE_X, UNSE_Y, UNSE_W, UNSE_H)


    import datetime
    LAST_SEEN_DELTA = datetime.timedelta(hours=6)


    RESTART_BLKLST = []


    IDLE_WHITELIST = [
        "unlock_prompt",
    ]


    def addIfNew(items, pool):
        
        
        
        
        
        
        
        
        
        
        
        for item in items:
            if item not in pool:
                pool.append(item)
        return pool

    def tuplizeEventLabelList(key_list, db):
        
        
        
        
        
        
        
        
        
        
        
        
        return [(db[x].prompt, x) for x in key_list]


    def _isFuture(ev, date=None):
        """INTERNAL
        Checks if the start_date of the given event happens after the
        given time.

        IN:
            ev - Event to check the start_time
            date - a datetime object used to check against
                If None is passed it will check against current time
                (Default: None)

        RETURNS:
            True if the Event's start_date is in the future, False otherwise
        """
        
        
        if ev is None:
            return False
        
        
        if date is None:
            date = datetime.datetime.now()
        
        start_date = ev.start_date
        
        
        if start_date is None:
            return False
        
        return date < start_date


    def _isPast(ev, date=None):
        """INTERNAL
        Checks if the end_date of the given event happens before the
        given time.

        IN:
            ev - Event to check the start_time
            date - a datetime object used to check against
                If None is passed it will check against current time
                (Default: None)

        RETURNS:
            True if the Event's end_date is in the past, False otherwise
        """
        
        
        if ev is None:
            return False
        
        
        if date is None:
            date = datetime.datetime.now()
        
        end_date = ev.end_date
        
        
        if end_date is None:
            return False
        
        return end_date < date


    def _isPresent(ev):
        """INTERNAL
        Checks if current date falls within the given event's start/end date
        range

        IN:
            ev - Event to check the start_time and end_time

        RETURNS:
            True if current time is inside the  Event's start_date/end_date
            interval, False otherwise
        """
        
        if ev is None:
            return False
        
        start_date = ev.start_date
        end_date = ev.end_date
        
        current = datetime.datetime.now()
        
        
        if start_date is None or end_date is None:
            return False
        
        return start_date <= current <= end_date


    def _hideEvent(
            event,
            lock=False,
            derandom=False,
            depool=False,
            decond=False
        ):
        """
        Internalized hideEvent
        """
        if event:
            
            if lock:
                event.unlocked = False
            
            if derandom:
                event.random = False
            
            if depool:
                event.pool = False
            
            if decond:
                event.conditional = None


    def _hideEventLabel(
            eventlabel,
            lock=False,
            derandom=False,
            depool=False,
            decond=False,
            eventdb=event_database
        ):
        """
        Internalized hideEventLabel
        """
        ev = eventdb.get(eventlabel, None)
        
        _hideEvent(
            ev,
            lock=lock,
            derandom=derandom,
            depool=depool,
            decond=decond
        )


    def _lockEvent(ev):
        """
        Internalized lockEvent
        """
        _hideEvent(ev, lock=True)


    def _lockEventLabel(evlabel, eventdb=event_database):
        """
        Internalized lockEventLabel
        """
        _hideEventLabel(evlabel, lock=True, eventdb=eventdb)


    def _unlockEvent(ev):
        """
        Internalized unlockEvent
        """
        if ev:
            ev.unlocked = True


    def _unlockEventLabel(evlabel, eventdb=event_database):
        """
        Internalized unlockEventLabel
        """
        _unlockEvent(eventdb.get(evlabel, None))


    def addYearsetBlacklist(evl, expire_dt):
        """
        Adds the given evl to the yearset blacklist, with the given expiration
        dt

        IN:
            evl - event label
            expire_dt - when the evl should be removed from the blacklist
        """
        if expire_dt > datetime.datetime.now():
            store.persistent._mas_ev_yearset_blacklist[evl] = expire_dt


    def cleanYearsetBlacklist():
        """
        Goes through the year setblacklist and removes expired entries
        """
        now_dt = datetime.datetime.now()
        for evl in store.persistent._mas_ev_yearset_blacklist.keys():
            if store.persistent._mas_ev_yearset_blacklist[evl] <= now_dt:
                store.persistent._mas_ev_yearset_blacklist.pop(evl)


    def isYearsetBlacklisted(evl):
        """
        Checks if the given evl is yearset blacklisted. Also checks expiration
        date and removes if needed.

        IN:
            evl - event label

        RETURNS: True if blacklisted, false if not
        """
        if evl not in store.persistent._mas_ev_yearset_blacklist:
            return False
        
        expire_dt = store.persistent._mas_ev_yearset_blacklist[evl]
        if expire_dt <= datetime.datetime.now():
            store.persistent._mas_ev_yearset_blacklist.pop(evl)
            return False
        
        return True


init python:
    import store.evhand as evhand
    import datetime

    def addEvent(
        event,
        eventdb=None,
        skipCalendar=False,
        restartBlacklist=False,
        markSeen=False,
        code="EVE"
    ):
        """
        Adds an event object to the given eventdb dict
        Properly checksfor label and conditional statements
        This function ensures that a bad item is not added to the database

        NOTE: this MUST be ran after init level 4.

        IN:
            event - the Event object to add to database
            eventdb - The Event databse (dict) we want to add to
                NOTE: DEPRECATED. Use code instead.
                NOTE: this can still be used for custom adds.
                (Default: None)
            skipCalendar - flag that marks wheter or not calendar check should
                be skipped

            restartBlacklist - True if this topic should be added to the restart blacklist
                (Default: False)

            markSeen - True if this topic should be `True` in persistent._seen_ever.
                (Default: False)

            code - code of the event database to add to.
                (Default: EVE) - event database
        """
        if eventdb is None:
            eventdb = mas_all_ev_db_map.get(code, None)
        
        if type(eventdb) is not dict:
            raise EventException("Given db is not of type dict")
        if type(event) is not Event:
            raise EventException("'" + str(event) + "' is not an Event object")
        if not renpy.has_label(event.eventlabel):
            raise EventException("'" + event.eventlabel + "' does NOT exist")
        if event.conditional is not None:
            eval(event.conditional)
        
        
        
        
        
        
        if not skipCalendar and type(event.start_date) is datetime.datetime:
            
            store.mas_calendar.addEvent(event)
        
        
        
        if not store.evhand.isYearsetBlacklisted(event.eventlabel):
            Event._verifyAndSetDatesEV(event)
        
        
        if restartBlacklist:
            evhand.RESTART_BLKLST.append(event.eventlabel)
        
        if markSeen:
            persistent._seen_ever[event.eventlabel] = True
        
        
        eventdb.setdefault(event.eventlabel, event)


    def hideEventLabel(
            eventlabel,
            lock=False,
            derandom=False,
            depool=False,
            decond=False,
            eventdb=evhand.event_database
        ):
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        mas_hideEventLabel(eventlabel, lock, derandom, depool, decond, eventdb)


    def hideEvent(
            event,
            lock=False,
            derandom=False,
            depool=False,
            decond=False
        ):
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        mas_hideEvent(event, lock, derandom, depool, decond)


    def mas_hideEvent(
            ev,
            lock=False,
            derandom=False,
            depool=False,
            decond=False
        ):
        """
        Hide an event by Falsing its unlocked/random/pool props

        IN:
            ev - event object we want to hide
            lock - True if we want to lock this event, False if not
                (Default: False)
            derandom - True fi we want to unrandom this Event, False if not
                (Default: False)
            depool - True if we want to unpool this event, Flase if not
                (Default: False)
            decond - True if we want to remove the conditional, False if not
                (Default: False)
        """
        evhand._hideEvent(
            ev,
            lock=lock,
            derandom=derandom,
            depool=depool,
            decond=decond
        )


    def mas_hideEventLabel(
            ev_label,
            lock=False,
            derandom=False,
            depool=False,
            decond=False,
            eventdb=evhand.event_database
        ):
        """
        Hide an event label by Falsing its unlocked/random/pool props

        NOTE: use this with custom eventdbs

        IN:
            ev_label - label of the event we wnat to hide
            lock - True if we want to lock this event, False if not
                (Default: False)
            derandom - True fi we want to unrandom this Event, False if not
                (Default: False)
            depool - True if we want to unpool this event, Flase if not
                (Default: False)
            decond - True if we want to remove the conditional, False if not
                (Default: False)
            eventdb - event databsae ev_label is in
                (Default: evhand.event_database)
        """
        evhand._hideEventLabel(
            ev_label,
            lock=lock,
            derandom=derandom,
            depool=depool,
            decond=decond,
            eventdb=eventdb
        )


    def mas_showEvent(
            ev,
            unlock=False,
            _random=False,
            _pool=False
        ):
        """
        Show an event by Truing its unlock/ranomd/pool props

        IN:
            ev - event to show
            unlock - True if we want to unlock this event, False if not
                (Default: False)
            _random - True if we want to random this event, Flase otherwise
                (Default: False)
            _pool - True if we want to pool this event, False otherwise
                (Default: False)
        """
        if ev:
            
            if unlock:
                ev.unlocked = True
            
            if _random:
                ev.random = True
            
            if _pool:
                ev.pool = True


    def mas_showEventLabel(
            ev_label,
            unlock=False,
            _random=False,
            _pool=False,
            eventdb=evhand.event_database
        ):
        """
        Shows an event label, by Truing the unlocked, random, and pool
        properties.

        NOTE: use this for custom event dbs

        IN:
            ev_label - label of event to show
            unlock - True if we want to unlock this event, False if not
                (DEfault: False)
            _random - True if we want to random this event, False if not
                (Default: False)
            _pool - True if we want to pool this event, False if not
                (Default: False)
            eventdb - eventdatabase this label belongs to
                (Default: evhannd.event_database)
        """
        mas_showEvent(eventdb.get(ev_label, None), unlock, _random, _pool)


    def lockEvent(ev):
        """
        NOTE: DEPRECATED
        Locks the given event object

        IN:
            ev - the event object to lock
        """
        mas_lockEvent(ev)


    def lockEventLabel(evlabel, eventdb=evhand.event_database):
        """
        NOTE: DEPRECATED
        Locks the given event label

        IN:
            evlabel - event label of the event to lock
            eventdb - Event database to find this label
        """
        mas_lockEventLabel(evlabel, eventdb)


    def mas_lockEvent(ev):
        """
        Locks the given event object

        IN:
            ev - the event object to lock
        """
        evhand._lockEvent(ev)


    def mas_lockEventLabel(evlabel, eventdb=evhand.event_database):
        """
        Locks the given event label

        IN:
            evlabel - event label of the event to lock
            eventdb - Event database to find this label
        """
        evhand._lockEventLabel(evlabel, eventdb=eventdb)


    def pushEvent(event_label, skipeval=False, notify=False):
        """
        This pushes high priority or time sensitive events onto the top of
        the event list

        IN:
            @event_label - a renpy label for the event to be called
            skipmidloopeval - do we want to skip the mid loop eval to prevent other rogue events
            from interrupting. (Defaults: False)
            notify - True will trigger a notification if appropriate. False
                will not

        ASSUMES:
            persistent.event_list
        """
        
        persistent.event_list.append((event_label, notify))
        
        if skipeval:
            mas_idle_mailbox.send_skipmidloopeval()
        return

    def queueEvent(event_label, notify=False):
        """
        This adds low priority or order-sensitive events onto the bottom of
        the event list. This is slow, but rarely called and list should be small.

        IN:
            @event_label - a renpy label for the event to be called
            notify - True will trigger a notification if appropriate, False
                will not

        ASSUMES:
            persistent.event_list
        """
        
        persistent.event_list.insert(0, (event_label, notify))
        return


    def unlockEvent(ev):
        """
        NOTE: DEPRECATED
        Unlocks the given evnet object

        IN:
            ev - the event object to unlock
        """
        mas_unlockEvent(ev)


    def unlockEventLabel(evlabel, eventdb=evhand.event_database):
        """
        NOTE: DEPRECATED
        Unlocks the given event label

        IN:
            evlabel - event label of the event to lock
            eventdb - Event database to find this label
        """
        mas_unlockEventLabel(evlabel, eventdb)


    def mas_unlockEvent(ev):
        """
        Unlocks the given evnet object

        IN:
            ev - the event object to unlock
        """
        evhand._unlockEvent(ev)


    def mas_unlockEventLabel(evlabel, eventdb=evhand.event_database):
        """
        Unlocks the given event label

        IN:
            evlabel - event label of the event to lock
            eventdb - Event database to find this label
        """
        evhand._unlockEventLabel(evlabel, eventdb=eventdb)


    def isFuture(ev, date=None):
        """
        Checks if the start_date of the given event happens after the
        given time.

        IN:
            ev - Event to check the start_time
            date - a datetime object used to check against
                If None is passed it will check against current time
                (Default: None)

        RETURNS:
            True if the Event's start_date is in the future, False otherwise
        """
        return evhand._isFuture(ev, date=date)


    def isPast(ev, date=None):
        """
        Checks if the end_date of the given event happens before the
        given time.

        IN:
            ev - Event to check the start_time
            date - a datetime object used to check against
                If None is passed it will check against current time
                (Default: None)

        RETURNS:
            True if the Event's end_date is in the past, False otherwise
        """
        return evhand._isPast(ev, date=date)


    def isPresent(ev):
        """
        Checks if current date falls within the given event's start/end date
        range

        IN:
            ev - Event to check the start_time and end_time

        RETURNS:
            True if current time is inside the  Event's start_date/end_date
            interval, False otherwise
        """
        return evhand._isPresent(ev)


    def popEvent(remove=True):
        """
        This returns the event name for the next event and makes it the
        current_monikatopic

        IN:
            remove = If False, then just return the name of the event but don't
            remove it

        ASSUMES:
            persistent.event_list
            persistent.current_monikatopic

        RETURNS: tuple of the folloiwng format:
            [0] - event lable of the next event
            [1] - whether or not we need to notify
        """
        if len(persistent.event_list) == 0:
            return None, None
        
        if store.mas_globals.in_idle_mode:
            
            
            ev_found = None
            
            for index in range(len(persistent.event_list)):
                ev_label, notify = persistent.event_list[index]
                ev_found = mas_getEV(ev_label)
                
                if (
                        (ev_found is not None and ev_found.show_in_idle)
                        or ev_label in evhand.IDLE_WHITELIST
                    ):
                    
                    if remove:
                        mas_rmEVL(ev_label)
                    
                    persistent.current_monikatopic = ev_label
                    return ev_label, notify
            
            
            return None, None
        
        elif remove:
            ev_data = persistent.event_list.pop()
            persistent.current_monikatopic = ev_data[0]
        else:
            ev_data = persistent.event_list[-1]
        
        return ev_data


    def seen_event(event_label):
        """
        This checks if an event has either been seen or is already in the
        event list.

        IN:
            event_lable = The label for the event to be checked

        ASSUMES:
            persistent.event_list
        """
        if renpy.seen_label(event_label) or mas_inEVL(event_label):
            return True
        else:
            return False


    def mas_findEVL(event_label):
        """
        Finds index of the given event label in the even tlist

        IN:
            event_label - event lable to check

        RETURNS: index of the event in teh even tlist, -1 if not found
        """
        for index in range(len(persistent.event_list)):
            if persistent.event_list[index][0] == event_label:
                return index
        
        return -1


    def mas_inEVL(event_label):
        """
        This checks if an event is in the event list

        IN:
            event_label - event lable to check

        RETURNS: True if in event list, False if not
        """
        for ev_data in persistent.event_list:
            if ev_data[0] == event_label:
                return True
        
        return False


    def mas_rmEVL(event_label):
        """
        REmoves an event from the event list if it exists

        IN:
            event label to remove
        """
        position = mas_findEVL(event_label)
        if position >= 0:
            persistent.event_list.pop(position)


    def mas_rmallEVL(event_label):
        """
        Removes all events with athe given label

        IN:
            event label to remove
        """
        position = mas_findEVL(event_label)
        while position >= 0:
            mas_rmEVL(event_label)
            position = mas_findEVL(event_label)


    def restartEvent():
        """
        This checks if there is a persistent topic, and if there was push it
        back on the stack with a little comment.
        """
        if not mas_isRstBlk(persistent.current_monikatopic):
            
            pushEvent(persistent.current_monikatopic)
            pushEvent('continue_event',skipeval=True)
            persistent.current_monikatopic = 0
        return


    def mas_isRstBlk(topic_label):
        """
        Checks if the event with the current label is blacklistd from being
        restarted

        IN:
            topic_label - label of the event we are trying to restart
        """
        if not topic_label:
            return True
        
        if topic_label.startswith("greeting_"):
            return True
        
        if topic_label.startswith("bye"):
            return True
        
        if topic_label.startswith("i_greeting"):
            return True
        
        if topic_label.startswith("ch30_reload"):
            return True
        
        
        if topic_label in evhand.RESTART_BLKLST:
            return True
        
        return False

    def mas_cleanEventList():
        """
        Iterates through the event list and removes items which shouldn't be restarted
        """
        for index in range(len(persistent.event_list)-1,-1,-1):
            if mas_isRstBlk(persistent.event_list[index][0]):
                mas_rmEVL(persistent.event_list[index][0])

    def mas_cleanJustSeen(eventlist, db):
        """
        Cleans the given event list of just seen items (withitn the THRESHOLD)
        retunrs not just seen items

        IN:
            eventlist - list of event labels to pick from
            db - database these events are tied to

        RETURNS:
            cleaned list of events (stuff not in the time THREASHOLD)
        """
        import datetime
        now = datetime.datetime.now()
        cleanlist = list()
        
        for evlabel in eventlist:
            ev = db.get(evlabel, None)
            
            if ev:
                if ev.last_seen:
                    if now - ev.last_seen >= store.evhand.LAST_SEEN_DELTA:
                        cleanlist.append(evlabel)
                
                else:
                    cleanlist.append(evlabel)
        
        return cleanlist


    def mas_cleanJustSeenEV(ev_list):
        """
        Cleans the given event list (of events) of just seen items
        (within the THRESHOLD). Returns not just seen items.
        Basically the same as mas_cleanJustSeen, except for Event object lists

        IN:
            ev_list - list of event objects

        RETURNS:
            cleaned list of events (stuff not in the tiem THRESHOLD)
        """
        import datetime
        now = datetime.datetime.now()
        cleaned_list = list()
        
        for ev in ev_list:
            if ev.last_seen is not None:
                
                if now - ev.last_seen >= store.evhand.LAST_SEEN_DELTA:
                    cleaned_list.append(ev)
            
            else:
                
                cleaned_list.append(ev)
        
        return cleaned_list


    def mas_unlockPrompt():
        """
        Unlocks a pool event

        RETURNS:
            True if an event was unlocked. False otherwise
        """
        pool_events = Event.filterEvents(
            evhand.event_database,
            unlocked=False,
            pool=True
        )
        pool_event_keys = [
            evlabel
            for evlabel in pool_events
            if "no unlock" not in pool_events[evlabel].rules
        ]
        
        if len(pool_event_keys)>0:
            sel_evlabel = renpy.random.choice(pool_event_keys)
            
            evhand.event_database[sel_evlabel].unlocked = True
            evhand.event_database[sel_evlabel].unlock_date = datetime.datetime.now()
            
            return True
        
        
        return False


init 1 python in evhand:






    import store
    import datetime


    def actionPush(ev, **kwargs):
        """
        Runs Push Event action for the given event

        IN:
            ev - event to push to event stack
        """
        store.pushEvent(ev.eventlabel, notify=True)


    def actionQueue(ev, **kwargs):
        """
        Runs Queue event action for the given event

        IN:
            ev - event to queue to event stack
        """
        store.queueEvent(ev.eventlabel, notify=True)


    def actionUnlock(ev, **kwargs):
        """
        Unlocks an event. Also setse the unlock_date to the given
            unlock time

        IN:
            ev - event to unlock
            unlock_time - time to set unlock_date to
        """
        ev.unlocked = True
        ev.unlock_date = kwargs.get("unlock_time", datetime.datetime.now())


    def actionRandom(ev, **kwargs):
        """
        Randos an event.

        IN:
            ev - event to random
            rebuild_ev - True if we wish to notify idle to rebuild events
        """
        ev.random = True
        if kwargs.get("rebuild_ev", False):
            store.mas_idle_mailbox.send_rebuild_msg()


    def actionPool(ev, **kwargs):
        """
        Pools an event.

        IN:
            ev - event to pool
        """
        ev.pool = True



    store.Event.ACTION_MAP = {
        store.EV_ACT_UNLOCK: actionUnlock,
        store.EV_ACT_QUEUE: actionQueue,
        store.EV_ACT_PUSH: actionPush,
        store.EV_ACT_RANDOM: actionRandom,
        store.EV_ACT_POOL: actionPool
    }





label call_next_event:


    $ event_label, notify = popEvent()
    if event_label and renpy.has_label(event_label):








        $ mas_RaiseShield_dlg()

        $ ev = mas_getEV(event_label)

        if (
                notify
                and ((ev is not None and "skip alert" not in ev.rules) or ev is None)
            ):

            if renpy.windows:
                $ display_notif(m_name, mas_win_notif_quips, "Topic Alerts")
            else:
                $ display_notif(m_name, mas_other_notif_quips, "Topic Alerts")

        call expression event_label from _call_expression
        $ persistent.current_monikatopic=0


        $ ev = evhand.event_database.get(event_label, None)
        if ev is not None:
            if ev.random and not ev.unlocked:
                python:
                    ev.unlocked=True
                    ev.unlock_date=datetime.datetime.now()
        else:



            $ ev = mas_getEV(event_label)

        if ev is not None:

            $ ev.shown_count += 1
            $ ev.last_seen = datetime.datetime.now()

        if _return is not None:
            $ ret_items = _return.split("|")

            if "derandom" in ret_items:
                $ ev.random = False

            if "no_unlock" in ret_items:
                $ ev.unlocked = False
                $ ev.unlock_date = None

            if "rebuild_ev" in ret_items:
                $ mas_rebuildEventLists()

            if "idle" in ret_items:
                $ store.mas_globals.in_idle_mode = True
                $ persistent._mas_in_idle_mode = True
                $ renpy.save_persistent()

            if "love" in ret_items:
                $ mas_ILY()

            if "quit" in ret_items:
                $ persistent.closed_self = True
                $ mas_clearNotifs()
                jump _quit

            if "prompt" in ret_items:
                show monika idle
                jump prompt_menu


        if len(persistent.event_list) > 0:
            jump call_next_event

    if store.mas_globals.in_idle_mode:

        $ mas_dlgToIdleShield()
    else:

        $ mas_DropShield_dlg()


    if not renpy.showing("monika idle"):
        show monika idle zorder MAS_MONIKA_Z at t11 with dissolve

    return False


default persistent._mas_pool_unlocks = 0



label unlock_prompt:
    python:
        if not mas_unlockPrompt():
            
            
            persistent._mas_pool_unlocks += 1

    return





label prompt_menu:

    $ mas_RaiseShield_dlg()

    if store.mas_globals.in_idle_mode:



        $ cb_label = mas_idle_mailbox.get_idle_cb()









        if cb_label is not None:
            call expression cb_label from _call_expression_5


        show monika idle with dissolve


        $ persistent._mas_greeting_type = None
        $ store.mas_globals.in_idle_mode = False


        $ pushEvent("mas_idle_mode_greeting_cleanup")
        $ mas_idle_mailbox.send_skipmidloopeval()



        $ store.mas_hotkeys.music_enabled = True

        jump prompt_menu_end

    python:

        mas_setTODVars()

        unlocked_events = Event.filterEvents(
            evhand.event_database,
            unlocked=True,
            aff=mas_curr_affection
        )
        sorted_event_keys = Event.getSortedKeys(unlocked_events,include_none=True)

        unseen_events = []
        for ev_label in sorted_event_keys:
            
            
            if not seen_event(ev_label) and ev_label != "mas_show_unseen":
                unseen_events.append(ev_label)

        if len(unseen_events) > 0 and persistent._mas_unsee_unseen:
            mas_showEVL('mas_show_unseen','EVE',unlock=True)
            unseen_num = len(unseen_events)
            mas_getEV('mas_show_unseen').prompt = "I would like to see 'Unseen' ([unseen_num]) again"
        else:
            mas_hideEVL('mas_show_unseen','EVE',lock=True)

        repeatable_events = Event.filterEvents(
            evhand.event_database,
            unlocked=True,
            pool=False,
            aff=mas_curr_affection
        )





    show monika at t21

    python:
        talk_menu = []
        if len(unseen_events)>0 and not persistent._mas_unsee_unseen:
            
            talk_menu.append((_("{b}Unseen{/b}"), "unseen"))
        if mas_hasBookmarks():
            talk_menu.append((_("Bookmarks"),"bookmarks"))
        talk_menu.append((_("Hey, [m_name]..."), "prompt"))
        if len(repeatable_events)>0:
            talk_menu.append((_("Repeat conversation"), "repeat"))
        if _mas_getAffection() > -50:
            if mas_passedILY(pass_time=datetime.timedelta(0,10)):
                talk_menu.append((_("I love you too!"),"love_too"))
            else:
                talk_menu.append((_("I love you!"), "love"))
        talk_menu.append((_("I'm feeling..."), "moods"))
        talk_menu.append((_("Goodbye"), "goodbye"))
        talk_menu.append((_("Nevermind"),"nevermind"))

        renpy.say(m, store.mas_affection.talk_quip()[1], interact=False)
        madechoice = renpy.display_menu(talk_menu, screen="talk_choice")

    if madechoice == "unseen":
        call show_prompt_list (unseen_events) from _call_show_prompt_list

    elif madechoice == "bookmarks":
        call mas_bookmarks from _call_mas_bookmarks

    elif madechoice == "prompt":
        call prompts_categories (True) from _call_prompts_categories

    elif madechoice == "repeat":
        call prompts_categories (False) from _call_prompts_categories_1

    elif madechoice == "love":
        $ pushEvent("monika_love",skipeval=True)
        $ _return = True

    elif madechoice == "love_too":
        $ pushEvent("monika_love_too",skipeval=True)
        $ _return = True

    elif madechoice == "moods":
        call mas_mood_start from _call_mas_mood_start

    elif madechoice == "goodbye":
        call mas_farewell_start from _call_select_farewell
    else:

        $ _return = None


    if _return is False:
        jump prompt_menu

label prompt_menu_end:

    show monika at t11
    $ mas_DropShield_dlg()
    jump ch30_loop

label show_prompt_list(sorted_event_keys):
    $ import store.evhand as evhand


    python:
        prompt_menu_items = []
        for event in sorted_event_keys:
            prompt_menu_items.append([unlocked_events[event].prompt,event])

    $ nvm_text = "Nevermind."

    $ remove = (mas_getEV("mas_hide_unseen").prompt, mas_getEV("mas_hide_unseen").eventlabel)

    call screen scrollable_menu(prompt_menu_items, evhand.UNSE_AREA, evhand.UNSE_XALIGN, nvm_text, remove)

    if _return:
        $ pushEvent(_return)

    return _return

label prompts_categories(pool=True):



    $ cat_lists = list()

    $ current_category = list()
    $ import store.evhand as evhand
    $ picked_event = False
    python:


        unlocked_events = Event.filterEvents(
            evhand.event_database,


            unlocked=True,
            pool=pool,
            aff=mas_curr_affection
        )


        main_cat_list = list()
        no_cat_list = list() 
        for key in unlocked_events:
            if unlocked_events[key].category:
                evhand.addIfNew(unlocked_events[key].category, main_cat_list)
            else:
                no_cat_list.append(unlocked_events[key])


        main_cat_list.sort()
        no_cat_list.sort(key=Event.getSortPrompt)




        dis_cat_list = [(x.capitalize() + "...",x) for x in main_cat_list]



        no_cat_list = [(x.prompt, x.eventlabel) for x in no_cat_list]


        dis_cat_list.extend(no_cat_list)


        cat_lists.append(evhand._NT_CAT_PANE(dis_cat_list, main_cat_list))

    while not picked_event:
        python:
            prev_items, prev_cats = cat_lists[len(cat_lists)-1]


            if len(current_category) == 0:
                main_items = None

            else:
                
                
                
                
                
                
                unlocked_events = Event.filterEvents(
                    evhand.event_database,

                    category=(False,current_category),
                    unlocked=True,
                    pool=pool,
                    aff=mas_curr_affection
                )
                
                
                
                
                
                
                
                no_cat_list = sorted(
                    unlocked_events.values(),
                    key=Event.getSortPrompt
                )
                
                
                no_cat_list = [(x.prompt, x.eventlabel) for x in no_cat_list]
                
                
                
                
                
                main_cats = []
                
                
                main_items = no_cat_list
                
                """ KEEP this for legacy purposes
#            sorted_event_keys = Event.getSortedKeys(unlocked_events,include_none=True)

            prompt_category_menu = []
            #Make a list of categories

            #Make a list of all categories
            subcategories=set([])
            for event in sorted_event_keys:
                if unlocked_events[event].category is not None:
                    new_categories=set(unlocked_events[event].category).difference(set(current_category))
                    subcategories=subcategories.union(new_categories)

            subcategories = list(subcategories)
            for category in sorted(subcategories, key=lambda s: s.lower()):
                #Don't list additional subcategories if adding them wouldn't change the same you are looking at
                test_unlock = Event.filterEvents(evhand.event_database,full_copy=True,category=[False,current_category+[category]],unlocked=True)

                if len(test_unlock) != len(sorted_event_keys):
                    prompt_category_menu.append([category.capitalize() + "...",category])


            #If we do have a category picked, make a list of the keys
            if sorted_event_keys is not None:
                for event in sorted_event_keys:
                    prompt_category_menu.append([unlocked_events[event].prompt,event])
                """

        call screen twopane_scrollable_menu(prev_items, main_items, evhand.LEFT_AREA, evhand.LEFT_XALIGN, evhand.RIGHT_AREA, evhand.RIGHT_XALIGN, len(current_category)) nopredict



        if _return in prev_cats:

            python:
                if len(current_category) > 0:
                    current_category.pop()
                current_category.append(_return)











        elif _return == -1:
            if len(current_category) > 0:
                $ current_category.pop()
        else:

            $ picked_event = True

            if _return is not False:
                $ pushEvent(_return)

    return _return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="mas_bookmarks",unlocked=False,rules={"no unlock":None}))


label mas_bookmarks:
    show monika idle
    python:

        def gen_bk_disp(bkpl):
            return [
                (bkpl[index][0], index, False, False)
                for index in range(len(bkpl))
            ]


        bookmarks_pl = [
            (renpy.substitute(ev.prompt), ev.eventlabel)
            for ev in mas_get_player_bookmarks()
        ]
        bookmarks_pl.sort()
        bookmarks_disp = gen_bk_disp(bookmarks_pl)

        remove_bookmark = (
            "I'd like to remove a bookmark.",
            -1,
            False,
            False,
            20
        )
        return_prompt_back = ("Nevermind.", -2, False, False, 0)


label mas_bookmarks_loop:


    if len(bookmarks_pl) < 1 or len(bookmarks_pl) != len(bookmarks_disp):


        return False

    show monika at t21
    call screen mas_gen_scrollable_menu(bookmarks_disp,(evhand.UNSE_X, evhand.UNSE_Y, evhand.UNSE_W, 500), evhand.UNSE_XALIGN, remove_bookmark, return_prompt_back)

    $ topic_choice = _return

    if topic_choice < -1:

        return False

    elif topic_choice < 0:


        call mas_bookmarks_unbookmark (bookmarks_pl, bookmarks_disp, gen_bk_disp) from _call_mas_bookmarks_unbookmark
        show monika idle


        $ bookmarks_disp = _return

    elif 0 <= topic_choice < len(bookmarks_pl):

        $ sel_evl = bookmarks_pl[topic_choice][1]
        show monika at t11
        $ pushEvent(sel_evl, skipeval=True)
        return True

    jump mas_bookmarks_loop












label mas_bookmarks_unbookmark(bookmarks_pl, bookmarks_disp, regen):
    pass

label mas_bookmarks_unbookmark_loop:

    if len(bookmarks_pl) < 1 or len(bookmarks_pl) != len(bookmarks_disp):


        return []

    $ unbookmark_back = ("Nevermind.", -1, False, False, 20)

    show monika 1eua at t21


    if len(bookmarks_disp) > 1:
        $ renpy.say(m,"Which bookmark do you want to remove?", interact=False)
    else:
        $ renpy.say(m,"Just click the bookmark if you're sure you want to remove it.", interact=False)

    call screen mas_gen_scrollable_menu(bookmarks_disp, (evhand.UNSE_X, evhand.UNSE_Y, evhand.UNSE_W, 500), evhand.UNSE_XALIGN, unbookmark_back)

    $ topic_choice = _return

    if topic_choice < 0:

        return bookmarks_disp


    if topic_choice < len(bookmarks_pl):


        python:

            sel_evl = bookmarks_pl[topic_choice][1]


            if sel_evl in persistent._mas_player_bookmarked:
                persistent._mas_player_bookmarked.remove(sel_evl)


            bookmarks_pl.pop(topic_choice)


            bookmarks_disp = regen(bookmarks_pl)

        show monika at t11
        m 1eua "Okay, [player]..."


        if len(bookmarks_disp) > 0:
            m 1eka "Are there any other bookmarks you want to remove?{nw}"
            $ _history_list.pop()
            menu:
                m "Are there any other bookmarks you want to remove?{fast}"
                "Yes.":
                    pass
                "No.":
                    m 3eua "Okay."
                    return bookmarks_disp
        else:
            m 3hua "All done!"
            return bookmarks_disp

    jump mas_bookmarks_unbookmark_loop
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
