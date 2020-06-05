





image def_weather_day = Movie(
    channel="window_1",
    play="mod_assets/window/def_day_mask.mp4",
    mask=None
)
image def_weather_day_fb = "mod_assets/window/def_day_mask_fb.png"

image def_weather_night = Movie(
    channel="window_2",
    play="mod_assets/window/def_night_mask.mp4",
    mask=None
)
image def_weather_night_fb = "mod_assets/window/def_night_mask_fb.png"

image rain_weather_day = Movie(
    channel="window_3",
    play="mod_assets/window/rain_day_mask.mpg",
    mask=None
)
image rain_weather_day_fb = "mod_assets/window/rain_day_mask_fb.png"

image rain_weather_night = Movie(
    channel="window_4",
    play="mod_assets/window/rain_night_mask.mpg",
    mask=None
)
image rain_weather_night_fb = "mod_assets/window/rain_night_mask_fb.png"

image overcast_weather_day = Movie(
    channel="window_5",
    play="mod_assets/window/overcast_day_mask.mpg",
    mask=None
)
image overcast_weather_day_fb = "mod_assets/window/overcast_day_mask_fb.png"

image overcast_weather_night = Movie(
    channel="window_6",
    play="mod_assets/window/overcast_night_mask.mpg",
    mask=None
)
image overcast_weather_night_fb = "mod_assets/window/overcast_night_mask_fb.png"

image snow_weather_day = Movie(
    channel="window_7",
    play="mod_assets/window/snow_day_mask.mp4",
    mask=None
)
image snow_weather_day_fb = "mod_assets/window/snow_day_mask_fb.png"

image snow_weather_night = Movie(
    channel="window_8",
    play="mod_assets/window/snow_night_mask.mp4",
    mask=None
)
image snow_weather_night_fb = "mod_assets/window/snow_night_mask_fb.png"










image mas_island_frame_day = "mod_assets/location/special/with_frame.png"
image mas_island_day = "mod_assets/location/special/without_frame.png"
image mas_island_frame_night = "mod_assets/location/special/night_with_frame.png"
image mas_island_night = "mod_assets/location/special/night_without_frame.png"
image mas_island_frame_rain = "mod_assets/location/special/rain_with_frame.png"
image mas_island_rain = "mod_assets/location/special/rain_without_frame.png"
image mas_island_frame_rain_night = "mod_assets/location/special/night_rain_with_frame.png"
image mas_island_rain_night = "mod_assets/location/special/night_rain_without_frame.png"
image mas_island_frame_overcast = "mod_assets/location/special/overcast_with_frame.png"
image mas_island_overcast = "mod_assets/location/special/overcast_without_frame.png"
image mas_island_frame_overcast_night = "mod_assets/location/special/night_overcast_with_frame.png"
image mas_island_overcast_night = "mod_assets/location/special/night_overcast_without_frame.png"
image mas_island_frame_snow = "mod_assets/location/special/snow_with_frame.png"
image mas_island_snow = "mod_assets/location/special/snow_without_frame.png"
image mas_island_frame_snow_night = "mod_assets/location/special/night_snow_with_frame.png"
image mas_island_snow_night = "mod_assets/location/special/night_snow_without_frame.png"







default persistent._mas_weather_MWdata = {}



default persistent._mas_date_last_checked_rain = None


default persistent._mas_should_rain_today = None


init python in mas_weather:

    def shouldRainToday():
        
        
        if store.mas_pastOneDay(store.persistent._mas_date_last_checked_rain):
            store.persistent._mas_date_last_checked_rain = datetime.date.today()
            
            
            chance = random.randint(1,100)
            
            
            
            
            
            
            
            
            
            
            if store.mas_isSpring():
                store.persistent._mas_should_rain_today = chance >= 30
            elif store.mas_isSummer():
                store.persistent._mas_should_rain_today = chance >= 85
            elif store.mas_isFall():
                store.persistent._mas_should_rain_today = chance >= 40
            else:
                store.persistent._mas_should_rain_today = False
        
        return store.persistent._mas_should_rain_today


    def _determineCloudyWeather(
            rain_chance,
            thunder_chance,
            overcast_chance,
            rolled_chance=None
        ):
        """
        Determines if weather should be rainiy/thunder/overcase, or none of
        those.

        IN:
            rain_chance - chance of rain out of 100
            thunder_chance - chance of thunder out of 100
                NOTE: this should be percentage based on rain chance, i.e.:
                thunder_chance * (rain_chance as %)
            overcast_chance - chance of overcast out of 100
            rolled_chance - if passed, then we use that chance instead of
                generating a random chance. None means we generate our
                own chance.
                (Default: None)

        RETURNS:
            appropriate weather type, or None if neither of these weathers.
        """
        if rolled_chance is None:
            rolled_chance = random.randint(1,100)
        
        if shouldRainToday():
            
            
            if rolled_chance <= rain_chance:
                
                
                if rolled_chance <= thunder_chance:
                    return store.mas_weather_thunder
                
                
                return store.mas_weather_rain
            
            
            
            rolled_chance -= rain_chance
        
        if rolled_chance <= overcast_chance:
            return store.mas_weather_overcast
        
        
        return None


init -20 python in mas_weather:
    import random
    import datetime
    import store


    force_weather = False


    WEATHER_MAP = {}



    WEAT_RETURN = "Nevermind"


    weather_change_time = None


    PRECIP_TYPE_DEF = "def"
    PRECIP_TYPE_RAIN = "rain"
    PRECIP_TYPE_OVERCAST = "overcast"
    PRECIP_TYPE_SNOW = "snow"


    temp_weather_storage = None












    def weatherProgress():
        """
        Runs a roll on mas_shouldRain() to pick a new weather to change to after a time between half an hour - one and a half hour

        RETURNS:
            - True or false on whether or not to call spaceroom
        """
        
        
        if force_weather or store.mas_current_background.disable_progressive:
            return False
        
        
        global weather_change_time
        
        if not weather_change_time:
            
            weather_change_time = datetime.datetime.now() + datetime.timedelta(0,random.randint(1800,5400))
        
        elif weather_change_time < datetime.datetime.now():
            
            weather_change_time = datetime.datetime.now() + datetime.timedelta(0,random.randint(1800,5400))
            
            
            new_weather = store.mas_shouldRain()
            if new_weather is not None and new_weather != store.mas_current_weather:
                
                if store.mas_current_background.isChangingRoom(
                        store.mas_current_weather,
                        new_weather
                ):
                    store.mas_idle_mailbox.send_scene_change()
                
                
                store.mas_changeWeather(new_weather)
                
                
                if new_weather == store.mas_weather_thunder:
                    renpy.play("mod_assets/sounds/amb/thunder_1.wav",channel="backsound")
                return True
            
            elif store.mas_current_weather != store.mas_weather_def:
                
                if store.mas_current_background.isChangingRoom(
                        store.mas_current_weather,
                        store.mas_weather_def
                ):
                    store.mas_idle_mailbox.send_scene_change()
                
                store.mas_changeWeather(store.mas_weather_def)
                return True
        
        return False


    def loadMWData():
        """
        Loads persistent MASWeather data into the weather map

        ASSUMES: weather map is already filled
        """
        if store.persistent._mas_weather_MWdata is None:
            return
        
        for mw_id, mw_data in store.persistent._mas_weather_MWdata.iteritems():
            mw_obj = WEATHER_MAP.get(mw_id, None)
            if mw_obj is not None:
                mw_obj.fromTuple(mw_data)


    def saveMWData():
        """
        Saves MASWeather data from weather map into persistent
        """
        for mw_id, mw_obj in WEATHER_MAP.iteritems():
            store.persistent._mas_weather_MWdata[mw_id] = mw_obj.toTuple()


    def unlockedWeathers():
        """
        Returns number of unlocked weather items
        """
        count = 0
        for mw_id, mw_obj in WEATHER_MAP.iteritems():
            if mw_obj.unlocked:
                count += 1
        
        return count






    def _weather_rain_entry(_old):
        """
        Rain start programming point
        """
        
        
        if _old != store.mas_weather_thunder:
            
            
            store.mas_is_raining = True
            
            
            renpy.music.play(
                store.audio.rain,
                channel="background",
                loop=True,
                fadein=1.0,
                if_changed=True
            )


    def _weather_rain_exit(_new):
        """
        RAIN stop programming point
        """
        
        
        if _new != store.mas_weather_thunder:
            
            store.mas_is_raining = False
            
            
            renpy.music.stop(channel="background", fadeout=1.0)


    def _weather_snow_entry(_old):
        """
        Snow entry programming point
        """
        
        store.mas_is_snowing = True
        
        
        
        if (
            store.mas_current_background.isFltNight()
            and not store.persistent.event_list
            and store.mas_getEV("monika_auroras").shown_count == 0
        ):
            store.queueEvent("monika_auroras", notify=True)


    def _weather_snow_exit(_new):
        """
        Snow exit programming point
        """
        
        store.mas_is_snowing = False


    def _weather_thunder_entry(_old):
        """
        Thunder entry programming point
        """
        
        
        if _old != store.mas_weather_rain:
            _weather_rain_entry(_old)
        
        
        store.mas_globals.show_lightning = True


    def _weather_thunder_exit(_new):
        """
        Thunder exit programming point
        """
        
        store.mas_globals.show_lightning = False
        
        
        
        if _new != store.mas_weather_rain:
            _weather_rain_exit(_new)


    def _weather_overcast_entry(_old):
        """
        Overcast entry programming point
        """
        pass

    def _weather_overcast_exit(_new):
        """
        Overcast exit programming point
        """
        pass


init -10 python:

    class MASWeather(object):
        """
        Weather class to determine some props for weather

        PROPERTIES:
            weather_id - Id that defines this weather object
            prompt - button label for this weater
            unlocked - determines if this weather is unlocked/selectable
            sp_day - image tag for windows in day time
            sp_night - image tag for windows in nighttime
            precip_type - type of precipitation (to use for the room type)
            isbg_wf_day - image PATH for islands bg daytime with frame
            isbg_wof_day = image PATH for islands bg daytime without frame
            isbg_wf_night - image PATH for island bg nighttime with frame
            isbg_wof_night - image PATH for island bg nighttime without framme

            entry_pp - programming point to execute when switching to this
                weather
            exit_pp - programming point to execute when leaving this weather

        NOTE: for all image tags, `_fb` is appeneded for fallbacks
        """
        import store.mas_weather as mas_weather
        
        def __init__(
                self,
                weather_id,
                prompt,
                sp_day,
                sp_night=None,
                precip_type=store.mas_weather.PRECIP_TYPE_DEF,
                isbg_wf_day=None,
                isbg_wof_day=None,
                isbg_wf_night=None,
                isbg_wof_night=None,
                entry_pp=None,
                exit_pp=None,
                unlocked=False
            ):
            """
            Constructor for a MASWeather object

            IN:
                weather_id - id that defines this weather object
                    NOTE: must be unique
                prompt - button label for this weathe robject
                sp_day - image tag for spaceroom's left window in daytime
                unlocked - True if this weather object starts unlocked,
                    False otherwise
                    (Default: False)
                sp_night - image tag for spaceroom's left window in night
                    If None, we use sp_day for this
                    (Default: None)
                precip_type - type of precipitation, def, rain, overcast, or snow
                    (Default: def)
                isbg_wf_day - image PATH for islands bg daytime with frame
                    (Default: None)
                isbg_wof_day = image PATH for islands bg daytime without frame
                    (Default: None)
                isbg_wf_night - image PATH for island bg nighttime with frame
                    If None, we use isbg_wf_day
                    (Default: None)
                isbg_wof_night - image PATH for island bg nighttime without
                    framme
                    If None, we use isbg_wof_day
                    (Default: None)
                entry_pp - programming point to execute after switching to
                    this weather
                    (Default: None)
                exit_pp - programming point to execute before leaving this
                    weather
                    (Default: None)

                #NOTE: Defaulting to the day frame stuff to avoid tracebacks
            """
            if weather_id in self.mas_weather.WEATHER_MAP:
                raise Exception("duplicate weather ID")
            
            self.weather_id = weather_id
            self.prompt = prompt
            self.sp_day = sp_day
            self.sp_night = sp_night
            self.precip_type = precip_type
            self.isbg_wf_day = isbg_wf_day
            self.isbg_wof_day = isbg_wof_day
            self.isbg_wf_night = isbg_wf_night
            self.isbg_wof_night = isbg_wof_night
            self.unlocked = unlocked
            self.entry_pp = entry_pp
            self.exit_pp = exit_pp
            
            
            if sp_night is None:
                self.sp_night = sp_day
            
            
            if isbg_wf_night is None:
                self.isbg_wf_night = isbg_wf_day
            
            if isbg_wof_night is None:
                self.isbg_wof_night = isbg_wof_day
            
            
            self.mas_weather.WEATHER_MAP[weather_id] = self
        
        
        def __eq__(self, other):
            if isinstance(other, MASWeather):
                return self.weather_id == other.weather_id
            return NotImplemented
        
        
        def __ne__(self, other):
            result = self.__eq__(other)
            if result is NotImplemented:
                return result
            return not result
        
        
        def entry(self, old_weather):
            """
            Runs entry programming point
            """
            if self.entry_pp is not None:
                self.entry_pp(old_weather)
        
        
        def exit(self, new_weather):
            """
            Runs exit programming point
            """
            if self.exit_pp is not None:
                self.exit_pp(new_weather)
        
        
        def fromTuple(self, data_tuple):
            """
            Loads data from tuple

            IN:
                data_tuple - tuple of the following format:
                    [0]: unlocked property
            """
            self.unlocked = data_tuple[0]
        
        
        def sp_window(self, day):
            """
            Returns spaceroom masks for window

            IN:
                day - True if we want day time masks

            RETURNS:
                image tag for the corresponding mask to use
            """
            
            if day:
                return self.sp_day
            
            return self.sp_night
        
        
        def isbg_window(self, day, no_frame):
            """
            Returns islands bg PATH for window

            IN:
                day - True if we want daytime bg
                no_frame - True if we want no frame
            """
            if day:
                if no_frame:
                    return self.isbg_wof_day
                
                return self.isbg_wf_day
            
            
            if no_frame:
                return self.isbg_wof_night
            
            return self.isbg_wf_night
        
        
        def toTuple(self):
            """
            Converts this MASWeather object into a tuple

            RETURNS: tuple of the following format:
                [0]: unlocked property
            """
            return (self.unlocked,)




init -1 python:


    mas_weather_def = MASWeather(
        "def",
        "Clear",

        
        "def_weather_day",

        
        "def_weather_night",

        precip_type=store.mas_weather.PRECIP_TYPE_DEF,

        
        isbg_wf_day="mod_assets/location/special/with_frame.png",
        isbg_wof_day="mod_assets/location/special/without_frame.png",

        
        isbg_wf_night="mod_assets/location/special/night_with_frame.png",
        isbg_wof_night="mod_assets/location/special/night_without_frame.png",

        unlocked=True
    )


    mas_weather_rain = MASWeather(
        "rain",
        "Rain",

        
        "rain_weather_day",

        
        "rain_weather_night",

        precip_type=store.mas_weather.PRECIP_TYPE_RAIN,

        
        isbg_wf_day="mod_assets/location/special/rain_with_frame.png",
        isbg_wof_day="mod_assets/location/special/rain_without_frame.png",

        
        isbg_wf_night="mod_assets/location/special/night_rain_with_frame.png",
        isbg_wof_night="mod_assets/location/special/night_rain_without_frame.png",

        entry_pp=store.mas_weather._weather_rain_entry,
        exit_pp=store.mas_weather._weather_rain_exit,

        unlocked=True
    )


    mas_weather_snow = MASWeather(
        "snow",
        "Snow",

        
        "snow_weather_day",

        
        "snow_weather_night",

        precip_type=store.mas_weather.PRECIP_TYPE_SNOW,

        
        isbg_wf_day="mod_assets/location/special/snow_with_frame.png",
        isbg_wof_day="mod_assets/location/special/snow_without_frame.png",

        
        isbg_wf_night="mod_assets/location/special/night_snow_with_frame.png",
        isbg_wof_night="mod_assets/location/special/night_snow_without_frame.png",

        entry_pp=store.mas_weather._weather_snow_entry,
        exit_pp=store.mas_weather._weather_snow_exit,

        unlocked=True
    )


    mas_weather_thunder = MASWeather(
        "thunder",
        "Thunder/Lightning",

        
        "rain_weather_day",

        
        "rain_weather_night",

        precip_type=store.mas_weather.PRECIP_TYPE_RAIN,

        
        isbg_wf_day="mod_assets/location/special/rain_with_frame.png",
        isbg_wof_day="mod_assets/location/special/rain_without_frame.png",

        
        isbg_wf_night="mod_assets/location/special/night_rain_with_frame.png",
        isbg_wof_night="mod_assets/location/special/night_rain_without_frame.png",

        entry_pp=store.mas_weather._weather_thunder_entry,
        exit_pp=store.mas_weather._weather_thunder_exit,

        unlocked=True
    )


    mas_weather_overcast = MASWeather(
        "overcast",
        "Overcast",

        
        "overcast_weather_day",

        
        "overcast_weather_night",

        precip_type=store.mas_weather.PRECIP_TYPE_OVERCAST,

        
        isbg_wf_day="mod_assets/location/special/overcast_with_frame.png",
        isbg_wof_day="mod_assets/location/special/overcast_without_frame.png",

        
        isbg_wf_night="mod_assets/location/special/night_overcast_with_frame.png",
        isbg_wof_night="mod_assets/location/special/night_overcast_without_frame.png",

        entry_pp=store.mas_weather._weather_overcast_entry,
        exit_pp=store.mas_weather._weather_overcast_exit,

        unlocked=True
    )




    store.mas_weather.loadMWData()


init 800 python:

    def mas_setWeather(_weather):
        """
        Sets the initial weather.
        This is meant for startup/ch30_reset

        NOTE: this does NOt call exit programming points

        IN:
            _weather - weather to set to.
        """
        global mas_current_weather
        old_weather = mas_current_weather
        mas_current_weather = _weather
        mas_current_weather.entry(old_weather)


    def mas_changeWeather(new_weather, by_user=None):
        """
        Changes weather without doing scene changes

        NOTE: this does NOT do scene change/spaceroom

        IN:
            new_weather - weather to change to
            by_user - flag for if user changes weather or not
        """
        
        if by_user is not None:
            mas_weather.force_weather = bool(by_user)
        
        mas_current_weather.exit(new_weather)
        mas_setWeather(new_weather)



    mas_current_weather = None
    mas_setWeather(mas_weather_def)










label mas_change_weather(new_weather, by_user=None):

    if by_user is not None:
        $ mas_weather.force_weather = bool(by_user)


    $ mas_current_weather.exit(new_weather)


    $ old_weather = mas_current_weather
    $ mas_current_weather = new_weather





    $ mas_current_weather.entry(old_weather)

    call spaceroom (scene_change=True, dissolve_all=True, force_exp="monika 1dsc_static") from _call_spaceroom_7

    return

init 5 python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_change_weather",
            category=["weather"],
            prompt="Can you change the weather?",
            pool=True,
            unlocked=True,
            rules={"no unlock": None},
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label monika_change_weather:
    show monika 1eua at t21

    $ renpy.say(m, "What kind of weather would you like?", interact=False)

    python:

        import store.mas_weather as mas_weather
        import store.mas_moods as mas_moods



        weathers = [(mas_weather_def.prompt, mas_weather_def, False, False)]


        other_weathers = [
            (mw_obj.prompt, mw_obj, False, False)
            for mw_id, mw_obj in mas_weather.WEATHER_MAP.iteritems()
            if mw_id != "def" and mw_obj.unlocked
        ]


        other_weathers.sort()


        weathers.extend(other_weathers)


        weathers.append(("Progressive","auto",False,False))


        final_item = (mas_weather.WEAT_RETURN, False, False, False, 20)


    call screen mas_gen_scrollable_menu(weathers, mas_ui.SCROLLABLE_MENU_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

    $ sel_weather = _return


    if sel_weather is False:
        return "prompt"

    elif sel_weather == "auto":
        show monika at t11
        if mas_weather.force_weather:
            m 1hub "Sure!"
            m 1dsc "Just give me a second.{w=0.5}.{w=0.5}.{nw}"


            $ mas_weather.force_weather = False
            m 1eua "There we go!"
        else:
            m 1hua "That's the current weather, silly."
            m "Try again~"
            jump monika_change_weather
        return

    if sel_weather == mas_current_weather and mas_weather.force_weather:
        m 1hua "That's the current weather, silly."
        m "Try again~"
        jump monika_change_weather

    $ skip_outro = False
    $ skip_leadin = False



    if sel_weather == mas_weather_rain or sel_weather == mas_weather_thunder:
        if not renpy.seen_label("monika_rain"):
            $ pushEvent("monika_rain")
            $ skip_outro = True

        elif persistent._mas_pm_likes_rain is False:
            m 1eka "I thought you didn't like rain."
            m 2etc "Maybe you changed your mind?"
            m 1dsc "..."
            $ skip_leadin = True



    if not skip_leadin:
        show monika at t11
        m 1eua "Alright!"
        m 1dsc "Just give me a second.{w=0.5}.{w=0.5}.{nw}"


    call mas_change_weather (sel_weather, by_user=True) from _call_mas_change_weather

    if not skip_outro:
        m 1eua "There we go!"

    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
