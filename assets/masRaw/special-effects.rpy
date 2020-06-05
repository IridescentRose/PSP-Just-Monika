


image yuri dragon2:
    parallel:
        "yuri/dragon1.png"
        0.01
        "yuri/dragon2.png"
        0.01
        repeat

image blood splatter1:
    size (1, 1)
    truecenter
    Blood("blood_particle",dripTime=0.5, burstSize=150, burstSpeedX=400.0, burstSpeedY=400.0, numSquirts=15, squirtPower=400, squirtTime=2.0).sm

image k_rects_eyes1:
    RectCluster(Solid("#000"), 4, 15, 5).sm
    pos (580, 270)
    size (20, 25)
    8.0

image k_rects_eyes2:
    RectCluster(Solid("#000"), 4, 15, 5).sm
    pos (652, 264)
    size (20, 25)
    8.0

image natsuki mas_ghost:
    "natsuki ghost2"
    parallel:
        easeout 0.25 zoom 4.5 yoffset 1200
    parallel:
        ease 0.025 xoffset -20
        ease 0.025 xoffset 20
        repeat
    0.25

image mujina:
    "mod_assets/other/mujina.png"
    zoom 1.25
    parallel:
        easeout 0.5 zoom 4.5 yoffset 1200
    0.5

image mas_lightning:
    "mod_assets/other/thunder.png"
    alpha 1.0

    choice:
        block:
            0.05
            alpha 0.0
            0.05
            alpha 1.0
            repeat 3
    choice:

        block:
            0.05
            alpha 0.0
            0.05
            alpha 1.0
            repeat 2
    choice:

        0.05

    parallel:
        easeout 2.8 alpha 0.0
    3.0
    Null()

image mas_lightning_s_bg = LiveComposite(
    (1280, 720),
    (0, 0), "mod_assets/other/thunder.png",
    (30, 200), "mod_assets/other/tree_sil.png"
)

image mas_lightning_s:
    "mas_lightning_s_bg"
    alpha 1.0
    block:

        0.05
        alpha 0.0
        0.05
        alpha 1.0
        repeat 2

    0.05
    alpha 0.0
    0.05
    "mod_assets/other/thunder.png"
    alpha 1.0

    parallel:
        easeout 2.8 alpha 0.0
    3.0
    Null()

image mas_lantern:
    "mod_assets/other/lantern.png"
    alpha 0.0
    block:
        0.05
        alpha 1.0
        0.05
        alpha 0.0
        repeat 4
    alpha 0.0

image mas_stab_wound:
    "mod_assets/other/stab-wound.png"
    zoom 0.9
    easein 1.0 zoom 1.0

image rects_bn1:
    RectCluster(Solid("#000"), 25, 20, 15).sm
    rotate 90
    pos (571, 217)
    size (20, 25)
    alpha 0.0
    easeout 1 alpha 1.0

image rects_bn2:
    RectCluster(Solid("#000"), 25, 20, 15).sm
    rotate 90
    pos (700, 217)
    size (20, 25)
    alpha 0.0
    easeout 1 alpha 1.0

image rects_bn3:
    RectCluster(Solid("#000"), 4, 15, 5).sm
    rotate 180
    pos (636, 302)
    size (25, 15)
    alpha 0.0
    easeout 1 alpha 1.0

transform k_scare:
    tinstant(640)
    ease 1.0 zoom 2.0

transform otei_appear(a=0.70, time=1.0):
    i11
    alpha 0.0
    linear time alpha a

transform fade_in(time=1.0):
    alpha 0.0
    ease time alpha 1.0


transform mas_kissing(_zoom, _y, time=2.0):
    i11
    xcenter 640 yoffset 700 yanchor 1.0
    linear time ypos _y zoom _zoom

transform mas_back_from_kissing(time, y):
    linear time xcenter 640 yoffset (y) zoom 0.80



default persistent._mas_first_kiss = None


default persistent._mas_last_kiss = None























label monika_kissing_motion(transition=4.0, duration=2.0, hide_ui=True, initial_exp="6dubfd", mid_exp="6tkbfu", final_exp="6ekbfa", fade_duration=1.0):




    if persistent._mas_first_kiss is None:
        $ persistent._mas_first_kiss = datetime.datetime.now()

    $ persistent._mas_last_kiss = datetime.datetime.now()

    window hide
    if hide_ui:

        $ HKBHideButtons()
        $ mas_RaiseShield_core()

    show monika at i11

    $ _mas_kiss_zoom = 4.9 / mas_sprites.value_zoom
    $ _mas_kiss_y = 2060 - ( 1700  * (mas_sprites.value_zoom - 1.1))
    $ _mas_kiss_y2 = -1320 + (1700 * (mas_sprites.value_zoom - 1.1))


    $ renpy.show("monika {}".format(initial_exp), [mas_kissing(_mas_kiss_zoom,int(_mas_kiss_y),transition)])


    $ renpy.pause(transition)

    show black zorder 100 at fade_in(fade_duration)

    $ renpy.pause(duration/2)
    play sound "mod_assets/sounds/effects/kissing.ogg"
    window auto
    "chu~{fast}{w=1}{nw}"
    window hide
    $ renpy.pause(duration/2)

    hide black

    $ renpy.show("monika {}".format(mid_exp),[mas_back_from_kissing(transition,_mas_kiss_y2)])
    pause transition
    $ renpy.show("monika {}".format(final_exp),[i11()])
    show monika with dissolve
    if hide_ui:
        if store.mas_globals.dlg_workflow:
            $ mas_MUMUDropShield()
            $ enable_esc()
        else:
            $ mas_DropShield_core()
        $ HKBShowButtons()
    window auto
    return


label monika_kissing_motion_short:
    call monika_kissing_motion (duration=0.5, initial_exp="6hua", fade_duration=0.5) from _call_monika_kissing_motion_1
    return








label monika_zoom_value_transition(new_zoom, transition=3.0):
    if new_zoom == mas_sprites.value_zoom:
        return

    if new_zoom > 2.1:
        $ new_zoom = 2.1
    elif new_zoom < 1.1:
        $ new_zoom = 1.1

    $ _mas_transition_time = transition


    $ _mas_old_zoom = mas_sprites.zoom_level
    $ _mas_old_zoom_value = mas_sprites.value_zoom
    $ _mas_old_y = mas_sprites.adjust_y


    $ _mas_new_zoom = ((new_zoom - mas_sprites.default_value_zoom) / mas_sprites.zoom_step ) + mas_sprites.default_zoom_level
    if _mas_new_zoom > mas_sprites.default_value_zoom:
        $ _mas_new_y = mas_sprites.default_y + ((_mas_new_zoom-mas_sprites.default_zoom_level) * mas_sprites.y_step)
    else:
        $ _mas_new_y = mas_sprites.default_y
    $ _mas_new_zoom = ((new_zoom - mas_sprites.default_value_zoom) / mas_sprites.zoom_step ) + mas_sprites.default_zoom_level


    $ _mas_zoom_diff = _mas_new_zoom - _mas_old_zoom
    $ _mas_zoom_value_diff = new_zoom - _mas_old_zoom_value
    $ _mas_zoom_y_diff = _mas_new_y - _mas_old_y

    show monika at mas_smooth_transition
    $ renpy.pause(transition, hard=True)
    return








label monika_zoom_fixed_duration_transition(new_zoom, transition=3.0):

    if new_zoom == mas_sprites.zoom_level:
        return
    if new_zoom > 20:
        $ new_zoom = 20
    elif new_zoom < 0:
        $ new_zoom = 0

    $ _mas_transition_time = transition


    $ _mas_old_zoom = mas_sprites.zoom_level
    $ _mas_old_zoom_value = mas_sprites.value_zoom
    $ _mas_old_y = mas_sprites.adjust_y


    if new_zoom > mas_sprites.default_zoom_level:
        $ _mas_new_y = mas_sprites.default_y + (
            (new_zoom - mas_sprites.default_zoom_level) * mas_sprites.y_step
        )
        $ _mas_new_zoom_value = mas_sprites.default_value_zoom + (
            (new_zoom - mas_sprites.default_zoom_level) * mas_sprites.zoom_step
        )
    else:
        $ _mas_new_y = mas_sprites.default_y
        if new_zoom == mas_sprites.default_zoom_level:
            $ _mas_new_zoom_value = mas_sprites.default_value_zoom
        else:
            $ _mas_new_zoom_value = mas_sprites.default_value_zoom - (
                (mas_sprites.default_zoom_level - new_zoom) * mas_sprites.zoom_step
            )

    $ _mas_zoom_diff = new_zoom - _mas_old_zoom
    $ _mas_zoom_value_diff = _mas_new_zoom_value - _mas_old_zoom_value
    $ _mas_zoom_y_diff = _mas_new_y - _mas_old_y

    show monika at mas_smooth_transition
    $ renpy.pause(transition, hard=True)
    return










label monika_zoom_transition(new_zoom, transition=3.0):

    if new_zoom == mas_sprites.zoom_level:
        return
    if new_zoom > 20:
        $ new_zoom = 20
    elif new_zoom < 0:
        $ new_zoom = 0


    $ _mas_old_zoom = mas_sprites.zoom_level
    $ _mas_old_zoom_value = mas_sprites.value_zoom
    $ _mas_old_y = mas_sprites.adjust_y


    if new_zoom > mas_sprites.default_zoom_level:
        $ _mas_new_y = mas_sprites.default_y + (
            (new_zoom - mas_sprites.default_zoom_level) * mas_sprites.y_step
        )
        $ _mas_new_zoom_value = mas_sprites.default_value_zoom + (
            (new_zoom - mas_sprites.default_zoom_level) * mas_sprites.zoom_step
        )
    else:
        $ _mas_new_y = mas_sprites.default_y
        if new_zoom == mas_sprites.default_zoom_level:
            $ _mas_new_zoom_value = mas_sprites.default_value_zoom
        else:
            $ _mas_new_zoom_value = mas_sprites.default_value_zoom - (
                (mas_sprites.default_zoom_level - new_zoom) * mas_sprites.zoom_step
            )


    $ _mas_zoom_diff = new_zoom - _mas_old_zoom
    $ _mas_zoom_value_diff = _mas_new_zoom_value - _mas_old_zoom_value
    $ _mas_zoom_y_diff = _mas_new_y - _mas_old_y


    $ _mas_transition_time = abs(_mas_zoom_value_diff) * transition


    show monika at mas_smooth_transition
    $ renpy.pause(_mas_transition_time, hard=True)
    return


label monika_zoom_transition_reset(transition=3.0):
    call monika_zoom_transition (store.mas_sprites.default_zoom_level, transition) from _call_monika_zoom_transition_2
    return

init python:
    def zoom_smoothly(trans, st, at):
        """
        Transition function used in mas_smooth_transition
        takes the standard parameters on functions used on transforms
        see https://www.renpy.org/doc/html/atl.html#function-statement
        ASSUMES:
            _mas_old_zoom - containing the old zoom
            _mas_old_zoom_value - containing the old zoom value
            _mas_old_y - containing the old y value
            _mas_zoom_diff - containing the difference between the old and new zoom levels
            _mas_zoom_value_diff - containing the difference between the old and new zoom values
            _mas_zoom_y_diff - containing the difference between the old and new y values
        """
        
        if _mas_transition_time > st:
            
            step = st / _mas_transition_time
            mas_sprites.zoom_level = _mas_old_zoom + (step * _mas_zoom_diff)
            mas_sprites.value_zoom = _mas_old_zoom_value + (step * _mas_zoom_value_diff)
            mas_sprites.adjust_y = int(_mas_old_y + (step * _mas_zoom_y_diff))
            if mas_sprites.adjust_y < mas_sprites.default_y:
                mas_sprites.adjust_y = mas_sprites.default_y
            
            renpy.restart_interaction()
            
            return 0.1
        else:
            
            mas_sprites.zoom_level = int(round(mas_sprites.zoom_level))
            mas_sprites.adjust_zoom()
            renpy.restart_interaction()
            
            return None


transform mas_smooth_transition:
    i11
    function zoom_smoothly
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
