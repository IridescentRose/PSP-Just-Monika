









init -10 python in mas_interactions:

    import ccmath.ccmath as cmath

    import store.mas_sprites as mas_sprites
    import store.mas_utils as mas_utils


    ZONE_CHEST = "chest"
    ZONE_CHEST_1 = "chest-1"
    ZONE_HEAD = "head"
    ZONE_NOSE = "nose"

    ZONE_ENUMS = (
        ZONE_CHEST,
        ZONE_CHEST_1,
        ZONE_HEAD,
        ZONE_NOSE,
    )


    cz_map = {
        ZONE_CHEST: [
            (514, 453),
            (491, 509),
            (489, 533),
            (493, 551),
            (506, 573),
            (525, 588),
            (541, 592),
            (652, 586),
            (709, 592),
            (761, 592),
            (787, 580),
            (806, 559),
            (813, 536),
            (813, 517),
            (789, 453),
        ],
        ZONE_CHEST_1: [
            (602, 487),
            (590, 531),
            (587, 597),
            (652, 586),
            (714, 592),
            (708, 530),
            (697, 487),
        ],
        ZONE_HEAD: [
            (634, 68-100),
            (597, 73-100),
            (552, 91-100),
            (540, 94-100),
            (531, 4),
            (517, 42),
            (498, 80),
            (486, 144),
            (708, 144),
            (778, 178),
            (792, 129),
            (792, 80),
            (777, 30),
            (751, 99-100),
            (690, 71-100),
        ],
        ZONE_NOSE: [
            (629, 240),
            (623, 252),
            (629, 258),
            (633, 252),
        ],
    }


    FOCAL_POINT = (640, 750)
    FOCAL_POINT_UP = (640, 740)

    ZOOM_INC_PER = 0.04


    def vertex_list_from_zoom(zoom_level, zone_enum):
        """
        Generates a vertex list from the given zoom

        IN:
            zoom_level - zoom level to generate vertex list
            zone_enum - zone enum to get vertex list for

        RETURNS: list of vertexes. might be empty list if invalid data passed
            in
        """
        if zone_enum not in ZONE_ENUMS:
            return []
        
        if zoom_level == mas_sprites.default_zoom_level:
            return cz_map[zone_enum]
        
        
        return _vx_list_zoom(
            zoom_level,
            zone_enum,
            zoom_level < mas_sprites.default_zoom_level
        )





    def _vx_list_zoom(zoom_level, zone_enum, zoom_out):
        """
        Generates vertex list for zooming.

        IN:
            zoom_level zoom level to generate vertex list for
            zone_enum - zone enum to get vertex list for
            zoom_out - True if we are zooming out, False if zooming in

        RETURNS: list of vertexes
        """
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        if zoom_out:
            zoom_diff = mas_sprites.default_zoom_level - zoom_level
            per_mod = -1 * (zoom_diff * ZOOM_INC_PER)
            xfc, yfc = FOCAL_POINT
            yfc_offset = 0
        
        else:
            zoom_diff = zoom_level - mas_sprites.default_zoom_level
            per_mod = zoom_diff * ZOOM_INC_PER
            xfc, yfc = FOCAL_POINT_UP
            yfc_offset = -1 * zoom_diff * mas_sprites.y_step
        
        
        pts = cz_map[zone_enum]
        vx_list = []
        for xcoord, ycoord in pts:
            
            xcoord -= xfc
            ycoord -= (yfc + yfc_offset)
            
            
            radius, angle = cmath.polar(xcoord, ycoord)
            
            
            radius += (radius * per_mod)
            
            
            new_x, new_y = cmath.rect(radius, angle)
            
            
            vx_list.append((
                int(new_x + xfc),
                int(new_y + yfc)
            ))
        
        return vx_list


init -9 python:

    class MASBoopInteractable(MASInteractable):
        """
        Interactable for nose booping
        """
        import store.mas_interactions as smi
        
        def __init__(self, chest_open):
            """
            contstructor

            IN:
                chest_open - true if the chest is fully open at start
            """




label mas_nose_boop_launch:



    show monika 6eua



    $ mas_DropShield_core()

    show monika idle


    jump ch30_loop
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
