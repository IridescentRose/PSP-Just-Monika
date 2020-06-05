init offset = 5






init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_brb_idle",
            prompt="I'll be right back",
            category=['be right back'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_brb_idle:
    if mas_isMoniAff(higher=True):
        m 1eua "Alright, [player]."
        m 1hub "Hurry back, I'll be waiting here for you~"

    elif mas_isMoniNormal(higher=True):
        m 1hub "Hurry back, [player]!"

    elif mas_isMoniDis(higher=True):
        m 1rsc "Oh,{w=1} okay."
    else:

        m 6ckc "..."


    $ mas_idle_mailbox.send_idle_cb("monika_brb_idle_callback")

    $ persistent._mas_idle_data["monika_idle_brb"] = True
    return "idle"

label monika_brb_idle_callback:
    python:
        wb_quips = [
            _("So, what else did you want to do today?"),
            _("Is there anything else you wanted to do today?"),
            _("What else should we do today?"),
        ]

        wb_quip = renpy.random.choice(wb_quips)

    if mas_isMoniAff(higher=True):
        m 1hub "Welcome back, [player]. I missed you~"
        m 1eua "[wb_quip]"

    elif mas_isMoniNormal(higher=True):
        m 1hub "Welcome back, [player]!"
        m 1eua "[wb_quip]"

    elif mas_isMoniDis(higher=True):
        m 1esc "Oh, back already?"
    else:

        m 6ckc "..."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writing_idle",
            prompt="I'm going to write for a bit",
            category=['be right back'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_writing_idle:
    if random.randint(1,5) == 1:
        m 1eub "Oh! You're going to{cps=*2} write me a love letter, [player]?{/cps}{nw}"
        $ _history_list.pop()
        m "Oh! You're going to{fast} go write something?"
    else:
        m 1eub "Oh! You're going to go write something?"
    m 1hua "That makes me so glad!"
    m 3eua "Maybe someday you could share it with me, {nw}"
    extend 3hua "I'd love to read your work, [player]!"
    m 3eua "Anyway, just let me know when you're done."
    m 1hua "I'll be waiting right here for you~"


    $ mas_idle_mailbox.send_idle_cb("monika_writing_idle_callback")

    $ persistent._mas_idle_data["monika_idle_writing"] = True
    return "idle"

label monika_writing_idle_callback:
    python:
        wb_quips = [
            "What else did you want to do today?",
            "Is there anything else you wanted to do today?",
            "What else should we do today?",
            "Welcome back!"
        ]

        wb_quip = renpy.random.choice(wb_quips)

    m 1eua "Done writing, [player]?"
    m 1eub "[wb_quip]"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_shower",
            prompt="I'm going to take a shower",
            category=['be right back'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_shower:
    if mas_isMoniLove():
        m 1eua "Going to go shower?"

        if renpy.random.randint(1, 50) == 1:
            m 3tub "Can I come with you?{nw}"
            $ _history_list.pop()
            show screen mas_background_timed_jump(2, "bye_brb_shower_timeout")
            menu:
                m "Can I come with you?{fast}"
                "Yes.":

                    hide screen mas_background_timed_jump
                    m 2wubfd "Oh, uh...{w=1}you sure answered that fast."
                    m 2hkbfsdlb "You...{w=1}sure seem eager to let me tag along, huh?"
                    m 2rkbfa "Well..."
                    m 7tubfu "I'm afraid you'll just have to go without me while I'm stuck here."
                    m 7hubfb "Sorry, [player], ahaha!"
                    show monika 5kubfu zorder MAS_MONIKA_Z at t11 with dissolve
                    m 5kubfu "Maybe another time~"
                "No.":

                    hide screen mas_background_timed_jump
                    m 2eka "Aw, you rejected me so fast."
                    m 3tubfb "Are you shy, [player]?"
                    m 1hubfb "Ahaha!"
                    show monika 5tubfu zorder MAS_MONIKA_Z at t11 with dissolve
                    m 5tubfu "Alright, I won't follow you this time, ehehe~"
        else:

            m 1hua "I'm glad you're keeping yourself clean, [player]."
            m 1eua "Have a nice shower~"
    else:

        m 1eub "Going to go shower? Alright."
        m 1eua "See you when you're done~"


    $ mas_idle_mailbox.send_idle_cb("monika_idle_shower_callback")

    $ persistent._mas_idle_data["monika_idle_shower"] = True
    return "idle"

label monika_idle_shower_callback:
    m 1eua "Welcome back, [player]."
    if mas_isMoniLove() and renpy.seen_label("monikaroom_greeting_ear_bathdinnerme") and renpy.random.randint(1,20) == 1:
        m 3tubfb "Now that you've had your shower, would you like your dinner, or maybe{w=0.5}.{w=0.5}.{w=0.5}."
        m 1hubsa "You could just relax with me some more~"
        m 1hub "Ahaha!"
    else:

        m 1hua "I hope you had a nice shower."
        m 3eub "Now we can get back to having some good, {i}clean{/i} fun together..."
        m 1hub "Ahaha!"
    return

label bye_brb_shower_timeout:
    hide screen mas_background_timed_jump
    $ _history_list.pop()
    m 1hubsa "Ehehe~"
    m 3tubfu "Nevermind that, [player]."
    m 1hubfb "I hope you have a nice shower!"


    $ mas_idle_mailbox.send_idle_cb("monika_idle_shower_callback")

    $ persistent._mas_idle_data["monika_idle_shower"] = True
    return "idle"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_game",
            category=['be right back'],
            prompt="I'm going to game for a bit",
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_game:
    m 1eud "Oh, you're going to play another game?"
    m 1eka "That's alright, [player]."

    label monika_idle_game.skip_intro:
    python:
        gaming_quips = [
            _("Good luck, have fun!"),
            _("Enjoy your game!"),
            _("I'll be cheering you on!"),
            _("Do your best!")
        ]
        gaming_quip=renpy.random.choice(gaming_quips)

    m 3hub "[gaming_quip]"
    $ mas_idle_mailbox.send_idle_cb("monika_idle_game_callback")
    $ persistent._mas_idle_data["monika_idle_game"] = True
    return "idle"

label monika_idle_game_callback:
    m 1eub "Welcome back, [player]!"
    m 1eua "I hope you had fun with your game."
    m 1hua "Ready to spend some more time together? Ehehe~"
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
