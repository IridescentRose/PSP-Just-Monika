

default persistent._mas_poems_seen = dict()

init python in mas_poems:
    import store
    poem_map = dict()

    poem_sort_key = lambda x:x.category

    paper_cat_map = {
        "f14": "mod_assets/poem_assets/poem_vday.jpg",
        "d25": "mod_assets/poem_assets/poem_d25.png",
        "ff": "mod_assets/poem_assets/poem_finalfarewell.png"
    }

    author_font_map = {
        "monika": "monika_text",
        "chibika": "chibika_note_text"
    }


    if store.persistent._mas_player_bday is not None:
        paper_cat_map["pbday"] = "mod_assets/poem_assets/poem_pbday_" + str(store.persistent._mas_player_bday.month) + ".png"

    def hasUnlockedPoems():
        """
        Checks if we have any poems that we've unlocked.
        """
        return len(store.persistent._mas_poems_seen) > 0

init 11 python in mas_poems:
    import store

    def getPoemsByCategory(category, unseen=False):
        """
        Returns a list of poems by the category provided

        IN:
            category:
                category to search for

            unseen:
                whether or not we only want unseen poems

        OUT:
            A list of poems based on the specifications above
        """
        
        
        if unseen:
            return [
                poem
                for poem in poem_map.itervalues()
                if not poem.is_seen() and poem.category == category
            ]
        
        
        return [
            poem
            for poem in poem_map.itervalues()
            if poem.category == category
        ]

    def getSeenPoems():
        """
        Returns a list of all seen poems ordered by category
        """
        return sorted([
            poem
            for poem in poem_map.itervalues()
            if poem.is_seen()
        ], key=poem_sort_key)

    def getUnseenPoems():
        """
        Returns a list of all unseen poems ordered by category
        """
        return sorted([
            poem
            for poem in poem_map.itervalues()
            if not poem.is_seen()
        ], key=poem_sort_key)

    def getPoem(poem_id):
        """
        Gets a poem by id

        IN:
            poem_id - poem id of the poem to get

        OUT:
            MASPoem if there's a poem with the id
            None if no poem with the id exists
        """
        return poem_map.get(poem_id, None)

    def getSeenPoemsMenu():
        """
        Gets a list of seen poems in scrollable menu format

        OUT:
            A list of seen poems in the format for a mas gen scrollable menu
        """
        return [
            (poem.prompt, poem, False, False)
            for poem in poem_map.itervalues()
            if poem.is_seen()
        ]

    def getRandomPoem(category,unseen=True):
        """
        Gets a random poem from the specified category
        IN:
            category:
                category to search for

            unseen:
                whether or not we only want unseen poems
                defaults to True

        OUT:
            A random poem
        """
        unseen_poem_amt = len(getPoemsByCategory(category, unseen=True))
        total_poem_amt = len(getPoemsByCategory(category, unseen=False))
        sel_poem_len = total_poem_amt-1
        
        if unseen:
            if unseen_poem_amt > 0:
                sel_poem_len = unseen_poem_amt-1
            else:
                unseen = False
        poem_num = renpy.random.randint(0, sel_poem_len)
        
        return getPoemsByCategory(category, unseen=unseen)[poem_num]

init 10 python:
    class MASPoem:
        def __init__(
            self,
            poem_id,
            category,
            prompt,
            title="",
            text="",
            author="monika",
        ):
            """
            MASPoem constructor

            Similar to the Poem class from DDLC, but excludes the yuri variables and adds a poem id property.


            poem_id:
                identifier for the poem.
                (NOTE: Must be unique)

            category:
                category for the poem is under (So we can get poems by category)

            prompt:
                prompt for this poem (So it can be viewed by a scrollable menu)

            title:
                poem title (supports renpy substitution)

            text:
                poem contents (supports renpy substitution)

            author:
                poem author
                (Default: monika)
            """
            if poem_id in store.mas_poems.poem_map:
                raise Exception ("poem_id {0} already exists in the poem map.".format(poem_id))
            
            self.poem_id=poem_id
            self.category=category
            self.prompt=prompt
            self.title=title
            self.text=text
            self.author=author
            
            
            store.mas_poems.poem_map[poem_id] = self
        
        def is_seen(self):
            """
            Checks if the poem is seen

            OUT:
                boolean:
                    - True if poem was seen before
                    - False otherwise
            """
            return self.poem_id in store.persistent._mas_poems_seen
        
        def get_shown_count(self):
            """
            Gets the shown count of the poem

            OUT:
                integer:
                    - The amount of times this poem was seen
            """
            return store.persistent._mas_poems_seen.get(self.poem_id, 0)













label mas_showpoem(poem=None, paper=None, background_action_label=None):

    if poem == None:
        return

    $ is_maspoem = isinstance(poem, MASPoem)
    if not paper:
        if is_maspoem:
            $ paper = mas_poems.paper_cat_map.get(poem.category, "paper")
        else:
            $ paper = "paper"


    play sound page_turn

    window hide
    $ renpy.game.preferences.afm_enable = False


    show screen mas_generic_poem(poem, paper=paper, _styletext=mas_poems.author_font_map.get(poem.author, "monika_text"))

    with Dissolve(1)


    if background_action_label and renpy.has_label(background_action_label):
        call expression background_action_label from _call_expression_6


    $ pause()


    hide screen mas_generic_poem


    with Dissolve(.5)
    window auto




    if is_maspoem and poem.prompt:
        if poem.poem_id in persistent._mas_poems_seen:
            $ persistent._mas_poems_seen[poem.poem_id] += 1
        else:
            $ persistent._mas_poems_seen[poem.poem_id] = 1
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_showpoem",
            prompt="Can I read one of your poems again?",
            category=["literature"],
            pool=True,
            unlocked=True,
            action=EV_ACT_UNLOCK,
            rules={"no unlock": None},
            aff_range=(mas_aff.ENAMORED,None)
        )
    )


label monika_showpoem:
    show monika 1eua at t21
    python:

        poems_list = [
            ("Hole in Wall (Part 1)", poem_m1, False, False),
            ("Hole in Wall (Part 2)", poem_m21, False, False),
            ("Save Me", poem_m2, False, False),
            ("The Lady Who Knows Everything", poem_m3, False, False),
            ("Happy End", poem_m4, False, False)
        ]

        ret_back = ("Nevermind", False, False, False, 20)

        poems_list.extend(sorted(mas_poems.getSeenPoemsMenu()))

        renpy.say(m, "Which poem would you like to read?", interact=False)

    call screen mas_gen_scrollable_menu(poems_list, mas_ui.SCROLLABLE_MENU_TXT_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, ret_back)

    $ _poem = _return

    if not _poem:
        return "prompt"

    show monika 3hua at t11
    m 3hua "Alright!"
    call mas_showpoem (_poem) from _call_mas_showpoem_9
    m 3eka "I hope you liked it, [player]."
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
