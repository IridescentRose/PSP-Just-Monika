

default persistent._mas_dark_mode_enabled = False


default persistent._mas_auto_mode_enabled = False

init -1 python in mas_globals:

    dark_mode = None


    change_textbox = True


    button_text_hover_color = None
    button_text_idle_color = None

init -201 python in mas_ui:

    dark_suffix = "_dark"




    CNF_BG = "gui/overlay/confirm.png"


    SEL_SB_FRAME = "mod_assets/frames/black70_pinkborder100_5px.png"

init -200 python in mas_ui:

    style_stash = {}

    dark_button_text_idle_color = "#FD5BA2"
    dark_button_text_hover_color = "#FFABD8"
    dark_button_text_insensitive_color = "#8C8C8C"

    light_button_text_idle_color = "#000"
    light_button_text_hover_color = "#fa9"
    light_button_text_insensitive_color = "#8C8C8C"




    cm_bg = CNF_BG


    sel_sb_frame = SEL_SB_FRAME

    SCROLLABLE_MENU_X = 680
    SCROLLABLE_MENU_Y = 40
    SCROLLABLE_MENU_W = 560
    SCROLLABLE_MENU_H = 640
    SCROLLABLE_MENU_TXT_H = 500
    SCROLLABLE_MENU_XALIGN = -0.05

    SCROLLABLE_MENU_AREA = (SCROLLABLE_MENU_X, SCROLLABLE_MENU_Y, SCROLLABLE_MENU_W, SCROLLABLE_MENU_H)
    SCROLLABLE_MENU_TXT_AREA = (SCROLLABLE_MENU_X, SCROLLABLE_MENU_Y, SCROLLABLE_MENU_W, SCROLLABLE_MENU_TXT_H)


init python:
    import store.mas_globals as mas_globals
    import store.mas_ui as mas_ui

    def mas_getTimeFile(filestring):
        """
        Returns the filestring pointing to the right asset for day/night

        IN:
            the DAY variant of the image file needed

        RETURNS:
            filestring pointing to the right path
        """
        
        
        if not mas_globals.dark_mode:
            return filestring
        
        
        else:
            
            if '.' in filestring:
                extension = filestring[filestring.index('.'):]
                path = filestring[:filestring.index('.')]
                return path + "_d" + extension
            
            return filestring


    def mas_swapStyle(base_name, dark_name, morning_flag):
        """
        Swaps the single style between default and dark variants.

        IN:
            morning_flag - Light/dark mode switch
        """
        if base_name not in mas_ui.style_stash:
            mas_ui.style_stash[base_name] = getattr(style, base_name)
        
        if morning_flag:
            stashed_style = mas_ui.style_stash[base_name]
            setattr(style, base_name, mas_ui.style_stash[base_name])
        else:
            dark_style = getattr(style, dark_name)
            setattr(style, base_name, dark_style)

    def mas_hasDarkStyle(style_name):
        """
        Check if selected style has a dark alternative.
        """
        dark_style_name = style_name + mas_ui.dark_suffix
        
        for other_tuple in renpy.style.styles:
            other_name = other_tuple[0]
            if other_name == dark_style_name:
                return True
        
        return False

    def mas_isDarkStyle(style_name):
        """
        Check if selected style is a dark style.
        """
        return style_name.endswith(mas_ui.dark_suffix)

    def mas_isTextDarkStyle(style_name):
        """
        Check if selected style is a text_dark style.
        """
        text_dark_suffix = "_text" + mas_ui.dark_suffix
        return style_name.endswith(text_dark_suffix)

    def mas_darkMode(morning_flag=False):
        """
        Swaps all styles to dark/light mode provided on the input

        IN:
            morning_flag - if True, light mode, if False, dark mode
        """
        
        
        new_aliases = {}
        
        for style_tuple, style_ptr in renpy.style.styles.iteritems():
            style_name = style_tuple[0]
            if mas_isTextDarkStyle(style_name):
                text_dark_suffix = "_text" + mas_ui.dark_suffix
                suffix_len = len(text_dark_suffix)
                alias_name = style_name[:-suffix_len] + mas_ui.dark_suffix + "_text"
                if not style.exists(alias_name):
                    new_aliases[alias_name] = style_ptr
        
        for alias_name, alias_style_ptr in new_aliases.iteritems():
            setattr(style, alias_name, alias_style_ptr)
        
        
        for style_tuple in renpy.style.styles.keys():
            style_name = style_tuple[0]
            if not mas_isDarkStyle(style_name) and mas_hasDarkStyle(style_name):
                dark_style_name = style_name + mas_ui.dark_suffix
                mas_swapStyle(style_name, dark_style_name, morning_flag)
        
        if not morning_flag:
            
            mas_globals.dark_mode = True
            
            mas_globals.button_text_idle_color = mas_ui.dark_button_text_idle_color
            mas_globals.button_text_hover_color = mas_ui.dark_button_text_hover_color
            mas_globals.button_text_insensitive_color = mas_ui.dark_button_text_insensitive_color
            
            
            if mas_globals.change_textbox:
                style.say_window = style.window_dark
        
        else:
            
            mas_globals.dark_mode = False
            
            mas_globals.button_text_idle_color = mas_ui.light_button_text_idle_color
            mas_globals.button_text_hover_color = mas_ui.light_button_text_hover_color
            mas_globals.button_text_insensitive_color = mas_ui.light_button_text_insensitive_color
            
            
            if mas_globals.change_textbox:
                style.say_window = style.window
        
        
        mas_ui.cm_bg = mas_getTimeFile(mas_ui.CNF_BG)
        mas_ui.sel_sb_frame = mas_getTimeFile(mas_ui.SEL_SB_FRAME)
        
        
        mas_globals.change_textbox = True
        
        style.rebuild()


init python in mas_settings:
    _persistent = renpy.game.persistent
    import store
    def _auto_mode_toggle():
        """
        Handles the toggling of fields so the menu options become mutually exclusive
        """
        
        if _persistent._mas_auto_mode_enabled:
            _persistent._mas_auto_mode_enabled = False
            if store.mas_current_background.isFltNight():
                store.mas_darkMode(True)
        
        
        else:
            _persistent._mas_auto_mode_enabled = True
            _persistent._mas_dark_mode_enabled = False

    def _dark_mode_toggle():
        """
        Handles the toggling of fields so the menu options become mutually exclusive
        """
        if _persistent._mas_dark_mode_enabled:
            _persistent._mas_dark_mode_enabled = False
        
        else:
            _persistent._mas_dark_mode_enabled = True
            _persistent._mas_auto_mode_enabled = False
        renpy.restart_interaction()




style generic_button_base:
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style generic_button_light is generic_button_base:
    background Frame("mod_assets/buttons/generic/[prefix_]bg.png", Borders(5, 5, 5, 5), tile=False)

style generic_button_dark is generic_button_base:
    background Frame("mod_assets/buttons/generic/[prefix_]bg_d.png", Borders(5, 5, 5, 5), tile=False)

style generic_button_text_base:
    font gui.default_font
    size gui.text_size
    align (0.5, 0.1)
    outlines []

style generic_button_text_light is generic_button_text_base:
    idle_color mas_ui.light_button_text_idle_color
    hover_color mas_ui.light_button_text_hover_color
    insensitive_color mas_ui.light_button_text_insensitive_color

style generic_button_text_dark is generic_button_text_base:
    idle_color mas_ui.dark_button_text_idle_color
    hover_color mas_ui.dark_button_text_hover_color
    insensitive_color mas_ui.dark_button_text_insensitive_color



image menu_bg:
    topleft
    ConditionSwitch(
        "not mas_globals.dark_mode", "gui/menu_bg.png",
        "mas_globals.dark_mode", "gui/menu_bg_d.png")
    menu_bg_move

image game_menu_bg:
    topleft
    ConditionSwitch(
        "not mas_globals.dark_mode", "gui/menu_bg.png",
        "mas_globals.dark_mode", "gui/menu_bg_d.png")
    menu_bg_loop

image menu_nav:
    ConditionSwitch(
        "not mas_globals.dark_mode", "gui/overlay/main_menu.png",
        "mas_globals.dark_mode", "gui/overlay/main_menu_d.png")
    menu_nav_move

init -1 python:



    gui.default_font = FontGroup().add(
        "mod_assets/font/SourceHanSansK-Regular.otf", 0xac00, 0xd7a3 
    ).add(
        "mod_assets/font/SourceHanSansSC-Regular.otf", 0x4e00, 0x9faf 
    ).add(
        "mod_assets/font/mplus-2p-regular.ttf", 0x3000, 0x4dff  
    ).add(
        "gui/font/Aller_Rg.ttf", 0x0000, 0xffff 
    )
    gui.interface_font = gui.default_font
    gui.button_text_font = gui.default_font
    gui.choice_button_text_font = gui.default_font

init -1 python in mas_ui:
    import store

    music_menu_font = store.FontGroup().add( 
        "mod_assets/font/SourceHanSansK-Regular.otf", 0xac00, 0xd7a3 
    ).add(
        "mod_assets/font/SourceHanSansSC-Regular.otf", 0x4e00, 0x9faf 
    ).add(
        "mod_assets/font/mplus-2p-regular.ttf", 0x0000, 0xffff  
    )
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
