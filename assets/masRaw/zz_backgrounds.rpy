
default persistent._mas_background_MBGdata = {}


init -10 python:





    class MASBackground(object):
        """
        Background class to get display props for bgs

        PROPERTIES:
            background_id - the id which defines this bg
            prompt - button label for the bg
            image_map - Dict mapping all images for the bgs, keys are precip types (See MASWeather)
            hide_calendar - whether or not we display the calendar with this
            hide_masks - whether or not we display the window masks
            disable_progressive - weather or not we disable progesssive weather
            unlocked - whether or not this background is unlocked
            entry_pp - entry programming points for bgs
            exit_pp - exit programming points
        """
        import store.mas_background as mas_background
        import store.mas_weather as mas_weather
        
        def __init__(
            self,
            background_id,
            prompt,
            image_day,
            image_night,
            image_rain_day=None,
            image_rain_night=None,
            image_overcast_day=None,
            image_overcast_night=None,
            image_snow_day=None,
            image_snow_night=None,
            hide_calendar=False,
            hide_masks=False,
            disable_progressive=None,
            unlocked=False,
            entry_pp=None,
            exit_pp=None
        ):
            """
            Constructor for background objects

            IN:
                background_id:
                    id that defines the background object
                    NOTE: Must be unique

                prompt:
                    button label for this bg

                image_day:
                    the renpy.image object we use for this bg during the day
                    NOTE: Mandatory

                image_night:
                    the renpy.image object we use for this bg during the night
                    NOTE: Mandatory

                image_rain_day:
                    the image tag we use for the background while it's raining (day)
                    (Default: None, not required)

                image_rain_night:
                    the image tag we use for the background while it's raining (night)
                    (Default: None, not required)

                image_overcast_day:
                    the image tag we use for the background while it's overcast (day)
                    (Default: None, not required)

                image_overcast_night:
                    the image tag we use for the background while it's overcast (night)
                    (Default: None, not required)

                image_snow_day:
                    the image tag we use for the background while it's snowing (day)
                    (Default: None, not required)

                image_snow_night:
                    the image tag we use for the background while it's snowing (night)
                    (Default: None, not required)

                hide_calendar:
                    whether or not we want to display the calendar
                    (Default: False)

                hide_masks:
                    weather or not we want to show the windows
                    (Default: False)

                disable_progressive:
                    weather or not we want to disable progressive weather
                    (Default: None, if hide masks is true and this is not provided, we assume True, otherwise False)

                unlocked:
                    whether or not this background starts unlocked
                    (Default: False)

                entry_pp:
                    Entry programming point for the background
                    (Default: None)

                exit_pp:
                    Exit programming point for this background
                    (Default: None)
            """
            
            if background_id in self.mas_background.BACKGROUND_MAP:
                raise Exception("duplicate background ID")
            
            self.background_id = background_id
            self.prompt = prompt
            self.image_day = image_day
            self.image_night = image_night
            
            
            self.image_map = {
                
                mas_weather.PRECIP_TYPE_DEF: (image_day, image_night),
                
                mas_weather.PRECIP_TYPE_RAIN: (image_rain_day if image_rain_day else image_day, image_rain_night if image_rain_night else image_night),
                
                mas_weather.PRECIP_TYPE_OVERCAST: (image_overcast_day if image_overcast_day else image_day, image_overcast_night if image_overcast_night else image_night),
                
                mas_weather.PRECIP_TYPE_SNOW: (image_snow_day if image_snow_day else image_day, image_snow_night if image_snow_night else image_night)
            }
            
            
            self.hide_calendar = hide_calendar
            self.hide_masks = hide_masks
            
            
            if disable_progressive is None:
                self.disable_progressive = hide_masks
            else:
                self.disable_progressive = disable_progressive
            
            self.unlocked = unlocked
            self.entry_pp = entry_pp
            self.exit_pp = exit_pp
            
            
            self.mas_background.BACKGROUND_MAP[background_id] = self
        
        
        def __eq__(self, other):
            if isinstance(other, MASBackground):
                return self.background_id == other.background_id
            return NotImplemented
        
        
        def __ne__(self, other):
            result = self.__eq__(other)
            if result is NotImplemented:
                return result
            return not result
        
        
        def entry(self, old_background):
            """
            Run the entry programming point
            """
            if self.entry_pp is not None:
                self.entry_pp(old_background)
        
        
        def exit(self, new_background):
            """
            Run the exit programming point
            """
            if self.exit_pp is not None:
                self.exit_pp(new_background)
        
        
        def fromTuple(self, data_tuple):
            """
            Loads data from tuple

            IN:
                data_tuple - tuple of the following format:
                    [0]: unlocked property
            """
            self.unlocked = data_tuple[0]
        
        
        def toTuple(self):
            """
            Converts this MASWeather object into a tuple

            RETURNS: tuple of the following format:
                [0]: unlocked property
            """
            return (self.unlocked,)
        
        def getDayRoom(self, weather=None):
            """
            Returns the day masks to use given the conditions/availablity of present assets
            """
            if weather is None:
                weather = store.mas_current_weather
            
            return self.image_map[weather.precip_type][0]
        
        def getNightRoom(self, weather=None):
            """
            Returns the night masks to use given the conditions/availablity of present assets
            """
            if weather is None:
                weather = store.mas_current_weather
            
            return self.image_map[weather.precip_type][1]
        
        def getRoomForTime(self, weather=None):
            """
            Gets the room for the current time

            IN:
                weather - get the room bg for the time and weather
                (Default: current weather)
            """
            if weather is None:
                weather = store.mas_current_weather
            if store.mas_isMorning():
                return self.getDayRoom(weather)
            return self.getNightRoom(weather)
        
        def isChangingRoom(self, old_weather, new_weather):
            """
            If the room has a different look for the new weather we're going into, the room is "changing" and we need to flag this to
            scene change and dissolve the spaceroom in the spaceroom label
            """
            return self.getRoomForTime(old_weather) != self.getRoomForTime(new_weather)
        
        def isFltDay(self, flt=None):
            """
            Checks if the given filter is considered a "day" filter according
            to this background.

            IN:
                flt - filter to check
                    if None, we use the current filter

            RETURNS: True if flt is a "day" filter according to this bg
            """
            
            
            
            if flt is None:
                flt = store.mas_sprites.get_filter()
            
            return flt == store.mas_sprites.FLT_DAY
        
        def isFltNight(self, flt=None):
            """
            Checks if the given filter is considered a "night" filter according
            to this background.

            IN:
                flt - filter to check
                    if None, we use the current filter

            RETURNS: True if flt is a "night" filter according to this BG
            """
            
            return not self.isFltDay(flt)



init -20 python in mas_background:
    import store
    BACKGROUND_MAP = {}
    BACKGROUND_RETURN = "Nevermind"

    def loadMBGData():
        """
        Loads persistent MASBackground data into the weather map

        ASSUMES: background map is already filled
        """
        if store.persistent._mas_background_MBGdata is None:
            return
        
        for mbg_id, mbg_data in store.persistent._mas_background_MBGdata.iteritems():
            mbg_obj = BACKGROUND_MAP.get(mbg_id, None)
            if mbg_obj is not None:
                mbg_obj.fromTuple(mbg_data)

    def saveMBGData():
        """
        Saves MASBackground data from weather map into persistent
        """
        for mbg_id, mbg_obj in BACKGROUND_MAP.iteritems():
            store.persistent._mas_background_MBGdata[mbg_id] = mbg_obj.toTuple()

    def getUnlockedBGCount():
        """
        Gets the number of unlocked backgrounds
        """
        unlocked_count = 0
        for mbg_obj in BACKGROUND_MAP.itervalues():
            unlocked_count += int(mbg_obj.unlocked)
        
        return unlocked_count


init 800 python:

    def mas_setBackground(_background):
        """
        Sets the initial bg

        NOTE: We don't handle exit pp's here

        IN:
            _background:
                The background we're changing to
        """
        global mas_current_background
        old_background = mas_current_background
        mas_current_background = _background
        mas_current_background.entry(old_background)

    def mas_changeBackground(new_background, by_user=None):
        """
        changes the background w/o any scene changes

        IN:
            new_background:
                The background we're changing to

            by_user:
                If the user switched the background themselves
        """
        if by_user is not None:
            mas_background.force_background = bool(by_user)
        
        mas_current_background.exit(new_background)
        mas_setBackground(new_background)


    mas_current_background = None
    mas_setBackground(mas_background_def)


    if mas_background.getUnlockedBGCount() < 2:
        mas_lockEVL("monika_change_background","EVE")


init -2 python in mas_background:
    import store

    def _def_background_entry(_old):
        """
        Entry programming point for befault background
        """
        if store.seen_event("mas_monika_islands"):
            store.mas_unlockEVL("mas_monika_islands", "EVE")

    def _def_background_exit(_new):
        """
        Exit programming point for befault background
        """
        store.mas_lockEVL("mas_monika_islands", "EVE")



init -1 python:

    mas_background_def = MASBackground(
        
        "spaceroom",
        "Spaceroom",

        
        "monika_day_room",
        "monika_room",

        
        image_rain_day="monika_rain_room",

        image_overcast_day="monika_rain_room",

        image_snow_day="monika_snow_room_day",
        image_snow_night="monika_snow_room_night",

        
        unlocked=True,

        
        entry_pp=store.mas_background._def_background_entry,
        exit_pp=store.mas_background._def_background_exit
    )




image monika_day_room = "mod_assets/location/spaceroom/spaceroom.png"
image monika_room = "mod_assets/location/spaceroom/spaceroom-n.png"

image monika_rain_room = "mod_assets/location/spaceroom/spaceroom_rain.png"

image monika_snow_room_day = "mod_assets/location/spaceroom/spaceroom_snow.png"
image monika_snow_room_night = "mod_assets/location/spaceroom/spaceroom_snow-n.png"


















label monika_change_background:

    m 1hua "Sure!"

label monika_change_background_loop:

    show monika 1eua at t21

    $ renpy.say(m, "Where would you like to go?", interact=False)

    python:

        import store.mas_background as mas_background
        import store.mas_moods as mas_moods



        backgrounds = [(mas_background_def.prompt, mas_background_def, False, False)]


        other_backgrounds = [
            (mbg_obj.prompt, mbg_obj, False, False)
            for mbg_id, mbg_obj in mas_background.BACKGROUND_MAP.iteritems()
            if mbg_id != "spaceroom" and mbg_obj.unlocked
        ]


        other_backgrounds.sort()


        backgrounds.extend(other_backgrounds)


        final_item = (mas_background.BACKGROUND_RETURN, False, False, False, 20)


    call screen mas_gen_scrollable_menu(backgrounds, mas_ui.SCROLLABLE_MENU_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

    $ sel_background = _return

    show monika at t11


    if sel_background is False:
        m 1eka "Oh, alright."
        m "If you want to go somewhere, just ask, okay?"
        return

    if sel_background == mas_current_background:
        m 1hua "We're here right now, silly."
        m "Try again~"
        jump monika_change_background_loop

    call mas_background_change (sel_background) from _call_mas_background_change
    return


label mas_background_change(new_bg, skip_leadin=False, skip_outro=False):

    if not skip_leadin:
        m 1eua "Alright!"
        m 1hua "Let's go, [player]!"


    hide monika
    scene black
    with dissolve
    pause 2.0


    $ mas_changeBackground(new_bg)


    if new_bg.disable_progressive and new_bg.hide_masks:
        $ mas_weather.temp_weather_storage = mas_current_weather
        $ mas_changeWeather(mas_weather_def)
        $ mas_lockEVL("monika_change_weather", "EVE")
    else:

        if mas_weather.temp_weather_storage is not None:
            $ mas_changeWeather(mas_weather.temp_weather_storage)
        else:


            $ set_to_weather = mas_shouldRain()
            if set_to_weather is not None:
                $ mas_changeWeather(set_to_weather)
            else:
                $ mas_changeWeather(mas_weather_def)


        $ mas_unlockEVL("monika_change_weather", "EVE")

    call spaceroom (scene_change=True, dissolve_all=True) from _call_spaceroom_42

    if not skip_outro:
        m 1eua "Here we are!"
        m "Let me know if you want to go somewhere else, okay?"
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
