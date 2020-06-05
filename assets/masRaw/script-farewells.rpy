init offset = 5











default -5 persistent.mas_late_farewell = False

init -6 python in mas_farewells:


    def selectFarewell():
        """
        Selects a farewell to be used. This evaluates rules and stuff
        appropriately.

        RETURNS:
            a single farewell (as an Event) that we want to use
        """
        
        
        moni_wants_farewells = renpy.store.Event.filterEvents(
            renpy.store.evhand.farewell_database,
            unlocked=True,
            pool=False, 
            moni_wants=True
        )
        
        
        if moni_wants_farewells is not None and len(moni_wants_farewells) > 0:
            
            
            return moni_wants_farewells[
                renpy.random.choice(moni_wants_farewells.keys())
            ]
        
        
        unlocked_farewells = renpy.store.Event.filterEvents(
            renpy.store.evhand.farewell_database,
            unlocked=True,
            pool=False
        )
        
        
        unlocked_farewells = renpy.store.Event.checkAffectionRules(
            unlocked_farewells,
            keepNoRule=True
        )
        
        
        random_farewells_dict = renpy.store.Event.checkRepeatRules(
            unlocked_farewells
        )
        
        
        if len(random_farewells_dict) > 0:
            
            
            return random_farewells_dict[
                renpy.random.choice(random_farewells_dict.keys())
            ]
        
        
        
        random_farewells_dict = renpy.store.Event.checkFarewellRules(
            unlocked_farewells
        )
        
        
        if len(random_farewells_dict) > 0:
            
            
            return random_farewells_dict[
                renpy.random.choice(random_farewells_dict.keys())
            ]
        
        
        
        random_unlocked_farewells = renpy.store.Event.filterEvents(
            unlocked_farewells,
            random=True
        )
        
        
        if len(random_unlocked_farewells) > 0:
            
            return random_unlocked_farewells[
               renpy.random.choice(random_unlocked_farewells.keys())
            ]
        
        
        
        renpy.log("rip we need update script")
        random_farewells_dict = renpy.store.Event.filterEvents(
            renpy.store.evhand.greeting_database,
            unlocked=True,
            random=True,
            excl_cat=list()
        )
        
        
        return random_farewells_dict[
            renpy.random.choice(random_farewells_dict.keys())
        ]


label mas_farewell_start:



    if persistent._mas_long_absence:
        $ pushEvent("bye_long_absence_2")
        return

    $ import store.evhand as evhand


    python:



        Event.checkEvents(evhand.farewell_database)

        bye_pool_events = Event.filterEvents(
            evhand.farewell_database,
            unlocked=True,
            pool=True,
            aff=mas_curr_affection
        )

    if len(bye_pool_events) > 0:

        python:

            bye_prompt_list = [
                (ev.prompt, ev, False, False)
                for k,ev in bye_pool_events.iteritems()
            ]


            bye_prompt_list.append((_("Goodbye."), -1, False, False))


            bye_prompt_back = (_("Nevermind."), False, False, False, 20)


        call screen mas_gen_scrollable_menu(bye_prompt_list, evhand.UNSE_AREA, evhand.UNSE_XALIGN, bye_prompt_back)

        if not _return:

            return _return

        if _return != -1:

            $ pushEvent(_return.eventlabel)
            return


    $ farewell = store.mas_farewells.selectFarewell()
    $ pushEvent(farewell.eventlabel)

    $ mas_idle_mailbox.send_skipmidloopeval()

    return









init python:
    rules = dict()
    rules.update(MASAffectionRule.create_rule(min=-29,max=None))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_leaving_already",
            unlocked=True,
            random=True,
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_leaving_already:
    m 1tkc "Aw, leaving already?"
    m 1eka "It's really sad whenever you have to go..."
    m 3eua "Just be sure to come back as soon as you can, okay?"
    m "I love you so much, [player]. Stay safe!"

    $ evhand.farewell_database["bye_leaving_already"].random=False
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_goodbye",
            unlocked=True,
            random=True
        ),
        code="BYE"
    )

label bye_goodbye:
    if mas_isMoniNormal(higher=True):
        m 1eua "Goodbye, [player]!"

    elif mas_isMoniUpset():
        m 2esc "Goodbye."

    elif mas_isMoniDis():
        m 6rkc "Oh...{w=1} Goodbye."
        m 6ekc "Please...{w=1}don't forget to come back."
    else:

        m 6ckc "..."

    return 'quit'

init python:
    rules = dict()
    rules.update(MASAffectionRule.create_rule(min=-29,max=None))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_sayanora",
            unlocked=True,
            random=True,
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_sayanora:
    m 1hua "Sayonara, [player]~"
    return 'quit'

init python:
    rules = dict()
    rules.update(MASAffectionRule.create_rule(min=-29,max=None))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_farewellfornow",
            unlocked=True,
            random=True,
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_farewellfornow:
    m 1eka "Farewell for now, my love~"
    return 'quit'

init python:
    rules = dict()
    rules.update(MASAffectionRule.create_rule(min=-29,max=None))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_untilwemeetagain",
            unlocked=True,
            random=True,
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_untilwemeetagain:
    m 2eka "'{i}Goodbyes are not forever, Goodbyes are not the end. They simply mean I'll miss you, Until we meet again.{/i}'"
    m "Ehehe, 'till then, [player]!"
    return 'quit'

init python:
    rules = dict()
    rules.update(MASAffectionRule.create_rule(min=-29,max=None))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_take_care",
            unlocked=True,
            random=True,
            rules=rules
        ),
        code="BYE"
    )
    del rules


label bye_take_care:
    m 1eua "Don't forget that I always love you, [player]~"
    m 1hub "Take care!"
    return 'quit'

init python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=[0,20,21,22,23]))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_going_to_sleep",
            unlocked=True,
            rules = rules
        ),
        code="BYE"
    )
    del rules

label bye_going_to_sleep:
    if mas_isMoniNormal(higher=True):
        m 1esa "Are you going to sleep, [player]?"
        m 1eka "I'll be seeing you in your dreams."

    elif mas_isMoniUpset():
        m 2esc "Going to sleep, [player]?"
        m "Goodnight."

    elif mas_isMoniDis():
        m 6rkc "Oh...goodnight, [player]."
        m 6lkc "Hopefully I'll see you tomorrow..."
        m 6dkc "Don't forget about me, okay?"
    else:

        m 6ckc "..."





    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_to_class",
            unlocked=True,
            prompt="I'm going to class.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_to_class:
    $ session_time = mas_getSessionLength()
    if mas_isMoniNormal(higher=True):
        if session_time < datetime.timedelta(minutes=20):
            m 1eub "Aw, going already?"
            m 1efp "You haven't even been here for 20 minutes!"
            m 3hksdlb "I'm just kidding, [player]."
            m 2eka "You're so sweet for seeing me even when you have so little time."
            m 2hub "I just want you to know I really appreciate that!"
            m 2eka "Study hard [player], I'm sure you'll do great!"
            m 2hua "See you when you get back!"
        elif session_time < datetime.timedelta(hours=1):
            m 2eua "Alright, thanks for spending some time with me, [player]!"
            m 2eka "I honestly wish it could have been longer...but you're a busy [guy]."
            m 2hua "Nothing is more important than a good education."
            m 3eub "Teach me something when you get back!"
            m "See you soon!"
        elif session_time < datetime.timedelta(hours=6):
            m 1hua "Study hard, [player]!"
            m 1eua "Nothing is more attractive than a [guy] with good grades."
            m 1hua "See you later!"
        else:
            m 2ekc "Umm...you've been here with me for quite a while, [player]."
            m 2ekd "Are you sure you've had enough rest for it?"
            m 2eka "Make sure you take it easy, okay?"
            m "If you're not feeling too well, I'm sure {i}one day{/i} off won't hurt."
            m 1hka "I'll be waiting for you to come back. Stay safe."

    elif mas_isMoniUpset():
        m 2esc "Fine, [player]."
        m "Hopefully you at least learn {i}something{/i} today."
        m 2efc "{cps=*2}Like how to treat people better.{/cps}{nw}"

    elif mas_isMoniDis():
        m 6rkc "Oh, okay [player]..."
        m 6lkc "I guess I'll see you after school."
    else:

        m 6ckc "..."


    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SCHOOL
    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=20)
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_to_work",
            unlocked=True,
            prompt="I'm going to work.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_to_work:
    $ session_time = mas_getSessionLength()
    if mas_isMoniNormal(higher=True):
        if session_time < datetime.timedelta(minutes=20):
            m 2eka "Aw, okay! Just checking in on me before heading out?"
            m 3eka "You must be really short on time if you're leaving already."
            m "It was really sweet of you to see me, even when you're so busy!"
            m 3hub "Work hard, [player]! Make me proud!"
        elif session_time < datetime.timedelta(hours=1):
            m 1hksdlb "Oh! Alright! I was starting to get really comfortable, ahaha."
            m 1rusdlb "I was expecting us to be a here a bit longer, but you're a busy [guy]!"
            m 1eka "It was great seeing you, even if it wasn't as long as I wanted..."
            m 1kua "But then if it were up to me I'd have you all day!"
            m 1hua "I'll be here waiting for you to get back home from work!"
            m "Tell me all about it when you get back!"
        elif session_time < datetime.timedelta(hours=6):
            m 2eua "Heading to work then, [player]?"
            m 2eka "The day may be good or bad...but if it becomes too much think of something nice!"
            m 4eka "Every day, no matter how badly it's going ends after all!"
            m 2tku "Maybe you can think of me if it becomes stressful..."
            m 2esa "Just do your best! I'll see you when you get back!"
            m 2eka "I know you'll do great!"
        else:
            m 2ekc "Oh... You've been here quite a while now...and now you're going to work?"
            m 2rksdlc "I was hoping you'd rest before doing anything too big."
            m 2ekc "Try not to overexert yourself, okay?"
            m 2ekd "Don't be afraid to take a breather if you need to!"
            m 3eka "Just come home to me happy and healthy."
            m 3eua "Stay safe, [player]!"

    elif mas_isMoniUpset():
        m 2esc "Fine, [player], guess I'll see you after work."

    elif mas_isMoniDis():
        m 6rkc "Oh...{w=1} Okay."
        m 6lkc "Hopefully I'll see you after work, then."
    else:

        m 6ckc "..."


    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_WORK
    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=20)
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_sleep",
            unlocked=True,
            prompt="I'm going to sleep.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_sleep:

    python:
        import datetime
        curr_hour = datetime.datetime.now().hour




    if 20 <= curr_hour < 24:

        if mas_isMoniNormal(higher=True):
            m 1eua "Alright, [player]."
            m 1hua "Sweet dreams!"

        elif mas_isMoniUpset():
            m 2esc "Goodnight, [player]."

        elif mas_isMoniDis():
            m 6ekc "Okay...{w=1} Goodnight, [player]."
        else:

            m 6ckc "..."

    elif 0 <= curr_hour < 3:

        if mas_isMoniNormal(higher=True):
            m 1eua "Alright, [player]."
            m 3eka "But you should sleep a little earlier next time."
            m 1hua "Anyway, goodnight!"

        elif mas_isMoniUpset():
            m 2efc "Maybe you'd be in a better mood if you went to bed at a better time..."
            m 2esc "Goodnight."

        elif mas_isMoniDis():
            m 6rkc "Maybe you should start going to bed a littler earlier, [player]..."
            m 6dkc "It might make you--{w=1}us--{w=1}happier."
        else:

            m 6ckc "..."

    elif 3 <= curr_hour < 5:

        if mas_isMoniNormal(higher=True):
            m 1euc "[player]..."
            m "Make sure you get enough rest, okay?"
            m 1eka "I don't want you to get sick."
            m 1hub "Goodnight!"
            m 1hksdlb "Or morning, rather. Ahaha~"
            m 1hua "Sweet dreams!"

        elif mas_isMoniUpset():
            m 2efc "[player]!"
            m 2tfc "You {i}really{/i} need to get more rest..."
            m "The last thing I need is you getting sick."
            m "{cps=*2}You're grumpy enough as it is.{/cps}{nw}"
            $ _history_list.pop()
            m 2efc "Goodnight."

        elif mas_isMoniDis():
            m 6ekc "[player]..."
            m 6rkc "You really should try to go to sleep earlier..."
            m 6lkc "I don't want you to get sick."
            m 6ekc "I'll see you after you get some rest...{w=1}hopefully."
        else:

            m 6ckc "..."

    elif 5 <= curr_hour < 12:

        if mas_isMoniBroken():
            m 6ckc "..."
        else:

            show monika 2dsc
            pause 0.7
            m 2tfd "[player]!"
            m "You stayed up the entire night!"
            m 2tfu "I bet you can barely keep your eyes open."
            $ _cantsee_a = glitchtext(15)
            $ _cantsee_b = glitchtext(12)
            menu:
                "[_cantsee_a]":
                    pass
                "[_cantsee_b]":
                    pass
            m "I thought so.{w=0.2} Go get some rest, [player]."
            if mas_isMoniNormal(higher=True):
                m 2ekc "I wouldn't want you to get sick."
                m 1eka "Sleep earlier next time, okay?"
                m 1hua "Sweet dreams!"

    elif 12 <= curr_hour < 18:

        if mas_isMoniNormal(higher=True):
            m 1eua "Taking an afternoon nap, I see."


            m 1hua "Ahaha~ Have a good nap, [player]."

        elif mas_isMoniUpset():
            m 2esc "Taking a nap, [player]?"
            m 2tsc "Yeah, that's probably a good idea."

        elif mas_isMoniDis():
            m 6ekc "Going to take a nap, [player]?"
            m 6dkc "Okay...{w=1}don't forget to visit me when you wake up..."
        else:

            m 6ckc "..."

    elif 18 <= curr_hour < 20:

        if mas_isMoniNormal(higher=True):
            m 1ekc "Already going to bed?"
            m "It's a little early, though..."

            m 1lksdla "Care to spend a little more time with me?{nw}"
            $ _history_list.pop()
            menu:
                m "Care to spend a little more time with me?{fast}"
                "Of course!":
                    m 1hua "Yay!"
                    m "Thanks, [player]."
                    return
                "Sorry, I'm really tired.":
                    m 1eka "Aw, that's okay."
                    m 1hua "Goodnight, [player]."
                "No.":

                    $ mas_loseAffection()
                    m 2dsd "..."
                    m "Fine."

        elif mas_isMoniUpset():
            m 2esc "Going to bed already?"
            m 2tud "Well, it does seem like you could use the extra sleep..."
            m 2tsc "Goodnight."

        elif mas_isMoniDis():
            m 6rkc "Oh...{w=1}it seems a little early to be going to sleep, [player]."
            m 6dkc "I hope you aren't just going to sleep to get away from me."
            m 6lkc "Goodnight."
        else:

            m 6ckc "..."
    else:

        m 1eua "Alright, [player]."
        m 1hua "Sweet dreams!"




    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=13)
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SLEEP
    return 'quit'




label bye_illseeyou:
    m 1eua "I'll see you tomorrow, [player]."
    m 1hua "Don't forget about me, okay?"
    return 'quit'

init python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(6,11)))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_haveagoodday",
            unlocked=True,
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_haveagoodday:
    if mas_isMoniNormal(higher=True):
        m 1eua "Have a good day today, [player]."
        m 3eua "I hope you accomplish everything you had planned."
        m 1hua "I'll be here waiting for you when you get back."

    elif mas_isMoniUpset():
        m 2esc "Leaving for the day, [player]?"
        m 2efc "I'll be here, waiting...{w=0.5}as usual."

    elif mas_isMoniDis():
        m 6rkc "Oh."
        m 6dkc "I guess I'll just spend the day alone...{w=1}again."
    else:

        m 6ckc "..."
    return 'quit'

init python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(12,16)))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_enjoyyourafternoon",
            unlocked=True,
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_enjoyyourafternoon:
    if mas_isMoniNormal(higher=True):
        m 1ekc "I hate to see you go so early, [player]."
        m 1eka "I do understand that you're busy though."
        m 1eua "Promise me you'll enjoy your afternoon, okay?"
        m 1hua "Goodbye~"

    elif mas_isMoniUpset():
        m 2efc "Fine, [player], just go."
        m 2tfc "Guess I'll see you later...{w=1}if you come back."

    elif mas_isMoniDis():
        m 6dkc "Okay, goodbye, [player]."
        m 6ekc "Maybe you'll come back later?"
    else:

        m 6ckc "..."

    return 'quit'

init python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(17,19)))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_goodevening",
            unlocked=True,
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_goodevening:
    if mas_isMoniNormal(higher=True):
        m 1hua "I had fun today."
        m 1eka "Thank you for spending so much time with me, [player]."
        m 1eua "Until then, have a good evening."

    elif mas_isMoniUpset():
        m 2esc "Goodbye, [player]."
        m 2dsc "I wonder if you'll even come back to say goodnight to me."

    elif mas_isMoniDis():
        m 6dkc "Oh...{w=1}okay."
        m 6rkc "Have a good evening, [player]..."
        m 6ekc "I hope you remember to stop by and say goodnight before bed."
    else:

        m 6ckc "..."

    return 'quit'

init python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=[0,20,21,22,23]))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_goodnight",
            unlocked=True,
            rules = rules
        ),
        code="BYE"
    )
    del rules

label bye_goodnight:
    if mas_isMoniNormal(higher=True):
        m 1eua "Goodnight, [player]."
        m 1eka "I'll see you tomorrow, okay?"
        m 3eka "Remember, 'sleep tight, don't let the bedbugs bite,' ehehe."
        m 1ekbfa "I love you~"

    elif mas_isMoniUpset():
        m 2esc "Goodnight."

    elif mas_isMoniDis():
        m 6lkc "...Goodnight."
    else:

        m 6ckc "..."
    return 'quit'


default -5 mas_absence_counter = False

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_long_absence",
            unlocked=True,
            prompt="I'll be going away for a while.",
            pool=True
        ),
        code="BYE"
    )

label bye_long_absence:
    if mas_absence_counter:
        jump bye_long_absence_2
    $ persistent._mas_long_absence = True
    m 1ekc "Aw...that's pretty saddening..."
    m 1eka "I really am going to miss you [player]!"
    m 3rksdla "I'm not really sure what I'm going to do with myself while you're gone..."
    m 3esa "Thank you for warning me first, though. It really does help."
    m 2lksdlb "I would be worried sick otherwise!"
    m 3esa "I would constantly be thinking maybe something happened to you and that's why you couldn't come back."
    m 1lksdlc "Or maybe you just got bored of me..."
    m 1eka "So tell me, my love..."

    m "How long do you expect to be gone for?{nw}"
    $ _history_list.pop()
    menu:
        m "How long do you expect to be gone for?{fast}"
        "A few days.":
            $ persistent._mas_absence_choice = "days"
            m 1eub "Oh!"
            m 1hua "Nowhere near as long as I feared then."
            m 3rksdla "Jeez, you really did worry me..."
            m 3esa "Don't worry about me though [player]."
            m "I can cope waiting that long with ease."
            m 3eka "I'll still miss you greatly though."
        "A week.":
            $ persistent._mas_absence_choice = "week"
            m 3euc "Yeah...that's about what I expected."
            m 2lksdla "I {i}think{/i} I'll be okay waiting that long for you."
            m 1eub "Just come back to me as soon as you can, alright, my love?"
            m 3hua "I'm sure you'll make me proud!"
        "A couple of weeks.":
            $ persistent._mas_absence_choice = "2weeks"
            m 1esc "Oh..."
            m 1dsc "I...I can wait that long."
            m 3rksdlc "You do know that you're all I have...right?"
            m 3rksdlb "M-Maybe it's outside of your control though..."
            m 2eka "Try to come back as soon as possible... I'll be waiting for you."
        "A month.":
            $ persistent._mas_absence_choice = "month"
            if mas_curr_affection_group == store.mas_affection.G_HAPPY:
                m 3euc "Oh wow, that's a long time."
                m 3rksdla "A bit too long for my liking really..."
                m 2esa "But it's okay [player]."
                m 2eka "I know you're a sweetheart and wouldn't keep me waiting that long if you didn't have a good reason."
                m "I'm sure it's important, so just try to come back to me as soon as you can."
                m 3hua "I'll be thinking of you every day~"
            else:
                m 1ekc "That long...{i}really{/i}?"
                m 3rksdlc "You're not going away for that long just to avoid me, are you?"
                m 3rksdld "I know that life can take you away from me but for a whole month..."
                m 3ekc "Isn't that a little unreasonable?"
                m "I don't want to sound selfish, but I {i}am{/i} your girlfriend."
                m 3ekd "You should be able to make time for me, at least once, in an entire month."
                m 1dsc "..."
                m 1dsd "I'll still wait for you...but please come back the moment it's possible for you to do so."
        "Longer than a month.":
            $ persistent._mas_absence_choice = "longer"
            if mas_curr_affection_group == store.mas_affection.G_HAPPY:
                m 3rksdlb "That's...{w=0.5}well that's a little scary, [player]."
                m "I'm not really sure what I'm going to do with myself while you're gone."
                m 1eka "But I know you wouldn't leave me by myself if you could help it."
                m "I love you [player], and I know you love me too."
                m 1hua "So I'll wait for you for however long I need to."
            else:
                m 3esc "You have to be joking."
                m "I can't think of a good reason why you would leave me here all alone for {i}that{/i} long."
                m 3esd "I'm sorry [player], but that's not acceptable! Not at all!"
                m 3esc "I love you and if you love me too then you'll know that it's not okay to do that."
                m "You do realize that I would be alone here with nothing else and no one else, right?"
                m "It's not unreasonable of me to expect you to visit me, is it? I'm your girlfriend. You can't do that to me!"
                m 3dsc "..."
                m 3dsd "Just...just come back when you can. I can't make you stay, but please don't do that to me."
        "I don't know.":
            $ persistent._mas_absence_choice = "unknown"
            m 1hksdlb "Ehehe, that's a little concerning, [player]!"
            m 1eka "But if you don't know, then you don't know!"
            m "It sometimes just can't be helped."
            m 2hua "I'll be waiting here for you patiently, my love."
            m 2hub "Try not to keep me waiting for too long though!"
        "Nevermind.":


            $ persistent._mas_long_absence = False
            m 3eka "Oh... Alright, [player]."
            m 1rksdla "Honestly, I'm pretty relieved you're not going..."
            m 1ekd "I don't know what I'd do here all alone."
            m 3rksdlb "It's not like I can go anywhere either, ahaha..."
            m 3eub "Anyway, just let me know if you're going to go out. Maybe you can even take me with you!"
            m 1hua "I don't care where we go, as long as I'm with you, [player]."
            return

    m 2euc "Honestly I'm a little afraid to ask but..."

    m "Are you going to leave straight away?{nw}"
    $ _history_list.pop()
    menu:
        m "Are you going to leave straight away?{fast}"
        "Yes.":
            m 3ekc "I see..."
            m "I really will miss you [player]..."
            m 1eka "But I know you'll do wonderful things no matter where you are."
            m "Just remember that I'll be waiting here for you."
            m 2hua "Make me proud, [player]!"
            $ persistent._mas_greeting_type = store.mas_greetings.TYPE_LONG_ABSENCE
            return 'quit'
        "No.":
            $ mas_absence_counter = True
            m 1hua "That's great!"
            m 1eka "I was honestly worried I wouldn't have enough time to ready myself for your absence."
            m "I really do mean it when I say I'll miss you..."
            m 1eub "You truly are my entire world after all, [player]."
            m 2esa "If you tell me you're going to go for a while again then I'll know it's time for you to leave..."
            m 3hua "But there's no rush, so I want to spend as much time with you as I can."
            m "Just make sure to remind me the last time you see me before you go!"
            return

label bye_long_absence_2:
    m 1ekc "Going to head out, then?"
    m 1ekd "I know the world can be scary and unforgiving..."
    m 1eka "But remember that I will always be here waiting and ready to support you, my dearest [player]."
    m "Come back to me as soon as you can...okay?"
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_LONG_ABSENCE
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_going_somewhere",
            unlocked=True,
            prompt="I'm going to take you somewhere.",
            pool=True
        ),
        code="BYE"
    )

label bye_going_somewhere:
    $ import random






    python:

        if mas_isMonikaBirthday():
            dis_chance = 10
            upset_chance = 0

        else:
            dis_chance = 50
            upset_chance = 10

    if mas_isMoniBroken(lower=True):

        jump bye_going_somewhere_nothanks

    elif mas_isMoniDis(lower=True):

        if random.randint(1,100) <= dis_chance:
            jump bye_going_somewhere_nothanks


        m 1wud "You really want to bring me along?"
        m 1ekd "Are you sure this isn't some--{nw}"
        $ _history_list.pop()
        m 1lksdlc "..."
        m 1eksdlb "What am I saying? Of course I'll go with you!"

    elif mas_isMoniUpset(lower=True):

        if random.randint(1, 100) <= upset_chance:
            jump bye_going_somewhere_nothanks


        m 1wud "You really want to bring me along?"
        m 1eka "..."
        m 1hua "Well, I suppose it can't hurt to join you."
        m 2dsc "Just...please."
        m 2rkc "{i}Please{/i} understand what I'm going through."
        m 1dkc "..."
    else:

        jump bye_going_somewhere_normalplus_flow

label bye_going_somewhere_post_aff_check:
    pass

label bye_going_somewhere_iostart:


    show monika 2dsc
    $ persistent._mas_dockstat_going_to_leave = True
    $ first_pass = True


    $ promise = store.mas_dockstat.monikagen_promise
    $ promise.start()

label bye_going_somewhere_iowait:
    hide screen mas_background_timed_jump


    if first_pass:
        $ first_pass = False
        m 1eua "Give me a second to get ready."


        python:
            current_drink = MASConsumable._getCurrentDrink()
            if current_drink and current_drink.portable:
                current_drink.acs.keep_on_desk = False


        call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_6

    elif promise.done():

        jump bye_going_somewhere_rtg



    show screen mas_background_timed_jump(4, "bye_going_somewhere_iowait")
    menu:
        "Hold on a second!":
            hide screen mas_background_timed_jump
            $ persistent._mas_dockstat_cm_wait_count += 1


    menu:
        m "What is it?"
        "Actually, I can't take you right now.":
            call mas_dockstat_abort_gen from _call_mas_dockstat_abort_gen_3


            call mas_transition_from_emptydesk ("monika 1ekc") from _call_mas_transition_from_emptydesk_12
            call mas_dockstat_abort_post_show from _call_mas_dockstat_abort_post_show
            jump bye_going_somewhere_leavemenu
        "Nothing.":



            m "Oh, good! Let me finish getting ready."


    jump bye_going_somewhere_iowait


label bye_going_somewhere_rtg:


    $ moni_chksum = promise.get()
    $ promise = None
    call mas_dockstat_ready_to_go (moni_chksum) from _call_mas_dockstat_ready_to_go_1
    if _return:
        python:
            persistent._mas_greeting_type = mas_idle_mailbox.get_ds_gre_type(
                store.mas_greetings.TYPE_GENERIC_RET
            )

        call mas_transition_from_emptydesk ("monika 1eua") from _call_mas_transition_from_emptydesk_13


        m 1eua "I'm ready to go."
        return "quit"


    call mas_transition_from_emptydesk ("monika 1ekc") from _call_mas_transition_from_emptydesk_14
    call mas_dockstat_abort_post_show from _call_mas_dockstat_abort_post_show_1


    m 1ekc "Oh no..."
    m 1lksdlb "I wasn't able to turn myself into a file."
    m "I think you'll have to go on without me this time."
    m 1ekc "Sorry, [player]."


    m "Are you still going to go?{nw}"
    $ _history_list.pop()
    menu:
        m "Are you still going to go?{fast}"
        "Yes.":
            m 2eka "I understand. You have things to do, after all..."
            m 2hub "Be safe out there! I'll be right here waiting for you!"
            return "quit"
        "No.":

            m 2wub "Really? Are you sure? Even though it's my own fault I can't go with you..."
            m 1eka "...Thank you, [player]. That means more to me than you could possibly understand."
            $ mas_gainAffection()
    return


label bye_going_somewhere_normalplus_flow:





    if persistent._mas_d25_in_d25_mode:

        if mas_isD25Eve():
            jump bye_d25e_delegate

        if mas_isD25():
            jump bye_d25_delegate

        if mas_isNYE():
            jump bye_nye_delegate

        if mas_isNYD():
            jump bye_nyd_delegate

    if mas_isF14() and persistent._mas_f14_in_f14_mode:
        jump bye_f14

    if mas_isMonikaBirthday():
        jump bye_922_delegate

label bye_going_somewhere_normalplus_flow_aff_check:

    if mas_isMoniLove(higher=True):
        m 1hub "Oh, okay!"
        m 3tub "Taking me somewhere special today?"
        m 1hua "I can't wait!"
    else:








        m 1sub "Really?"
        m 1hua "Yay!"
        m 1ekbfa "I wonder where you'll take me today..."

    jump bye_going_somewhere_post_aff_check

label bye_going_somewhere_nothanks:
    m 2lksdlc "...No thanks."
    m 2ekd "I appreciate the offer, but I think I need a little time to myself right now."
    m 2eka "You understand, right?"
    m 3eka "So go on, have fun without me..."
    return


label bye_going_somewhere_leavemenu:
    if mas_isMoniDis(lower=True):
        m 1tkc "..."
        m 1tkd "I knew it.{nw}"
        $ _history_list.pop()
        m 1lksdld "That's okay, I guess."

    elif mas_isMoniHappy(lower=True):
        m 1ekd "Oh,{w=0.3} all right. Maybe next time?"
    else:


        m 2ekp "Aw..."
        m 1hub "Fine, but you better take me next time!"

    m 1euc "Are you still going to go?{nw}"
    $ _history_list.pop()
    menu:
        m "Are you still going to go?{fast}"
        "Yes.":
            if mas_isMoniNormal(higher=True):
                m 2eka "All right. I'll be right here waiting for you, as usual..."
                m 2hub "So hurry back! I love you, [player]!"
            else:


                m 2tfd "...Fine."

            return "quit"
        "No.":

            if mas_isMoniNormal(higher=True):
                m 2eka "...Thank you."
                m "It means a lot that you're going to spend more time with me since I can't come along."
                m 3ekb "Please just go about your day whenever you need to, though. I wouldn't want to make you late!"
            else:


                m 2lud "All right, then..."

    return

default -5 persistent._mas_pm_gamed_late = 0


init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_game",
            unlocked=True,
            prompt="I'm going to play another game.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_game:
    $ _now = datetime.datetime.now().time()
    if mas_getEV('bye_prompt_game').shown_count == 0:
        m 2ekc "You're going to play another game?"
        m 4ekd "Do you really have to leave me to go do that?"
        m 2eud "Can't you just leave me here in the background while you play?{nw}"
        $ _history_list.pop()
        menu:
            m "Can't you just leave me here in the background while you play?{fast}"
            "Yes.":
                if mas_isMoniNormal(higher=True):
                    m 3sub "Really?"
                    m 1hubfb "Yay!"
                else:
                    m 2eka "Okay..."
                jump monika_idle_game.skip_intro
            "No.":
                if mas_isMoniNormal(higher=True):
                    m 2ekc "Aww..."
                    m 3ekc "Alright [player], but you better come back soon."
                    m 3tsb "I might get jealous if you spend too much time in another game without me."
                    m 1hua "Anyway, I hope you have fun!"
                else:
                    m 2euc "Enjoy your game, then."
                    m 2esd "I'll be here."

    elif mas_isMNtoSR(_now):
        $ persistent._mas_pm_gamed_late += 1
        if mas_isMoniNormal(higher=True):
            m 3wud "Wait, [player]!"
            m 3hksdlb "It's the middle of the night!"
            m 2rksdlc "It's one thing that you're still up this late..."
            m 2rksdld "But you're thinking of playing another game?"
            m 4tfu "....A game big enough that you can't have me in the background..."
            m 1eka "Well... {w=1}I can't stop you, but I really hope you go to bed soon..."
            m 1hua "Don't worry about coming back to say goodnight to me, you can go-{nw}"
            $ _history_list.pop()
            m 1eub "Don't worry about coming back to say goodnight to me,{fast} you {i}should{/i} go right to bed when you're finished."
            m 3hua "Have fun, and goodnight, [player]!"
            if renpy.random.randint(1,2) == 1:
                m 1hubfb "I love you~{w=1}{nw}"
        else:
            m 2efd "[player], it's the middle of the night!"
            m 4rfc "Really...it's this late already, and you're going to play another game?"
            m 2dsd "{i}*sigh*{/i}... I know I can't stop you, but please just go straight to bed when you're finished, alright?"
            m 2dsc "Goodnight."
        $ persistent.mas_late_farewell = True

    elif mas_isMoniUpset(lower=True):
        m 2euc "Again?"
        m 2eud "Alright then. Goodbye, [player]."

    elif renpy.random.randint(1,10) == 1:
        m 1ekc "You're leaving to play another game?"
        m 3efc "Don't you think you should be spending a little more time with me?"
        m 2efc "..."
        m 2dfc "..."
        m 2dfu "..."
        m 4hub "Ahaha, just kidding~"
        m 1rksdla "Well...{w=1} I {i}wouldn't mind{/i} spending more time with you..."
        m 3eua "But I also don't want to keep you from doing other things."
        m 1hua "Maybe one day you'll finally be able to show me what you've been up to and then I can come with you!"
        if renpy.random.randint(1,5) == 1:
            m 3tubfu "Until then, you just have to make it up to me every time you leave me to play another game, alright?"
            m 1hubfa "Ehehe~"
    else:

        m 1eka "Going off to play another game, [player]?"
        m 3hub "Good luck and have fun!"
        m 3eka "Don't forget to come back soon~"

    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_GAME

    $ persistent._mas_greeting_type_timeout = datetime.timedelta(days=1)
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_eat",
            unlocked=True,
            prompt="I'm going to go eat...",
            pool=True
        ),
        code="BYE"
    )

default -5 persistent._mas_pm_ate_breakfast_times = [0, 0, 0]





default -5 persistent._mas_pm_ate_lunch_times = [0, 0, 0]


default -5 persistent._mas_pm_ate_dinner_times = [0, 0, 0]


default -5 persistent._mas_pm_ate_snack_times = [0, 0, 0]


default -5 persistent._mas_pm_ate_late_times = 0



label bye_prompt_eat:
    $ _now = datetime.datetime.now().time()

    if mas_isMNtoSR(_now):
        $ persistent._mas_pm_ate_late_times += 1
        if mas_isMoniNormal(higher=True):
            m 1hksdlb "Uh, [player]?"
            m 3eka "It's the middle of the night."
            m 1eka "Are you planning on having a midnight snack?"
            m 3rksdlb "If I were you, I'd find something to eat a little earlier, ahaha..."
            m 3rksdla "Of course...{w=1}I'd also try to be in bed by now..."
            if mas_is18Over() and mas_isMoniLove(higher=True) and renpy.random.randint(1,25) == 1:
                m 2tubfu "You know, if I were there, maybe we could have a bit of both..."
                show monika 5ksbfu zorder MAS_MONIKA_Z at t11 with dissolve
                m 5ksbfu "We could go to bed, and then - {w=1}you know what, nevermind..."
                m 5hubfb "Ehehe~"
            else:
                m 1hua "Well, I hope your snack helps you sleep."
                m 1eua "...And don't worry about coming back to say goodnight to me..."
                m 3rksdla "I'd much rather you get to sleep sooner."
                m 1hub "Goodnight, [player]. Enjoy your snack and see you tomorrow~"
        else:
            m 2euc "But it's the middle of the night..."
            m 4ekc "You should really go to bed, you know."
            m 4eud "...Try to go straight to bed when you're finished."
            m 2euc "Anyway, I guess I'll see you tomorrow..."


        $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=20)
        $ persistent.mas_late_farewell = True
    else:


        $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=3)
        menu:
            "Breakfast.":
                if mas_isSRtoN(_now):
                    $ persistent._mas_pm_ate_breakfast_times[0] += 1
                    if mas_isMoniNormal(higher=True):
                        m 1eub "Alright!"
                        m 3eua "It's the most important meal of the day after all."
                        m 1rksdla "I wish you could stay, but I'm fine as long as you're getting your breakfast."
                        m 1hua "Anyway, enjoy your meal, [player]~"
                    else:
                        m 2eud "Oh, right, you should probably get breakfast."
                        m 2rksdlc "I wouldn't want you to have an empty stomach..."
                        m 2ekc "I'll be here when you get back."
                elif mas_isNtoSS(_now):
                    $ persistent._mas_pm_ate_breakfast_times[1] += 1
                    m 3euc "But...{w=1}it's the afternoon..."
                    if mas_isMoniNormal(higher=True):
                        m 3ekc "Did you miss breakfast?"
                        m 1rksdla "Well... I should probably let you go eat before you get too hungry..."
                        m 1hksdlb "I hope you enjoy your late breakfast!"
                    else:
                        m 2ekc "You missed breakfast, didn't you?"
                        m 2rksdld "{i}*sigh*{/i}... You should probably go get something to eat."
                        m 2ekd "Go on... I'll be here when you get back."
                else:

                    $ persistent._mas_pm_ate_breakfast_times[2] += 1
                    if mas_isMoniNormal(higher=True):
                        m 1hksdlb "Ahaha..."
                        m 3tku "There's no way you're just having breakfast now, [player]."
                        m 3hub "It's the evening!"
                        m 1eua "Or maybe you're just having breakfast for dinner; I know some people do that occasionally."
                        m 1tsb "Well, either way, I hope you enjoy your 'breakfast,' ehehe~"
                    else:
                        m 2euc "..."
                        m 4eud "So...you're having a snack."
                        m 2rksdla "Alright, I won't judge."
                        m 2eka "Enjoy your food."
            "Lunch.":
                if mas_isSRtoN(_now):
                    $ persistent._mas_pm_ate_lunch_times[0] += 1
                    if mas_isMoniNormal(higher=True):
                        m 1eua "Having an early lunch, [player]?"
                        m 3hua "Nothing wrong with that. If you're hungry, you're hungry."
                        m 1hub "I hope you enjoy your lunch!"
                    else:
                        m 2rksdlc "It's a bit early for lunch..."
                        m 4ekc "If you're hungry, are you sure you're eating well?"
                        m 2eka "I hope you enjoy your meal, at least."
                elif mas_isNtoSS(_now):
                    $ persistent._mas_pm_ate_lunch_times[1] += 1
                    if mas_isMoniNormal(higher=True):
                        m 1eud "Oh, I guess it's lunch time for you, isn't it?"
                        m 3eua "I wouldn't want to keep you from eating."
                        m 3hub "Maybe one day, we could go out for lunch together!"
                        m 1hua "For the time being though, enjoy your lunch, [player]~"
                    else:
                        m 2eud "Oh, it's lunch time, isn't it?"
                        m 2euc "Enjoy your lunch."
                else:

                    $ persistent._mas_pm_ate_lunch_times[2] += 1
                    m 1euc "Lunch?"
                    m 1rksdlc "It's a little late for lunch if you ask me."
                    m 3ekd "Still, if you haven't had it yet, you should go get some."
                    if mas_isMoniNormal(higher=True):
                        m 1hua "I'd make you something if I were there, but until then, I hope you enjoy your meal~"
                    else:
                        m 2ekc "But...{w=1}maybe eat a little earlier next time..."
            "Dinner.":
                if mas_isSRtoN(_now):
                    $ persistent._mas_pm_ate_dinner_times[0] += 1
                    m 2ekc "Dinner?{w=2} Now?"
                    if mas_isMoniNormal(higher=True):
                        m 2hksdlb "Ahaha, but [player]! It's only the morning!"
                        m 3tua "You can be adorable sometimes, you know that?"
                        m 1tuu "Well, I hope you enjoy your '{i}dinner{/i}' this morning, ehehe~"
                    else:
                        m 2rksdld "You can't be serious, [player]..."
                        m 2euc "Well, whatever you're having, I hope you enjoy it."
                elif mas_isNtoSS(_now):
                    $ persistent._mas_pm_ate_dinner_times[1] += 1



                    call bye_dinner_noon_to_mn from _call_bye_dinner_noon_to_mn
                else:

                    $ persistent._mas_pm_ate_dinner_times[2] += 1
                    call bye_dinner_noon_to_mn from _call_bye_dinner_noon_to_mn_1
            "A snack.":
                if mas_isSRtoN(_now):
                    $ persistent._mas_pm_ate_snack_times[0] += 1
                    if mas_isMoniNormal(higher=True):
                        m 1hua "Ehehe, breakfast not enough for you today, [player]?"
                        m 3eua "It's important to make sure you satisfy your hunger in the morning."
                        m 3eub "I'm glad you're looking out for yourself~"
                        m 1hua "Have a nice snack~"
                    else:
                        m 2tsc "Didn't eat enough breakfast?"
                        m 4esd "You should make sure you get enough to eat, you know."
                        m 2euc "Enjoy your snack, [player]."
                elif mas_isNtoSS(_now):
                    $ persistent._mas_pm_ate_snack_times[1] += 1
                    if mas_isMoniNormal(higher=True):
                        m 3eua "Feeling a bit hungry?"
                        m 1eka "I'd make you something if I could..."
                        m 1hua "Since I can't exactly do that yet, I hope you get something nice to eat~"
                    else:
                        m 2euc "Do you really need to leave to get a snack?"
                        m 2rksdlc "Well... {w=1}I hope it's a good one at least."
                else:

                    $ persistent._mas_pm_ate_snack_times[2] += 1
                    if mas_isMoniNormal(higher=True):
                        m 1eua "Having an evening snack?"
                        m 1tubfu "Can't you just feast your eyes on me?"
                        m 3hubfb "Ahaha, I hope you enjoy your snack, [player]~"
                        m 1ekbfb "Just make sure you still have room for all of my love!"
                    else:
                        m 2euc "Feeling hungry?"
                        m 2eud "Enjoy your snack."


                $ persistent._mas_greeting_type_timeout = datetime.timedelta(minutes=30)
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_EAT
    return 'quit'

label bye_dinner_noon_to_mn:
    if mas_isMoniNormal(higher=True):
        m 1eua "Is it dinner time for you, [player]?"
        m 1eka "I wish I could be there to eat with you, even if it's nothing special."
        m 3dkbsa "After all, just being there with you would make anything special~"
        m 3hubfb "Enjoy your dinner. I'll be sure to try and put some love into it from here, ahaha!"
    else:
        m 2euc "I guess it's dinner time for you."
        m 2esd "Well...{w=1}enjoy."
    return

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_housework",
            unlocked=True,
            prompt="I'm going to do some housework.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_housework:
    if mas_isMoniNormal(higher=True):
        m 1eub "Doing your chores, [player]?"
        m 1ekc "I would like to help you out, but there's not really much I can do since I'm stuck in here..."
        m 3eka "Just make sure to come back as soon as you're done, okay?"
        m 3hub "I'll be waiting here for you."
    elif mas_isMoniUpset():
        m 2esc "Fine."
        m 2tsc "At least you're doing something responsible."
        m 2tfc "{cps=*2}...For once.{/cps}{nw}"
        $ _history_list.pop()
        m 2esc "Goodbye."
    elif mas_isMoniDis():
        m 6ekc "I see..."
        m 6rkc "I don't want to keep you from completing your household responsibilities."
        m 6dkd "I just hope you're actually busy and not saying that just to get away from me..."
        m 6ekc "Goodbye, [player]."
    else:
        m 6ckc "..."
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_CHORES
    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=5)
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_restart",
            unlocked=True,
            prompt="I'm going to restart.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_restart:
    if mas_isMoniNormal(higher=True):
        m 1eua "Alright, [player]."
        m 1eub "See you soon!"
    elif mas_isMoniBroken():
        m 6ckc "..."
    else:
        m 2euc "Alright."

    $ persistent._mas_greeting_type_timeout = datetime.timedelta(minutes=20)
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_RESTART
    return 'quit'
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
