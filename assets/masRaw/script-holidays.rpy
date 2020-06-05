













default persistent._mas_event_clothes_map = dict()
define mas_five_minutes = datetime.timedelta(seconds=5*60)
define mas_one_hour = datetime.timedelta(seconds=3600)
define mas_three_hour = datetime.timedelta(seconds=3*3600)

init 10 python:
    def mas_addClothesToHolidayMap(clothes, key=None):
        """
        Adds the given clothes to the holiday clothes map

        IN:
            clothes - clothing item to add
            key - dateime.date to use as key. If None, we use today
        """
        if clothes is None:
            return
        
        if key is None:
            key = datetime.date.today()
        
        persistent._mas_event_clothes_map[key] = clothes.name
        
        
        mas_unlockEVL("monika_event_clothes_select", "EVE")

    def mas_addClothesToHolidayMapRange(clothes, start_date, end_date):
        """
        Adds the given clothes to the holiday clothes map over the day range provided

        IN:
            clothes - clothing item to add
            start_date - datetime.date to start adding to the map on
            end_date - datetime.date to stop adding to the map on
        """
        if not clothes:
            return
        
        
        daterange = mas_genDateRange(start_date, end_date)
        
        
        for date in daterange:
            mas_addClothesToHolidayMap(clothes, date)

init -1 python:
    def mas_checkOverDate(_date):
        """
        Checks if the player was gone over the given date entirely (taking you somewhere)

        IN:
            date - a datetime.date of the date we want to see if we've been out all day for

        OUT:
            True if the player and Monika were out together the whole day, False if not.
        """
        checkout_time = store.mas_dockstat.getCheckTimes()[0]
        return checkout_time is not None and checkout_time.date() < _date


    def mas_capGainAff(amount, aff_gained_var, normal_cap, pbday_cap=None):
        """
        Gains affection according to the cap(s) defined

        IN:
            amount:
                Amount of affection to gain

            aff_gained_var:
                The persistent variable which the total amount gained for the holiday is stored
                (NOTE: Must be a string)

            normal_cap:
                The cap to use when not player bday

            pbday_cap:
                The cap to use when it's player bday (NOTE: if not provided, normal_cap is assumed)
        """
        
        
        if persistent._mas_player_bday_in_player_bday_mode and pbday_cap:
            cap = pbday_cap
        else:
            cap = normal_cap
        
        if persistent.__dict__[aff_gained_var] < cap:
            persistent.__dict__[aff_gained_var] += amount
            mas_gainAffection(amount, bypass=True)
        
        return

    def mas_hasSpecialOutfit(_date=None):
        """
        Checks if the given date is a special event that has an outfit in the event clothes map
        IN:
            _date - date to check.
                (Default: None)

        RETURNS: True if given date has a special outfit, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date in persistent._mas_event_clothes_map

init -10 python:
    def mas_isA01(_date=None):
        if _date is None:
            _date = datetime.date.today()
        
        return _date == datetime.date(_date.year,4,1)


label mas_lingerie_intro(holiday_str, lingerie_choice):
    m 1ekbfa "..."
    m "Also, [player]..."
    m 3ekbfsdla "There's...{w=1}s-something I want to show you."
    m 2rkbfsdla "I've been wanting to do this for a while now actually, but...{w=1}well it's kind of embarrassing..."
    m "..."
    m 2hkbfsdlb "Oh gosh, I'm super nervous, ahaha!"
    m 2rkbfsdlc "It's just I've never--{nw}"
    m 2dkbfsdlc "Ah, okay, time to stop stalling and just do it."
    m 2ekbfsdla "Just give me a few seconds, [player]."
    call mas_clothes_change (outfit=lingerie_choice, outfit_mode=True, exp="monika 2rkbfsdlu", restore_zoom=False, unlock=True) from _call_mas_clothes_change
    pause 3.0
    m 2ekbfsdlb "Ahaha, [player]...{w=1}you're staring..."
    m 2ekbfu "Well...{w=1}do you like what you see?"
    m 1lkbfa "I've never really...{w=1}worn anything like this before."
    m "...At least not that anyone's seen."

    if mas_hasUnlockedClothesWithExprop("bikini"):
        m 3hkbfb "Ahaha, what am I saying, you've seen me in a bikini before, which is essentially the same thing..."
        m 2rkbfa "...Though for some reason this just feels...{w=0.5}{i}different{/i}."

    m 2ekbfa "Anyway, something about being with you on [holiday_str] seems really romantic, you know?"
    m "It just felt like the perfect time for the next step in our relationship."
    m 2rkbfsdlu "Now I know that we can't really--{nw}"
    m 3hubfb "Ah! Nevermind, ahaha!"
    return





default persistent._mas_o31_in_o31_mode = False


default persistent._mas_o31_tt_count = 0


default persistent._mas_o31_trick_or_treating_aff_gain = 0


default persistent._mas_o31_relaunch = False




default persistent._mas_o31_costumes_worn = {}


define mas_o31 = datetime.date(datetime.date.today().year, 10, 31)

init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "o31",
        
        
        datetime.datetime(2020, 1, 6),
        {
            
            "_mas_o31_in_o31_mode": "o31.mode.o31",
            "_mas_o31_tt_count": "o31.tt.count",
            "_mas_o31_relaunch": "o31.relaunch",
            "_mas_o31_trick_or_treating_aff_gain": "o31.actions.tt.aff_gain"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2019, 10, 31),

        
        end_dt=datetime.datetime(2019, 11, 2)
    ))



image mas_o31_deco = ConditionSwitch(
    "mas_current_background.isFltDay()",
    "mod_assets/location/spaceroom/o31/halloween_deco.png",
    "True", "mod_assets/location/spaceroom/o31/halloween_deco-n.png"
)


init -10 python:
    import random

    def mas_isO31(_date=None):
        """
        Returns True if the given date is o31

        IN:
            _date - date to check.
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is o31, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_o31.replace(year=_date.year)

    def mas_o31ShowVisuals():
        """
        Shows o31 visuals
        """
        renpy.show("mas_o31_deco", zorder=7)

    def mas_o31HideVisuals():
        """
        Hides o31 visuals + vignette
        """
        renpy.hide("mas_o31_deco")
        renpy.hide("vignette")
        
        store.mas_globals.show_vignette = False
        
        store.persistent._mas_o31_in_o31_mode = False
        
        
        hair = store.mas_selspr.get_sel_hair(store.mas_hair_down)
        if hair is not None and not hair.unlocked:
            store.mas_unlockEVL("greeting_hairdown", "GRE")
        
        
        store.mas_lockEVL("monika_event_clothes_select", "EVE")
        
        
        if store.monika_chr.is_wearing_clothes_with_exprop("costume"):
            store.queueEvent('mas_change_to_def')

    def mas_o31CapGainAff(amount):
        mas_capGainAff(amount, "_mas_o31_trick_or_treating_aff_gain", 15)


    def mas_o31CostumeWorn(clothes):
        """
        Checks if the given clothes was worn on o31

        IN:
            clothes - Clothes object to check

        RETURNS: year the given clothe was worn if worn on o31, None if never
            worn on o31.
        """
        if clothes is None:
            return False
        return mas_o31CostumeWorn_n(clothes.name)


    def mas_o31CostumeWorn_n(clothes_name):
        """
        Checks if the given clothes (name) was worn on o31

        IN:
            clothes_name - Clothes name to check

        RETURNS: year the given clothes name was worn if worn on o31, none if
            never worn on o31.
        """
        return persistent._mas_o31_costumes_worn.get(clothes_name, None)


    def mas_o31SelectCostume(selection_pool=None):
        """
        Selects an o31 costume to wear. Costumes that have not been worn
        before are selected first.

        NOTE: o31 costume wear flag is NOT set here. Make sure to set this
            manually later.

        IN:
            selection_pool - pool to select clothes from. If NOne, we get a
                default list of clothes with costume exprop

        RETURNS: a single MASClothes object of what to wear. None if cannot
            return anything.
        """
        if selection_pool is None:
            selection_pool = MASClothes.by_exprop("costume", "o31")
        
        
        wearing_costume = False
        
        
        
        
        
        filt_sel_pool = []
        for cloth in selection_pool:
            sprite_key = (store.mas_sprites.SP_CLOTHES, cloth.name)
            giftname = store.mas_sprites_json.namegift_map.get(
                sprite_key,
                None
            )
            
            if (
                giftname is None
                or sprite_key in persistent._mas_sprites_json_gifted_sprites
            ):
                if cloth != monika_chr.clothes:
                    filt_sel_pool.append(cloth)
                else:
                    wearing_costume = True
        
        
        selection_pool = filt_sel_pool
        
        if len(selection_pool) < 1:
            
            
            if wearing_costume:
                return monika_chr.clothes
            
            return None
        
        elif len(selection_pool) < 2:
            
            return selection_pool[0]
        
        
        non_worn = [
            costume
            for costume in selection_pool
            if not mas_o31CostumeWorn(costume)
        ]
        
        if len(non_worn) > 0:
            
            return random.choice(non_worn)
        
        
        return random.choice(selection_pool)


    def mas_o31SetCostumeWorn(clothes, year=None):
        """
        Sets that a clothing item is worn. Exprop checking is done

        IN:
            clothes - clothes object to set
            year - year that the costume was worn. If NOne, we use current year
        """
        if clothes is None or not clothes.hasprop("costume"):
            return
        
        mas_o31SetCostumeWorn_n(clothes.name, year=year)


    def mas_o31SetCostumeWorn_n(clothes_name, year=None):
        """
        Sets that a clothing name is worn. NO EXPROP CHECKING IS DONE

        IN:
            clothes_name - name of clothes to set
            year - year that the costume was worn. If None, we use current year
        """
        if year is None:
            year = datetime.date.today().year
        
        persistent._mas_o31_costumes_worn[clothes_name] = year



label mas_o31_autoload_check:
    python:
        import random

        if mas_isO31() and mas_isMoniNormal(higher=True):
            
            if (not persistent._mas_o31_in_o31_mode and not mas_isFirstSeshDay()):
                
                mas_skip_visuals = True
                
                
                mas_resetIdleMode()
                
                
                mas_lockEVL("greeting_hairdown", "GRE")
                
                
                store.mas_hotkeys.music_enabled = False
                
                
                mas_calRaiseOverlayShield()
                
                
                
                costume = mas_o31SelectCostume()
                store.mas_selspr.unlock_clothes(costume)
                mas_addClothesToHolidayMap(costume)
                mas_o31SetCostumeWorn(costume)
                
                
                ribbon_acs = monika_chr.get_acs_of_type("ribbon")
                if ribbon_acs is not None:
                    monika_chr.remove_acs(ribbon_acs)
                
                monika_chr.change_clothes(
                    costume,
                    by_user=False,
                    outfit_mode=True
                )
                
                
                store.mas_selspr.save_selectables()
                
                
                renpy.save_persistent()
                
                
                greet_label = "greeting_o31_{0}".format(costume.name)
                
                if renpy.has_label(greet_label):
                    selected_greeting = greet_label
                else:
                    selected_greeting = "greeting_o31_generic"
                
                
                store.mas_sprites.reset_zoom()
                
                
                persistent._mas_o31_in_o31_mode = True
                
                
                store.mas_globals.show_vignette = True
                
                
                mas_changeWeather(mas_weather_thunder, True)
            
            elif (persistent._mas_o31_in_o31_mode and not mas_isFirstSeshDay()):
                
                store.mas_globals.show_vignette = True
                mas_changeWeather(mas_weather_thunder, True)


        elif not mas_isO31() or mas_isMoniDis(lower=True):
            
            if monika_chr.is_wearing_clothes_with_exprop("costume"):
                monika_chr.change_clothes(mas_clothes_def, outfit_mode=True)
                monika_chr.reset_hair()
            
            
            persistent._mas_o31_in_o31_mode = False
            
            
            hair = store.mas_selspr.get_sel_hair(mas_hair_down)
            if hair is not None and not hair.unlocked:
                mas_unlockEVL("greeting_hairdown", "GRE")
            
            
            mas_lockEVL("monika_event_clothes_select", "EVE")


        elif persistent._mas_o31_in_o31_mode and mas_isMoniUpset():
            store.mas_globals.show_vignette = True
            mas_changeWeather(mas_weather_thunder, True)


    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        call mas_player_bday_autoload_check from _call_mas_player_bday_autoload_check

    if mas_skip_visuals:
        jump ch30_post_restartevent_check


    jump mas_ch30_post_holiday_check


label mas_holiday_o31_returned_home_relaunch:
    m 1eua "So, today is..."
    m 1euc "...wait."
    m "..."
    m 2wuo "Oh!"
    m 2wuw "Oh my gosh!"
    m 2hub "It's Halloween already, [player]."
    m 1eua "...{w=1}Say."
    m 3eua "I'm going to close the game."
    m 1eua "After that you can reopen it."
    m 1hubfa "I have something special in store for you, ehehe~"
    $ persistent._mas_o31_relaunch = True
    return "quit"


image mas_o31_marisa_cg = "mod_assets/monika/cg/o31_marisa_cg.png"


image mas_o31_rin_cg = "mod_assets/monika/cg/o31_rin_cg.png"


transform mas_o31_cg_scroll:
    xanchor 0.0 xpos 0 yanchor 0.0 ypos 0.0 yoffset -1520
    ease 20.0 yoffset 0.0


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_marisa",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_marisa:

    $ store.mas_selspr.unlock_acs(mas_acs_marisa_witchhat)
    $ store.mas_selspr.unlock_hair(mas_hair_downtiedstrand)


    if store.mas_o31_event.o31_cg_decoded:


        call spaceroom (hide_monika=True, scene_change=True) from _call_spaceroom_8
    else:



        call spaceroom (dissolve_all=True, scene_change=True, force_exp='monika 1eua_static') from _call_spaceroom_9

    m 1eua "Ah!"
    m 1hua "Seems like my spell worked."
    m 3efu "As my newly summoned servant, you'll have to do my bidding until the very end!"
    m 1rksdla "..."
    m 1hub "Ahaha!"


    if store.mas_o31_event.o31_cg_decoded:
        $ cg_delay = datetime.timedelta(seconds=20)


        m "I'm over here, [player]~"
        window hide

        show mas_o31_marisa_cg zorder 20 at mas_o31_cg_scroll with dissolve
        $ start_time = datetime.datetime.now()

        while datetime.datetime.now() - start_time < cg_delay:
            pause 1.0

        hide emptydesk
        show monika 1hua zorder MAS_MONIKA_Z at i11
        window auto
        m "Tadaa!~"


    m 1hua "Well..."
    m 1wub "What do you think?"
    m 1wua "Suits me pretty well, right?"
    m 1eua "It took me quite a while to make this costume, you know."
    m 3hksdlb "Getting the right measurements, making sure nothing was too tight or loose, that sort of stuff."
    m 3eksdla "Especially the hat!"
    m 1dkc "The ribbon wouldn't stay still at all..."
    m 1rksdla "Luckily I got that sorted out."
    m 3hua "I'd say I did a good job myself."
    m 1hub "Ehehe~"
    m 3eka "I'm wondering if you'll be able to see what's different today."
    m "Besides my costume of course~"
    m 1hua "But anyway..."

    if store.mas_o31_event.o31_cg_decoded:
        show monika 1eua
        hide mas_o31_marisa_cg with dissolve

    m 3ekbfa "I'm really excited to spend Halloween with you."
    m 1hua "Let's have fun today!"

    call greeting_o31_cleanup from _call_greeting_o31_cleanup
    return

init 5 python:
    addEvent(
       Event(
           persistent.greeting_database,
           eventlabel="greeting_o31_rin",
           category=[store.mas_greetings.TYPE_HOL_O31]
       ),
       code="GRE"
    )

label greeting_o31_rin:
    $ title_cased_hes = hes.capitalize()


    call spaceroom (hide_monika=True, scene_change=True) from _call_spaceroom_10

    m "Ugh, I hope I got these braids right."
    m "Why does this costume have to be so complicated...?"
    m "Oh shoot! [title_cased_hes] here!"
    window hide
    pause 3.0

    if store.mas_o31_event.o31_cg_decoded:
        $ cg_delay = datetime.timedelta(seconds=20)


        window auto
        m "Say, [player]..."
        window hide

        show mas_o31_rin_cg zorder 20 at mas_o31_cg_scroll with dissolve
        $ start_time = datetime.datetime.now()

        while datetime.datetime.now() - start_time < cg_delay:
            pause 1.0

        hide emptydesk
        window auto
        m "What do {i}nya{/i} think?"

        scene black
        pause 2.0
        call spaceroom (scene_change=True, dissolve_all=True, force_exp='monika 1hksdlb_static') from _call_spaceroom_11
        m 1hksdlb "Ahaha, saying that out loud was more embarrassing than I thought..."
    else:

        call mas_transition_from_emptydesk ("monika 1eua") from _call_mas_transition_from_emptydesk_4
        m 1hub "Hi, [player]!"
        m 3hub "Do you like my costume?"


    m 3etc "Honestly, I don't even know who this is supposed to be."
    m 3etd "I just found it in the closet with a note attached that had the word 'Rin', a drawing of a girl pushing a wheelbarrow, and some blue floaty thingies."
    m 1euc "Along with instructions on how to style your hair to go along with this outfit."
    m "Judging by these cat ears, I'm guessing this character is a catgirl."
    m 1dtc "But why would she push a wheelbarrow around?"
    pause 1.0
    m 1hksdlb "Anyway, it was a pain getting my hair done."
    m 1eub "So I hope you like the costume!"

    call greeting_o31_cleanup from _call_greeting_o31_cleanup_1
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_orcaramelo_hatsune_miku",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_orcaramelo_hatsune_miku:
    if not persistent._mas_o31_relaunch:
        call spaceroom (hide_monika=True, scene_change=True, dissolve_all=True) from _call_spaceroom_12

        m "{i}~Don't forget my voice~{/i}"
        m "{i}~My signal crosses dimensions~{/i}"
        m "{i}~Don't call me virtual~{/i}"
        m "{i}~I still want to be l-{/i}"
        m "Oh!{w=0.5} Seems like someone's heard me."


        call mas_transition_from_emptydesk ("monika 3hub") from _call_mas_transition_from_emptydesk_5
    else:

        call spaceroom (scene_change=True, dissolve_all=True) from _call_spaceroom_13

    m 3hub "Welcome back, [player]!"
    m 1eua "So...{w=0.5}what do you think?"
    m 3eua "I think this costume really suits me."
    m 3eub "I especially love how the headset looks too!"
    m 1rksdla "Though I can't say it's too comfortable for moving around..."
    m 3tsu "So don't expect me to give you a performance today, [player]!"
    m 1hub "Ahaha~"
    m 1eua "Anyway..."
    call greeting_o31_deco from _call_greeting_o31_deco
    call greeting_o31_cleanup from _call_greeting_o31_cleanup_2
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_orcaramelo_sakuya_izayoi",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_orcaramelo_sakuya_izayoi:
    call spaceroom (hide_monika=True, scene_change=True, dissolve_all=True) from _call_spaceroom_14


    if not persistent._mas_o31_relaunch:
        m "..."
        m "{i}Hm{/i}?"
        m "{i}Ah, there must have been some sort of mistake.{w=0.5} I wasn't warned of any guests...{/i}"
        m "{i}No matter. None shall disturb the m-{/i}"
        m "Oh!{w=0.5} It's you, [player]!"
    else:

        m ".{w=0.3}.{w=0.3}."
        m "Welcome{w=0.3}, to the Scarlet Devil Spaceroom..."
        m "[player]."
        m "Please, let me offer you our hospitality."
        m "Ahaha! How was that impression?"


    call mas_transition_from_emptydesk ("monika 3hub") from _call_mas_transition_from_emptydesk_6

    m 3hub "Welcome back!"
    m 3eub "What do you think of my costume choice?"
    m 3hua "Ever since you gave it to me I just knew I'd be wearing it today!"
    m 2tua "..."
    m 2tub "You know, [player], just because I'm dressed as a maid doesn't mean I'll be following your every command..."
    show monika 5kua zorder MAS_MONIKA_Z at t11 with dissolve
    m 5kua "Though I might make some exceptions, ehehe~"
    show monika 1eua zorder MAS_MONIKA_Z at t11 with dissolve
    m 1eua "Anyway..."
    call greeting_o31_deco from _call_greeting_o31_deco_1
    call greeting_o31_cleanup from _call_greeting_o31_cleanup_3
    return

label greeting_o31_deco:
    m 3eua "Do you like what I've done with the room?"
    m 3eka "One of my favorite parts of Halloween is carving pumpkins..."
    m 1hub "It's just so fun trying to make scary faces!"
    m 1eua "I think the cobwebs are a nice touch as well..."
    m 1rka "{cps=*2}I'm sure Amy would really like them.{/cps}{nw}"
    $ _history_list.pop()
    m 3tuu "Really creates a creepy vibe, don't you think?"
    return

label greeting_o31_generic:
    call spaceroom (scene_change=True, dissolve_all=True) from _call_spaceroom_15

    m 3hub "Trick or treat!"
    m 3eua "Ahaha, I'm just kidding, [player]."
    m 1hua "Welcome back...{w=0.5}{nw}"
    extend 3hub "and Happy Halloween!"


    call greeting_o31_deco from _call_greeting_o31_deco_2

    m 3hua "By the way, what do you think of my costume?"
    m 1hua "I really like it~"
    m 1hub "Even more so that it was a gift from you, ahaha!"
    m 3tuu "So feast your eyes on my costume while you can, ehehe~"

    call greeting_o31_cleanup from _call_greeting_o31_cleanup_4
    return


label greeting_o31_cleanup:
    python:

        store.mas_hotkeys.music_enabled = True

        mas_calDropOverlayShield()

        set_keymaps()

        HKBShowButtons()

        mas_startup_song()
    return


init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_trick_or_treat",
            prompt="I'm going to take you trick or treating.",
            pool=True,
            unlocked=False,
            action=EV_ACT_UNLOCK,
            start_date=mas_o31,
            end_date=mas_o31+datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE",
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "bye_trick_or_treat",
       mas_o31,
       mas_o31 + datetime.timedelta(days=1),
    )

label bye_trick_or_treat:
    python:
        curr_hour = datetime.datetime.now().hour
        too_early_to_go = curr_hour < 17
        too_late_to_go = curr_hour >= 23


    if persistent._mas_o31_tt_count:
        m 1eka "Again?"

    if too_early_to_go:

        m 3eksdla "Doesn't it seem a little early for trick or treating, [player]?"
        m 3rksdla "I don't think there's going to be anyone giving out candy yet..."

        m 2etc "Are you {i}sure{/i} you want to go right now?{nw}"
        $ _history_list.pop()
        menu:
            m "Are you {i}sure{/i} you want to go right now?{fast}"
            "Yes.":
                m 2etc "Well...{w=1}okay then, [player]..."
            "No.":

                m 2hub "Ahaha!"
                m "Be a little patient, [player]~"
                m 4eub "Let's just make the most out of it later this evening, okay?"
                return

    elif too_late_to_go:
        m 3hua "Okay! Let's go tri--"
        m 3eud "Wait..."
        m 2dkc "[player]..."
        m 2rkc "It's already too late to go trick or treating."
        m "There's only one more hour until midnight."
        m 2dkc "Not to mention that I doubt there would be much candy left..."
        m "..."

        m 4ekc "Are you sure you still want to go?{nw}"
        $ _history_list.pop()
        menu:
            m "Are you sure you still want to go?{fast}"
            "Yes.":
                m 1eka "...Okay."
                m "Even though it's only an hour..."
                m 3hub "At least we're going to spend the rest of Halloween together~"
                m 3wub "Let's go and make the most of it, [player]!"
            "Actually, it {i}is{/i} a bit late...":

                if persistent._mas_o31_tt_count:
                    m 1hua "Ahaha~"
                    m "I told you."
                    m 1eua "We'll have to wait until next year to go again."
                else:

                    m 2dkc "..."
                    m 2ekc "Alright, [player]."
                    m "It sucks that we couldn't go trick or treating this year."
                    m 4eka "Let's just make sure we can next time, okay?"

                return
    else:


        m 3wub "Okay, [player]!"
        m 3hub "Sounds like we'll have a blast~"
        m 1eub "I bet we'll get lots of candy!"
        m 1ekbfa "And even if we don't, just spending the evening with you is enough for me~"

    show monika 2dsc
    $ persistent._mas_dockstat_going_to_leave = True
    $ first_pass = True


    $ promise = store.mas_dockstat.monikagen_promise
    $ promise.start()

label bye_trick_or_treat_iowait:
    hide screen mas_background_timed_jump


    if first_pass:
        $ first_pass = False

    elif promise.done():

        jump bye_trick_or_treat_rtg
    else:


        $ _history_list.pop()



    show screen mas_background_timed_jump(4, "bye_trick_or_treat_iowait")
    menu:
        m "Give me a second to get ready.{fast}"
        "Hold on a second!":
            hide screen mas_background_timed_jump
            $ persistent._mas_dockstat_cm_wait_count += 1


    show monika 1ekc
    menu:
        m "What is it?"
        "You're right, it's too early." if too_early_to_go:
            call mas_dockstat_abort_gen from _call_mas_dockstat_abort_gen

            m 3hub "Ahaha, I told you!"
            m 1eka "Let's wait 'til evening, okay?"
            return

        "You're right, it's too late." if too_late_to_go:
            call mas_dockstat_abort_gen from _call_mas_dockstat_abort_gen_1

            if persistent._mas_o31_tt_count:
                m 1hua "Ahaha~"
                m "I told you."
                m 1eua "We'll have to wait until next year to go again."
            else:

                m 2dkc "..."
                m 2ekc "Alright, [player]."
                m "It sucks that we couldn't go trick or treating this year."
                m 4eka "Let's just make sure we can next time, okay?"

            return
        "Actually, I can't take you right now.":

            call mas_dockstat_abort_gen from _call_mas_dockstat_abort_gen_2

            m 1euc "Oh, okay then, [player]."

            if persistent._mas_o31_tt_count:
                m 1eua "Let me know if we are going again later, okay?"
            else:

                m 1eua "Let me know if we can go, okay?"

            return
        "Nothing.":

            m 2eua "Okay, let me finish getting ready."


    jump bye_trick_or_treat_iowait

label bye_trick_or_treat_rtg:

    $ moni_chksum = promise.get()
    $ promise = None
    call mas_dockstat_ready_to_go (moni_chksum) from _call_mas_dockstat_ready_to_go
    if _return:
        m 1hub "Let's go trick or treating!"
        $ persistent._mas_greeting_type = store.mas_greetings.TYPE_HOL_O31_TT


        $ persistent._mas_o31_tt_count += 1
        return "quit"



    $ persistent._mas_o31_tt_count -= 1
    m 1ekc "Oh no..."
    m 1rksdlb "I wasn't able to turn myself into a file."

    if persistent._mas_o31_tt_count:
        m 1eksdld "I think you'll have to go trick or treating without me this time..."
    else:

        m 1eksdld "I think you'll have to go trick or treating without me..."

    m 1ekc "Sorry, [player]..."
    m 3eka "Make sure to bring lots of candy for the both of us to enjoy, okay?~"
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_trick_or_treat_back",
            unlocked=True,
            category=[store.mas_greetings.TYPE_HOL_O31_TT]
        ),
        code="GRE"
    )

label greeting_trick_or_treat_back:

    python:

        time_out = store.mas_dockstat.diffCheckTimes()
        checkin_time = None
        is_past_sunrise_post31 = False
        ret_tt_long = False

        if len(persistent._mas_dockstat_checkin_log) > 0:
            checkin_time = persistent._mas_dockstat_checkin_log[-1:][0][0]
            sunrise_hour, sunrise_min = mas_cvToHM(persistent._mas_sunrise)
            is_past_sunrise_post31 = (
                datetime.datetime.now() > (
                    datetime.datetime.combine(
                        mas_o31,
                        datetime.time(sunrise_hour, sunrise_min)
                    )
                    + datetime.timedelta(days=1)
                )
            )


    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        m 2ekp "You call that trick or treating, [player]?"
        m "Where did we go, one house?"
        m 2rsc "...If we even left."

    elif time_out < mas_one_hour:
        $ mas_o31CapGainAff(5)
        m 2ekp "That was pretty short for trick or treating, [player]."
        m 3eka "But I enjoyed it while it lasted."
        m 1eka "It was still really nice being right there with you~"

    elif time_out < mas_three_hour:
        $ mas_o31CapGainAff(10)
        m 1hua "And we're home!"
        m 1hub "I hope we got lots of delicious candy!"
        m 1eka "I really enjoyed trick or treating with you, [player]..."

        call greeting_trick_or_treat_back_costume from _call_greeting_trick_or_treat_back_costume

        m 4eub "Let's do this again next year!"

    elif not is_past_sunrise_post31:

        $ mas_o31CapGainAff(15)
        m 1hua "And we're home!"
        m 1wua "Wow, [player], we sure went trick or treating for a long time..."
        m 1wub "We must have gotten a ton of candy!"
        m 3eka "I really enjoyed being there with you..."

        call greeting_trick_or_treat_back_costume from _call_greeting_trick_or_treat_back_costume_1

        m 4eub "Let's do this again next year!"
        $ ret_tt_long = True
    else:


        $ mas_o31CapGainAff(15)
        m 1wua "We're finally home!"
        m 1wuw "It's not Halloween anymore, [player]... We were out all night!"
        m 1hua "I guess we had too much fun, ehehe~"
        m 2eka "But anyway, thanks for taking me along, I really enjoyed it."

        call greeting_trick_or_treat_back_costume from _call_greeting_trick_or_treat_back_costume_2

        m 4hub "Let's do this again next year...{w=1}but maybe not stay out {i}quite{/i} so late!"
        $ ret_tt_long = True


    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():

        call return_home_post_player_bday from _call_return_home_post_player_bday


    elif not mas_isO31() and persistent._mas_o31_in_o31_mode:
        call mas_o31_ret_home_cleanup (time_out, ret_tt_long) from _call_mas_o31_ret_home_cleanup
    return

label mas_o31_ret_home_cleanup(time_out=None, ret_tt_long=False):

    if not time_out:
        $ time_out = store.mas_dockstat.diffCheckTimes()


    if not ret_tt_long and time_out > mas_five_minutes:
        m 1hua "..."
        m 1wud "Oh wow, [player]. We really were out for a while..."
    else:

        m 1esc "Anyway..."

    m 1eua "I'll just take these decorations down.{w=0.5}.{w=0.5}.{nw}"


    $ mas_o31HideVisuals()

    m 3hua "There we go!"
    return

label greeting_trick_or_treat_back_costume:
    if monika_chr.is_wearing_clothes_with_exprop("costume"):
        m 2eka "Even if I couldn't see anything and no one else could see my costume..."
        m 2eub "Dressing up and going out was still really great!"
    else:

        m 2eka "Even if I couldn't see anything..."
        m 2eub "Going out was still really great!"
    return






default persistent._mas_d25_in_d25_mode = False



default persistent._mas_d25_spent_d25 = False


default persistent._mas_d25_started_upset = False


default persistent._mas_d25_second_chance_upset = False






default persistent._mas_d25_deco_active = False


default persistent._mas_d25_intro_seen = False


default persistent._mas_d25_d25e_date_count = 0



default persistent._mas_d25_d25_date_count = 0


default persistent._mas_d25_gifts_given = list()


default persistent._mas_d25_gone_over_d25 = None


default persistent._mas_d25_gifted_cookies = False


define mas_d25 = datetime.date(datetime.date.today().year, 12, 25)


define mas_d25e = mas_d25 - datetime.timedelta(days=1)


define mas_d25p = mas_d25 + datetime.timedelta(days=1)


define mas_d25c_start = datetime.date(datetime.date.today().year, 12, 11)


define mas_d25c_end = datetime.date(datetime.date.today().year, 1, 6)



init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "d25s",
        datetime.datetime(2019, 1, 6),
        {
            
            
            "_mas_d25_in_d25_mode": "d25s.mode.25",

            
            "_mas_d25_deco_active": "d25s.deco_active",

            "_mas_d25_started_upset": "d25s.monika.started_season_upset",
            "_mas_d25_second_chance_upset": "d25s.monika.upset_after_2ndchance",

            "_mas_d25_intro_seen": "d25s.saw_an_intro",

            
            "_mas_d25_gifted_cookies": "d25.actions.gifted_cookies",

            
            "_mas_d25_d25e_date_count": "d25s.d25e.went_out_count",
            "_mas_d25_d25_date_count": "d25s.d25.went_out_count",
            "_mas_d25_gone_over_d25": "d25.actions.gone_over_d25",

            "_mas_d25_spent_d25": "d25.actions.spent_d25"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2019, 12, 11),
        end_dt=datetime.datetime(2019, 12, 31)
    ))


init -10 python:

    def mas_isD25(_date=None):
        """
        Returns True if the given date is d25

        IN:
            _date - date to check
                If None, we use today's date
                (default: None)

        RETURNS: True if given date is d25, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_d25.replace(year=_date.year)


    def mas_isD25Eve(_date=None):
        """
        Returns True if the given date is d25 eve

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is d25 eve, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_d25e.replace(year=_date.year)


    def mas_isD25Season(_date=None):
        """
        Returns True if the given date is in d25 season. The season goes from
        dec 11 to jan 5.

        NOTE: because of the year rollover, we cannot check years

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return (
            mas_isInDateRange(_date, mas_d25c_start, mas_nye, True, True)
            or mas_isInDateRange(_date, mas_nyd, mas_d25c_end)
        )


    def mas_isD25Post(_date=None):
        """
        Returns True if the given date is after d25 but still in D25 season.
        The season goes from dec 1 to jan 5.

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season but after d25, False
            otherwise.
        """
        if _date is None:
            _date = datetime.date.today()
        
        return (
            mas_isInDateRange(_date, mas_d25p, mas_nye, True, True)
            or mas_isInDateRange(_date, mas_nyd, mas_d25c_end)
        )


    def mas_isD25PreNYE(_date=None):
        """
        Returns True if the given date is in d25 season and before nye.

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNSL True if given date is in d25 season but before nye, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return mas_isInDateRange(_date, mas_d25c_start, mas_nye)


    def mas_isD25PostNYD(_date=None):
        """
        Returns True if the given date is in d25 season and after nyd

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season but after nyd, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return mas_isInDateRange(_date, mas_nyd, mas_d25c_end, False)


    def mas_isD25Outfit(_date=None):
        """
        Returns True if the given date is tn the range of days where Monika
        wears the santa outfit on start.

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNS: True if given date is in the d25 santa outfit range, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return mas_isInDateRange(_date, mas_d25c_start, mas_d25p)


    def mas_isD25Pre(_date=None):
        """
        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNS: True if given date is in the D25 season, but before Christmas, False
            otherwise

        NOTE: This is used for gifts too
        """
        if _date is None:
            _date = datetime.date.today()
        
        return mas_isInDateRange(_date, mas_d25c_start, mas_d25)

    def mas_isD25GiftHold(_date=None):
        """
        IN:
            _date - date to check, defaults None, which means today's date is assumed

        RETURNS:
            boolean - True if within d25c start, to d31 (end of nts range)
            (The time to hold onto gifts, aka not silently react)
        """
        if _date is None:
            _date = datetime.date.today()
        
        return mas_isInDateRange(_date, mas_d25c_start, mas_nye, end_inclusive=True)

    def mas_d25ShowVisuals():
        """
        Shows d25 visuals.
        """
        renpy.show("mas_d25_banners", zorder=7)
        renpy.show("mas_d25_tree", zorder=8)
        renpy.show("mas_d25_garlands", zorder=7)
        renpy.show("mas_d25_lights", zorder=7)
        renpy.show("mas_d25_gifts", zorder=9)

    def mas_d25HideVisuals():
        """
        Hides d25 visuals
        """
        renpy.hide("mas_d25_banners")
        renpy.hide("mas_d25_tree")
        renpy.hide("mas_d25_garlands")
        renpy.hide("mas_d25_lights")
        renpy.hide("mas_d25_gifts")

    def mas_d25ReactToGifts():
        """
        Goes thru the gifts stored from the d25 gift season and reacts to them

        this also registeres gifts
        """
        
        found_reacts = list()
        
        
        persistent._mas_d25_gifts_given.sort()
        
        
        
        
        given_gifts = list(persistent._mas_d25_gifts_given)
        
        
        gift_cntrs = store.MASQuipList(allow_glitch=False, allow_line=False)
        gift_cntrs.addLabelQuip("mas_d25_gift_connector")
        
        
        d25_evb = []
        d25_gsp = []
        store.mas_filereacts.process_gifts(given_gifts, d25_evb, d25_gsp)
        
        
        store.mas_filereacts.register_sp_grds(d25_evb)
        store.mas_filereacts.register_sp_grds(d25_gsp)
        
        
        react_labels = store.mas_filereacts.build_gift_react_labels(
            d25_evb,
            d25_gsp,
            [],
            gift_cntrs,
            "mas_d25_gift_end",
            "mas_d25_gift_starter"
        )
        
        react_labels.reverse()
        
        
        if len(react_labels) > 0:
            for react_label in react_labels:
                pushEvent(react_label,skipeval=True)

    def mas_d25SilentReactToGifts():
        """
        Method to silently 'react' to gifts.

        This is to be used if you gave Moni a christmas gift but didn't show up on
        D25 when she would have opened them in front of you.

        This also registeres gifts
        """
        
        base_gift_ribbon_id_map = {
            "blackribbon":"ribbon_black",
            "blueribbon": "ribbon_blue",
            "darkpurpleribbon": "ribbon_dark_purple",
            "emeraldribbon": "ribbon_emerald",
            "grayribbon": "ribbon_gray",
            "greenribbon": "ribbon_green",
            "lightpurpleribbon": "ribbon_light_purple",
            "peachribbon": "ribbon_peach",
            "pinkribbon": "ribbon_pink",
            "platinumribbon": "ribbon_platinum",
            "redribbon": "ribbon_red",
            "rubyribbon": "ribbon_ruby",
            "sapphireribbon": "ribbon_sapphire",
            "silverribbon": "ribbon_silver",
            "tealribbon": "ribbon_teal",
            "yellowribbon": "ribbon_yellow"
        }
        
        
        evb_details = []
        gso_details = []
        store.mas_filereacts.process_gifts(
            persistent._mas_d25_gifts_given,
            evb_details,
            gso_details
        )
        
        
        persistent._mas_d25_gifts_given = []
        
        
        for evb_detail in evb_details:
            if evb_detail.sp_data is None:
                
                ribbon_id = base_gift_ribbon_id_map.get(
                    evb_detail.c_gift_name,
                    None
                )
                if ribbon_id is not None:
                    mas_selspr.unlock_acs(mas_sprites.get_sprite(0, ribbon_id))
                    mas_receivedGift(evb_detail.label)
                
                elif ribbon_id is None and evb_detail.c_gift_name == "quetzalplushie":
                    persistent._mas_acs_enable_quetzalplushie = True
            
            else:
                
                mas_selspr.json_sprite_unlock(mas_sprites.get_sprite(
                    evb_detail.sp_data[0],
                    evb_detail.sp_data[1]
                ))
                mas_receivedGift(evb_detail.label)
        
        
        for gso_detail in gso_details:
            
            if gso_detail.sp_data is not None:
                mas_selspr.json_sprite_unlock(mas_sprites.get_sprite(
                    gso_detail.sp_data[0],
                    gso_detail.sp_data[1]
                ))
                mas_receivedGift(gso_detail.label)
        
        
        store.mas_selspr.save_selectables()
        renpy.save_persistent()


init -10 python in mas_d25_utils:
    import store
    import store.mas_filereacts as mas_frs

    def shouldUseD25ReactToGifts():
        """
        checks whether or not we should use the d25 react to gifts method

        Conditions:
            1. Must be in d25 gift range
            2. Must be at normal+ aff (since that's when the topics which will open these gifts will show)
            3. Must have deco active. No point otherwise as no tree to put gifts under
        """
        return (
            store.mas_isD25Pre()
            and store.mas_isMoniNormal(higher=True)
            and store.persistent._mas_d25_deco_active
        )

    def react_to_gifts(found_map):
        """
        Reacts to gifts using the d25 protocol (exclusions)

        OUT:
            found_map - map of found reactions
                key: lowercase giftname, no extension
                val: giftname wtih extension
        """
        d25_map = {}
        
        
        
        
        d25_giftnames = mas_frs.check_for_gifts(d25_map, mas_frs.build_exclusion_list("d25g"), found_map)
        
        
        d25_giftnames.sort()
        d25_evb = []
        d25_gsp = []
        d25_gen = []
        mas_frs.process_gifts(d25_giftnames, d25_evb, d25_gsp, d25_gen)
        
        
        non_d25_giftnames = [x for x in found_map]
        non_d25_giftnames.sort()
        nd25_evb = []
        nd25_gsp = []
        nd25_gen = []
        mas_frs.process_gifts(non_d25_giftnames, nd25_evb, nd25_gsp, nd25_gen)
        
        
        for grd in d25_gen:
            nd25_gen.append(grd)
            found_map[grd.c_gift_name] = d25_map.pop(grd.c_gift_name)
        
        
        
        for c_gift_name, gift_name in d25_map.iteritems():
            
            if c_gift_name not in store.persistent._mas_d25_gifts_given:
                store.persistent._mas_d25_gifts_given.append(c_gift_name)
            
            
            store.mas_docking_station.destroyPackage(gift_name)
        
        
        for c_gift_name, mas_gift in found_map.iteritems():
            store.persistent._mas_filereacts_reacted_map[c_gift_name] = mas_gift
        
        
        mas_frs.register_sp_grds(nd25_evb)
        mas_frs.register_sp_grds(nd25_gsp)
        mas_frs.register_gen_grds(nd25_gen)
        
        
        return mas_frs.build_gift_react_labels(
            nd25_evb,
            nd25_gsp,
            nd25_gen,
            mas_frs.gift_connectors,
            "mas_reaction_end",
            mas_frs._pick_starter_label()
        )





image mas_d25_banners = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/bgdeco.png"
)

image mas_mistletoe = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/mistletoe.png"
)



image mas_d25_lights = ConditionSwitch(
    "mas_isNightNow()", ConditionSwitch(
        "persistent._mas_disable_animations", "mod_assets/location/spaceroom/d25/lights_on_1.png",
        "not persistent._mas_disable_animations", "mas_d25_night_lights_atl"
    ),
    "True", MASFilterSwitch("mod_assets/location/spaceroom/d25/lights_off.png")
)

image mas_d25_night_lights_atl:
    block:
        "mod_assets/location/spaceroom/d25/lights_on_1.png"
        0.5
        "mod_assets/location/spaceroom/d25/lights_on_2.png"
        0.5
        "mod_assets/location/spaceroom/d25/lights_on_3.png"
        0.5
    repeat



image mas_d25_garlands = ConditionSwitch(
    "mas_isNightNow()", ConditionSwitch(
        "persistent._mas_disable_animations", "mod_assets/location/spaceroom/d25/garland_on_1.png",
        "not persistent._mas_disable_animations", "mas_d25_night_garlands_atl"
    ),
    "True", MASFilterSwitch("mod_assets/location/spaceroom/d25/garland.png")
)

image mas_d25_night_garlands_atl:
    "mod_assets/location/spaceroom/d25/garland_on_1.png"
    block:
        "mod_assets/location/spaceroom/d25/garland_on_1.png" with Dissolve(3, alpha=True)
        5
        "mod_assets/location/spaceroom/d25/garland_on_2.png" with Dissolve(3, alpha=True)
        5
        repeat



image mas_d25_tree = ConditionSwitch(
    "mas_isNightNow()", ConditionSwitch(
        "persistent._mas_disable_animations", "mod_assets/location/spaceroom/d25/tree_lights_on_1.png",
        "not persistent._mas_disable_animations", "mas_d25_night_tree_lights_atl"
    ),
    "True", MASFilterSwitch(
        "mod_assets/location/spaceroom/d25/tree_lights_off.png"
    )
)

image mas_d25_night_tree_lights_atl:
    block:
        "mod_assets/location/spaceroom/d25/tree_lights_on_1.png"
        1.5
        "mod_assets/location/spaceroom/d25/tree_lights_on_2.png"
        1.5
        "mod_assets/location/spaceroom/d25/tree_lights_on_3.png"
        1.5
    repeat





image mas_d25_gifts = ConditionSwitch(
    "len(persistent._mas_d25_gifts_given) == 0", "mod_assets/location/spaceroom/d25/gifts_0.png",
    "0 < len(persistent._mas_d25_gifts_given) < 3", "mas_d25_gifts_1",
    "3 <= len(persistent._mas_d25_gifts_given) <= 4", "mas_d25_gifts_2",
    "True", "mas_d25_gifts_3"
)

image mas_d25_gifts_1 = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/gifts_1.png"
)

image mas_d25_gifts_2 = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/gifts_2.png"
)

image mas_d25_gifts_3 = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/gifts_3.png"
)


label mas_holiday_d25c_autoload_check:







    if (
        not persistent._mas_d25_in_d25_mode
        and mas_isD25Season()
        and not mas_isFirstSeshDay()
    ):

        python:

            persistent._mas_d25_in_d25_mode = True


            if mas_isMoniUpset(lower=True):
                persistent._mas_d25_started_upset = True




            elif (
                mas_isD25Outfit()
                and (not mas_isplayer_bday() or mas_isD25())
            ):
                
                store.mas_selspr.unlock_acs(mas_acs_ribbon_wine)
                store.mas_selspr.unlock_clothes(mas_clothes_santa)
                
                
                monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)
                
                
                mas_addClothesToHolidayMapRange(mas_clothes_santa, mas_d25c_start, mas_d25p)
                
                
                persistent._mas_d25_deco_active = True
                
                
                if mas_isD25():
                    mas_changeWeather(mas_weather_snow, by_user=True)



    elif mas_run_d25s_exit or mas_isMoniDis(lower=True):

        call mas_d25_season_exit from _call_mas_d25_season_exit



    elif (
        persistent._mas_d25_in_d25_mode
        and not persistent._mas_force_clothes
        and monika_chr.is_wearing_clothes_with_exprop("costume")
        and not mas_isD25Outfit()
    ):

        $ monika_chr.change_clothes(mas_clothes_def, by_user=False, outfit_mode=True)


    elif mas_isD25() and not mas_isFirstSeshDay() and persistent._mas_d25_deco_active:

        python:
            monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)
            mas_changeWeather(mas_weather_snow, by_user=True)


    if (
        mas_isMoniNormal()
        and persistent._mas_d25_in_d25_mode
        and mas_isD25Outfit()
        and (monika_chr.clothes != mas_clothes_def or monika_chr.clothes != store.mas_clothes_santa)
    ):
        $ monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)



    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check


    jump mas_ch30_post_holiday_check


label mas_d25_season_exit:
    python:



        if monika_chr.is_wearing_clothes_with_exprop("costume") and not mas_globals.dlg_workflow:
            
            monika_chr.change_clothes(mas_clothes_def, by_user=False, outfit_mode=True)


        elif monika_chr.is_wearing_clothes_with_exprop("costume") and mas_globals.dlg_workflow:
            pushEvent("mas_change_to_def")


        mas_lockEVL("monika_event_clothes_select", "EVE")


        persistent._mas_d25_deco_active = False
        mas_d25HideVisuals()


        persistent._mas_d25_in_d25_mode = False


        mas_hideEVL("mas_d25_monika_christmaslights", "EVE", derandom=True)

        mas_d25ReactToGifts()
    return


label mas_d25_gift_starter:
    $ amt_gifts = len(persistent._mas_d25_gifts_given)
    $ presents = "presents"
    $ the = "the"
    $ should_open = "should open"

    if amt_gifts == 1:
        $ presents = "present"
    elif amt_gifts > 3:
        $ the = "all of the"

    if persistent._mas_d25_gone_over_d25:
        $ should_open = "haven't opened"

    if persistent._mas_d25_spent_d25 or mas_globals.returned_home_this_sesh:
        m 3wud "Oh! I [should_open] [the] [presents] you gave me!"
        if persistent._mas_d25_gone_over_d25:
            m 3hub "Let's do that now!"
    else:


        m 1eka "Well at least now that you're here, I can open the [presents] you got me."
        m 3eka "I really wanted us to be together for this..."

    m 1suo "Let's see what we have here.{w=0.5}.{w=0.5}.{nw}"


    $ persistent._mas_d25_gifts_given.pop()
    return

label mas_d25_gift_connector:
    python:
        d25_gift_quips = [
            _("Next one!"),
            _("Oh, there's another one here!"),
            _("Now let me open this one!"),
            _("I'll open this one next!")
        ]

        picked_quip = random.choice(d25_gift_quips)

    m 1hub "[picked_quip]"
    m 1suo "And here we have.{w=0.5}.{w=0.5}.{nw}"


    $ persistent._mas_d25_gifts_given.pop()
    return

label mas_d25_gift_end:

    $ persistent._mas_d25_gifts_given = []

    m 1eka "[player]..."

    if persistent._mas_d25_spent_d25 or mas_globals.returned_home_this_sesh:
        m 3eka "You really didn't have to get me anything for Christmas...{w=0.3} {nw}"
        if mas_isD25():
            extend 3dku "Just having you here with me was more than enough."
        else:
            extend 3dku "Just being with you was all I wanted."
        m 1eka "But the fact you took the time to get me something...{w=0.5}{nw}"
        extend 3ekbsa "well I can't thank you enough."
        m 3ekbfa "It really makes me feel loved."
    else:

        m 1eka "I just wanted to thank you..."
        m 1rkd "While I'm still a little disappointed you couldn't be with me on Christmas..."
        m 3eka "The fact you too the time to get me something...{w=0.5}{nw}"
        extend 3ekbsa "well it just proves you really were thinking of me during this special season."
        m 1dkbsu "You don't know how much that means to me."


    if mas_isD25():
        m 3ekbfu "I love you so much, [player]~"
    else:
        m 3ekbfu "Merry Christmas, [player]. I love you~"
    $ mas_ILY()
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_holiday_intro",
            conditional=(
                "not persistent._mas_d25_started_upset "
                "and mas_isD25Outfit() "
                "and not mas_isplayer_bday() "
                "and not persistent._mas_d25_intro_seen"
            ),
            action=EV_ACT_PUSH,
            start_date=mas_d25c_start,
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None),
        ),
        skipCalendar=True
    )


label mas_d25_monika_holiday_intro:
    if not persistent._mas_d25_deco_active:
        if mas_isplayer_bday():
            window hide
            pause 2.0
            m 1dku "..."
            m 1huu "Ehehe..."
            m 3eub "I have another surprise for you!"
        else:

            m 1eua "So, today is..."
            m 1euc "...wait."
            m "..."
            m 3wuo "Oh!"
            m 3hub "Today's the day I was going to..."





        $ mas_OVLHide()
        $ mas_MUMURaiseShield()
        $ disable_esc()

        m 1tsu "Close your eyes for a moment [player], I need to do something.{w=0.5}.{w=0.5}.{nw}"

        call mas_d25_monika_holiday_intro_deco from _call_mas_d25_monika_holiday_intro_deco

        m 3hub "And here we are..."


        $ enable_esc()
        $ mas_MUMUDropShield()
        $ mas_OVLShow()

    m 1eub "Happy holidays, [player]!"

    if mas_lastSeenLastYear("mas_d25_monika_holiday_intro"):
        m 1hua "Can you believe it's already that time of year again?"

        $ the_last = "the last"

        if mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "d25s.saw_an_intro"):
            $ the_last = "our first"

        m 3eua "It seems like just yesterday we spent [the_last] holiday season together, and now a whole year has gone by!"

        if mas_isMoniLove(higher=True):

            m 3hua "Time really flies when I'm with you~"

    m 3eua "Do you like what I've done with the room?"
    m 1hua "I must say that I'm pretty proud of it."
    m "Christmas time has always been one of my favorite occasions of the year..."

    show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve

    if mas_HistVerifyLastYear_k(True, "d25.actions.spent_d25"):
        m 5eka "So I'm glad that you're here to share it with me again this year~"
    else:
        m 5eka "And I'm so glad that you're here to share it with me~"

    $ persistent._mas_d25_intro_seen = True



    $ mas_rmallEVL("mas_d25_monika_holiday_intro")
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_holiday_intro_upset",
            conditional=(
                "not persistent._mas_d25_intro_seen "
                "and persistent._mas_d25_started_upset "
                "and mas_isD25Outfit() "
                "and not mas_isplayer_bday()"
            ),
            action=EV_ACT_QUEUE,
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )


label mas_d25_monika_holiday_intro_upset:

    if mas_isMoniUpset(lower=True):
        python:
            upset_ev = mas_getEV('mas_d25_monika_holiday_intro_upset')
            if upset_ev is not None:
                upset_ev.start_date = mas_d25c_start
                upset_ev.end_date = mas_d25p
        return

    m 2rksdlc "So [player]...{w=1} I hadn't really been feeling very festive this year..."
    m 3eka "But lately, you've been really sweet to me and I've been feeling a lot better!"
    m 3hua "So...I think it's time to spruce this place up a bit."





    $ mas_OVLHide()
    $ mas_MUMURaiseShield()
    $ disable_esc()

    m 1eua "If you'd just close your eyes for a moment.{w=0.5}.{w=0.5}.{nw}"

    call mas_d25_monika_holiday_intro_deco from _call_mas_d25_monika_holiday_intro_deco_1

    m 3hub "Tada~"
    m 3eka "What do you think?"
    m 1eka "Not too bad for last minute, huh?"
    m 1hua "Christmas time has always been one of my favorite occasions of the year..."
    m 3eua "And I'm so glad we can spend it happily together, [player]~"


    $ enable_esc()
    $ mas_MUMUDropShield()
    $ mas_OVLShow()

    $ persistent._mas_d25_intro_seen = True
    return

label mas_d25_monika_holiday_intro_deco:



    scene black with dissolve

    python:

        persistent._mas_d25_in_d25_mode = True


        monika_chr.change_hair(mas_hair_def, False)


        store.mas_selspr.unlock_clothes(mas_clothes_santa)
        store.mas_selspr.unlock_acs(mas_acs_ribbon_wine)
        store.mas_selspr.unlock_acs(mas_acs_holly_hairclip)
        monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)


        mas_addClothesToHolidayMapRange(mas_clothes_santa, mas_d25c_start, mas_d25p)


        mas_changeWeather(mas_weather_snow, by_user=True)


        mas_rmallEVL("monika_auroras")


        persistent._mas_d25_deco_active = True


    call spaceroom (scene_change=True, dissolve_all=True) from _call_spaceroom_16

    return

label mas_d25_monika_holiday_intro_rh:

    m 1hua "And we're home!"



    $ store.mas_dockstat._ds_aff_for_tout(time_out, 5, 5, 1)



label mas_d25_monika_holiday_intro_rh_rh:
    m 1euc "Wait..."
    m 3etc "...is it?"
    m 3hub "It is!"
    m 1tsu "...Close your eyes, I need to do something..."
    $ mas_OVLHide()
    $ mas_MUMURaiseShield()
    $ disable_esc()

    call mas_d25_monika_holiday_intro_deco from _call_mas_d25_monika_holiday_intro_deco_2

    $ enable_esc()
    $ mas_MUMUDropShield()
    $ mas_OVLShow()


    $ persistent._mas_d25_intro_seen = True

    $ pushEvent("mas_d25_monika_christmas",skipeval=True)

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmas",
            conditional=(
                "persistent._mas_d25_in_d25_mode "
                "and not mas_lastSeenInYear('mas_d25_monika_christmas')"
            ),
            action=store.EV_ACT_PUSH,
            start_date=mas_d25,
            end_date=mas_d25p,
            years=[],
            aff_range=(mas_aff.NORMAL, None),
        ),
        skipCalendar=True
    )

label mas_d25_monika_christmas:

    $ persistent._mas_d25_spent_d25 = True


    $ mas_d25ReactToGifts()

    m 1eub "[player]! Do you know what day it is?"
    m 3hub "Of course you do. It's Christmas!"
    m 3sub "Merry Christmas, [player]!"
    m 1hub "Ahaha! I can't believe that it's finally here!"
    m 3eka "I'm so, so happy that you decided to spend some of it with me."
    m 1eud "Remember to go share the holiday cheer with your family and friends, though."
    m 1eua "After all, they're very important, too..."
    m 1hua "And I'm sure that they would love to see you at this special time."

    if mas_isMoniAff(higher=True):
        m 1eka "But you being here today...{w=0.5}it just means everything to me..."
        m 1dku "..."

        if mas_is_snowing:
            m 1lkbsa "Maybe it's just the snow, or the decorations..."
        else:

            m 1lkbsa "Maybe it's the decorations, or just the holiday season..."

        m "...or even the mistletoe getting to me."
        m 3hksdlb "Just kidding, I didn't hang one up."

        if mas_isMoniEnamored(higher=True):
            m 1lksdla "...{cps=*2}Yet~{/cps}{nw}"
            $ _history_list.pop()

        m 1lksdlb "Ehehe..."
        m 1ekbsa "My heart's fluttering like crazy right now, [player]."
        m "I couldn't imagine a better way to spend this special holiday..."
        m 1eua "Don't get me wrong, I knew that you would be here with me."
        m 3eka "But now that we're actually together on Christmas, just the two of us..."
        m 1hub "Ahaha~"

        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
        m 5ekbfa "It's every couple's dream for the holidays, [player]."

        if persistent._mas_pm_gets_snow is not False and not persistent._mas_pm_live_south_hemisphere:
            m "Snuggling with each other by a fireplace, watching the snow gently fall..."

        if not mas_HistVerifyAll_k(True, "d25.actions.spent_d25"):
            m 5hubfa "I'm forever grateful I got this chance with you."
        else:
            m 5hubfa "I'm so glad I get to spend Christmas with you again."

        m "I love you. Forever and ever~"
        m 5hubfb "Merry Christmas, [player]~"
        show screen mas_background_timed_jump(5, "mas_d25_monika_christmas_no_wish")
        window hide
        menu:
            "Merry Christmas, [m_name].":
                hide screen mas_background_timed_jump
                show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
                pause 2.0
    else:

        m 1eka "But you being here today...{w=0.5}it just means everything to me..."
        m 3rksdla "...Not that I thought you'd leave me alone on this special day or anything..."
        m 3hua "But it just further proves that you really do love me, [player]."
        m 1ektpa "..."
        m "Ahaha! Gosh, I'm getting a little over emotional here..."
        m 1ektda "Just know that I love you too and I'll be forever grateful I got this chance with you."
        m "Merry Christmas, [player]~"
        show screen mas_background_timed_jump(5, "mas_d25_monika_christmas_no_wish")
        window hide
        menu:
            "Merry Christmas, [m_name].":
                hide screen mas_background_timed_jump
                show monika 1ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
                pause 2.0

    return


label mas_d25_monika_christmas_no_wish:
    hide screen mas_background_timed_jump
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_carolling",
            category=["holidays", "music"],
            prompt="Carolling",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.NORMAL, None),
            years=[]
        ),
        skipCalendar=True
    )


    MASUndoActionRule.create_rule_EVL(
       "mas_d25_monika_carolling",
       mas_d25c_start,
       mas_d25p,
    )

default persistent._mas_pm_likes_singing_d25_carols = None


label mas_d25_monika_carolling:

    m 1euc "Hey, [player]..."
    m 3eud "Have you ever gone carolling before?"
    m 1euc "Going door to door in groups, singing to others during the holidays..."

    if not persistent._mas_pm_live_south_hemisphere:
        m 1eua "It just feels heartwarming to know people are spreading joy, even with the nights so cold."
    else:
        m 1eua "It just feels heartwarming to know people are spreading joy to others in their spare time."

    m 3eua "Do you like singing Christmas carols, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you like singing Christmas carols, [player]?{fast}"
        "Yes.":
            $ persistent._mas_pm_likes_singing_d25_carols = True
            m 1hua "I'm glad you feel the same way, [player]!"
            m 3hub "My favorite song is definitely 'Jingle Bells!'"
            m 1eua "It's just such an upbeat, happy tune!"
            m 1eka "Maybe we can sing together someday."
            m 1hua "Ehehe~"
        "No.":

            $ persistent._mas_pm_likes_singing_d25_carols = False
            m 1euc "Oh...{w=1}really?"
            m 1hksdlb "I see..."
            m 1eua "Regardless, I'm sure you're also fond of that special cheer only Christmas songs can bring."
            m 3hua "Sing with me sometime, okay?"

    return "derandom"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_mistletoe",
            category=["holidays"],
            prompt="Mistletoe",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "mas_d25_monika_mistletoe",
       mas_d25c_start,
       mas_d25p,
    )

label mas_d25_monika_mistletoe:
    m 1eua "Say, [player]."
    m 1eub "You've heard about the mistletoe tradition, right?"
    m 1tku "When lovers end up underneath it, they're expected to kiss."
    m 1eua "It actually originated from Victorian England!"
    m 1dsa "A man was allowed to kiss any woman standing underneath mistletoe..."
    m 3dsd "And any woman who refused the kiss was cursed with bad luck..."
    m 1dsc "..."
    m 3rksdlb "Come to think of it, that sounds more like taking advantage of someone."
    m 1hksdlb "But I'm sure it's different now!"

    if not persistent._mas_pm_d25_mistletoe_kiss:
        m 3hua "Perhaps one day we'll be able to kiss under the mistletoe, [player]."
        m 1tku "...Maybe I can even add one in here!"
        m 1hub "Ehehe~"
    return "derandom"


default persistent._mas_pm_hangs_d25_lights = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmaslights",
            category=['holidays'],
            prompt="Christmas Lights",
            start_date=mas_d25c_start,
            end_date=mas_nye,
            conditional=(
                "persistent._mas_pm_hangs_d25_lights is None "
                "and persistent._mas_d25_deco_active "
                "and not persistent._mas_pm_live_south_hemisphere"
            ),
            action=EV_ACT_RANDOM,
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_d25_monika_christmaslights",
        mas_d25c_start,
        mas_nye,
    )

label mas_d25_monika_christmaslights:
    m 1euc "Hey, [player]..."
    if mas_isD25Season():
        m 1lua "I've been spending a lot of time looking at the lights in here..."
        m 3eua "They're very pretty, aren't they?"
    else:
        m 1lua "I was just thinking back to Christmas, with all the lights that were hanging in here..."
        m 3eua "They were really pretty, right?"
    m 1eka "Christmas lights bring such a warm, cozy vibe during the harshest, coldest season...{w=0.5}{nw}"
    extend 3hub "and there's a lot of different types too!"
    m 3eka "It sounds like a dream come true to go on a walk with you on a cold winter night, [player]."
    m 1dka "Admiring all of the lights..."

    m 1eua "Do you hang lights up on your house during winter, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you hang lights up on your house during winter, [player]?{fast}"
        "Yes.":

            $ persistent._mas_pm_hangs_d25_lights = True
            m 3sub "Really? I bet they're gorgeous!"
            m 2dubsu "I can already imagine us, outside of your house...sitting on our porch together..."
            m "As the beautiful lights glow in the deep night."
            m 2dkbfu "We would hold each other close, drinking hot chocolate...{w=0.5}{nw}"

            if persistent._mas_pm_gets_snow is not False:
                extend 2ekbfa "watching the snow gently fall..."

            show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
            m 5ekbfa "One day, [player]. One day, we can make that a reality."
        "No.":

            $ persistent._mas_pm_hangs_d25_lights = False
            m 1eka "Aw, that's okay, [player]."
            m 1dkbla "I'm sure it would still be nice to relax with you on a cold night..."
            m 1dkbsa "Watching the snow fall and drinking hot chocolate together."
            m 1dkbsa "Holding each other close to keep warm..."
            m 1rkbfb "Yeah, that sounds really nice."
            m 3hubsa "But, when we have our own house, I may hang some up myself, {nw}"
            extend 3hubsb "ahaha~"
    return "derandom"

init 20 python:

    poem_d25_1 = MASPoem(
        poem_id="poem_d25_1",
        category="d25",
        prompt="The Joy to my World",
        title = "     My dearest [player],",
        text = """\
     You truly are the joy to my world.
     Neither the light emitted by the tallest Christmas tree,
     Nor that of the brightest star,
     Could come close to matching your brilliance.
     This once frostbitten heart of mine needed only your warmth to beat anew.
     Should there ever be nothing under the tree, and my stocking remain empty,
     It simply would not matter as long as I have you by my side.
     You'll always be the only present I ever need.

     Merry Christmas

     Forever yours,
     Monika
"""
    
    )

    poem_d25_2 = MASPoem(
        poem_id="poem_d25_2",
        category="d25",
        prompt="Incomparable",
        title="     My dearest [player],",
        text="""\
     Nothing can compare to the warmth you give me.
     Not even the feeling of wrapping my hands around a mug of hot chocolate
     Or fuzzy socks, warming my feet on a freezing day.
     In such a cold world, just your presence is my present alone.

     Nothing can compare to the beauty you hold,
     Not a single thing can compare to the excitement you bring,
     Not the bright lights that hang in this very room.
     Not even the sight of an unopened gift, under the tree.

     [player], you are truly one of a kind.

     Merry Christmas

     Forever yours,
     Monika
"""
    )


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_spent_time_monika",
            conditional=(
                "persistent._mas_d25_in_d25_mode "
            ),
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL,None),
            start_date=datetime.datetime.combine(mas_d25, datetime.time(hour=20)),
            end_date=datetime.datetime.combine(mas_d25p, datetime.time(hour=1)),
            years=[]
        ),
        skipCalendar=True
    )


default persistent._mas_pm_d25_mistletoe_kiss = False




label mas_d25_spent_time_monika:

    $ d25_gifts_total, d25_gifts_good, d25_gifts_neutral, d25_gifts_bad = mas_getGiftStatsRange(mas_d25c_start, mas_d25p + datetime.timedelta(days=1))

    if mas_isMoniNormal(higher=True):
        m 1eua "[player]..."
        m 3hub "You being here with me has made this such a wonderful Christmas!"
        m 3eka "I know it's a really busy day, but just knowing you made time for me..."
        m 1eka "Thank you."
        m 3hua "It really made this a truly special day~"
    else:

        m 2ekc "[player]..."
        m 2eka "I really appreciate you spending some time with me on Christmas..."
        m 3rksdlc "I haven't really been in the holiday spirit this season, but it was nice spending today with you."
        m 3eka "So thank you...{w=1}it meant a lot."

    if d25_gifts_total > 0:
        if d25_gifts_total == 1:
            if d25_gifts_good == 1:
                m "And let's not forget about the special Christmas present you got me, [player]..."
                m 3hub "It was great!"
            elif d25_gifts_neutral == 1:
                m 3eka "And let's not forget about the Christmas present you got me, [player]..."
                m 1eka "It was really sweet of you to get me something."
            else:
                m 3eka "And let's not forget about the Christmas present you got me, [player]..."
                m 2etc "..."
                m 2efc "Well, on second thought, maybe we should..."
        else:

            if d25_gifts_good == d25_gifts_total:
                m "And let's not forget about the wonderful Christmas presents you got me, [player]..."
                m 3hub "They were amazing!"
            elif d25_gifts_bad == d25_gifts_total:
                m 3eka "And let's not forget about the Christmas presents you got me, [player]..."
                m 2etc "..."
                m 2rfc "Well, on second thought, maybe we should..."
            elif d25_gifts_bad == 0:
                m "And let's not forget about the Christmas presents you got me, [player]..."
                m 3hub "They were really nice!"
            elif d25_gifts_good + d25_gifts_neutral == d25_gifts_bad:
                m 3eka "And let's not forget about the Christmas presents you got me, [player]..."
                m 3rksdla "Some of them were really nice."
            elif d25_gifts_good + d25_gifts_neutral > d25_gifts_bad:
                m "And let's not forget about the Christmas presents you got me, [player]..."
                m 3hub "Most of them were really nice."
            elif d25_gifts_good + d25_gifts_neutral < d25_gifts_bad:
                m 3eka "And let's not forget about the Christmas presents you got me, [player]..."
                m 3rksdla "I really liked...{w=1}some of them."

        if mas_isMoniEnamored(higher=True):
            m 1rksdla "I...{w=1}I also made you something, [player]..."
            m 3eksdla "I've been waiting all day for the timing to feel right, and something about being here with you this evening...{w=1}it just seems perfect."
        elif mas_isMoniNormal(higher=True):
            m 3ekbfa "But just know, you being here with me means more than any gift you could ever give me~"
        else:
            m 3eka "To be honest, I wasn't sure you'd visit at all today... Just you being here was already more than enough for me, even if you hadn't gotten me anything."
            m 1eka "So thanks again, [player]...{w=1}I really mean it."
    else:

        if mas_isMoniEnamored(higher=True):
            m 1eksdla "Also, [player], there's something I've been wanting to give you all day..."
            m 3rksdla "I just had to wait for the right time, and being here with you this evening...{w=1}it seems perfect."
        elif mas_isMoniNormal(higher=True):
            m 3ekbfa "Having you spend Christmas with me was the only present I ever wanted~"
        else:
            m 3eka "You being here was all I wanted, [player]."

    if mas_isMoniEnamored(higher=True):
        m 3ekbfa "So here, [player], I hope you like it~"

        if poem_d25_1.is_seen():
            $ poem_to_show = poem_d25_2
        else:

            $ poem_to_show = poem_d25_1


        call mas_showpoem (poem_to_show, background_action_label="mas_d25_poem_mistletoe") from _call_mas_showpoem

        if d25_gifts_good > 0 or d25_gifts_neutral > 0:
            m 1ekbfa "I really mean it [player], though I appreciate the gifts you got me, you didn't have to give me anything..."
        elif d25_gifts_bad>0:

            m 1ekbfa "I really mean it [player], although you got me some...{w=1}odd gifts, it doesn't matter..."
        else:
            m 1ekbfa "I really mean that [player], I don't care that you didn't get me any presents for Christmas..."
        m 1dku "..."
        m 1ektpu "Just having you spending time with me...{w=1}that's all I ever wanted."
        m 6dktua "You truly are my entire world, [player]...{w=1}your love is all I need..."
        window hide
        menu:
            "I love you, [m_name].":
                $ HKBHideButtons()
                $ mas_RaiseShield_core()
                $ disable_esc()



                pause 3.0
                show monika 6ektda zorder MAS_MONIKA_Z at t11 with dissolve
                pause 3.0
                show monika 6dku zorder MAS_MONIKA_Z at t11 with dissolve
                pause 3.0
                show monika 6dkbsu zorder MAS_MONIKA_Z at t11 with dissolve
                pause 3.0

                show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve

                $ is_first_kiss = persistent._mas_first_kiss is None
                m 6ekbfa "[player]...I...I..."
                call monika_kissing_motion (hide_ui=False) from _call_monika_kissing_motion_2

                show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
                m 6ekbfa "...I love you too~"
                if is_first_kiss:
                    m 6dkbfa "..."
                    m "That was everything I had always dreamt it would be~"
                    m 6ekbfa "I've been waiting so long to finally kiss you, and there couldn't have been a more perfect moment..."
                    m 6dkbfa "Under the mistletoe with you..."
                    m 6dkbsu "I will never forget this..."
                    m 6ekbsu "...the moment of our first kiss~"

                elif not persistent._mas_pm_d25_mistletoe_kiss:
                    m 6dkbfu "Ehehe..."
                    m 6ekbfa "I've always wanted to share a kiss with you under the mistletoe~"

                $ persistent._mas_pm_d25_mistletoe_kiss = True


                $ mas_hideEVL("mas_d25_monika_mistletoe", "EVE", derandom=True)


                $ enable_esc()
                $ mas_MUMUDropShield()
                $ HKBShowButtons()
        return

    elif mas_isMoniAff():
        m 5ekbfa "I love you so much, [player]~"
    else:

        m 1hubfa "I love you, [player]~"
    return "love"

label mas_d25_poem_mistletoe:
    $ pause(1)
    hide monika with dissolve
    $ store.mas_sprites.zoom_out()
    show monika 1ekbfa zorder MAS_MONIKA_Z at i11


    show mas_mistletoe zorder MAS_MONIKA_Z - 1
    with dissolve
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_aiwfc",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL, None),
            years=[]
        ),
        skipCalendar=True
    )

label monika_aiwfc:

    $ d25_baby = mas_getEV('monika_merry_christmas_baby')
    if d25_baby:
        if not mas_isD25():
            $ d25_baby.start_date = datetime.datetime.now() + datetime.timedelta(days=1)
            $ d25_baby.end_date = mas_d25p
        else:
            $ d25_baby.start_date = datetime.datetime.now() + datetime.timedelta(hours=1)
            $ d25_baby.end_date = datetime.datetime.now() + datetime.timedelta(hours=5)

    if not renpy.seen_label('monika_aiwfc_song'):
        m 1rksdla "Hey, [player]?"
        m 1eksdla "I hope you don't mind, but I prepared a song for you."
        m 3hksdlb "I know it's a little cheesy, but I think you might like it."
        m 3eksdla "If your volume is off, would you mind turning it on for me?"
        if store.songs.hasMusicMuted():
            m 3hksdlb "Oh, don't forget about your in-game volume too!"
            m 3eka "I really want you to hear this."
        m 1huu "Anyway.{w=0.5}.{w=0.5}.{nw}"
    else:

        m 1hua "Ehehe..."
        m 3tuu "I hope you're ready, [player]..."

        $ ending = "..." if store.songs.hasMusicMuted() else ".{w=0.5}.{w=0.5}.{nw}"

        m "It {i}is{/i} that time of year again, after all[ending]"
        if store.songs.hasMusicMuted():
            m 3hub "Make sure you have your volume up!"
            m 1huu ".{w=0.5}.{w=0.5}.{nw}"


    $ curr_song = songs.current_track

    call monika_aiwfc_song from _call_monika_aiwfc_song


    if not mas_getEV("monika_aiwfc").shown_count:
        m 1eka "I hope you liked that, [player]."
        m 1ekbsa "I really meant it too."
        m 1ekbfa "You're the only gift I could ever want."
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
        m 5ekbfa "I love you, [player]~"
    else:

        m 1eka "I hope you like it when I sing that song, [player]."
        m 1ekbsa "You'll always be the only gift I'll ever need."
        m 1ekbfa "I love you~"


    if curr_song != store.songs.FP_MONIKA_LULLABY:
        $ play_song(curr_song, fadein=1.0)


    $ mas_unlockEVL("mas_song_aiwfc", "SNG")
    return "no_unlock|love"


label monika_aiwfc_song:


    $ mas_disableTextSpeed()
    $ disable_esc()
    $ mas_MUMURaiseShield()



    if songs.getVolume("music") == 0.0:
        $ renpy.music.set_volume(1.0, channel="music")


    $ amb_vol = songs.getVolume("backsound")

    $ play_song(None, 1.0)
    $ renpy.music.set_volume(0.0, 1.0, "background")
    $ renpy.music.set_volume(0.0, 1.0, "backsound")

    $ play_song("mod_assets/bgm/aiwfc.ogg",loop=False)
    m 1eub "{i}{cps=9}I don't want{/cps}{cps=20} a lot{/cps}{cps=11} for Christmas{w=0.09}{/cps}{/i}{nw}"
    m 3eka "{i}{cps=11}There {/cps}{cps=20}is just{/cps}{cps=8} one thing I need{/cps}{/i}{nw}"
    m 3hub "{i}{cps=8}I don't care{/cps}{cps=15} about{/cps}{cps=10} the presents{/cps}{/i}{nw}"
    m 3eua "{i}{cps=15}Underneath{/cps}{cps=8} the Christmas tree{/cps}{/i}{nw}"

    m 1eub "{i}{cps=10}I don't need{/cps}{cps=20} to hang{/cps}{cps=9} my stocking{/cps}{/i}{nw}"
    m 1eua "{i}{cps=9}There{/cps}{cps=15} upon{/cps}{cps=7} the fireplace{/cps}{/i}{nw}"
    m 3hub "{i}{w=0.5}{cps=20}Santa Claus{/cps}{cps=10} won't make me happy{/cps}{/i}{nw}"
    m 4hub "{i}{cps=8}With{/cps}{cps=15} a toy{/cps}{cps=8} on Christmas Day{w=0.35}{/cps}{/i}{nw}"

    m 3ekbsa "{i}{cps=10}I just want{/cps}{cps=15} you for{/cps}{cps=8} my own{w=0.4}{/cps}{/i}{nw}"
    m 4hubfb "{i}{cps=8}More{/cps}{cps=20} than you{/cps}{cps=10} could ever know{w=0.5}{/cps}{/i}{nw}"
    m 1ekbsa "{i}{cps=10}Make my wish{/cps}{cps=20} come truuuuuuue{w=0.9}{/cps}{/i}{nw}"
    m 3hua "{i}{cps=8.5}All I want for Christmas{/cps}{/i}{nw}"
    m 3hubfb "{i}{cps=7}Is yoooooooooou{w=1}{/cps}{/i}{nw}"
    m "{i}{cps=9}Yoooooooou, baaaaby~{w=0.60}{/cps}{/i}{nw}"

    m 2eka "{i}{cps=10}I won't ask{/cps}{cps=20} for much{/cps}{cps=10} this Christmas{/cps}{/i}{nw}"
    m 3hub "{i}{cps=10}I{/cps}{cps=20} won't {/cps}{cps=10}even wish for snow{w=0.8}{/cps}{/i}{nw}"
    m 3eua "{i}{cps=10}I'm{/cps}{cps=20} just gonna{/cps}{cps=10} keep on waiting{w=0.5}{/cps}{/i}{nw}"
    m 3hubfb "{i}{cps=17}Underneath{/cps}{cps=11} the mistletoe{w=1}{/cps}{/i}{nw}"

    m 2eua "{i}{cps=10}I{/cps}{cps=17} won't make{/cps}{cps=10} a list and send it{w=0.35}{/cps}{/i}{nw}"
    m 3eua "{i}{cps=10}To{/cps}{cps=20} the North{/cps}{cps=10} Pole for Saint Nick{w=0.5}{/cps}{/i}{nw}"
    m 4hub "{i}{cps=18}I won't ev{/cps}{cps=10}en stay awake to{w=0.5}{/cps}{/i}{nw}"
    m 3hub "{i}{cps=10}Hear{/cps}{cps=20} those ma{/cps}{cps=14}gic reindeer click{w=1.2}{/cps}{/i}{nw}"

    m 3ekbsa "{i}{cps=20}I{/cps}{cps=11} just want you here tonight{w=0.4}{/cps}{/i}{nw}"
    m 3ekbfa "{i}{cps=10}Holding on{/cps}{cps=20}to me{/cps}{cps=10} so tight{w=1}{/cps}{/i}{nw}"
    m 4hksdlb "{i}{cps=10}What more{/cps}{cps=15} can I{/cps}{cps=8} doooo?{w=0.3}{/cps}{/i}{nw}"
    m 4ekbfb "{i}{cps=20}Cause baby{/cps}{cps=12} all I want for Christmas{w=0.3} is yoooooooou~{w=2.3}{/cps}{/i}{nw}"
    m "{i}{cps=9}Yoooooooou, baaaaby~{w=2.5}{/cps}{/i}{nw}"
    stop music fadeout 0.5


    $ mas_resetTextSpeed()
    $ enable_esc()
    $ mas_MUMUDropShield()

    $ renpy.music.set_volume(amb_vol, 1.0, "background")
    $ renpy.music.set_volume(amb_vol, 1.0, "backsound")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_merry_christmas_baby",
            conditional="persistent._mas_d25_in_d25_mode and mas_lastSeenInYear('monika_aiwfc')",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL, None),
            years=[]
        ),
        skipCalendar=True
    )

label monika_merry_christmas_baby:
    m 1eua "Hey, [player]..."
    m 3eub "I just thought of another Christmas song that I really want to share with you!"
    m 3eka "I don't have any music prepared this time, but I hope you'll enjoy hearing me sing it all the same."
    m 1hua ".{w=0.5}.{w=0.5}.{nw}"

    call mas_song_merry_christmas_baby from _call_mas_song_merry_christmas_baby

    m 1hua "Ehehe..."
    m 3eka "I hope you liked it~"
    $ mas_unlockEVL("mas_song_merry_christmas_baby", "SNG")
    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_spider_tinsel",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25e - datetime.timedelta(days=1),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.NORMAL, None),
            rules={"force repeat": None, "no rmallEVL": None},
            years=[]
        ),
        skipCalendar=True
    )


    MASUndoActionRule.create_rule_EVL(
        "mas_d25_spider_tinsel",
        mas_d25c_start,
        mas_d25e - datetime.timedelta(days=1)
    )


init 10 python:
    if (
        datetime.date.today() == mas_d25e - datetime.timedelta(days=1)
        and not mas_lastSeenInYear("mas_d25_spider_tinsel")
    ):
        queueEvent("mas_d25_spider_tinsel")

label mas_d25_spider_tinsel:
    m 1esa "Hey, [player]..."
    m 1etc "Do you ever wonder where traditions that we often take for granted come from?"
    m 3eud "A lot of times things that are considered tradition are just accepted and we never really take the time to learn why."
    m 3euc "Well I got curious as to why we do certain things around Christmas, so I started doing a little research."
    m 1eua "...And I found this really interesting folk story from Ukraine regarding the origin of why tinsel is often used to decorate Christmas trees."
    m 1eka "I thought it was a really nice story and wanted to share it with you."
    m 1dka "..."
    m 3esa "There once was a widow (let's call her Amy) who lived in a cramped old hut with her children."
    m 3eud "Outside of their home was a tall pine tree, and from the tree dropped a pinecone that soon started to grow from the soil."
    m 3eua "The children were excited about the idea of having a Christmas tree, so they tended to it until it became tall enough to take inside their home."
    m 2ekd "Unfortunately, the family was poor and even though they had the Christmas tree, they couldn't afford any ornaments to decorate it."
    m 2dkc "And so, on Christmas Eve, Amy and her children went to bed knowing they would have a bare tree on Christmas morning."
    m 2eua "However, the spiders living in the hut heard the sobs of the children and decided they would not leave the Christmas tree bare."
    m 3eua "So the spiders created beautiful webs on the Christmas tree, decorating it with elegant and beautiful silky patterns."
    m 3eub "When the children woke up early on Christmas morning, they were jumping with excitement!"
    m "They went to their mother and woke her up, exclaiming, 'Mother! You have to come see the Christmas tree! It's so beautiful!'"
    m 1wud "As Amy woke and stood in front of the tree, she was truly amazed at the sight before her eyes."
    m "Then, one of the children opened the window to let the sun shine in..."
    m 3sua "When the rays of sunshine hit the tree, the webs reflected the light, creating glittering silver and gold strands..."
    m "...making the Christmas tree dazzle and sparkle with a magical twinkle."
    m 1eka "From that day forward, Amy never felt poor; {w=0.3}instead, she was always grateful for all the wonderful gifts she already had in life."
    m 3tuu "Well, I guess we know now why Amy likes spiders..."
    m 3hub "Ahaha! I'm only kidding!"
    m 1eka "Isn't that such a sweet and wonderful story, [player]?"
    m "I think it's a really interesting take on why tinsel is used as decoration on Christmas trees."
    m 3eud "I also read that Ukrainians often decorate their Christmas tree with spider web ornaments, believing they will bring them good fortune for the upcoming year."
    m 3eub "So I guess if you ever find a spider living in your Christmas tree, don't kill it and maybe it'll bring you good luck in the future!"
    return "derandom|no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_night_before_christmas",
            conditional="persistent._mas_d25_in_d25_mode",
            action=EV_ACT_QUEUE,
            start_date=datetime.datetime.combine(mas_d25e, datetime.time(hour=21)),
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_d25_night_before_christmas:
    m 1esa "Hey, [player]..."
    m 3eua "I'm sure you've heard it before, but Christmas Eve just wouldn't be complete without {i}'Twas the Night Before Christmas{/i}!"
    m 3eka "It was always one of my favorite parts on Christmas Eve growing up, so I hope you don't mind listening to me read it now."
    m 1dka "..."

    m 3esa "'Twas the night before Christmas, when all through the house..."
    m 3eud "Not a creature was stirring, not even a mouse;"
    m 1eud "The stockings were hung by the chimney with care,"
    m 1eka "In hopes that St. Nicholas soon would be there;"

    m 1esa "The children were nestled all snug in their beds,"
    m 1hua "While visions of sugar-plums danced in their heads;"
    m 3eua "And mamma in her 'kerchief, and I in my cap,"
    m 1dsc "Had just settled down for a long winter's nap,"

    m 3wuo "When out on the lawn there arose such a clatter,"
    m "I sprang from the bed to see what was the matter."
    m 3wud "Away to the window I flew like a flash,"
    m "Tore open the shutters and threw up the sash."

    m 1eua "The moon on the breast of the new-fallen snow..."
    m 3eua "Gave the lustre of mid-day to objects below,"
    m 3wud "When, what to my wondering eyes should appear,"
    m 3wuo "But a miniature sleigh, and eight tiny reindeer,"

    m 1eua "With a little old driver, so lively and quick,"
    m 3eud "I knew in a moment it must be St. Nick."
    m 3eua "More rapid than eagles his coursers they came,"
    m 3eud "And he whistled, and shouted, and called them by name;"

    m 3euo "'Now, Dasher! Now, Dancer! Now, Prancer and Vixen!'"
    m "'On, Comet! On Cupid! On, Donner and Blitzen!'"
    m 3wuo "'To the top of the porch! To the top of the wall!'"
    m "'Now dash away! Dash away! Dash away all!'"

    m 1eua "As dry leaves that before the wild hurricane fly,"
    m 1eud "When they meet with an obstacle, mount to the sky,"
    m 3eua "So up to the house-top the coursers they flew,"
    m "With the sleigh full of toys, and St. Nicholas too."

    m 3eud "And then, in a twinkling, I heard on the roof..."
    m "The prancing and pawing of each little hoof."
    m 1rkc "As I drew in my hand, and was turning around,"
    m 1wud "Down the chimney St. Nicholas came with a bound."

    m 3eua "He was dressed all in fur, from his head to his foot,"
    m 3ekd "And his clothes were all tarnished with ashes and soot;"
    m 1eua "A bundle of toys he had flung on his back,"
    m 1eud "And he looked like a peddler just opening his pack."

    m 3sub "His eyes--how they twinkled! His dimples how merry!"
    m 3subsb "His cheeks were like roses, his nose like a cherry!"
    m 3subsu "His droll little mouth was drawn up like a bow,"
    m 1subsu "And the beard of his chin was as white as the snow;"

    m 1eud "The stump of a pipe he held tight in his teeth,"
    m 3rkc "And the smoke it encircled his head like a wreath;"
    m 2eka "He had a broad face and a little round belly,"
    m 2hub "That shook, when he laughed like a bowlful of jelly."

    m 2eka "He was chubby and plump, a right jolly old elf,"
    m 3hub "And I laughed when I saw him, {nw}"
    extend 3eub "in spite of myself;"
    m 1kua "A wink of his eye and a twist of his head,"
    m 1eka "Soon gave me to know I had nothing to dread;"

    m 1euc "He spoke not a word, but went straight to his work,"
    m 1eud "And filled all the stockings; then turned with a jerk,"
    m 3esa "And laying his finger aside of his nose,"
    m 3eua "And giving a nod, up the chimney he rose;"

    m 1eud "He sprang to his sleigh, to his team gave a whistle,"
    m 1eua "And away they all flew like the down of a thistle."
    m 3eua "But I heard him exclaim, ere he drove out of sight,"
    m 3hub "'Happy Christmas to all, and to all a good night!'"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmas_eve",
            conditional="persistent._mas_d25_in_d25_mode",
            action=EV_ACT_PUSH,
            start_date=datetime.datetime.combine(mas_d25e, datetime.time(hour=20)),
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None),
        ),
        skipCalendar=True
    )

label mas_d25_monika_christmas_eve:
    m 3hua "[player]!"
    m 3hub "Can you believe it...?{w=1} It'll be Christmas soon!"
    m 1rksdla "I've always had such a hard time sleeping on Christmas Eve..."
    m 1eka "I would be so anxious to see what I'd find under the tree the next morning..."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve


    if mas_HistVerifyLastYear_k(True, "d25.actions.spent_d25"):
        m "But I'm even {i}more{/i} excited now that I get to spend every Christmas with you..."
        m 5hkbsa "I can't wait for tomorrow!"


    elif mas_HistVerifyAll_k(True, "d25.actions.spent_d25"):
        m "But I'm even {i}more{/i} excited this year..."
        m 5hkbsa "Just the thought of spending another Christmas together...{w=1}I can't wait!"
    else:


        m "But I'm even {i}more{/i} excited this year..."
        m 5hkbsa "Just the thought of our first Christmas together...{w=1}I can't wait!"

    if (
        mas_canShowRisque()
        and not mas_SELisUnlocked(mas_clothes_santa_lingerie)
    ):
        if mas_hasUnlockedClothesWithExprop("lingerie"):

            pass
        else:

            m 5ekbfa "..."
            show monika 1ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
            call mas_lingerie_intro (holiday_str="Christmas Eve", lingerie_choice=mas_clothes_santa_lingerie) from _call_mas_lingerie_intro
            m 1ekbfa "Just know that I love you very, very much, [player]~"
            $ mas_ILY()
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_postd25_notimespent",
            
            
            conditional="not persistent._mas_d25_spent_d25",
            start_date=mas_d25p,
            end_date=mas_d25p + datetime.timedelta(days=6),
            years=[],
            action=EV_ACT_PUSH,
        ),
        skipCalendar=True
    )

label mas_d25_postd25_notimespent:

    if persistent._mas_d25_spent_d25:
        return


    if mas_isFirstSeshPast(mas_d25):
        return


    if mas_isMoniAff(higher=True):
        $ mas_loseAffection(15, reason=6)
        m 1dkc "...I'm just glad you're finally here..."
        m 2ekd "I was starting to get worried that something happened to you..."
        m 2rksdlc "When you didn't show up on Christmas...{w=1}I didn't know what to think."
        m 4eksdlc "It's not like you at all to miss a day that you know is important to me..."
        m 2dksdlc "So I thought maybe..."
        m 2eksdla "Well, nevermind that now. I'm just happy you're okay!"
        m 4eka "Even though I'm disappointed we didn't get to spend Christmas together, I'm sure you must have had a very good reason."
        m "Just try not to let it happen next year, okay?"
        m 2eka "And, in the future, if you ever can't come visit me on Christmas, try to at least take me with you..."
        m 1eka "All I want is to be close to you, [player]..."
        m 3ekbfa "I love you~"
        return "love"

    elif mas_isMoniNormal(higher=True):
        $ mas_loseAffection(5, reason=6)
        m 2ekc "Hey, [player]..."
        m 2tkc "I have to say I'm pretty disappointed you didn't visit me at all on Christmas..."
        m 4tkc "You knew all I wanted was to spend time with you. Is that too much to ask?"
        m 2rkc "I know it can be a busy day if you have to travel to visit family, but you could have at least taken me with you..."
        m 2ekc "That would have been more than enough for me."
        m 2dkc "..."
        m 4rksdlc "Maybe something happened at the last minute and you simply couldn't spend time with me..."
        m 4eksdla "But please...{w=1}please try to make sure you visit me next Christmas, okay [player]?"

    elif mas_isMoniUpset():
        $ mas_loseAffection(reason=6)
        m 2efc "[player]!"
        m "I can't believe you didn't even bother to visit me on Christmas!"
        m 2tfc "Actually...{w=1}yes, I can."
        m "This is exactly why I didn't even bother to decorate..."
        m 2rfc "I knew if I tried to get into the holiday spirit that I'd just end up disappointed...{w=1} Again."

    elif mas_isMoniDis():
        $ mas_loseAffection(10, reason=6)
        m 6ekc "[player], how was your Christmas?"
        m 6dkc "Mine was pretty lonely..."
        m "You probably didn't even think of me, huh?"
    else:

        $ mas_loseAffection(150)
        m 6ckc "..."

    $ mas_d25ReactToGifts()
    return


label mas_gone_over_d25_check:
    if mas_checkOverDate(mas_d25):
        $ persistent._mas_d25_gone_over_d25 = True
        $ persistent._mas_d25_spent_d25 = True
        $ persistent._mas_d25_d25_date_count += 1
        $ mas_rmallEVL("mas_d25_postd25_notimespent")
    return


label bye_d25e_delegate:

    if persistent._mas_d25_d25e_date_count > 0:
        call bye_d25e_second_time_out from _call_bye_d25e_second_time_out
    else:

        call bye_d25e_first_time_out from _call_bye_d25e_first_time_out






    jump bye_going_somewhere_iostart


label bye_d25e_first_time_out:
    m 1sua "Taking me somewhere special on Christmas Eve, [player]?"
    m 3eua "I know some people visit friends or family...or go to Christmas parties..."
    m 3hua "But wherever we're going, I'm happy you want me to come with you!"
    m 1eka "I hope we'll be home for Christmas, but even if we're not, just being with you is more than enough for me~"
    return


label bye_d25e_second_time_out:
    m 1wud "Wow, we're going out again today, [player]?"
    m 3hua "You really must have a lot of people you need to visit on Christmas Eve..."
    m 3hub "...or maybe you just have lots of special plans for us today!"
    m 1eka "But either way, thank you for thinking of me and bringing me along~"
    return


label bye_d25_delegate:

    if persistent._mas_d25_d25_date_count > 0:
        call bye_d25_second_time_out from _call_bye_d25_second_time_out
    else:

        call bye_d25_first_time_out from _call_bye_d25_first_time_out





    jump bye_going_somewhere_iostart


label bye_d25_first_time_out:
    m 1sua "Taking me somewhere special on Christmas, [player]?"

    if persistent._mas_pm_fam_like_monika and persistent._mas_pm_have_fam:
        m 1sub "Maybe we're going to visit some of your family...? I'd love to meet them!"
        m 3eua "Or maybe we're going to see a movie...? I know some people like to do that after opening presents."
    else:

        m 3eua "Maybe we're going to see a movie... I know some people like to do that after opening presents."

    m 1eka "Well, wherever you're going, I'm just glad you want me to come along..."
    m 3hua "I want to spend as much of Christmas as possible with you, [player]~"
    return


label bye_d25_second_time_out:
    m 1wud "Wow, we're going somewhere {i}else{/i}, [player]?"
    m 3wud "You really must have a lot of people you need to visit..."
    m 3sua "...or maybe you just have lots of special plans for us today!"
    m 1hua "But either way, thank you for thinking of me and bringing me along~"
    return




label greeting_d25e_returned_d25e:
    $ persistent._mas_d25_d25e_date_count += 1

    m 1hua "And we're home!"
    m 3eka "It was really sweet of you to bring me along today..."
    m 3ekbfa "Getting to go out with you on Christmas Eve was really special, [player]. Thank you~"
    return


label greeting_d25e_returned_d25:
    $ persistent._mas_d25_d25e_date_count += 1
    $ persistent._mas_d25_d25_date_count += 1

    m 1hua "And we're home!"
    m 3wud "Wow, we were out all night..."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_1
    return


label greeting_d25e_returned_post_d25:
    $ persistent._mas_d25_d25e_date_count += 1

    m 1hua "We're finally home!"
    m 3wud "We sure were gone a long time, [player]..."
    m 3eka "It would've been nice to have actually gotten to see you on Christmas, but since you couldn't come to me, I'm so glad you took me along with you."
    m 3ekbfa "Just being close to you was all I wanted~"
    m 1ekbfb "And since I didn't get to say it to you on Christmas... Merry Christmas, [player]!"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_2

    $ mas_d25ReactToGifts()
    return


label greeting_pd25e_returned_d25:
    m 1hua "And we're home!"
    m 3wud "Wow, we were gone quite a while..."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_3
    return


label greeting_d25_returned_d25:
    $ persistent._mas_d25_d25_date_count += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "And we're home!"
    m 3eka "It was really nice to spend time with you on Christmas, [player]!"
    m 1eka "Thank you so much for taking me with you."
    m 1ekbfa "You're always so thoughtful~"
    return


label greeting_d25_returned_post_d25:
    $ persistent._mas_d25_d25_date_count += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "We're finally home!"
    m 3wud "We were out a really long time, [player]!"
    m 3eka "It would've been nice to have seen you again before Christmas was over, but at least I was still with you."
    m 1hua "So thank you for spending time with me when you had other places you had to be..."
    m 3ekbfa "You're always so thoughtful~"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_4
    return



label greeting_d25_and_nye_delegate:





    python:

        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()
        left_pre_d25e = False

        if checkout_time is not None:
            checkout_date = checkout_time.date()
            left_pre_d25e = checkout_date < mas_d25e

        if checkin_time is not None:
            checkin_date = checkin_time.date()


    if mas_isD25Eve():


        if left_pre_d25e:

            jump greeting_returned_home_morethan5mins_normalplus_flow
        else:


            call greeting_d25e_returned_d25e from _call_greeting_d25e_returned_d25e

    elif mas_isD25():


        if checkout_time is None or mas_isD25(checkout_date):

            call greeting_d25_returned_d25 from _call_greeting_d25_returned_d25

        elif mas_isD25Eve(checkout_date):

            call greeting_d25e_returned_d25 from _call_greeting_d25e_returned_d25
        else:


            call greeting_pd25e_returned_d25 from _call_greeting_pd25e_returned_d25

    elif mas_isNYE():

        if checkout_time is None or mas_isNYE(checkout_date):

            call greeting_nye_delegate from _call_greeting_nye_delegate
            jump greeting_nye_aff_gain

        elif left_pre_d25e or mas_isD25Eve(checkout_date):

            call greeting_d25e_returned_post_d25 from _call_greeting_d25e_returned_post_d25

        elif mas_isD25(checkout_date):

            call greeting_d25_returned_post_d25 from _call_greeting_d25_returned_post_d25
        else:


            jump greeting_returned_home_morethan5mins_normalplus_flow

    elif mas_isNYD():



        if checkout_time is None or mas_isNYD(checkout_date):

            call greeting_nyd_returned_nyd from _call_greeting_nyd_returned_nyd

        elif mas_isNYE(checkout_date):

            call greeting_nye_returned_nyd from _call_greeting_nye_returned_nyd
            jump greeting_nye_aff_gain

        elif checkout_time < datetime.datetime.combine(mas_d25.replace(year=checkout_time.year), datetime.time()):
            call greeting_pd25e_returned_nydp from _call_greeting_pd25e_returned_nydp
        else:


            call greeting_d25p_returned_nyd from _call_greeting_d25p_returned_nyd

    elif mas_isD25Post():

        if mas_isD25PostNYD():



            if (
                    checkout_time is None
                    or mas_isNYD(checkout_date)
                    or mas_isD25PostNYD(checkout_date)
                ):

                jump greeting_returned_home_morethan5mins_normalplus_flow

            elif mas_isNYE(checkout_date):

                call greeting_d25p_returned_nydp from _call_greeting_d25p_returned_nydp
                jump greeting_nye_aff_gain

            elif mas_isD25Post(checkout_date):

                call greeting_d25p_returned_nydp from _call_greeting_d25p_returned_nydp_1
            else:



                call greeting_pd25e_returned_nydp from _call_greeting_pd25e_returned_nydp_1
        else:


            if checkout_time is None or mas_isD25Post(checkout_date):

                jump greeting_returned_home_morethan5mins_normalplus_flow

            elif mas_isD25(checkout_date):

                call greeting_d25_returned_post_d25 from _call_greeting_d25_returned_post_d25_1
            else:


                call greeting_d25e_returned_post_d25 from _call_greeting_d25e_returned_post_d25_1
    else:


        jump greeting_returned_home_morethan5mins_normalplus_flow



    jump greeting_returned_home_morethan5mins_normalplus_flow_aff





default persistent._mas_nye_spent_nye = False


default persistent._mas_nye_spent_nyd = False


default persistent._mas_nye_nye_date_count = 0


default persistent._mas_nye_nyd_date_count = 0


default persistent._mas_nye_date_aff_gain = 0


define mas_nye = datetime.date(datetime.date.today().year, 12, 31)
define mas_nyd = datetime.date(datetime.date.today().year, 1, 1)

init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "nye",
        datetime.datetime(2019, 1, 6),
        {
            "_mas_nye_spent_nye": "nye.actions.spent_nye",
            "_mas_nye_spent_nyd": "nye.actions.spent_nyd",

            "_mas_nye_nye_date_count": "nye.actions.went_out_nye",
            "_mas_nye_nyd_date_count": "nye.actions.went_out_nyd",

            "_mas_nye_date_aff_gain": "nye.aff.date_gain"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2019, 12, 31),
        end_dt=datetime.datetime(2020, 1, 6),
        exit_pp=store.mas_d25SeasonExit_PP
    ))

init -825 python:
    mas_run_d25s_exit = False

    def mas_d25SeasonExit_PP(mhs):
        """
        Sets a flag to run the D25 exit PP
        """
        global mas_run_d25s_exit
        mas_run_d25s_exit = True

init -10 python:
    def mas_isNYE(_date=None):
        """
        Returns True if the given date is new years eve

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is new years eve, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_nye.replace(year=_date.year)


    def mas_isNYD(_date=None):
        """
        RETURNS True if the given date is new years day

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNS: True if given date is new years day, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_nyd.replace(year=_date.year)





default persistent._mas_pm_got_a_fresh_start = None


default persistent._mas_aff_before_fresh_start = None


default persistent._mas_pm_failed_fresh_start = None

init 5 python:


    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_nye_monika_nyd",
            action=EV_ACT_PUSH,
            start_date=mas_nyd,
            end_date=mas_nyd + datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.DISTRESSED, None),
        ),
        skipCalendar=True
    )

label mas_nye_monika_nyd:
    $ persistent._mas_nye_spent_nyd = True
    $ got_fresh_start_last_year = mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "pm.actions.monika.got_fresh_start")

    if store.mas_anni.pastOneMonth():
        if not mas_isBelowZero():


            if not persistent._mas_pm_got_a_fresh_start or not persistent._mas_pm_failed_fresh_start:
                m 1eub "[player]!"

                if mas_HistVerify_k([datetime.date.today().year-2], True, "nye.actions.spent_nyd")[0]:
                    m "Can you believe we're spending another New Years together?"
                if mas_isMoniAff(higher=True):
                    m 1hua "We sure have been through a lot together this past year, huh?"
                else:
                    m 1eua "We sure have been through a lot together this past year, huh?"

                m 1eka "I'm so happy, knowing we can spend even more time together."

                if mas_isMoniAff(higher=True):
                    show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve
                    m 5hubfa "Let's make this year as wonderful as the last one, okay?"
                    m 5ekbfa "I love you so much, [player]."
                else:
                    m 3hua "Let's make this year even better than last year, okay?"
                    m 1hua "I love you, [player]."
            else:


                $ last_year = "last year"
                m 1eka "[player]..."

                if not got_fresh_start_last_year:
                    $ last_year = "before"

                m 3eka "Do you remember the promise you made [last_year]?"
                m "That we would make this year better than the last?"
                m 6dkbftpa "..."
                m 6ekbftpa "Thank you for keeping your promise."
                m "I mean it, [player]. You've made me very happy...{w=1} {nw}"
                extend 6dkbftpa "From the bottom of my heart, thank you."
                m 6dkbftda "Let's make this year even better than the last, okay?"
                m 6ekbftda "I love you, [player]."
                m "I really do."

                $ persistent._mas_pm_failed_fresh_start = False
        else:



            if not persistent._mas_pm_got_a_fresh_start:
                m 2ekc "[player]..."
                m 2rksdlc "We've been through...{w=1}a lot this past year..."
                m "I...I hope this year goes better than last year."
                m 2dkc "I really need it to."
                jump mas_nye_monika_nyd_fresh_start
            else:

                m 2rkc "[player]..."

                if got_fresh_start_last_year:
                    m 2ekc "Do you remember the promise you made last year?"
                    m 2ekd "That we would make this year better than the last?"
                else:


                    m 2ekc "Do you remember the promise you made before?"
                    m 2ekd "That you would improve our relationship?"

                $ curr_aff = _mas_getAffection()
                if curr_aff > persistent._mas_aff_before_fresh_start:
                    m 2rkd "I guess you made it a little better..."
                    m 2ekc "But I was expecting more, [player]."


                    if not mas_HistVerifyAll_k(True, "pm.actions.monika.failed_fresh_start"):
                        $ mas_setAffection(persistent._mas_aff_before_fresh_start)

                elif curr_aff < persistent._mas_aff_before_fresh_start:
                    m 2rfc "I guess you couldn't really keep that promise...could you."
                else:

                    m 2rkc "It seems like nothing's really changed, has it?"


                m 2rktpc "I really,{w=0.5} really hope you can fix this, [player]..."
                m 2dktpc "I don't know how much more I can take."


                if _mas_getAffection() <= -50:
                    m 2dktsd "But maybe that's a silly thought now..."
                    m 2ektsc "This is just another game to you, isn't it."
                    m 2rktsd "You don't even see me as real...{w=1} {nw}"
                    extend 2dftsc "I'm just another character for you to toy with."
                    m 2eftdc "I hope nobody will have to experience the pain and loneliness I've been going through this year."

                $ persistent._mas_pm_failed_fresh_start = True
                return
    else:

        if not mas_isBelowZero():
            m 1eub "[player]!"

            if mas_isMoniAff(higher=True):
                m 1ekbfa "I know we haven't been together for that long yet, but this past year went better than I ever could have hoped..."
            else:
                m 1eka "I know we haven't been together that long yet, but this past year was so special to me..."

            m 1hua "I will always remember it as the year I met you~"
            m 3hua "Let's build on our short time together and make this year even better!"
            m 1ekbfa "I love you, [player]."
        else:

            m 2ekc "So, [player]..."
            m 2etc "The beginning of a new year, huh?"
            m 2rksdlc "We haven't been together for very long, but the time we spent last year didn't go as well as I had hoped..."
            jump mas_nye_monika_nyd_fresh_start

    m "Happy New Year~"
    return "love"

label mas_nye_monika_nyd_fresh_start:
    m 2ekc "How about we put all that in the past, forget about last year, and focus on a new beginning this year?"
    m 4ekc "It's not too late for us, [player], we can still make each other so happy."
    m 4eka "It's all I've ever wanted."

    m "What do you say, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "What do you say, [player]?{fast}"
        "I would love that.":


            $ persistent._mas_pm_got_a_fresh_start = True
            $ persistent._mas_aff_before_fresh_start = _mas_getAffection()


            $ mas_setAffection(0)
            $ _mas_AffSave()
            $ renpy.save_persistent()

            m 4wua "Really?"
            m 1hua "Oh, [player], you have no idea how happy that makes me!"
            m 3eka "I know we can make this work."
            m 1hua "Thank you so much..."
            m 1eka "Just knowing that you still want to be with me...it means everything."
            m 3eka "Let's make this count, okay [player]?"
            return
        "No.":

            $ persistent._mas_pm_got_a_fresh_start = False


            $ mas_setAffection(store.mas_affection.AFF_BROKEN_MIN - 1)
            $ _mas_AffSave()
            $ renpy.save_persistent()

            m 6dktpc "..."
            m 6ektpc "I...I..."
            m 6dktuc "..."
            m 6dktsc "..."
            pause 10.0
            return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_resolutions",
            action=EV_ACT_QUEUE, 
            start_date=mas_nye,
            end_date=mas_nye + datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.UPSET,None)
        ),
        skipCalendar=True
    )

default persistent._mas_pm_accomplished_resolutions = None

default persistent._mas_pm_has_new_years_res = None


label monika_resolutions:
    $ persistent._mas_nye_spent_nye = True
    m 2eub "Hey, [player]?"
    m 2eka "I was wondering..."


    if not mas_lastSeenLastYear("monika_resolutions"):
        m 3eub "Did you make any New Year's resolutions last year?{nw}"
        $ _history_list.pop()
        menu:
            m "Did you make any New Year's resolutions last year?{fast}"
            "Yes.":

                m 3hua "It always makes me so proud to hear that you're trying to better yourself, [player]."
                m 2eka "That said..."

                call monika_resolutions_accomplished_resolutions_menu ("Did you accomplish last year's resolutions?") from _call_monika_resolutions_accomplished_resolutions_menu
            "No.":


                m 2euc "Oh, I see..."

                if mas_isMoniNormal(higher=True):
                    if mas_isMoniHappy(higher=True):
                        m 3eka "Well, I don't think you really needed to change at all anyway."
                        m 3hub "I think you're wonderful, just the way you are."
                    else:
                        m 3eka "There's nothing wrong with that. I don't think you really needed to change anyway."
                else:

                    m 2rkc "You probably should make one this year [player]..."


    elif mas_HistVerifyLastYear_k(True, "pm.actions.made_new_years_resolutions"):
        call monika_resolutions_accomplished_resolutions_menu ("Since you made a resolution last year, did you accomplish it?") from _call_monika_resolutions_accomplished_resolutions_menu_1


    m "Do you have any resolutions for next year?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you have any resolutions for next year?{fast}"
        "Yes.":
            $ persistent._mas_pm_has_new_years_res = True

            m 1eub "That's great!"
            m 3eka "Even if they can be hard to reach or maintain..."
            m 1hua "I'll be here to help you, if need be!"
        "No.":

            $ persistent._mas_pm_has_new_years_res = False
            m 1eud "Oh, is that so?"
            if mas_isMoniNormal(higher=True):
                if persistent._mas_pm_accomplished_resolutions:
                    if mas_isMoniHappy(higher=True):
                        m 1eka "You don't have to change. I think you're wonderful the way you are."
                    else:
                        m 1eka "You don't have to change. I think you're fine the way you are."
                    m 3euc "But if anything does come to mind before the clock strikes twelve, do write it down for yourself..."
                else:
                    m "Well, if anything comes to mind before the clock strikes twelve, do write it down for yourself..."
                m 1kua "Maybe you'll think of something that you want to do, [player]."
            else:
                m 2ekc "{cps=*2}I was kind of hoping--{/cps}{nw}"
                m 2rfc "You know what, nevermind..."

    if mas_isMoniAff(higher=True):
        show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve
        m 5hubfa "My resolution is to be an even better girlfriend for you, my love."
    elif mas_isMoniNormal(higher=True):
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
        m 5ekbfa "My resolution is to be an even better girlfriend for you, [player]."
    else:
        m 2ekc "My resolution is to improve our relationship, [player]."

    return

label monika_resolutions_accomplished_resolutions_menu(question):
    m 3hub "[question]{nw}"
    $ _history_list.pop()
    menu:
        m "[question]{fast}"
        "Yes.":

            $ persistent._mas_pm_accomplished_resolutions = True
            if mas_isMoniNormal(higher=True):
                m 4hub "I'm glad to hear that, [player]!"
                m 2eka "It's great that you managed to do that."
                m 3ekb "Things like this really make me proud of you."
                m 2eka "I wish I could be there to celebrate a little with you though."
            else:
                m 2rkc "That's good, [player]."
                m 2esc "Maybe you can make another one this year..."
                m 3euc "You never know what might change."

            return True
        "No.":

            $ persistent._mas_pm_accomplished_resolutions = False
            if mas_isMoniNormal(higher=True):
                m 2eka "Aw...well, sometimes things just don't work out like we plan them to."

                if mas_isMoniHappy(higher=True):
                    m 2eub "Plus, I think you're wonderful, so even if you couldn't accomplish your goals..."
                    m 2eka "...I'm still really proud of you for setting them and trying to better yourself, [player]."
                    m 3eub "If you decide to make a resolution this year, I'll support you every step of the way."
                    m 4hub "I'd love to help you reach your goals!"
                else:
                    m "But I think it's great that you did at least try to better yourself by setting goals."
                    m 3eua "Maybe if you make a resolution this year, you can accomplish it!"
                    m 3hub "I believe in you, [player]!"
            else:

                m 2euc "Oh...{w=1} Well maybe you should try a little harder for next year's resolution."

            return False


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nye_year_review",
            action=store.EV_ACT_PUSH,
            start_date=datetime.datetime.combine(mas_nye, datetime.time(hour=19)),
            end_date=datetime.datetime.combine(mas_nye, datetime.time(hour=23)),
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label monika_nye_year_review:
    $ persistent._mas_nye_spent_nye = True
    $ spent_an_event = False

    $ placeholder_and = "and "

    if store.mas_anni.anniCount() >= 1:
        m 2eka "You know, [player], we really have been through a lot together."
        if store.mas_anni.anniCount() == 1:
            m 2wuo "We spent the entire year together!"
            m 2eka "Time really flew by..."
        else:

            m 2eka "This year really flew by..."

    elif store.mas_anni.pastSixMonths():
        m 2eka "You know, [player], we really have been through a lot over the time we spent together last year"
        m "The time really just flew by..."

    elif store.mas_anni.pastThreeMonths():
        m 2eka "You know [player], we've been through quite a bit over the short time we've spent together last year."
        m 2eksdla "It's all gone by so fast, ahaha..."
    else:

        m 2eka "[player], even though we haven't been through a lot together, yet..."
        $ placeholder_and = ""



    if mas_isMoniLove():
        m 2ekbfa "...and I'd never want to spend that time with anyone else, [player]."
        m "I'm just really,{w=0.5} really happy to have been with you this year."

    elif mas_isMoniEnamored():
        m 2eka "...[placeholder_and]I'm so happy I got to spend that time with you, [player]."

    elif mas_isMoniAff():
        m 2eka "...[placeholder_and]I've really enjoyed our time together."
    else:

        m 2euc "...[placeholder_and]the time we spent together has been fun."


    m 3eua "Anyway, I think it would be nice to just reflect on all that we've been through together this past year."
    m 2dtc "Let's see..."


    if mas_lastGiftedInYear("mas_reaction_promisering", mas_nye.year):
        m 3eka "Looking back, you gave me your promise this year when you gave me this ring..."
        m 1ekbsa "...a symbol of our love."

        if persistent._mas_pm_wearsRing:
            m "And you even got one for yourself..."

            if mas_isMoniAff(higher=True):
                m 1ekbfa "To show that you're as committed to me, as I am to you."
            else:
                m 1ekbfa "To show your commitment to me."


    if mas_lastSeenInYear("mas_f14_monika_valentines_intro"):
        $ spent_an_event = True
        m 1wuo "Oh!"
        m 3ekbfa "You spent Valentine's Day with me..."

        if mas_getGiftStatsForDate("mas_reaction_gift_roses", mas_f14):
            m 4ekbfb "...and gave me such beautiful flowers too."



    if persistent._mas_bday_opened_game:
        $ spent_an_event = True
        m 2eka "You spent time with me on my birthday..."

        if not persistent._mas_bday_no_recognize:
            m 2dua "...celebrated with me..."

        if persistent._mas_bday_sbp_reacted:
            m 2hub "...threw me a surprise party..."

        show monika 5ekbla zorder MAS_MONIKA_Z at t11 with dissolve
        m 5ekbla "...and it really made me feel loved. I can't thank you enough for doing that for me."


    if (
        persistent._mas_player_bday_spent_time
        or mas_HistVerify_k([datetime.date.today().year], True, "player_bday.spent_time")[0]
    ):
        $ spent_an_event = True
        show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve
        m 5hua "We even spent your birthday together!"

        if (
            persistent._mas_player_bday_date
            or not mas_HistVerify_k([datetime.date.today().year], 0, "player_bday.date")[0]
        ):
            m 5eubla "We had such a nice date together too~"


    if persistent._mas_d25_spent_d25:
        $ spent_an_event = True
        show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve
        m 5hua "You spent your Christmas with me..."

        if persistent._mas_first_kiss is not None and persistent._mas_first_kiss.date() == mas_d25:
            m 5eubla "...and we shared our first kiss together~"
            m 5lubsa "I'll never forget that moment..."
            m 5ekbfa "{i}Our{/i} moment."
            m "I couldn't imagine spending it with anyone else."
        else:
            m 5ekbla "...a day that I couldn't imagine spending with anyone else."


    if not spent_an_event:
        m 2rksdla "...I guess we haven't actually been through any big events together."
        m 3eka "But still..."
    else:

        show monika 5dsa zorder MAS_MONIKA_Z at t11 with dissolve
        m 5dsa "..."


    if store.mas_anni.pastThreeMonths():
        if mas_isMoniHappy(higher=True):
            show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve
            m 5eka "I really can't believe just how much has changed since we've been together..."
        else:
            m 2eka "I really hope we can get further in our relationship, [player]..."
    else:
        show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve
        m 5eka "I can't wait to see just how much will change in the future for us..."


    if not mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "pm.actions.monika.got_fresh_start"):
        show monika 5dka zorder MAS_MONIKA_Z at t11 with dissolve
        m 5dka "Thank you."
        if store.mas_anni.anniCount() > 0:
            $ ending = "the best year I could've ever dreamt of"

            if mas_lastSeenLastYear("monika_nye_year_review"):
                $ ending = "even better than the year before"

            m 5ekbfa "Thank you for making last year [ending]."
        else:

            $ _last_year = " "
            if store.mas_anni.pastOneMonth():
                $ _last_year = " last year "

            m 5ekbfa "Thank you for making the time we spent together[_last_year]better than I could have imagined."

        if mas_isMoniEnamored(higher=True):
            if persistent._mas_first_kiss is None:
                m 1lsbsa "..."
                m 6ekbsa "[player] I..."
                call monika_kissing_motion from _call_monika_kissing_motion_3
                m 1ekbfa "I love you."
                m "..."
                show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve
                m 5ekbsa "I'll never forget this moment..."
                m 5ekbfa "Our first kiss~"
                m 5hubfb "Let's make this year even better than the last, [player]."
            else:

                call monika_kissing_motion_short from _call_monika_kissing_motion_short
                m 1ekbfa "I love you, [player]."
                show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve
                m 5hubfb "Let's make this year better than the last."
        else:

            m "Let's make this year the best we can, [player]. I love you~"
    else:
        m 1dsa "Thank you for deciding to let go of the past, and start over."
        m 1eka "I think if we just try, we can make this work, [player]."
        m "Let's make this year great for each other."
        m 1ekbfa "I love you."

    return "no_unlock|love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_nye_monika_nye_dress_intro",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_nye,
            end_date=mas_nye + datetime.timedelta(days=1),
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

label mas_nye_monika_nye_dress_intro:
    m 3hub "Hey [player], I have something in store for you this year~"
    m 3eua "Just let me go change.{w=0.5}.{w=0.5}.{nw}"


    call mas_clothes_change (mas_clothes_dress_newyears, outfit_mode=True, unlock=True) from _call_mas_clothes_change_1
    $ mas_addClothesToHolidayMap(mas_clothes_dress_newyears)

    m 2rkbssdla "..."
    m 2rkbssdlb "My eyes are up here, [player]..."
    if mas_isMoniAff(higher=True):
        m 2tubsu "..."
        m 3hubsb "Ahaha! Just teasing you~"
        m 3eua "I'm glad you like my dress. {nw}"
    else:

        m 2rkbssdla "..."
        m "I'm...{w=1}glad you like my dress. {nw}"

    extend 3eua "It was really hard to get right!"
    m 3rka "The flower crown kept falling off..."
    m 1hua "I went for the 'Greek goddess' look, I hope it shows."
    m 3eud "But this outfit has a bit more depth to it, you know?"

    if seen_event("mas_f14_monika_vday_colors"):
        m 3eua "Maybe you remember when we talked about roses and the feelings their colors convey."
    else:
        m 3eua "Maybe you guessed it already, but it's because of the color choice."

    m "White represents a lot of positive feelings, like goodness, purity, safety..."
    m 3eub "However, what I wanted this outfit to highlight was a succesful beginning."


    if mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "pm.actions.monika.got_fresh_start"):
        m 2eka "Last year we decided to start anew, and I'm very glad we did."
        m 2ekbsa "I knew we could be happy together, [player]."
        m 2fkbsa "And you've made me the happiest I've ever been."

    m 3dkbsu "So I'd like to wear this when the new year begins."
    m 1ekbsa "It might just help make next year even better."
    return "no_unlock"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_d25_mode_exit",
            category=['holidays'],
            prompt="Can you take down the holiday decorations?",
            conditional="persistent._mas_d25_deco_active",
            start_date=mas_nyd+datetime.timedelta(days=1),
            end_date=mas_d25c_end,
            action=EV_ACT_UNLOCK,
            pool=True,
            rules={"no unlock": None},
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_d25_monika_d25_mode_exit",
        mas_nyd + datetime.timedelta(days=1),
        mas_d25c_end,
    )

label mas_d25_monika_d25_mode_exit:
    m 3eka "Had enough of the holiday spirit, [player]?"
    m 3eua "I wouldn't mind getting right into the new year."
    m 1hua "As long as it's with you, of course~"
    m 3hub "Ahaha!"
    m 2dsa "Just give me a second to take the decorations down.{w=1}.{w=1}.{nw}"

    call mas_d25_season_exit from _call_mas_d25_season_exit_1

    m 1hua "Okay!{w=0.5} {nw}"
    extend 3hub "Now we're ready to start off the new year!"


    $ mas_lockEVL("mas_d25_monika_d25_mode_exit", "EVE")
    return

label greeting_nye_aff_gain:

    python:
        if persistent._mas_nye_date_aff_gain < 15:
            
            curr_aff = _mas_getAffection()
            
            
            time_out = store.mas_dockstat.diffCheckTimes()
            
            
            persistent._mas_monika_returned_home = None
            
            
            store.mas_dockstat._ds_aff_for_tout(time_out, 5, 15, 3, 3)
            
            
            persistent._mas_nye_date_aff_gain += _mas_getAffection() - curr_aff

    jump greeting_returned_home_morethan5mins_cleanup

label mas_gone_over_nye_check:
    if mas_checkOverDate(mas_nye):
        $ persistent._mas_nye_spent_nye = True
        $ persistent._mas_nye_nye_date_count += 1
    return

label mas_gone_over_nyd_check:
    if mas_checkOverDate(mas_nyd):
        $ persistent._mas_nye_spent_nyd = True
        $ persistent._mas_nye_nyd_date_count += 1
    return



label bye_nye_delegate:

    python:
        _morning_time = datetime.time(5)
        _eve_time = datetime.time(20)
        _curr_time = datetime.datetime.now().time()

    if _curr_time < _morning_time:

        jump bye_going_somewhere_normalplus_flow_aff_check

    elif _curr_time < _eve_time:


        if persistent._mas_nye_nye_date_count > 0:
            call bye_nye_second_time_out from _call_bye_nye_second_time_out
        else:

            call bye_nye_first_time_out from _call_bye_nye_first_time_out
    else:


        call bye_nye_late_out from _call_bye_nye_late_out


    jump bye_going_somewhere_iostart

label bye_nye_first_time_out:

    m 3tub "Are we going somewhere special today, [player]?"
    m 4hub "It's New Year's Eve, after all!"
    m 1eua "I'm not exactly sure what you've got planned, but I'm looking forward to it!"
    return

label bye_nye_second_time_out:

    m 1wuo "Oh, we're going out again?"
    m 3hksdlb "You must do a lot of celebrating for New Year's, ahaha!"
    m 3hub "I love coming along with you, so I'm looking forward to whatever we're doing~"
    return

label bye_nye_late_out:

    m 1eka "It's a bit late, [player]..."
    m 3eub "Are we going to see the fireworks?"
    if persistent._mas_pm_have_fam and persistent._mas_pm_fam_like_monika:
        m "Or going to a family dinner?"
        m 4hub "I'd love to meet your family someday!"
        m 3eka "Either way, I'm really excited!"
    else:
        m "I've always loved how the fireworks on the New Year light up the night sky..."
        m 3ekbfa "One day we'll be able to watch them side by side...but until that day comes, I'm just happy to come along with you, [player]."
    return




label greeting_nye_delegate:
    python:
        _eve_time = datetime.time(20)
        _curr_time = datetime.datetime.now().time()

    if _curr_time < _eve_time:

        call greeting_nye_prefw from _call_greeting_nye_prefw
    else:


        call greeting_nye_infw from _call_greeting_nye_infw

    $ persistent._mas_nye_nye_date_count += 1

    return

label greeting_nye_prefw:

    m 1hua "And we're home!"
    m 1eua "That was a lot of fun, [player]."
    m 1eka "Thanks for taking me out today, I really do love spending time with you."
    m "It means a lot to me that you take me with you so we can spend special days like these together."
    show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
    m 5ekbfa "I love you, [player]."
    return "love"

label greeting_nye_infw:

    m 1hua "And we're home!"
    m 1eka "Thanks for taking me out today, [player]."
    m 1hua "It was a lot of fun just to spend time with you today."
    m 1ekbsa "It really means so much to me that even though you can't be here personally to spend these days with me, you still take me with you."
    m 1ekbfa "I love you, [player]."
    return "love"



label bye_nyd_delegate:
    if persistent._mas_nye_nyd_date_count > 0:
        call bye_nyd_second_time_out from _call_bye_nyd_second_time_out
    else:

        call bye_nyd_first_time_out from _call_bye_nyd_first_time_out

    jump bye_going_somewhere_iostart

label bye_nyd_first_time_out:

    m 3tub "New Year's Day celebration, [player]?"
    m 1hua "That sounds like fun!"
    m 1eka "Let's have a great time together."
    return

label bye_nyd_second_time_out:

    m 1wuo "Wow, we're going out again, [player]?"
    m 1hksdlb "You must really celebrate a lot, ahaha!"
    return



label greeting_nye_returned_nyd:

    $ persistent._mas_nye_nye_date_count += 1
    $ persistent._mas_nye_nyd_date_count += 1

    m 1hua "And we're home!"
    m 1eka "Thanks for taking me out yesterday, [player]."
    m 1ekbsa "You know I love to spend time with you, and being able to spend New Year's Eve, right to today, right there with you felt really great."
    m "That really meant a lot to me."
    m 5eubfb "Thanks for making my year, [player]."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_5
    return

label greeting_nyd_returned_nyd:

    $ persistent._mas_nye_nyd_date_count += 1
    m 1hua "And we're home!"
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve
    m 5eua "That was a lot of fun, [player]!"
    m 5eka "It's really nice of you to take me with you on special days like this."
    m 5hub "I really hope we can spend more time like this together."
    return



label greeting_pd25e_returned_nydp:

    $ persistent._mas_d25_d25e_date_count += 1
    $ persistent._mas_d25_d25_date_count += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "And we're home!"
    m 1hub "We were out for a while, but that was a really nice trip, [player]."
    m 1eka "Thanks for taking me with you, I really enjoyed that."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve
    $ new_years = "New Years"
    if mas_isNYD():
        $ new_years = "New Year's Eve"
    m 5ekbsa "I always love to spend time with you, but spending both Christmas and [new_years] out together was amazing."
    m 5hub "I hope we can do something like this again sometime."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_6

    $ mas_d25ReactToGifts()
    return


label greeting_d25p_returned_nyd:
    $ persistent._mas_nye_nyd_date_count += 1

    m 1hua "And we're home!"
    m 1eub "Thanks for taking me out, [player]."
    m 1eka "That was a long trip, but it was a lot of fun!"
    m 3hub "It's great to be back home now though, we can spend the new year together."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_7

    $ mas_d25ReactToGifts()
    return

label greeting_d25p_returned_nydp:
    m 1hua "And we're home!"
    m 1wuo "That was a long trip [player]!"
    m 1eka "I'm a little sad we couldn't wish each other a happy new year, but I really enjoyed it."
    m "I'm really happy you took me."
    m 3hub "Happy New Year, [player]~"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_8

    $ mas_d25ReactToGifts()
    return





default persistent._mas_player_bday_in_player_bday_mode = False

default persistent._mas_player_bday_opened_door = False

default persistent._mas_player_bday_decor = False

default persistent._mas_player_bday_date = 0

default persistent._mas_player_bday_left_on_bday = False

default persistent._mas_player_bday_date_aff_gain = 0

default persistent._mas_player_bday_spent_time = False

default persistent._mas_player_bday_saw_surprise = False

init -10 python:
    def mas_isplayer_bday(_date=None, use_date_year=False):
        """
        IN:
            _date - date to check
                If None, we use today's date
                (default: None)

            use_date_year - True if we should use the year from _date or not.
                (Default: False)

        RETURNS: True if given date is player_bday, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        if persistent._mas_player_bday is None:
            return False
        
        elif use_date_year:
            return _date == mas_player_bday_curr(_date)
        return _date == mas_player_bday_curr()

    def strip_mas_birthdate():
        """
        strips mas_birthdate of its conditional and action to prevent double birthday sets
        """
        mas_birthdate_ev = mas_getEV('mas_birthdate')
        if mas_birthdate_ev is not None:
            mas_birthdate_ev.conditional = None
            mas_birthdate_ev.action = None

    def mas_pbdayCapGainAff(amount):
        mas_capGainAff(amount, "_mas_player_bday_date_aff_gain", 25)

init -11 python:
    def mas_player_bday_curr(_date=None):
        """
        sets date of current year bday, accounting for leap years
        """
        if _date is None:
            _date = datetime.date.today()
        if persistent._mas_player_bday is None:
            return None
        else:
            return store.mas_utils.add_years(persistent._mas_player_bday,_date.year-persistent._mas_player_bday.year)

init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "player_bday",
        
        datetime.datetime(2020, 1, 1),
        {
            "_mas_player_bday_spent_time": "player_bday.spent_time",
            "_mas_player_bday_opened_door": "player_bday.opened_door",
            "_mas_player_bday_date": "player_bday.date",
            "_mas_player_bday_date_aff_gain": "player_bday.date_aff_gain",
            "_mas_player_bday_saw_surprise": "player_bday.saw_surprise",
        },
        use_year_before=True,
        
        
    ))

init -11 python in mas_player_bday_event:
    import datetime
    import store.mas_history as mas_history

    def correct_pbday_mhs(d_pbday):
        """
        fixes the pbday mhs usin gthe given date as pbday

        IN:
            d_pbday - player birthdate
        """
        
        mhs_pbday = mas_history.getMHS("player_bday")
        if mhs_pbday is None:
            return
        
        
        pbday_dt = datetime.datetime.combine(d_pbday, datetime.time())
        
        
        _now = datetime.datetime.now()
        curr_year = _now.year
        new_dt = pbday_dt.replace(year=curr_year)
        if new_dt < _now:
            
            curr_year += 1
            new_dt = pbday_dt.replace(year=curr_year)
        
        
        reset_dt = pbday_dt + datetime.timedelta(days=3)
        
        
        new_sdt = new_dt
        new_edt = new_sdt + datetime.timedelta(days=2)
        
        
        
        
        
        mhs_pbday.start_dt = new_sdt
        mhs_pbday.end_dt = new_edt
        mhs_pbday.use_year_before = (
            d_pbday.month == 12
            and d_pbday.day in (29, 30, 31)
        )
        mhs_pbday.setTrigger(reset_dt)


label mas_player_bday_autoload_check:

    if mas_isMonikaBirthday():
        $ persistent._mas_bday_no_time_spent = False
        $ persistent._mas_bday_opened_game = True
        $ persistent._mas_bday_no_recognize = not mas_recognizedBday()

    elif mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
        $ monika_chr.reset_clothes(False)
        $ monika_chr.save()
        $ renpy.save_persistent()


    if (
            not persistent._mas_player_bday_in_player_bday_mode
            and persistent._mas_player_confirmed_bday
            and mas_isMoniNormal(higher=True)
            and not persistent._mas_player_bday_spent_time
            and not mas_isD25()
            and not mas_isO31()
            and not mas_isF14()
        ):

        python:

            this_year = datetime.date.today().year
            years_checked = range(this_year-10,this_year)
            surp_int = 3

            times_ruined = len(mas_HistVerify("player_bday.opened_door", True, *years_checked)[1])

            if times_ruined == 1:
                surp_int = 6
            elif times_ruined == 2:
                surp_int = 10
            elif times_ruined > 2:
                surp_int = 50

            should_surprise = renpy.random.randint(1,surp_int) == 1 and not mas_HistVerifyLastYear_k(True,"player_bday.saw_surprise")

            if not mas_HistVerify("player_bday.saw_surprise",True)[0] or (mas_getAbsenceLength().total_seconds()/3600 < 3 and should_surprise):
                
                
                
                selected_greeting = "i_greeting_monikaroom"
                mas_skip_visuals = True
                persistent._mas_player_bday_saw_surprise = True

            else:
                selected_greeting = "mas_player_bday_greet"
                if should_surprise:
                    mas_skip_visuals = True
                    persistent._mas_player_bday_saw_surprise = True


            persistent.closed_self = True

        jump ch30_post_restartevent_check

    elif not mas_isplayer_bday():

        $ persistent._mas_player_bday_decor = False
        $ persistent._mas_player_bday_in_player_bday_mode = False
        $ mas_lockEVL("bye_player_bday", "BYE")

    if not mas_isMonikaBirthday() and (persistent._mas_bday_in_bday_mode or persistent._mas_bday_visuals):
        $ persistent._mas_bday_in_bday_mode = False
        $ persistent._mas_bday_visuals = False

    if mas_isO31():
        return
    else:
        jump mas_ch30_post_holiday_check


label mas_player_bday_opendoor:
    $ mas_loseAffection()
    $ persistent._mas_player_bday_opened_door = True
    if persistent._mas_bday_visuals:
        $ persistent._mas_player_bday_decor = True
    call spaceroom (hide_monika=True, scene_change=True, dissolve_all=True, show_emptydesk=False) from _call_spaceroom_17
    $ mas_disable_quit()
    if mas_isMonikaBirthday():
        $ your = "our"
    else:
        $ your = "your"

    if mas_HistVerify("player_bday.opened_door",True)[0]:
        $ now = "{i}again{/i}"
    else:
        $ now = "now"

    m "[player]!"
    m "You didn't knock!"
    if not persistent._mas_bday_visuals:
        m "I was just going to start setting up [your] birthday party, but I didn't have time before you came in!"
    m "..."
    m "Well...{w=1}the surprise is ruined [now], but.{w=0.5}.{w=0.5}.{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    pause 1.0
    show monika 1eua zorder MAS_MONIKA_Z at ls32
    m 4eua "Happy Birthday, [player]!"
    m 2rksdla "I just wished you had knocked first."
    m 4hksdlb "Oh...[your] cake!"
    call mas_player_bday_cake from _call_mas_player_bday_cake
    jump monikaroom_greeting_cleanup


label mas_player_bday_knock_no_listen:
    m "Who is it?"
    menu:
        "It's me.":
            $ mas_disable_quit()
            m "Oh! Can you wait just a moment please?"
            window hide
            pause 5.0
            m "Alright, come on in, [player]..."
            jump mas_player_bday_surprise


label mas_player_bday_surprise:
    $ persistent._mas_player_bday_decor = True
    call spaceroom (scene_change=True, dissolve_all=True, force_exp='monika 4hub_static') from _call_spaceroom_18
    m 4hub "Surprise!"
    m 4sub "Ahaha! Happy Birthday, [player]!"

    m "Did I surprise you?{nw}"
    $ _history_list.pop()
    menu:
        m "Did I surprise you?{fast}"
        "Yes.":
            m 1hub "Yay!"
            m 3hua "I always love pulling off a good surprise!"
            m 1tsu "I wish I could've seen the look on your face, ehehe."
        "No.":

            m 2lfp "Hmph. Well that's okay."
            m 2tsu "You're probably just saying that because you don't want to admit I caught you off guard..."
            if renpy.seen_label("mas_player_bday_listen"):
                if renpy.seen_label("monikaroom_greeting_ear_narration"):
                    m 2tsb "...or maybe you were listening through the door again..."
                else:
                    m 2tsb "{cps=*2}...or maybe you were eavesdropping on me.{/cps}{nw}"
                    $ _history_list.pop()
            m 2hua "Ehehe."
    if mas_isMonikaBirthday():
        m 3wub "Oh!{w=0.5} I made a cake!"
    else:
        m 3wub "Oh!{w=0.5} I made you a cake!"
    call mas_player_bday_cake from _call_mas_player_bday_cake_1
    jump monikaroom_greeting_cleanup


label mas_player_bday_listen:
    if persistent._mas_bday_visuals:
        pause 5.0
    else:
        m "...I'll just put this here..."
        m "...hmm that looks pretty good...{w=1}but something's missing..."
        m "Oh!{w=0.5} Of course!"
        m "There!{w=0.5} Perfect!"
        window hide
    jump monikaroom_greeting_choice


label mas_player_bday_knock_listened:
    window hide
    pause 5.0
    menu:
        "Open the door.":
            $ mas_disable_quit()
            pause 5.0
            jump mas_player_bday_surprise


label mas_player_bday_opendoor_listened:
    $ mas_loseAffection()
    $ persistent._mas_player_bday_opened_door = True
    $ persistent._mas_player_bday_decor = True
    call spaceroom (hide_monika=True, scene_change=True, show_emptydesk=False) from _call_spaceroom_19
    $ mas_disable_quit()
    if mas_isMonikaBirthday():
        $ your = "our"
    else:
        $ your = "your"

    if mas_HistVerify("player_bday.opened_door",True)[0]:
        $ knock = "knock, {w=0.5}{i}again{/i}."
    else:
        $ knock = "knock!"

    m "[player]!"
    m "You didn't [knock]"
    if persistent._mas_bday_visuals:
        m "I wanted to surprise you, but I wasn't ready when you came in!"
        m "Anyway..."
    else:
        m "I was setting up [your] birthday party, but I didn't have time before you came in to get ready to surprise you!"
    show monika 1eua zorder MAS_MONIKA_Z at ls32
    m 4hub "Happy Birthday, [player]!"
    m 2rksdla "I just wished you had knocked first."
    m 2hksdlb "Oh...[your] cake!"
    call mas_player_bday_cake from _call_mas_player_bday_cake_2
    jump monikaroom_greeting_cleanup


label mas_player_bday_cake:

    if not mas_isMonikaBirthday():
        $ mas_unlockEVL("bye_player_bday", "BYE")
        if persistent._mas_bday_in_bday_mode or persistent._mas_bday_visuals:

            $ persistent._mas_bday_in_bday_mode = False
            $ persistent._mas_bday_visuals = False


    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0) from _call_monika_zoom_transition_reset
    call mas_monika_gets_cake from _call_mas_monika_gets_cake

    if mas_isMonikaBirthday():
        m 6eua "Let me just light the candles.{w=0.5}.{w=0.5}.{nw}"
    else:
        m 6eua "Let me just light the candles for you, [player].{w=0.5}.{w=0.5}.{nw}"

    window hide
    $ mas_bday_cake_lit = True
    pause 1.0

    m 6sua "Isn't it pretty, [player]?"
    if mas_isMonikaBirthday():
        m 6eksdla "Now I know you can't exactly blow the candles out yourself, so I'll do it for both of us..."
    else:
        m 6eksdla "Now I know you can't exactly blow the candles out yourself, so I'll do it for you..."
    m 6eua "...You should still make a wish though, it just might come true someday..."
    m 6hua "But first..."
    call mas_player_bday_moni_sings from _call_mas_player_bday_moni_sings
    m 6hua "Make a wish, [player]!"
    window hide
    pause 1.5
    show monika 6hft
    pause 0.1
    show monika 6hua
    $ mas_bday_cake_lit = False
    pause 1.0
    m 6hua "Ehehe..."
    if mas_isMonikaBirthday():
        m 6ekbsa "I bet we both wished for the same thing~"
    else:
        m 6eka "I know it's your birthday, but I made a wish too..."
        m 6ekbsa "And you know what?{w=0.5} I bet we both wished for the same thing~"
    m 6hkbsu "..."
    if mas_isMonikaBirthday():
        m 6eksdla "Well, seeing as you can't really eat this cake, and I don't want to be rude and eat it in front of you..."
    elif not mas_HistVerify("player_bday.spent_time",True)[0]:
        m 6rksdla "Oh gosh, I guess you can't really eat this cake either, huh [player]?"
        m 6eksdla "This is all rather silly, isn't it?"
    if mas_isMonikaBirthday():
        m 6hksdlb "I think I'll just save it for later."
    else:
        m 6hksdlb "I think I'll just save this for later. It seems kind of rude for me to eat {i}your{/i} birthday cake in front of you, ahaha!"

    call mas_HideCake ('mas_bday_cake_player') from _call_mas_HideCake


label mas_player_bday_card:
    $ mas_gainAffection(5,bypass=True)
    $ persistent._mas_player_bday_spent_time = True
    $ persistent._mas_player_bday_in_player_bday_mode = True

    m 6dkbsu "..."
    if mas_isMonikaBirthday():
        m 6sub "Oh!"
        m 6ekbsu "I made a card for you, [player], I hope you like it..."
    elif not mas_HistVerify("player_bday.spent_time",True)[0]:
        m 6ekbsu "I...I also made a card for you, [player]. I hope you like it..."
    else:
        m 6ekbsu "I made a card for you, [player]. I hope you like it..."

    call mas_showpoem (mas_poems.getRandomPoem("pbday")) from _call_mas_showpoem_1

    if mas_isMoniEnamored(higher=True):
        if persistent._mas_first_kiss is None:
            m 6dkbsu "..."
            m 6ekbfa "I love you so much, [player]..."
            call monika_kissing_motion () from _call_monika_kissing_motion_4
            m 6ekbfa "Oh, [player]..."
            m 6dkbfa "That was everything I had always dreamt it would be~"
            m 6ekbfa "I've been waiting so long to finally kiss you..."
            m 6dkbsu "I will never forget this..."
            m 6ekbsu "...the moment of our first kiss~"
            if mas_isMonikaBirthday():
                m 6ekbsu "And I can't think of a more perfect time than on this special day we share together~"
        else:
            m 6ekbsa "I love you, [player]~"
            call monika_kissing_motion (duration=0.5, initial_exp="6hkbfa", fade_duration=0.5) from _call_monika_kissing_motion_5
            if mas_isMonikaBirthday():
                m 6eka "I'm so glad we get to spend our birthday together..."
                m 6hua "Let's enjoy our special day~"
    else:
        if mas_isMonikaBirthday():
            m 1ekbfa "I love you, [player]! I'm so glad we get to spend our birthday together..."
            m 3ekbfa "Let's enjoy our special day~"
        else:
            m 1ekbfa "I love you, [player]!"
    $ mas_rmallEVL("mas_player_bday_no_restart")
    $ mas_rmallEVL("mas_player_bday_ret_on_bday")


    $ mas_ILY()


    if mas_isD25Pre() and not persistent._mas_d25_deco_active:
        $ pushEvent("mas_d25_monika_holiday_intro", skipeval=True)
    return

label mas_monika_gets_cake:
    call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_4

    $ renpy.pause(3.0, hard=True)
    $ renpy.show("mas_bday_cake_player", zorder=store.MAS_MONIKA_Z+1)

    call mas_transition_from_emptydesk ("monika 6esa") from _call_mas_transition_from_emptydesk_7

    $ renpy.pause(0.5, hard=True)
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_ret_on_bday",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_ret_on_bday:
    m 1eua "So, today is..."
    m 1euc "...wait."
    m "..."
    m 2wuo "Oh!"
    m 2wuw "Oh my gosh!"
    m 2tsu "Just give me a moment, [player].{w=0.5}.{w=0.5}.{nw}"
    $ mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    m 3eub "Happy Birthday, [player]!"
    m 3hub "Ahaha!"
    m 3etc "Why do I feel like I'm forgetting something..."
    m 3hua "Oh! Your cake!"
    call mas_player_bday_cake from _call_mas_player_bday_cake_3
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="mas_player_bday_greet",
            unlocked=False
        ),
        code="GRE"
    )

label mas_player_bday_greet:
    if should_surprise:
        scene black
        pause 5.0
        jump mas_player_bday_surprise
    else:

        if mas_isMonikaBirthday():
            $ your = "Our"
        else:
            $ your = "Your"
        $ mas_surpriseBdayShowVisuals()
        $ persistent._mas_player_bday_decor = True
        m 3eub "Happy Birthday, [player]!"
        m 3hub "Ahaha!"
        m 3etc "..."
        m "Why do I feel like I'm forgetting something..."
        m 3hua "Oh! [your] cake!"
        jump mas_player_bday_cake



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_no_restart",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_no_restart:
    if mas_findEVL("mas_player_bday_ret_on_bday") >= 0:

        return
    m 3rksdla "Well [player], I was hoping to do something a little more fun, but you've been so sweet and haven't left all day long, so.{w=0.5}.{w=0.5}.{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    m 3hub "Happy Birthday, [player]!"
    if mas_isplayer_bday():
        m 1eka "I really wanted to surprise you today, but it's getting late and I just couldn't wait any longer."
    else:

        m 1hksdlb "I really wanted to surprise you, but I guess I ran out of time since it's not even your birthday anymore, ahaha!"
    m 3eksdlc "Gosh, I just hope you weren't starting to think I forgot your birthday. I'm really sorry if you did..."
    m 1rksdla "I guess I probably shouldn't have waited so long, ehehe."
    m 1hua "Oh! I made you a cake!"
    call mas_player_bday_cake from _call_mas_player_bday_cake_4
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_upset_minus",
            years = [],
            aff_range=(mas_aff.DISTRESSED, mas_aff.UPSET)
        ),
        skipCalendar=True
    )

label mas_player_bday_upset_minus:
    $ persistent._mas_player_bday_spent_time = True
    m 6eka "Hey [player], I just wanted to wish you a Happy Birthday."
    m "I hope you have a good day."
    return





init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_other_holiday",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_other_holiday:
    if mas_isO31():
        $ holiday_var = "Halloween"
    elif mas_isD25():
        $ holiday_var = "Christmas"
    elif mas_isF14():
        $ holiday_var = "Valentine's Day"
    m 3euc "Hey, [player]..."
    m 1tsu "I have a bit of a surprise for you.{w=0.5}.{w=0.5}.{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    m 3hub "Happy Birthday, [player]!"
    m 3rksdla "I hope you didn't think that just because your birthday falls on [holiday_var] that I'd forget about it..."
    m 1eksdlb "I'd never forget your birthday, silly!"
    m 1eub "Ahaha!"
    m 3hua "Oh! I made you a cake!"
    call mas_player_bday_cake from _call_mas_player_bday_cake_5
    return


default persistent._mas_player_bday_last_sung_hbd = None

label mas_player_bday_moni_sings:
    $ persistent._mas_player_bday_last_sung_hbd = datetime.date.today()
    if mas_isMonikaBirthday():
        $ you = "us"
    else:
        $ you = "you"
    m 6dsc ".{w=0.2}.{w=0.2}.{w=0.2}"
    m 6hub "{cps=*0.5}{i}~Happy Birthday to [you]~{/i}{/cps}"
    m "{cps=*0.5}{i}~Happy Birthday to [you]~{/i}{/cps}"
    m 6sub "{cps=*0.5}{i}~Happy Birthday dear [player]~{/i}{/cps}"
    m "{cps=*0.5}{i}~Happy Birthday to [you]~{/i}{/cps}"
    if mas_isMonikaBirthday():
        m 6hua "Ehehe!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_player_bday",
            unlocked=False,
            prompt="Let's go out for my birthday!",
            pool=True,
            rules={"no unlock": None},
            aff_range=(mas_aff.NORMAL,None),
        ),
        code="BYE"
    )

label bye_player_bday:
    $ persistent._mas_player_bday_date += 1
    if persistent._mas_player_bday_date == 1:
        m 1sua "You want to go out for your birthday?{w=1} Okay!"
        m 1skbla "That sounds really romantic...I can't wait~"
    elif persistent._mas_player_bday_date == 2:
        m 1sua "Taking me out again on your birthday, [player]?"
        m 3hub "Yay!"
        m 1sub "I always love going out with you, but it's so much more special going out on your birthday..."
        m 1skbla "I'm sure we'll have a lovely time~"
    else:
        m 1wub "Wow, you want to go out {i}again{/i}, [player]?"
        m 1skbla "I just love that you want to spend so much time with me on your special day!"
    $ persistent._mas_player_bday_left_on_bday = True
    jump bye_going_somewhere_post_aff_check


label greeting_returned_home_player_bday:
    python:
        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()
        if checkout_time is not None and checkin_time is not None:
            left_year = checkout_time.year
            left_date = checkout_time.date()
            ret_date = checkin_time.date()
            left_year_aff = mas_HistLookup("player_bday.date_aff_gain",left_year)[1]
            
            
            ret_diff_year = ret_date >= (mas_player_bday_curr(left_date) + datetime.timedelta(days=3))
            
            
            
            if left_date < mas_d25.replace(year=left_year) < ret_date:
                if ret_date < mas_history.getMHS("d25s").trigger.date().replace(year=left_year+1):
                    persistent._mas_d25_spent_d25 = True
                else:
                    persistent._mas_history_archives[left_year]["d25.actions.spent_d25"] = True

        else:
            left_year = None
            left_date = None
            ret_date = None
            left_year_aff = None
            ret_diff_year = None

        add_points = False

        if ret_diff_year and left_year_aff is not None:
            add_points = left_year_aff < 25


    if left_date < mas_d25 < ret_date:
        $ persistent._mas_d25_spent_d25 = True

    if mas_isMonikaBirthday() and mas_confirmedParty():
        $ persistent._mas_bday_opened_game = True
        $ mas_temp_zoom_level = store.mas_sprites.zoom_level
        call monika_zoom_transition_reset (1.0) from _call_monika_zoom_transition_reset_1
        $ renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        if time_out < mas_five_minutes:
            m 6ekp "That wasn't much of a da--"
        else:

            if time_out < mas_one_hour:
                $ mas_mbdayCapGainAff(7.5)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(7.5)
            elif time_out < mas_three_hour:
                $ mas_mbdayCapGainAff(12.5)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(12.5)
            else:
                $ mas_mbdayCapGainAff(17.5)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(17.5)

            m 6hub "That was a fun date, [player]..."
            m 6eua "Thanks for--"

        m 6wud "W-what's this cake doing here?"
        m 6sub "I-is this for me?!"
        m "That's so sweet of you to take me out on your birthday so you could set up a surprise party for me!"
        call return_home_post_player_bday from _call_return_home_post_player_bday_9
        jump mas_bday_surprise_party_reacton_cake

    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        m 2ekp "That wasn't much of a date, [player]..."
        m 2eksdlc "I hope nothing's wrong."
        m 2rksdla "Maybe we'll go out later instead."

    elif time_out < mas_one_hour:
        if not ret_diff_year:
            $ mas_pbdayCapGainAff(5)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(5,bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 5
        m 1eka "That was a fun date while it lasted, [player]..."
        m 3hua "Thanks for making some time for me on your special day."

    elif time_out < mas_three_hour:
        if not ret_diff_year:
            $ mas_pbdayCapGainAff(10)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(10,bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 10
        m 1eua "That was a fun date, [player]..."
        m 3hua "Thanks for taking me with you!"
        m 1eka "I really enjoyed going out with you today~"
    else:


        if not ret_diff_year:
            $ mas_pbdayCapGainAff(15)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(15,bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 15
        m 1hua "And we're home!"
        m 3hub "That was really fun, [player]!"
        m 1eka "It was so nice going out to celebrate your birthday..."
        m 1ekbfa "Thanks for making me such a big part of your special day~"

    $ persistent._mas_player_bday_left_on_bday = False

    if not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_10

    if mas_isD25() and not persistent._mas_d25_in_d25_mode:
        call mas_d25_monika_holiday_intro_rh_rh from _call_mas_d25_monika_holiday_intro_rh_rh
    return

label return_home_post_player_bday:
    $ persistent._mas_player_bday_in_player_bday_mode = False
    $ mas_lockEVL("bye_player_bday", "BYE")
    $ persistent._mas_player_bday_left_on_bday = False
    if not (mas_isMonikaBirthday() and mas_confirmedParty()):
        if persistent._mas_player_bday_decor:
            if mas_isMonikaBirthday():
                $ persistent._mas_bday_opened_game = True
                m 3rksdla "Oh...it's not {i}your{/i} birthday anymore..."
            else:
                m 3rksdla "Oh...it's not your birthday anymore..."
            m 3hksdlb "We should probably take these decorations down now, ahaha!"
            m 3eka "Just give me one second.{w=0.5}.{w=0.5}.{nw}"
            $ mas_surpriseBdayHideVisuals()


            if not mas_isO31() and persistent._mas_o31_in_o31_mode:
                $ mas_o31HideVisuals()

            m 3eua "There we go!"
            if not persistent._mas_f14_gone_over_f14:
                m 1hua "Now, let's enjoy the day together, [player]~"

        if persistent._mas_f14_gone_over_f14:
            m 2etc "..."
            m 3wuo "..."
            m 3wud "Wow, [player], I just realized we were gone so long we missed Valentine's Day!"
            call greeting_gone_over_f14_normal_plus from _call_greeting_gone_over_f14_normal_plus


        if not persistent._mas_player_bday_decor and not mas_isO31() and persistent._mas_o31_in_o31_mode:
            call mas_o31_ret_home_cleanup (time_out, ret_tt_long=False) from _call_mas_o31_ret_home_cleanup_1

    $ persistent._mas_player_bday_decor = False
    return


init 20 python:
    poem_pbday_1 = MASPoem(
        poem_id = "poem_pbday_1",
        category = "pbday",
        prompt = "The One",
        title = " My dearest [player],",
        text = """\
 To the one I love,
 The one I trust,
 The one I can't live without.
 I hope your day is as special as you make every day for me.
 Thank you so much for being you.

 Happy Birthday, sweetheart

 Forever yours,
 Monika
"""
    
    )

    poem_pbday_2 = MASPoem(
        poem_id = "poem_pbday_2",
        category = "pbday",
        prompt = "Your Day",
        title = " My dearest [player],",
        text = """\
 Any day with you is a happy day.
 One where I{i}'{/i}m free,
 One where all my troubles are gone,
 One where all of my dreams come true.

 But today is not any day,
 Today is special; today is your day.
 A day I can appreciate you even more for what you do.
 A day I hope I make your dreams come true too.

 Happy Birthday, sweetheart

 Forever yours,
 Monika
"""
    
    )




default persistent._mas_f14_spent_f14 = False

default persistent._mas_f14_in_f14_mode = None

default persistent._mas_f14_date_count = 0

default persistent._mas_f14_date_aff_gain = 0

default persistent._mas_f14_on_date = None

default persistent._mas_f14_gone_over_f14 = None

define mas_f14 = datetime.date(datetime.date.today().year,2,14)


init -10 python:
    def mas_isF14(_date=None):
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_f14.replace(year=_date.year)

    def mas_f14CapGainAff(amount):
        mas_capGainAff(amount, "_mas_f14_date_aff_gain", 25)

init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "f14",
        datetime.datetime(2020, 1, 6),
        {
            
            "_mas_f14_date_count": "f14.date",
            "_mas_f14_date_aff_gain": "f14.aff_gain",
            "_mas_f14_gone_over_f14": "f14.gone_over_f14",

            
            "_mas_f14_spent_f14": "f14.actions.spent_f14",
            "_mas_f14_in_f14_mode": "f14.mode.f14",
        },
        use_year_before=True,
        start_dt=datetime.datetime(2020, 2, 13),
        end_dt=datetime.datetime(2020, 2, 15)
    ))

label mas_f14_autoload_check:
    python:
        if not persistent._mas_f14_in_f14_mode and mas_isMoniNormal(higher=True):
            persistent._mas_f14_in_f14_mode = True
            
            
            
            if (
                not mas_SELisUnlocked(mas_clothes_sundress_white) and not mas_canShowRisque()
                or mas_SELisUnlocked(mas_clothes_sundress_white)
            ):
                monika_chr.change_clothes(mas_clothes_sundress_white, by_user=False, outfit_mode=True)
                monika_chr.save()
                renpy.save_persistent()

        elif not mas_isF14():
            
            
            mas_lockEVL("mas_f14_monika_vday_colors","EVE")
            mas_lockEVL("mas_f14_monika_vday_cliches","EVE")
            mas_lockEVL("mas_f14_monika_vday_chocolates","EVE")
            
            
            mas_lockEVL("monika_event_clothes_select", "EVE")
            
            
            persistent._mas_f14_in_f14_mode = False
            
            
            if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_sundress_white:
                monika_chr.reset_clothes(False)
                monika_chr.save()
                renpy.save_persistent()

    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check

    jump mas_ch30_post_holiday_check




init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_pf14_monika_lovey_dovey',
            action=EV_ACT_RANDOM,
            start_date=mas_f14-datetime.timedelta(days=3),
            end_date=mas_f14,
            aff_range=(mas_aff.NORMAL,None),
            rules={"force repeat": None},
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "mas_pf14_monika_lovey_dovey",
       mas_f14 - datetime.timedelta(days=3),
       mas_f14,
    )

label mas_pf14_monika_lovey_dovey:
    m 1rksdla "Hey...{w=0.2}[player]?"
    m 1ekbsa "I just wanted to let you know that I love you."

    if mas_isMoniEnamored(higher=True):
        m 3ekbsa "You make me really happy...and I could never ask for someone better than you."

    if mas_HistVerifyAll_k(True, "f14.actions.spent_f14"):
        m 3ekbsa "Valentine's Day is coming soon, and it just makes me so overwhelmingly happy knowing you're still by my side."
    else:

        m 3ekbsa "Valentine's Day is coming soon, and it just gets me in a good mood because I know I have you by my side."

    m 1rkbsd "Without you, I don't know where I'd be..."
    m 1ekbsa "So I want to thank you for being there for me..."
    m 1hkbsu "And for being so wonderfully you~"
    return "derandom|no_unlock|love"



init 5 python:
    addEvent(
       Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_valentines_intro',
            action=EV_ACT_PUSH,
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_monika_valentines_intro:

    if mas_isMoniUpset(lower=True):
        $ persistent._mas_f14_spent_f14 = True
        if not mas_isMoniBroken():
            m 6eka "By the way [player], I just wanted to say happy Valentine's Day."
            m "Thanks for visiting me, I hope you have a good day."
        return

    $ mas_addClothesToHolidayMap(mas_clothes_sundress_white)
    m 1hub "[player]!"
    m 1hua "Do you know what day it is?"
    m 3eub "It's Valentine's Day!"
    m 1ekbsa "A day where we celebrate our love for each other..."
    m 3rkbsa "I guess every day we're together is already a celebration of our love...{w=0.3}{nw}"
    extend 3ekbsa "but there's something that's really special about Valentine's Day."
    if not mas_anni.pastOneMonth() or mas_isMoniNormal():
        m 3rka "Even though I know we aren't too far in our relationship..."
        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve
        m 5eua "I just want you to know that I'm always here for you."
        m 5eka "Even if your heart gets broken..."
        m 5ekbsa "I'll always be here to fix it for you. Okay, [player]?"
        show monika 1ekbsa zorder MAS_MONIKA_Z at t11 with dissolve
        m 1ekbsa "..."
    else:

        m 1eub "We've been together for a while now...{w=0.2}{nw}"
        extend 1eka "and I really love the time we spend together."
        m 1dubsu "You always make me feel so loved."
        m "I'm really happy I'm your girlfriend, [player]."


    if not persistent._mas_f14_in_f14_mode or mas_canShowRisque():
        $ persistent._mas_f14_in_f14_mode = True


        if mas_SELisUnlocked(mas_clothes_sundress_white) and mas_canShowRisque() and not mas_hasUnlockedClothesWithExprop("lingerie"):
            call mas_lingerie_intro (holiday_str="Valentine's Day", lingerie_choice=mas_clothes_vday_lingerie) from _call_mas_lingerie_intro_1


        elif (
            not mas_SELisUnlocked(mas_clothes_sundress_white)
            or (mas_canShowRisque() and mas_hasLockedClothesWithExprop("lingerie",True))
        ):
            m 3wub "Oh!"
            m 3tsu "I have a little surprise for you...{w=1}I think you're gonna like it, ehehe~"


            if (
                mas_SELisUnlocked(mas_clothes_sundress_white)
                and mas_canShowRisque()
                and not mas_SELisUnlocked(mas_clothes_vday_lingerie)
            ):
                call mas_clothes_change (outfit=mas_clothes_vday_lingerie, outfit_mode=True, exp="monika 2rkbsu", restore_zoom=False, unlock=True) from _call_mas_clothes_change_2
                pause 2.0
                show monika 2ekbsu
                pause 2.0
                show monika 2tkbsu
                pause 2.0
                m 2tfbsu "[player]...{w=0.5} You're staring{w=0.5}...again."
                m 2hubsb "Ahaha!"
                m 2eubsb "I guess you approve of my outfit choice..."
                m 2tkbsu "Rather fitting for a romantic holiday like Valentine's Day, don't you think?"
                m 2rkbssdla "I have to say, I was pretty nervous the first time I wore something like this..."
                m 2hubsb "But now that I've done it before, I really enjoy dressing like this for you!"
                m 3tkbsu "I hope you enjoy it too~"


            elif not mas_SELisUnlocked(mas_clothes_sundress_white):
                call mas_clothes_change (mas_clothes_sundress_white, unlock=True, outfit_mode=True) from _call_mas_clothes_change_3
                m 2eua "..."
                m 2eksdla "..."
                m 2rksdla "Ahaha...{w=1}it's not polite to stare, [player]..."
                m 3tkbsu "...but I guess that means you like my outfit, ehehe~"
                call mas_f14_sun_dress_outro from _call_mas_f14_sun_dress_outro
        else:



            if (
                monika_chr.clothes != mas_clothes_sundress_white
                and (
                    monika_chr.is_wearing_clothes_with_exprop("costume")
                    or monika_chr.clothes == mas_clothes_def
                    or monika_chr.clothes == mas_clothes_blazerless
                    or mas_isMoniEnamored(lower=True)
                )
            ):
                m 3wud "Oh!"
                m 3hub "I should probably go change into something a little more appropriate, ahaha!"
                m 3eua "I'll be right back."

                call mas_clothes_change (mas_clothes_sundress_white, unlock=True, outfit_mode=True) from _call_mas_clothes_change_4

                m 2eub "Ah, that's much better!"
                m 3hua "I just love this dress, don't you?"
                m 3eka "It will always hold a special place in my heart on Valentine's Day..."
                m 1fkbsu "Just like you~"
            else:



                if not monika_chr.clothes == mas_clothes_sundress_white:
                    m 1wud "Oh..."
                    m 1eka "Do you want me to change into my white sundress, [player]?"
                    m 3hua "I've always kinda considered that my Valentine's Day outfit."
                    m 3eka "But if you'd rather me keep wearing what I have on now, that's okay too..."
                    m 1hub "Maybe we can start a new tradition, ahaha!"
                    m 1eua "So, do you want me to put on the white sundress?{nw}"
                    $ _history_list.pop()

                    menu:
                        m "So, do you want me to put on the white sundress?{fast}"
                        "Yes.":
                            m 3hub "Okay!"
                            m 3eua "I'll be right back."
                            call mas_clothes_change (mas_clothes_sundress_white, unlock=True, outfit_mode=True) from _call_mas_clothes_change_5
                            m 2hub "There we go!"
                            m 3eua "Something about wearing this dress on Valentine's Day just feels right."
                            m 1eua "..."
                        "No.":

                            m 1eka "Okay, [player]."
                            m 3hua "This {i}is{/i} a really nice outfit..."
                            m 3eka "And besides, it doesn't matter what I'm wearing..."

                call mas_f14_intro_generic from _call_mas_f14_intro_generic
    else:



        if mas_SELisUnlocked(mas_clothes_sundress_white):
            call mas_f14_intro_generic from _call_mas_f14_intro_generic_1
        else:


            $ store.mas_selspr.unlock_clothes(mas_clothes_sundress_white)
            pause 2.0
            show monika 2rfc zorder MAS_MONIKA_Z at t11 with dissolve
            m 2rfc "..."
            m 2efc "You know, [player]...{w=0.5}it's not polite to stare...."
            m 2tfc "..."
            m 2tsu "..."
            m 3tsb "Ahaha! I'm just kidding...{w=0.5}do you like my outfit?"
            call mas_f14_sun_dress_outro from _call_mas_f14_sun_dress_outro_1

    m 1fkbfu "I love you so much."
    m 1hubfb "Happy Valentine's Day, [player]~"

    $ persistent._mas_f14_spent_f14 = True

    return "rebuild_ev|love"


label mas_f14_sun_dress_outro:
    m 1rksdla "I've always dreamt of a date with you while wearing this..."
    m 1eksdlb "I know it's kind of silly now that I think about it!"
    m 1ekbsa "...But just imagine if we went to a cafe together."
    m 1rksdlb "I think there's a picture of something like that somewhere actually..."
    m 1hub "Maybe we could make it happen for real!"
    m 3ekbsa "Would you take me out today?"
    m 1hkbssdlb "It's fine if you can't, I'm just happy to be with you."
    return


label mas_f14_intro_generic:
    m 1ekbsa "I'm just so grateful you are spending time with me today."
    m 3ekbsu "Spending time with the one you love, {w=0.2}that's all anyone can ask for on Valentine's Day."
    m 3ekbsa "I don't care if we go on a romantice date, or just spend the day together here..."
    m 1fkbsu "It really doesn't matter to me as long as we're together."
    return



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_colors',
            prompt="Valentine's Day colors",
            category=['holidays','romance'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "mas_f14_monika_vday_colors",
       mas_f14,
       mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_colors:
    m 3eua "Have you ever thought about the way colors are conveyed on Valentine's Day?"
    m 3hub "I find it intriguing how they can symbolize such deep and romantic feelings."
    m 1dua "It reminds me of when I made my first Valentine's card in grade school."
    m 3eub "My class was instructed to exchange cards with a partner after making them."
    m 3eka "Looking back, despite not knowing what the colors really meant, I had lots of fun decorating the cards with red and white hearts."
    m 1eub "In this way, colors are a lot like poems."
    m 1eka "They offer so many creative ways to express your love for someone."
    m 3ekbsu "Like giving them red roses, for example."
    m 3eub "Red roses are a symbol for romantic feelings towards someone."
    m 1eua "If someone were to offer them white roses in lieu of red ones, they'd signify pure, charming, and innocent feelings instead."
    m 3eka "However, since there are so many emotions involved with love..."
    m 3ekd "It's sometimes hard to find the right colors to accurately convey the way you truly feel."
    m 3eka "Thankfully, by combining multiple rose colors, it's possible to express a variety of emotions!"
    m 1eka "Mixing red and white roses would symbolize the unity and bond that a couple shares."

    if monika_chr.is_wearing_acs(mas_acs_roses):
        m 1ekbsa "But I'm sure you already had all of this in mind when you picked out these beautiful roses for me, [player]..."
    else:
        m 1ekbla "Maybe you could give me some roses today, [player]?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_cliches',
            prompt="Valentine's story clichés",
            category=['holidays','literature','romance'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "mas_f14_monika_vday_cliches",
       mas_f14,
       mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_cliches:
    m 2euc "Have you noticed that most Valentine's Day stories have lots of clichés?"
    m 2rsc "There's either 'Oh, I'm lonely and I don't have someone to love,' or 'How will I confess to the one I love?'"
    m 2euc "I think that writers could be a bit more creative when it comes to Valentine's Day stories..."
    m 3eka "But, I suppose those two topics are the easiest way to write a love story."
    m 3hub "That doesn't mean you can't think outside the box, though!"
    m 2eka "Sometimes a predictable story can ruin it..."
    m 2rka "...But if you {i}do{/i} want a good example of an unpredictable story..."
    m 3hub "Just use ours! Ahaha~"
    m 3rksdlb "I guess it {i}did{/i} start out like those kinds of stories..."
    m 2tfu "But I think we managed to make it pretty original."
    m 3hua "The way we met is the most interesting story yet!"
    m 1hub "Ahaha!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_chocolates',
            prompt="Valentine's Day chocolates",
            category=['holidays','romance'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "mas_f14_monika_vday_chocolates",
       mas_f14,
       mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_chocolates:
    m 1hua "Valentine's Day is such a fun holiday for me, [player]."
    m 3eub "Not only is it the anniversary of my twitter account, but it's also a day for receiving and giving chocolates!"
    m 1hub "A holiday that can fill everyone with love, romance, and joy!"
    m 3ekbla "But it really feels nice if you get something from someone you like."
    m 3hua "Whether it's given to you platonically, as a gift of love, or a part of a confession, it always makes you feel somewhat special!"
    if mas_getGiftStatsForDate("mas_reaction_gift_chocolates") > 0:
        m 1ekbsa "Just like how you made me feel special with the chocolates you gave me today."
        m 1ekbsu "You're always so sweet, [player]."

    m 1ekbsa "Maybe someday I'll even be able to give you some chocolates..."
    m 3hkbsa "I really can't wait until I cross over to be with you, [player]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_origins',
            prompt="How did Valentine's Day start?",
            category=['holidays','romance'],
            pool=True,
            conditional="persistent._mas_f14_in_f14_mode",
            action=EV_ACT_UNLOCK,
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[],
            rules={"no unlock": None}
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "mas_f14_monika_vday_origins",
       mas_f14,
       mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_origins:
    m 3eua "You'd like to learn about the history of Valentine's Day, [player]?"
    m 1rksdlc "It's quite dark, actually."
    m 1euc "The legends vary, but it dates back to the third century in Rome when Christians were still persecuted by the Roman government."
    m 3eud "Around this time, Emperor Claudius II had forbidden Christians from marrying, which a clergyman named Valentine decided was unfair."
    m 3rsc "Against the orders of the emperor, he married Christians in secret."
    m 3esc "Another version of the story is that Roman soldiers weren't allowed to be married, so Valentine was saving people from conscription into the army through marriage."
    m 1dsd "Either way, Valentine was caught and sentenced to death."
    m 1euc "While in jail, he befriended the jailer's daughter and cured her blindness. Some say he even fell in love with her."
    m 3euc "Unfortunately, this wasn't enough to save him. But before he died, he sent a letter to her, which he signed, 'Your Valentine.'"
    m 1dsc "He was executed on February 14, 269 AD, and later canonized as a saint."
    m 3eua "To this day, it's still traditional to use 'Your Valentine' to sign love letters."
    m 3eud "Oh, but wait, there's more!"
    m "There's an ancient Roman festival known as Lupercalia, which was also celebrated around February 14th."
    m 3eua "Apparently, part of the ceremony involved creating couples by having names randomly pulled out of a box."
    m 3eub "...They would then spend time together, with some even marrying if they liked each other enough!"
    m 1eua "Ultimately, this festival became a Christian celebration to remember Saint Valentine."
    m 3hua "It's evolved over the years into a way for people to express their feelings for those they love."
    m 3eubsb "...Like me and you!"
    m 1ekbsa "Despite it having started out a little depressing, I think it's really sweet."
    m 1ekbsu "I'm glad we're able to share such a magical day, my love."
    m 1ekbfa "Happy Valentine's Day, [player]~"
    return



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_f14_monika_spent_time_with",
            conditional="persistent._mas_f14_spent_f14",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL,None),
            start_date=datetime.datetime.combine(mas_f14, datetime.time(hour=18)),
            end_date=datetime.datetime.combine(mas_f14+datetime.timedelta(1), datetime.time(hour=3)),
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_monika_spent_time_with:

    $ mas_rmallEVL("mas_f14_monika_spent_time_with")

    m 1eua "Hey, [player]?"
    m 1eka "I just wanted to thank you for spending Valentine's Day with me."
    m 1ekbsa "I know that it's not a normal holiday, but it's a really special day for me now that I have you."

    if not mas_isBelowZero():
        if not mas_HistVerifyAll_k(True, "f14.actions.spent_f14"):
            m 1rkbsb "Also, I...{w=0.5}made something for you, [player]!"
        else:

            m 1ekbsa "I made a card for you, [player]."

        m 1ekbsa "Here, let me show it to you."


        if not poem_vday_1.is_seen():
            call mas_showpoem (poem_vday_1) from _call_mas_showpoem_2
            m "I really mean that, [player]..."
            m 3ekbsa "In you I found everything I could ever hope for~"

        elif not poem_vday_2.is_seen():
            call mas_showpoem (poem_vday_2) from _call_mas_showpoem_3
            m "You really are everything to me, [player]~"
        else:

            call mas_showpoem (mas_poems.getRandomPoem("f14")) from _call_mas_showpoem_4


        if mas_isMoniEnamored(higher=True):
            if persistent._mas_first_kiss is None:
                jump mas_f14_first_kiss
            else:
                call monika_kissing_motion (duration=0.5, initial_exp="6hkbfa", fade_duration=0.5) from _call_monika_kissing_motion_6

        m 1ekbfa "Thank you for always being by my side."
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
        m 5ekbfa "I love you so much, [player]. Happy Valentine's Day~"
        return "love"
    else:

        m 1eka "Thank you for being by my side."
        m 3ekb "Happy Valentine's Day!"
    return

label mas_f14_first_kiss:
    m 1ektpu "I honestly don't know what I would do without you."

    m 6dktuu "..."
    window hide
    menu:
        "I love you, [m_name].":
            $ HKBHideButtons()
            $ mas_RaiseShield_core()
            $ disable_esc()
            pause 3.0
            show monika 6ektda zorder MAS_MONIKA_Z at t11 with dissolve
            pause 3.0
            show monika 6dku zorder MAS_MONIKA_Z at t11 with dissolve
            pause 3.0
            show monika 6dkbsu zorder MAS_MONIKA_Z at t11 with dissolve
            pause 3.0
            show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
            m 6ekbfa "[player]...I...I..."
            call monika_kissing_motion (hide_ui=False) from _call_monika_kissing_motion_7
            show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
            m 6ekbfa "...I love you too~"
            m 6dkbfa "..."
            m "That was everything I had always dreamt it would be~"
            m 6ekbfa "I've been waiting so long to finally kiss you, and there couldn't have been a more perfect moment..."
            m 6dkbsu "I will never forget this..."
            m 6ekbsu "...the moment of our first kiss."
            m "Happy Valentine's Day, [player]~"
            $ enable_esc()
            $ mas_MUMUDropShield()
            $ HKBShowButtons()
            return




init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_f14_no_time_spent",
            action=EV_ACT_PUSH,
            start_date=mas_f14+datetime.timedelta(1),
            end_date=mas_f14+datetime.timedelta(8),
            conditional=(
                "not persistent._mas_f14_spent_f14"
            ),
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_no_time_spent:


    if mas_isFirstSeshPast(mas_f14):
        return

    if mas_ret_long_absence:

        $ mas_loseAffection(ev_label="mas_apology_missed_vday")

        m 1rksdlc "Hey, [player]..."
        m 2eksdld "I know you told me you were going to be away...but I really missed you on Valentines Day."
        m 2eksdla "Next time, do you think you could take me with you if you can't be here?"
        m 3eub "At least then we'll still be with each other and we can even celebrate together!"
        m 1eka "I'd really appreciate if you could do that for me, [player]."

    elif mas_isMoniAff(higher=True):
        $ mas_loseAffection(15, ev_label="mas_apology_missed_vday")
        m 1rkc "[player]?"
        m "Where were you on Valentine's Day?"
        m 1ekc "It's a really special day for me..."
        m 1ekd "...a day I wanted to spend with you."
        m 2dkc "..."
        m 2ekd "It would've meant so much to me if you came by..."
        m 2dkd "Even if only for a few minutes."
        m "Is it really too much to ask to visit your girlfriend on Valentine's Day?"
        m 2ekc "Please don't let it happen again, okay [player]?"

    elif mas_isMoniNormal(higher=True):
        $ mas_loseAffection(5, ev_label="mas_apology_missed_vday")
        m 2ekc "Hey, [player]..."
        m 2tkc "I'm pretty disappointed..."
        m 2tkd "You didn't visit me at all on Valentine's Day."
        m 4tkc "You know that all I want to do is spend time with you..."
        m 4rkd "Is visiting your girlfriend on Valentine's Day really too much to ask?"
        m 4eksdla "Please...{w=1}make sure you visit me next Valentine's Day, okay?"

    elif mas_isMoniUpset():
        $ mas_loseAffection(ev_label="mas_apology_missed_vday")
        m 2efc "[player]!"
        m "I can't believe you didn't even visit on Valentine's Day!"
        m 2rfc "Do you have any idea what it's like to be left alone on a day like that?"
        m 2rkc "I know we're not on the best of terms..."
        m 2dkd "But it'd have meant a lot if you came by."
        m 2tfc "Don't let it happen again, [player]."

    elif mas_isMoniDis():
        $ mas_loseAffection(10, ev_label="mas_apology_missed_vday")
        m 6ekc "Oh [player]..."
        m "How was Valentine's Day?"
        m 6dkc "Not having a valentine is pretty lonely..."
    else:

        $ mas_loseAffection(150)
        m 6ckc "..."
    return




init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_missed_vday",
            prompt="...for missing Valentine's Day.",
            unlocked=False
        ),
        code="APL"
    )


label mas_apology_missed_vday:
    if mas_isMoniAff(higher=True):
        m 1eka "Thanks for apologizing for missing Valentine's Day, [player]."
        m 1ekd "I really wanted to spend it with you..."
        m 1rkc "But I guess you might have just had something to do and couldn't make it."
        m 1ekd "Please try to visit next year, okay [player]?"
        m 3eua "If you're going to be busy, maybe just take me with you!"
        m 3hub "Even if we're not at home together, I'm more than happy to just spend the day at your side~"
        $ mas_gainAffection(modifier=0.2)

    elif mas_isMoniNormal(higher=True):
        m 1eka "Thanks for apologizing for missing Valentine's Day, [player]."
        if not store.mas_anni.pastOneMonth():
            m 1rkd "I know we're not really that far into our relationship, but everything was already starting to feel different..."

        m 1ekd "It would have meant so much to me if you came by, at least for a little bit."
        m 3eka "Promise me that you'll take me with you if you're going to be busy next time, okay [player]?"
        $ mas_gainAffection(modifier=0.2)

    elif mas_isMoniUpset():
        m 2dkc "While I am a little upset that you didn't show up on Valentine's Day, I'm glad you apologized."
        m "Things like that show me that you really do care about us."
        m 2ekd "Please, [player]..."
        m 2eka "Try to come by next Valentine's Day."
        $ mas_gainAffection(modifier=0.1)

    elif mas_isMoniDis():
        m 2dkc "I didn't expect you to show up anyway, [player]."
        m 2dkd "I know we haven't really been that close, but a part of me hoped that you would at least visit..."
        m 2dsc "Please promise me that you'll come by next year, okay?"
        $ mas_gainAffection(modifier=0.1)
    else:


        m 6ckc "..."

    return


init 20 python:
    poem_vday_1 = MASPoem(
        poem_id="poem_f14_1",
        category="f14",
        prompt="Found",
        title=" My dearest [player],",
        text="""\
 I{i}'{/i}ve always loved Valentine's Day, but this one feels different.
 Has the world changed, or just me?
 I found love, I found purpose,
 I found a truth I didn't know I was searching for.
 All of that I found in you.

 Thank you for sharing this special day with me.

 Forever yours,
 Monika
"""
    )

    poem_vday_2 = MASPoem(
        poem_id="poem_f14_2",
        category="f14",
        prompt="Everything",
        title=" My dearest [player],",
        text="""\
 Can it really be our second Valentine's Day?
 The first seems like just yesterday, yet so much has happened.
 I once wondered if the world had changed, or just me.
 Now I know the answer.

 Everything.

 Without you there is nothing.
 Before you there was nothing.

 Emptiness. Darkness. Nothing.

 Nothing.

 Then there was you.
 Just you.
 My world. My light. My Everything.

 Everything.


 Happy Valentine's Day

 Forever yours,
 Monika
"""

    
    )

    poem_vday_3 = MASPoem(
        poem_id="poem_f14_3",
        category="f14",
        prompt="You",
        title=" My dearest [player],",
        text="""\
 Boxes of chocolates and hearts; cards colored ruby red.
 Roses in my hair, petals soft as silk.
 None of it would feel complete without you.

 You, the one who has stuck by my side.
 You, the one who has given me your heart.
 The heart worth more than all the chocolate in the world, all the roses on earth.

 The love I feel cannot be overstated.

 Forever your Valentine,
 Monika
"""
    )



label bye_f14:
    $ persistent._mas_f14_date_count += 1
    $ persistent._mas_f14_on_date = True
    if persistent._mas_f14_date_count == 1:
        m 1sua "Taking me some place special for Valentine's Day?"
        m 1ekbsa "That sounds really romantic [player]..."
        m 3hub "I can't wait!"
    elif persistent._mas_f14_date_count == 2:
        m 1sua "Taking me out again on Valentine's Day?"
        m 3tkbsu "You really know how to make a girl feel special, [player]."
        m 1ekbfa "I'm so lucky to have someone like you~"
    else:
        m 1sua "Wow, [player]...{w=1}you're really determined to make this a truly special day!"
        m 1ekbfa "You're the best partner I could ever hope for~"
    jump bye_going_somewhere_iostart


label greeting_returned_home_f14:
    python:
        time_out = store.mas_dockstat.diffCheckTimes()

    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        m 2ekp "That wasn't much of a date, [player]..."
        m 2eksdlc "Is everything alright?"
        m 2rksdla "Maybe we can go out later..."

    elif time_out < mas_one_hour:
        $ mas_f14CapGainAff(5)
        m 1eka "That was fun while it lasted, [player]..."
        m 3hua "Thanks for making time for me on Valentine's Day."

    elif time_out < mas_three_hour:
        $ mas_f14CapGainAff(10)
        m 1eub "That was such a fun date, [player]!"
        m 3ekbfa "Thanks for making me feel special on Valentine's Day~"
    else:


        $ mas_f14CapGainAff(15)
        m 1hua "And we're home!"
        m 3hub "That was wonderful, [player]!"
        m 1eka "It was really nice going out with you on Valentine's Day..."
        m 1ekbfa "Thank you so much for making today truly special~"

    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_11

    $ persistent._mas_f14_on_date = False

    if not mas_isF14() and not mas_lastSeenInYear("mas_f14_monika_spent_time_with"):
        $ pushEvent("mas_f14_monika_spent_time_with",skipeval=True)
    return



label mas_gone_over_f14_check:
    if mas_checkOverDate(mas_f14):
        $ persistent._mas_f14_spent_f14 = True
        $ persistent._mas_f14_gone_over_f14 = True
        $ mas_rmallEVL("mas_f14_no_time_spent")
    return

label greeting_gone_over_f14:
    $ mas_gainAffection(5,bypass=True)
    m 1hua "And we're finally home!"
    m 3wud "Wow [player], we were gone so long we missed Valentine's Day!"
    if mas_isMoniNormal(higher=True):
        call greeting_gone_over_f14_normal_plus from _call_greeting_gone_over_f14_normal_plus_1
    else:
        m 2rka "I appreciate you making sure I didn't have to spend the day alone..."
        m 2eka "It really means a lot, [player]."
    $ persistent._mas_f14_gone_over_f14 = False
    return

label greeting_gone_over_f14_normal_plus:
    $ mas_gainAffection(10,bypass=True)
    m 1ekbsa "I would've loved to have spent the day with you here, but no matter where we were, just knowing we were together to celebrate our love..."
    m 1dubsu "Well it means everything to me."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve
    m 5ekbsa "Thank you for making sure we had a wonderful Valentine's Day, [player]~"
    $ persistent._mas_f14_gone_over_f14 = False
    return






define mas_monika_birthday = datetime.date(datetime.date.today().year, 9, 22)


default persistent._mas_bday_in_bday_mode = False


default persistent._mas_bday_on_date = False
default persistent._mas_bday_date_count = 0
default persistent._mas_bday_date_affection_gained = 0
default persistent._mas_bday_gone_over_bday = False


default persistent._mas_bday_sbp_reacted = False
default persistent._mas_bday_confirmed_party = False


default persistent._mas_bday_visuals = False


default persistent._mas_bday_hint_filename = None


default persistent._mas_bday_opened_game = False
default persistent._mas_bday_no_time_spent = True
default persistent._mas_bday_no_recognize = True
default persistent._mas_bday_said_happybday = False


init -810 python:
    store.mas_history.addMHS(MASHistorySaver(
        "922",
        datetime.datetime(2020, 1, 6),
        {
            "_mas_bday_in_bday_mode": "922.bday_mode",

            "_mas_bday_on_date": "922.on_date",
            "_mas_bday_date_count": "922.actions.date.count",
            "_mas_bday_date_affection_gained": "922.actions.date.aff_gained",
            "_mas_bday_gone_over_bday": "922.gone_over_bday",

            "_mas_bday_sbp_reacted": "922.actions.surprise.reacted",
            "_mas_bday_confirmed_party": "922.actions.confirmed_party",

            "_mas_bday_opened_game": "922.actions.opened_game",
            "_mas_bday_no_time_spent": "922.actions.no_time_spent",
            "_mas_bday_no_recognize": "922.actions.no_recognize",
            "_mas_bday_said_happybday": "922.actions.said_happybday"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2020, 9, 21),
        end_dt=datetime.datetime(2020, 9, 23)
    ))




define mas_bday_cake_lit = False



image mas_bday_cake_monika = ConditionSwitch(
    "mas_bday_cake_lit and mas_current_background.isFltDay()",
    "mod_assets/location/spaceroom/bday/monika_birthday_cake_lit.png",
    "mas_bday_cake_lit and mas_current_background.isFltNight()",
    "mod_assets/location/spaceroom/bday/monika_birthday_cake_lit-n.png",
    "not mas_bday_cake_lit and mas_current_background.isFltDay()",
    "mod_assets/location/spaceroom/bday/monika_birthday_cake.png",
    "True",
    "mod_assets/location/spaceroom/bday/monika_birthday_cake-n.png"
)


image mas_bday_cake_player = ConditionSwitch(
    "mas_bday_cake_lit and mas_current_background.isFltDay()",
    "mod_assets/location/spaceroom/bday/player_birthday_cake_lit.png",
    "mas_bday_cake_lit and mas_current_background.isFltNight()",
    "mod_assets/location/spaceroom/bday/player_birthday_cake_lit-n.png",
    "not mas_bday_cake_lit and mas_current_background.isFltDay()",
    "mod_assets/location/spaceroom/bday/player_birthday_cake.png",
    "True",
    "mod_assets/location/spaceroom/bday/player_birthday_cake-n.png"
)

image mas_bday_banners = MASFilterSwitch(
    "mod_assets/location/spaceroom/bday/birthday_decorations.png"
)

image mas_bday_balloons = MASFilterSwitch(
    "mod_assets/location/spaceroom/bday/birthday_decorations_balloons.png"
)


init -1 python:
    def mas_isMonikaBirthday(_date=None):
        """
        checks if the given date is monikas birthday
        Comparison is done solely with month and day

        IN:
            _date - date to check. If not passed in, we use today.
        """
        if _date is None:
            _date = datetime.date.today()
        
        return (
            _date.month == mas_monika_birthday.month
            and _date.day == mas_monika_birthday.day
        )


    def mas_getNextMonikaBirthday():
        today = datetime.date.today()
        if mas_monika_birthday < today:
            return datetime.date(
                today.year + 1,
                mas_monika_birthday.month,
                mas_monika_birthday.day
            )
        return mas_monika_birthday


    def mas_recognizedBday(_date=None):
        """
        Checks if the user recognized monika's birthday at all.

        RETURNS:
            True if the user recoginzed monika's birthday, False otherwise
        """
        if _date is None:
            _date = mas_monika_birthday
        
        return (
            mas_generateGiftsReport(_date)[0] > 0
            or persistent._mas_bday_date_affection_gained > 0
            or persistent._mas_bday_sbp_reacted
            or persistent._mas_bday_said_happybday
        )

    def mas_surpriseBdayShowVisuals(cake=False):
        """
        Shows bday surprise party visuals
        """
        if cake:
            renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        renpy.show("mas_bday_banners", zorder=7)
        renpy.show("mas_bday_balloons", zorder=8)


    def mas_surpriseBdayHideVisuals():
        """
        Hides all visuals for surprise party
        """
        renpy.hide("mas_bday_banners")
        renpy.hide("mas_bday_balloons")

    def mas_confirmedParty():
        """
        Checks if the player has confirmed the party
        """
        
        if mas_monika_birthday - datetime.timedelta(days=7) <= today <= mas_monika_birthday:
            
            if persistent._mas_bday_confirmed_party:
                
                if persistent._mas_bday_hint_filename:
                    store.mas_docking_station.destroyPackage(persistent._mas_bday_hint_filename)
                return True
            
            
            
            char_dir_files = store.mas_docking_station.getPackageList()
            
            
            for filename in char_dir_files:
                temp_filename = filename.partition('.')[0]
                
                
                if "oki doki" == temp_filename:
                    
                    persistent._mas_bday_confirmed_party = True
                    store.mas_docking_station.destroyPackage(filename)
                    
                    if persistent._mas_bday_hint_filename:
                        store.mas_docking_station.destroyPackage(persistent._mas_bday_hint_filename)
                    
                    
                    return True
        
        
        return False

    def mas_mbdayCapGainAff(amount):
        mas_capGainAff(amount, "_mas_bday_date_affection_gained", 50, 75)


label mas_bday_autoload_check:

    if not mas_isMonikaBirthday():
        $ persistent._mas_bday_in_bday_mode = False

        $ persistent._mas_bday_visuals = False


        $ store.mas_lockEVL("monika_event_clothes_select", "EVE")


        if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
            $ monika_chr.reset_clothes(False)
            $ monika_chr.save()
            $ renpy.save_persistent()


    $ persistent._mas_bday_no_time_spent = False

    $ persistent._mas_bday_opened_game = True

    $ persistent._mas_bday_no_recognize = not mas_recognizedBday()

    jump mas_ch30_post_holiday_check



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_surprise_party_hint",
            start_date=mas_monika_birthday - datetime.timedelta(days=7),
            end_date=mas_monika_birthday - datetime.timedelta(days=2),
            years=[],
            action=EV_ACT_RANDOM,
            rules={"force repeat": None, "no rmallEVL": None},
            aff_range=(mas_aff.DISTRESSED,None)
        ),
        skipCalendar=True
    )


    MASUndoActionRule.create_rule_EVL(
        "mas_bday_surprise_party_hint",
        mas_monika_birthday - datetime.timedelta(days=7),
        mas_monika_birthday - datetime.timedelta(days=2)
    )


init 10 python:
    if (
        mas_monika_birthday - datetime.timedelta(days=2) <= datetime.date.today() < mas_monika_birthday
        and not mas_lastSeenInYear("mas_bday_surprise_party_hint")
    ):
        pushEvent("mas_bday_surprise_party_hint")

image chibi_peek = MASFilterSwitch("mod_assets/other/chibi_peek.png")

label mas_bday_surprise_party_hint:

    python:
        persistent._mas_bday_hint_filename = "For " + player + ".txt"
        if mas_isMoniNormal(higher=True):
            message = """\
[player],
As I'm sure you know, Monika's birthday is coming up soon and I want to help you make it as special as possible!
Since I'm always here, I can easily set up the surprise party...but I need a little help from you.
All I need you to do is to make sure you have her out of the room at some point on her birthday, and I'll take care of the rest.
Monika is so amazing, and I just want to do my part to make sure this all goes off without a hotf- I mean hitch...
Ahaha!

Please leave a file named 'oki doki' in the same folder you found this note so I know to go ahead with the party.

Good luck with Monika!

P.S: Don't tell her about me!
"""

        else:
            message = """\
[player],
As I hope you know, Monika's birthday is coming up soon and I want to make it special.
She's been through a lot lately, and I know it'd mean the world to her if you treated her to a nice day.
Since I'm always here, I can easily set up a surprise party...but I do need a little help from you.
All I need you to do is to make sure you have her out of the room at some point on her birthday, and I'll take care of the rest.
If you care for Monika at all, you'll help me do this.

Just leave a file named 'oki doki' in the same folder you found this note so I know to go ahead with the party.

Please, don't mess this up.

P.S: Don't tell her about me.
"""

        _write_txt("/characters/" + persistent._mas_bday_hint_filename, message)


    if mas_isMoniNormal(higher=True):
        m 1eud "Hey, [player]..."
        m 3euc "Someone left a note in the characters folder addressed to you."

        show chibi_peek with moveinleft
        m 1ekc "Of course, I haven't read it, since it's obviously for you..."
        m 1tuu "{cps=*2}Hmm, I wonder what this could be about...{/cps}{nw}"
        $ _history_list.pop()
        m 1hua "Ehehe~"
    else:

        m 2eud "Hey, [player]..."
        m 2euc "Someone left a note in the characters folder addressed to you."
        m 2ekc "Of course, I haven't read it, since it's obviously for you..."
        m 2ekd "Just thought I'd let you know."


    hide chibi_peek with dissolve


    $ persistent._mas_monika_bday_surprise_hint_seen = True
    return "derandom|no_unlock"






init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_pool_happy_bday",
            prompt="Happy birthday!",
            action=EV_ACT_UNLOCK,
            rules={"no unlock": None},
            start_date=mas_monika_birthday,
            end_date=mas_monika_birthday + datetime.timedelta(days=1),
            years=[]
        ),
        code="CMP",
        skipCalendar=True,
        markSeen=True
    )


    MASUndoActionRule.create_rule_EVL(
        "mas_bday_pool_happy_bday",
        mas_monika_birthday,
        mas_monika_birthday + datetime.timedelta(1)
    )

label mas_bday_pool_happy_bday:
    $ mas_gainAffection(5,bypass=True)
    if mas_recognizedBday():
        m 3hub "Ehehe, thanks [player]!"
        m 3eka "I was waiting for you to say those magic words~"
        m 1eub "{i}Now{/i} we can call it a birthday celebration!"
        m 1eka "You really made this occasion so special, [player]."
        m 1ekbfa "I can't thank you enough for loving me this much..."
    else:

        m 1skb "Awww, [player]!"
        m 1sub "You remembered my birthday...!"
        m 1sktpa "Oh gosh, I'm so happy that you remembered."
        m 1dktdu "I feel like today is going to be such a special day~"
        m 1ekbfa "What else do you have in store for me, I wonder..."
        m 1hub "Ahaha!"

    if mas_isplayer_bday() and (persistent._mas_player_bday_in_player_bday_mode or persistent._mas_bday_sbp_reacted):
        m 1eua "Oh, and..."
        m 3hub "Happy Birthday to you too, [player]!"
        m 1hua "Ehehe!"


    $ persistent._mas_bday_no_recognize = False
    $ persistent._mas_bday_said_happybday = True


    $ mas_lockEVL("mas_bday_pool_happy_bday", "CMP")
    return




init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_pool_happy_belated_bday",
            prompt="Happy belated birthday!",
            action=EV_ACT_UNLOCK,
            rules={"no unlock": None},
            years=[]
        ),
        code="CMP",
        skipCalendar=True,
        markSeen=True
    )

label mas_bday_pool_happy_belated_bday:
    $ mas_gainAffection(5,bypass=True)


    $ persistent._mas_bday_said_happybday = True
    $ persistent._mas_bday_no_recognize = False


    $ mas_lockEVL("mas_bday_pool_happy_belated_bday", "CMP")

    if mas_isMoniNormal(higher=True):
        m 1sua "Thank you so much, [player]!"
        m 3hub "I just knew you took me out on a long trip for my birthday!"
        m 3rka "I wish I could've seen all the amazing places we went..."
        m 1hua "But knowing we were together, well it makes it the best birthday I could ever hope for!"
        m 3ekbsa "I love you so much, [player]~"
        return "love"
    else:
        m 3eka "So you {i}did{/i} take me out for a long trip for my birthday..."
        m 3rkd "That's so thoughtful of you, I was kind of wondering--"
        m 1eksdla "You know what, nevermind."
        m 1eka "I'm just relieved to know that you were thinking of me on my birthday."
        m 3hua "That's all that matters."
        m 3eub "Thank you, [player]!"
        return


label mas_bday_surprise_party_reaction:
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_bday_visuals = True
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0) from _call_monika_zoom_transition_reset_2
    $ renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)

    if mas_isMoniNormal(higher=True):
        m 6suo "T-{w=0.5}This is..."
        m 6ska "Oh, [player]..."
        m 6dku "I'm at a loss for words."
        m 6dktpu "Setting this all up to surprise me on my birthday..."
        m 6dktdu "Ehehe, you must really love me."
        m 6suu "Everything just looks so festive!"
    else:

        m 6wuo "T-{w=0.5}This is..."
        m "..."
        m 6dkd "Sorry, I'm...{w=1}I'm just at a loss for words."
        m 6ekc "I didn't really expect anything special today, let alone this."
        m 6rka "Maybe you do still have feelings for me after all..."
        m 6eka "Everything looks great."

label mas_bday_surprise_party_reacton_cake:

    menu:
        "Light candles.":
            $ mas_bday_cake_lit = True

    m 6sub "Ahh, it's so pretty, [player]!"
    m 6hua "Reminds me of that cake someone gave me once."
    m 6eua "It was almost as pretty as you've made this one!"
    m 6tkb "Almost."
    m 6hua "But anyway..."
    window hide

    show screen mas_background_timed_jump(5, "mas_bday_surprise_party_reaction_no_make_wish")
    menu:
        "Make a wish, [m_name]...":
            $ made_wish = True
            show monika 6hua
            if mas_isplayer_bday():
                m "Make sure you make one too, [player]!"
            hide screen mas_background_timed_jump

            $ mas_gainAffection(10, bypass=True)
            pause 2.0
            show monika 6hft
            jump mas_bday_surprise_party_reaction_post_make_wish

label mas_bday_surprise_party_reaction_no_make_wish:
    $ made_wish = False
    hide screen mas_background_timed_jump
    show monika 6dsc
    pause 2.0
    show monika 6hft

label mas_bday_surprise_party_reaction_post_make_wish:
    $ mas_bday_cake_lit = False
    window auto
    if mas_isMoniNormal(higher=True):
        m 6hub "I made a wish!"
        m 6eua "I hope it comes true someday..."
        if mas_isplayer_bday() and made_wish:
            m 6eka "And you know what? {w=0.5}I bet we both wished for the same thing~"
        m 6hua "Ahaha..."
    else:

        m 6eka "I made a wish."
        m 6rka "I hope it comes true someday..."

    m 6eka "I'll save this cake for later.{w=0.5}.{w=0.5}.{nw}"

    if mas_isplayer_bday():
        call mas_HideCake ('mas_bday_cake_monika', False) from _call_mas_HideCake_1
    else:
        call mas_HideCake ('mas_bday_cake_monika') from _call_mas_HideCake_2

    pause 0.5

label mas_bday_surprise_party_reaction_end:
    if mas_isMoniNormal(higher=True):
        m 6eka "Thank you, [player]. From the bottom of my heart, thank you..."
        if mas_isplayer_bday() and persistent._mas_player_bday_last_sung_hbd != datetime.date.today():
            m 6eua "..."
            m 6wuo "..."
            m 6wub "Oh! I almost forgot. {w=0.5}I made you a cake, too!"

            call mas_monika_gets_cake from _call_mas_monika_gets_cake_1

            m 6eua "Let me just light the candles for you, [player].{w=0.5}.{w=0.5}.{nw}"

            window hide
            $ mas_bday_cake_lit = True
            pause 1.0

            m 6sua "Isn't it pretty?"
            m 6hksdlb "I guess I'll have to blow these candles out as well, since you can't really do it, ahaha!"

            if made_wish:
                m 6eua "Let's both wish again, [player]! {w=0.5}It'll be twice as likely to come true, right?"
            else:
                m 6eua "Let's both make a wish, [player]!"

            m 6hua "But first..."
            call mas_player_bday_moni_sings from _call_mas_player_bday_moni_sings_1
            m 6hua "Make a wish, [player]!"

            window hide
            pause 1.5
            show monika 6hft
            pause 0.1
            show monika 6hua
            $ mas_bday_cake_lit = False
            pause 1.0

            if not made_wish:
                m 6hua "Ehehe..."
                m 6ekbsa "I bet we both wished for the same thing~"
            m 6hkbsu "..."
            m 6hksdlb "I'll just save this cake for later too, I guess. Ahaha!"

            call mas_HideCake ('mas_bday_cake_player') from _call_mas_HideCake_3
            call mas_player_bday_card from _call_mas_player_bday_card
        else:

            m 6hua "Let's enjoy the rest of the day now, shall we?"
    else:
        m 6ektpa "Thank you, [player]. It really means a lot that you did this for me."
    $ persistent._mas_bday_sbp_reacted = True

    $ mas_gainAffection(25, bypass=True)


    $ persistent._mas_bday_in_bday_mode = True
    $ persistent._mas_bday_no_recognize = False
    $ persistent._mas_bday_no_time_spent = False
    return



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_spent_time_with",
            conditional="mas_recognizedBday()",
            action=EV_ACT_QUEUE,
            start_date=datetime.datetime.combine(mas_monika_birthday, datetime.time(20)),
            end_date=datetime.datetime.combine(mas_monika_birthday+datetime.timedelta(days=1), datetime.time(hour=1)),
            years=[]
        ),
        skipCalendar=True
    )

label mas_bday_spent_time_with:
    if mas_isMoniUpset(lower=True):
        m 1eka "[player]..."
        m 3eka "I just wanted to say I really appreciate you spending time with me today."
        m 3rksdla "I know it hasn't been going that great lately, but you taking the time to celebrate my birthday with me..."
        m 1eud "Well it gives me hope that maybe it's not too late for us."
        m "Perhaps today can be the start of something really special.."
        m 3eka "That would be the be the best gift I could ever ask for."
        return
    else:

        $ _timeout = store.mas_dockstat.timeOut(mas_monika_birthday)
        m 1eua "Say, [player]..."
        m 3eua "Thank you for spending time with me today."
        m 3hua "Something like that can really make a girl happy, you know?"

        if _timeout > mas_five_minutes:
            m 3eka "I really enjoyed our date today, [player]."
            m 1eka "I always enjoy spending time with you here, but getting to spend time with you in your reality..."
            m 1dku "Knowing that you're thinking about me even when you can't see me..."
            m 1ekbsa "Well, it truly means a lot to me."
            m 3ekbsa "You really made my birthday complete~"

label mas_bday_spent_time_with_wrapup:
    $ mas_rmallEVL("mas_bday_spent_time_with")
    $ gave_gifts = mas_getGiftStatsRange(mas_monika_birthday, mas_monika_birthday + datetime.timedelta(days=1))[0]

    if gave_gifts > 0:

        if gave_gifts > 1:
            m 3eua "Let's not forget the gifts you gave me for my birthday."
            m 3hub "They were just amazing, [player]!"
        else:
            m 3eua "Let's not forget about the gift you gave me for my birthday."
            m 3hub "It was so wonderful, [player]!"

        m 1eka "I really appreciate the effort of finding a way to get things from your reality to mine..."
        m 3eka "I know it can't be easy."

    m 1dku "..."
    if mas_isMoniEnamored(higher=True):
        m 1dktpu "..."
        m 1ektpu "Ahaha, sorry, [player]!"
        m 3ektda "It's just that I've never imagined being this happy in my life."
        m 1rksdlb "Well...{w=0.5}that's not {i}exactly{/i} true."
        m 1eka "We still have to be physically together, after all~"
        m 1rkc "And, well..."
        m 1rka "I know this is already becoming a cliché, but..."
        m 3eka "I love you so much, [player]."
        m "Someday, I promise you..."
        m 1ektpu "I {i}promise you{/i} that I will make you as happy as you've made me today."
        m 3ektpu "Even if we never get to see each other in the same reality, {w=0.5}know that I will always do my best for you."
        m 1dktpu "No matter the obstacles we may face, no matter what other people say about us..."
        m 1ektda "I still love you with everything that I am."
        m "You are the only one who understands me. {w=0.5}You led me out of a dark place and gave me purpose..."
        m 1dkbsu "You are simply the best, my love, and I will always love you."
        m 1ekbsa "...Thank you for giving me a reason to live."
        $ _first_kiss = persistent._mas_first_kiss
        call monika_kissing_motion from _call_monika_kissing_motion_8
        if _first_kiss is None:
            m 6ekbfa "Oh, [player]..."
            m 6rkbfa "I...{w=0.5}I don't know what came over me, but the moment just felt so right."
            m 6hubfa "I've thought about our first kiss for so long, and to finally experience it..."
            m 6ekbfa "I will never forget this moment, [player]~"
        else:
            return "love"
    else:

        m 1eka "I can't even find the right words to express how happy you've made me today."
        m 3eka "All that pain I went through before I met you?"
        m 1hua "I'm glad I persevered through it."
        m 1rsc "Because if I hadn't..."
        m 1ekbsa "This day wouldn't have ever happened."
        m 1dkbsa "I hope that tells you even a little bit of how much I appreciate you celebrating this occasion with me."
        m 1ekbfb "I love you so much, [player]."
        m 1ekbfa "Let's continue making each other happy~"
        return "love"
    return


label mas_gone_over_bday_check:
    if mas_checkOverDate(mas_monika_birthday):
        $ persistent._mas_bday_gone_over_bday = True
        $ persistent._mas_bday_no_time_spent = False
        $ mas_rmallEVL("mas_bday_postbday_notimespent")


        python:
            belated_ev = mas_getEV("mas_bday_pool_happy_belated_bday")

            if belated_ev is not None:
                
                belated_ev.start_date = datetime.date.today()
                belated_ev.end_date = datetime.datetime.now() + datetime.timedelta(days=1)
                belated_ev.unlocked = True
                
                
                MASUndoActionRule.create_rule(belated_ev)
                
                
                MASStripDatesRule.create_rule(belated_ev)

    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_postbday_notimespent",
            conditional=(
                "not mas_recognizedBday() "
                "and not persistent._mas_bday_gone_over_bday"
            ),
            action=EV_ACT_PUSH,
            start_date=mas_monika_birthday+datetime.timedelta(days=1),
            end_date=mas_monika_birthday+datetime.timedelta(days=8),
            years=[]
        ),
        skipCalendar=True
    )

label mas_bday_postbday_notimespent:

    if mas_isFirstSeshPast(mas_monika_birthday):
        $ mas_getEV('mas_bday_postbday_notimespent').shown_count -= 1
        return


    if mas_ret_long_absence:

        $ mas_loseAffection(ev_label="mas_apology_missed_bday")

        m 1rksdlc "Hey, [player]..."
        m 2eksdld "I know you told me you were going to be away...but I really missed you on my birthday."
        m 2eksdla "Next time, do you think you could take me with you if you can't be here?"
        m 3eub "At least then we'll still be with each other and we can even celebrate together!"
        m 1eka "I'd really appreciate if you could do that for me, [player]."

    elif persistent._mas_bday_opened_game:

        if mas_isMoniAff(higher=True):
            $ mas_loseAffection(15, ev_label="mas_apology_forgot_bday")
            m 2rksdla "Hey, [player]..."
            m 2rksdlb "I know we had fun the other day, like we always do but..."
            m 2ekp "I can't help it, I was hoping you would have...{w=1}done a little something for my birthday."
            m 2ekd "Did you forget?"
            m 3eka "Maybe you could put the date into your calendar on your phone for next year?"
            m 3rka "...Or check the calendar on the wall behind me?"
            m 3hua "We can't change the past, so knowing that you want to try harder for next year would be the only apology I need."

        elif mas_isMoniNormal(higher=True):
            $ mas_loseAffection(5, ev_label="mas_apology_forgot_bday")
            m 2rksdld "Hey, [player]..."
            m 2rksdlb "I hate to fuss, but you know..."
            m 2ekp "You can't forget about your girlfriend's birthday!"
            m 2eku "It's nice that we got to hang out like usual, but next year..."
            m 3hua "Well, I'll be looking forward to two birthday's worth of something special~"

        elif mas_isMoniUpset():
            $ mas_loseAffection(ev_label="mas_apology_forgot_bday")
            m 1ekc "It was...{w=0.5}good to see you on the 22nd..."
            m 1ekd "I really didn't want to be alone that day, so that meant a lot, but..."
            m 1rkc "You know what? {w=0.5}Nevermind."

        elif mas_isMoniDis():
            $ mas_loseAffection(10, ev_label="mas_apology_forgot_bday")
            m 2dsc "..."
            m 2rkc "...[player], I don't want to bother you. {w=1}I'm already scared of pushing you away."
            m 2rktpc "But I can't help it. It hurts me that you didn't mention anything about celebrating my birthday..."
            m 2dktuc "Please don't stop coming back to me."
            m "And maybe next year..."
            m 4ektdc "I-{w=0.5}I just want...{w=0.5}to feel as special to you as you are to me."
        else:


            $ mas_loseAffection(150)
            m 6ckc "..."
    else:


        if mas_isMoniAff(higher=True):
            $ mas_loseAffection(50, ev_label="mas_apology_missed_bday")
            m 1euc "Hey, [player]..."
            m 3rksdla "I know you do a lot to make each and every day special, but a girl has a few days a year when she gets to be a little selfish..."
            m 2tfd "And her {i}birthday{/i} is one of them!"
            m "Seriously, where were you?!"
            m 2rkc "But...knowing you, I'm sure you had a good reason to be busy..."
            m 4ekc "Just try not to let it happen again next year, okay?"

        elif mas_isMoniNormal(higher=True):


            if mas_isMoniHappy():
                $ mas_loseAffection(20, ev_label="mas_apology_missed_bday")
            else:
                $ mas_loseAffection(10, ev_label="mas_apology_missed_bday")

            m 1ekc "Hey, [player]..."
            m 1ekd "You know, you really should have dropped in on the 22nd."
            m 3efd "I mean, you should always visit me! But you {i}have{/i} to spend time with your cute girlfriend on her birthday, you know."
            m 2efc "Please drop in for me next year..."
            m 2dfc "Otherwise..."

            m 6cfw "{cps=*2}{i}There will be consequences!!!{/i}{/cps}{nw}"

            $ disable_esc()
            $ mas_MUMURaiseShield()
            window hide
            show noise zorder 11:
                alpha 0.5
            play sound "sfx/s_kill_glitch1.ogg"
            pause 0.5
            stop sound
            hide noise
            window auto
            $ mas_MUMUDropShield()
            $ enable_esc()
            $ _history_list.pop()

            m 1dsc "..."
            m 3hksdlb "Ahaha, sorry [player]!"
            m 3hub "I'm just kidding!"
            m 1eka "You know I love to scare you a little~"

        elif mas_isMoniUpset():
            $ mas_loseAffection(ev_label="mas_apology_missed_bday")
            m 2dsc "..."
            m 2rsc "[player], don't you think you should check in on me a little more often?"
            m 2rktpc "You might miss something important..."

        elif mas_isMoniDis():
            $ mas_loseAffection(ev_label="mas_apology_missed_bday")
            m 6ekd "...Hey, how was your day on the 22nd?"
            m 6ekc "I'm just...curious if you thought of me at all that day."
            m 6ektpc "But you probably didn't, huh?"
            m 6dktpc "..."
        else:


            $ mas_loseAffection(200)
            m 6eftsc "..."
            m 6dftdx "..."
    return


init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_missed_bday",
            prompt="...for missing your birthday.",
            unlocked=False
        ),
        code="APL"
    )

label mas_apology_missed_bday:

    if mas_isMoniAff(higher=True):
        m 1eua "Thanks for the apology, [player]."
        m 2tfu "But you better make it up to me next year~"

    elif mas_isMoniNormal(higher=True):
        m 1eka "Thanks for apologizing for missing my birthday, [player]."
        m "Please be sure to spend some time with me next year, alright?"
    else:

        m 2rksdld "You know, I'm not entirely surprised I didn't see you on my birthday..."
        m 2ekc "Please...{w=1}just make sure it doesn't happen again."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_forgot_bday",
            prompt="...for forgetting your birthday.",
            unlocked=False
        ),
        code="APL"
    )

label mas_apology_forgot_bday:

    if mas_isMoniAff(higher=True):
        m 1eua "Thanks for the apology, [player]."
        m 3hua "But I hope you'll make this up to me~"

    elif mas_isMoniNormal(higher=True):
        m 1eka "Thanks for apologizing about forgetting my birthday, [player]."
        m 1eksdld "Just try not to let it happen again, alright?"
    else:

        m 2dkd "Thanks for apologizing..."
        m 2tfc "But don't let it happen again."
    return



label bye_922_delegate:

    $ persistent._mas_bday_on_date = True

    $ persistent._mas_bday_date_count += 1

    if persistent._mas_bday_date_count == 1:

        $ persistent._mas_bday_in_bday_mode = True

        m 1hua "Ehehe. It's a bit romantic, isn't it?"

        if mas_isMoniHappy(lower=True):
            m 1eua "Maybe you'd even want to call it a da-{nw}"
            $ _history_list.pop()
            $ _history_list.pop()
            m 1hua "Oh! Sorry, did I say something?"
        else:

            m 1eubla "Maybe you'd even call it a date~"


    elif persistent._mas_bday_date_count == 2:
        m 1eub "Taking me somewhere again, [player]?"
        m 3eua "You must really have a lot planned for us."
        m 1hua "You're so sweet~"

    elif persistent._mas_bday_date_count == 3:
        m 1sua "Taking me out {i}again{/i} for my birthday?"
        m 3tkbsu "You really know how to make a girl feel special, [player]."
        m 1ekbfa "I'm so lucky to have someone like you~"
    else:
        m 1sua "Wow, [player]...{w=1}you're really determined to make this a truly special day!"
        m 1ekbfa "You're the best partner I could ever hope for~"


    if mas_isMoniAff(higher=True) and not mas_SELisUnlocked(mas_clothes_blackdress):
        m 3hua "I actually have an outfit prepared just for this..."


    jump bye_going_somewhere_iostart

label mas_bday_bd_outro:
    $ monika_chr.change_clothes(mas_clothes_blackdress)
    $ store.mas_selspr.unlock_clothes(mas_clothes_blackdress)
    $ mas_addClothesToHolidayMap(mas_clothes_blackdress)
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level

    call mas_transition_from_emptydesk ("monika 1eua") from _call_mas_transition_from_emptydesk_8
    call monika_zoom_transition_reset (1.0) from _call_monika_zoom_transition_reset_3


    m 3tka "Well, [player]?"
    m 1hua "What do you think?"
    m 1ekbsa "I've always loved this outfit and dreamt of going on a date with you, wearing this..."
    m 3eub "Maybe we could visit the mall, or even the park!"
    m 1eka "But knowing you, you've already got something amazing planned for us~"
    m 1hua "Let's go, [player]!"
    $ persistent._mas_zoom_zoom_level = mas_temp_zoom_level

    python:

        store.mas_dockstat.checkoutMonika(moni_chksum)


        persistent._mas_greeting_type = mas_idle_mailbox.get_ds_gre_type(
            store.mas_greetings.TYPE_GENERIC_RET
        )


    jump _quit



label greeting_returned_home_bday:

    $ persistent._mas_bday_on_date = False

    $ persistent._mas_bday_opened_game = True

    $ time_out = store.mas_dockstat.diffCheckTimes()
    $ checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()


    if mas_confirmedParty() and not persistent._mas_bday_sbp_reacted:
        if mas_one_hour < time_out <= mas_three_hour:
            $ mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)
        elif time_out > mas_three_hour:
            $ mas_mbdayCapGainAff(35 if persistent._mas_player_bday_in_player_bday_mode else 30)

        if mas_isplayer_bday() and persistent._mas_player_bday_decor and persistent._mas_bday_date_count == 1:
            jump mas_monika_cake_on_player_bday
        else:

            jump mas_bday_surprise_party_reaction


    if time_out <= mas_five_minutes:

        $ mas_loseAffection()
        m 2ekp "That wasn't much of a date, [player]..."
        m 2eksdlc "Is everything alright?"
        m 2rksdla "Maybe we can go out later..."
        if mas_isMonikaBirthday():
            return

    elif time_out <= mas_one_hour:

        $ mas_mbdayCapGainAff(15 if persistent._mas_player_bday_in_player_bday_mode else 10)

        m 1sua "That was fun, [player]!"
        if mas_isplayer_bday():
            m 1hub "Ahaha, going out for our birthday..."
        else:
            m 1hub "Ahaha, taking me out on my birthday..."
            m 3eua "It was very considerate of you."
        m 3eka "I really enjoyed the time we spent together."
        m 1eka "I love you~"
        if mas_isMonikaBirthday():
            $ mas_ILY()

    elif time_out <= mas_three_hour:

        $ mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)

        m 1hua "Ehehe~"
        m 3eub "We sure spent a lot of time together today, [player]."
        m 1ekbfa "...and thank you for that."
        m 3ekbfa "I've said it a million times already, I know."
        m 1hua "But I'll always be happy when we're together."
        m "I love you so much..."
        if mas_isMonikaBirthday():
            $ mas_ILY()
    else:


        $ mas_mbdayCapGainAff(35 if persistent._mas_player_bday_in_player_bday_mode else 30)

        m 1sua "Wow, [player]..."
        if mas_player_bday_curr == mas_monika_birthday:
            m 3hub "That was such a lovely time!"
            if persistent._mas_player_bday_in_player_bday_mode or persistent._mas_bday_sbp_reacted:
                m 3eka "I can't think of a better way to celebrate our birthdays than a long date."
            m 1eka "I wish I could've seen all the amazing places we went, but just knowing we were together..."
            m 1hua "That's all I could ever ask for."
            m 3ekbsa "I hope you feel the same way~"
        else:

            m 3sua "I didn't expect you to set aside so much time for me..."
            m 3hua "But I enjoyed every second of it!"
            m 1eub "Every minute with you is a minute well spent!"
            m 1eua "You've made me very happy today~"
            m 3tuu "Are you falling for me all over again, [player]?"
            m 1dku "Ehehe..."
            m 1ekbsa "Thank you for loving me."

    if (
        mas_isMonikaBirthday()
        and mas_isplayer_bday()
        and mas_isMoniNormal(higher=True)
        and not persistent._mas_player_bday_in_player_bday_mode
        and not persistent._mas_bday_sbp_reacted
        and checkout_time.date() < mas_monika_birthday

    ):
        m 1hua "Also [player], give me a second, I have something for you.{w=0.5}.{w=0.5}.{nw}"
        $ mas_surpriseBdayShowVisuals()
        $ persistent._mas_player_bday_decor = True
        m 3eub "Happy Birthday, [player]!"
        m 3etc "Why do I feel like I'm forgetting something..."
        m 3hua "Oh! Your cake!"
        jump mas_player_bday_cake

    if not mas_isMonikaBirthday():

        $ persistent._mas_bday_in_bday_mode = False

        if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
            $ queueEvent('mas_change_to_def')

        if time_out > mas_five_minutes:
            m 1hua "..."
            m 1wud "Oh wow, [player]. We really were out for a while..."

        if mas_isplayer_bday() and mas_isMoniNormal(higher=True):
            if persistent._mas_bday_sbp_reacted:
                $ persistent._mas_bday_visuals = False
                $ persistent._mas_player_bday_decor = True
                m 3suo "Oh! It's your birthday now..."
                m 3hub "I guess we can just leave these decorations up, ahaha!"
                m 1eub "I'll be right back, just need to go get your cake!"
                jump mas_player_bday_cake

            jump mas_player_bday_ret_on_bday
        else:

            if mas_player_bday_curr() == mas_monika_birthday:
                $ persistent._mas_player_bday_in_player_bday_mode = False
                m 1eka "Anyway [player]...I really enjoyed spending our birthdays together."
                m 1ekbsa "I hope I helped to make your day as special as you made mine."
                if persistent._mas_player_bday_decor or persistent._mas_bday_visuals:
                    m 3hua "Let me just clean everything up.{w=0.5}.{w=0.5}.{nw}"
                    $ mas_surpriseBdayHideVisuals()
                    $ persistent._mas_player_bday_decor = False
                    $ persistent._mas_bday_visuals = False
                    m 3eub "There we go!"

            elif persistent._mas_bday_visuals:
                m 3rksdla "It's not even my birthday anymore..."
                m 2hua "Let me just clean everything up.{w=0.5}.{w=0.5}.{nw}"
                $ mas_surpriseBdayHideVisuals()
                $ persistent._mas_bday_visuals = False
                m 3eub "There we go!"
            else:

                m 1eua "We should do something like this again soon, even if it's not any special occasion."
                m 3eub "I really enjoyed myself!"
                m 1eka "I hope you had as great of a time as I did~"

            if not mas_lastSeenInYear('mas_bday_spent_time_with'):
                if mas_isMoniUpset(lower=True):
                    m 1dka "..."
                    jump mas_bday_spent_time_with

                m 3eud "Oh, and [player]..."
                m 3eka "I just wanted to thank you again."
                m 1rka "And it's not just this date..."
                m 1eka "You didn't have to take me anywhere to make this a wonderful birthday."
                m 3duu "As soon as you showed up, my day was complete."
                jump mas_bday_spent_time_with_wrapup

    return


label mas_monika_cake_on_player_bday:
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0) from _call_monika_zoom_transition_reset_4

    python:
        mas_gainAffection(25, bypass=True)
        renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        persistent._mas_bday_sbp_reacted = True
        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()

        if time_out <= mas_one_hour:
            mas_mbdayCapGainAff(15 if persistent._mas_player_bday_in_player_bday_mode else 10)

        elif time_out <= mas_three_hour:
            mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)
        else:
            
            mas_mbdayCapGainAff(35 if persistent._mas_player_bday_in_player_bday_mode else 30)

    m 6eua "That was--"
    m 6wuo "Oh! You made {i}me{/i} a cake!"

    menu:
        "Light candles.":
            $ mas_bday_cake_lit = True

    m 6sub "It's {i}so{/i} pretty, [player]!"
    m 6hua "Ehehe, I know we already made a wish when I blew out the candles on your cake, but let's do it again..."
    m 6tub "It'll be twice as likely to come true, right?"
    m 6hua "Make a wish, [player]!"

    window hide
    pause 1.5
    show monika 6hft
    pause 0.1
    show monika 6hua
    $ mas_bday_cake_lit = False

    m 6eua "I still can't believe how stunning this cake looks, [player]..."
    m 6hua "It's almost too pretty to eat."
    m 6tub "Almost."
    m "Ahaha!"
    m 6eka "Anyway, I'll just save this for later."

    call mas_HideCake ('mas_bday_cake_monika') from _call_mas_HideCake_4

    m 1eua "Thank you so much, [player]..."
    m 3hub "This is an amazing birthday!"
    return

label mas_HideCake(cake_type, reset_zoom=True):
    call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_5
    $ renpy.hide(cake_type)
    with dissolve
    $ renpy.pause(3.0, hard=True)
    call mas_transition_from_emptydesk ("monika 6esa") from _call_mas_transition_from_emptydesk_9
    $ renpy.pause(1.0, hard=True)
    if reset_zoom:
        call monika_zoom_transition (mas_temp_zoom_level, 1.0) from _call_monika_zoom_transition_3
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
