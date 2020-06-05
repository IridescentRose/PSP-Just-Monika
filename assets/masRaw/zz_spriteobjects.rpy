














init -2 python in mas_sprites:



    import store

    temp_storage = dict()








    _hair__testing_entry = False
    _hair__testing_exit = False
    _clothes__testing_entry = False
    _clothes__testing_exit = False
    _acs__testing_entry = False
    _acs__testing_exit = False





    def _acs_wear_if_found(_moni_chr, acs_name):
        """
        Wears the acs if the acs exists

        IN:
            _moni_chr - MASMonika object
            acs_name - name of the accessory
        """
        acs_to_wear = store.mas_sprites.get_sprite(
            store.mas_sprites.SP_ACS,
            acs_name
        )
        if acs_to_wear is not None:
            _moni_chr.wear_acs(acs_to_wear)


    def _acs_wear_if_gifted(_moni_chr, acs_name):
        """
        Wears the acs if it exists and has been gifted/reacted.
        It has been gifted/reacted if the selectable is unlocked.

        IN:
            _moni_chr - MASMonika object
            acs_name - name of the accessory
        """
        acs_to_wear = store.mas_sprites.get_sprite(
            store.mas_sprites.SP_ACS,
            acs_name
        )
        if acs_to_wear is not None and store.mas_SELisUnlocked(acs_to_wear):
            _moni_chr.wear_acs(acs_to_wear)


    def _acs_wear_if_in_tempstorage(_moni_chr, key):
        """
        Wears the acs in tempstorage at the given key, if any.

        IN:
            _moni_chr - MASMonika object
            key - key in tempstorage
        """
        acs_items = temp_storage.get(key, None)
        if acs_items is not None:
            for acs_item in acs_items:
                _moni_chr.wear_acs(acs_item)


    def _acs_wear_if_in_tempstorage_s(_moni_chr, key):
        """
        Wears a single acs in tempstorage at the given key, if any.

        IN:
            _moni_chr - MASMonika object
            key - key in tempstorage
        """
        acs_item = temp_storage.get(key, None)
        if acs_item is not None:
            _moni_chr.wear_acs(acs_item)


    def _acs_wear_if_wearing_acs(_moni_chr, acs, acs_to_wear):
        """
        Wears the given acs if wearing another acs.

        IN:
            _moni_chr - MASMonika object
            acs - acs to check if wearing
            acs_to_wear - acs to wear if wearing acs
        """
        if _moni_chr.is_wearing_acs(acs):
            _moni_chr.wear_acs(acs_to_wear)


    def _acs_wear_if_wearing_type(_moni_chr, acs_type, acs_to_wear):
        """
        Wears the given acs if wearing an acs of the given type.

        IN:
            _moni_chr - MASMonika object
            acs_type - acs type to check if wearing
            acs_to_wear - acs to wear if wearing acs type
        """
        if _moni_chr.is_wearing_acs_type(acs_type):
            _moni_chr.wear_acs(acs_to_wear)


    def _acs_wear_if_not_wearing_type(_moni_chr, acs_type, acs_to_wear):
        """
        Wears the given acs if NOT wearing an acs of the given type.

        IN:
            _moni_chr - MASMonika object
            acs_type - asc type to check if not wearing
            acs_to_wear - acs to wear if not wearing acs type
        """
        if not _moni_chr.is_wearing_acs_type(acs_type):
            _moni_chr.wear_acs(acs_to_wear)


    def _acs_remove_if_found(_moni_chr, acs_name):
        """
        REmoves an acs if the name exists

        IN:
            _moni_chr - MASMonika object
            acs_name - name of the accessory to remove
        """
        acs_to_remove = store.mas_sprites.get_sprite(
            store.mas_sprites.SP_ACS,
            acs_name
        )
        if acs_to_remove is not None:
            _moni_chr.remove_acs(acs_to_remove)


    def _acs_ribbon_save_and_remove(_moni_chr):
        """
        Removes ribbon acs and aves them to temp storage.

        IN:
            _moni_chr - MASMonika object
        """
        prev_ribbon = _moni_chr.get_acs_of_type("ribbon")
        
        
        if prev_ribbon != store.mas_acs_ribbon_blank:
            temp_storage["hair.ribbon"] = prev_ribbon
        
        if prev_ribbon is not None:
            _moni_chr.remove_acs(prev_ribbon)
        
        
        store.mas_lockEVL("monika_ribbon_select", "EVE")


    def _acs_ribbon_like_save_and_remove(_moni_chr):
        """
        Removes ribbon-like acs and saves them to temp storage, if found

        IN:
            _moni_chr - MASMonika object
        """
        prev_ribbon_like = _moni_chr.get_acs_of_exprop("ribbon-like")
        
        if prev_ribbon_like is not None:
            _moni_chr.remove_acs(prev_ribbon_like)
            temp_storage["hair.ribbon"] = prev_ribbon_like


    def _acs_save_and_remove_exprop(_moni_chr, exprop, key, lock_topics):
        """
        Removes acs with given exprop, saving them to temp storage with
        given key.
        Also locks topics with the exprop if desired

        IN:
            _moni_chr - MASMonika object
            exprop - exprop to remove and save acs
            key - key to use for temp storage
            lock_topics - True will lock topics associated with this exprop
                False will not
        """
        acs_items = _moni_chr.get_acs_of_exprop(exprop, get_all=True)
        if len(acs_items) > 0:
            temp_storage[key] = acs_items
            _moni_chr.remove_acs_exprop(exprop)
        
        if lock_topics:
            lock_exprop_topics(exprop)


    def _hair_unlock_select_if_needed():
        """
        Unlocks the hairdown selector if enough hair is unlocked.
        """
        if len(store.mas_selspr.filter_hair(True)) > 1:
            store.mas_unlockEVL("monika_hair_select", "EVE")


    def _clothes_baked_entry(_moni_chr):
        """
        Clothes baked entry
        """
        for prompt_key in store.mas_selspr.PROMPT_MAP:
            if prompt_key != "clothes":
                prompt_ev = store.mas_selspr.PROMPT_MAP[prompt_key].get(
                    "_ev",
                    None
                )
                if prompt_ev is not None:
                    store.mas_lockEVL(prompt_ev, "EVE")
        
        
        _moni_chr.remove_all_acs()
        
        store.mas_selspr._switch_to_wear_prompts()









    def _hair_def_entry(_moni_chr, **kwargs):
        """
        Entry programming point for ponytail
        """
        pass


    def _hair_def_exit(_moni_chr, **kwargs):
        """
        Exit programming point for ponytail
        """
        pass


    def _hair_down_entry(_moni_chr, **kwargs):
        """
        Entry programming point for hair down
        """
        pass


    def _hair_down_exit(_moni_chr, **kwargs):
        """
        Exit programming point for hair down
        """
        pass


    def _hair_bun_entry(_moni_chr, **kwargs):
        """
        Entry programming point for hair bun
        """
        pass


    def _hair_orcaramelo_bunbraid_exit(_moni_chr, **kwargs):
        """
        Exit prog point for bunbraid
        """
        
        _acs_remove_if_found(_moni_chr, "orcaramelo_sakuya_izayoi_headband")









    def _clothes_def_entry(_moni_chr, **kwargs):
        """
        Entry programming point for def clothes
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            
            _moni_chr.change_hair(store.mas_hair_def)
            _moni_chr.wear_acs(store.mas_acs_ribbon_def)




    def _clothes_rin_entry(_moni_chr, **kwargs):
        """
        Entry programming point for rin clothes
        """
        
        temp_storage["clothes.rin"] = store.mas_acs_promisering.pose_map
        store.mas_acs_promisering.pose_map = store.MASPoseMap(
            p1=None,
            p2=None,
            p3="3",
            p4=None,
            p5=None,
            p6=None
        )
        wearing_promise_ring = _moni_chr.is_wearing_acs(
            store.mas_acs_promisering
        )
        
        
        
        
        
        
        
        
        
        
        _acs_ribbon_save_and_remove(_moni_chr)
        _acs_ribbon_like_save_and_remove(_moni_chr)
        
        
        
        
        
        
        
        
        
        
        _moni_chr.lock_hair = True
        
        
        
        
        
        
        
        _acs_save_and_remove_exprop(
            _moni_chr,
            "left-hair-strand-eye-level",
            "acs.left-hair-strand-eye-level",
            True
        )
        
        
        
        
        _moni_chr.remove_acs(store.mas_acs_ear_rose)
        
        
        _clothes_baked_entry(_moni_chr)
        
        
        if wearing_promise_ring:
            _moni_chr.wear_acs(store.mas_acs_promisering)


    def _clothes_rin_exit(_moni_chr, **kwargs):
        """
        Exit programming point for rin clothes
        """
        rin_map = temp_storage.get("clothes.rin", None)
        if rin_map is not None:
            store.mas_acs_promisering.pose_map = rin_map
        
        
        
        
        
        
        _acs_wear_if_in_tempstorage_s(_moni_chr, "hair.ribbon")
        
        
        
        
        
        
        
        
        
        
        
        
        
        _moni_chr.lock_hair = False
        
        
        
        
        _acs_wear_if_in_tempstorage(
            _moni_chr,
            "acs.left-hair-strand-eye-level"
        )


    def _clothes_marisa_entry(_moni_chr, **kwargs):
        """
        Entry programming point for marisa clothes
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            _moni_chr.change_hair(store.mas_hair_downtiedstrand)
            _moni_chr.wear_acs(store.mas_acs_marisa_strandbow)
            _moni_chr.wear_acs(store.mas_acs_marisa_witchhat)


    def _clothes_marisa_exit(_moni_chr, **kwargs):
        """
        Exit programming point for marisa clothes
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        _moni_chr.remove_acs(store.mas_acs_marisa_strandbow)
        
        if outfit_mode:
            _moni_chr.remove_acs(store.mas_acs_marisa_witchhat)


    def _clothes_orcaramelo_hatsune_miku_entry(_moni_chr, **kwargs):
        """
        Entry pp for orcaramelo miku
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            
            twintails = store.mas_sprites.get_sprite(
                store.mas_sprites.SP_HAIR,
                "orcaramelo_twintails"
            )
            if twintails is not None:
                _moni_chr.change_hair(twintails)
                
                
                _acs_wear_if_found(
                    _moni_chr,
                    "orcaramelo_hatsune_miku_headset"
                )
                _acs_wear_if_found(
                    _moni_chr,
                    "orcaramelo_hatsune_miku_twinsquares"
                )


    def _clothes_orcaramelo_hatsune_miku_exit(_moni_chr, **kwargs):
        """
        Exit pp for orcaramelo miku
        """
        
        _acs_remove_if_found(
            _moni_chr,
            "orcaramelo_hatsune_miku_headset"
        )
        _acs_remove_if_found(
            _moni_chr,
            "orcaramelo_hatsune_miku_twinsquares"
        )


    def _clothes_orcaramelo_sakuya_izayoi_entry(_moni_chr, **kwargs):
        """
        Entry pp for orcaramelo sakuya
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            
            bunbraid = store.mas_sprites.get_sprite(
                store.mas_sprites.SP_HAIR,
                "orcaramelo_bunbraid"
            )
            if bunbraid is not None:
                _moni_chr.change_hair(bunbraid)
                
                
                _acs_wear_if_found(
                    _moni_chr,
                    "orcaramelo_sakuya_izayoi_headband"
                )
                _acs_wear_if_found(
                    _moni_chr,
                    "orcaramelo_sakuya_izayoi_strandbow"
                )
                
                
                ribbon_acs = _moni_chr.get_acs_of_type("ribbon")
                if ribbon_acs is not None:
                    _moni_chr.remove_acs(ribbon_acs)


    def _clothes_orcaramelo_sakuya_izayoi_exit(_moni_chr, **kwargs):
        """
        Exit pp for orcaramelo sakuya
        """
        
        _acs_remove_if_found(
            _moni_chr,
            "orcaramelo_sakuya_izayoi_headband"
        )
        _acs_remove_if_found(
            _moni_chr,
            "orcaramelo_sakuya_izayoi_strandbow"
        )


    def _clothes_santa_entry(_moni_chr, **kwargs):
        """
        Entry programming point for santa clothes
        """
        store.mas_selspr.unlock_acs(store.mas_acs_holly_hairclip)
        
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            _moni_chr.change_hair(store.mas_hair_def)
            _moni_chr.wear_acs(store.mas_acs_ribbon_wine)
            _moni_chr.wear_acs(store.mas_acs_holly_hairclip)


    def _clothes_santa_exit(_moni_chr, **kwargs):
        """
        Exit programming point for santa clothes
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            _moni_chr.remove_acs(store.mas_acs_holly_hairclip)


    def _clothes_santa_lingerie_entry(_moni_chr, **kwargs):
        """
        Entry programming point for santa lingerie
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            _moni_chr.wear_acs(store.mas_acs_holly_hairclip)


    def _clothes_santa_lingerie_exit(_moni_chr, **kwargs):
        """
        Exit programming point for santa lingerie
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            _moni_chr.remove_acs(store.mas_acs_holly_hairclip)


    def _clothes_dress_newyears_entry(_moni_chr, **kwargs):
        """
        entry progpoint for dress_newyears
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            
            ponytailbraid = store.mas_sprites.get_sprite(
                store.mas_sprites.SP_HAIR,
                "orcaramelo_ponytailbraid"
            )
            if ponytailbraid is not None:
                _moni_chr.change_hair(ponytailbraid)
            
            _moni_chr.wear_acs(store.mas_acs_flower_crown)
            _moni_chr.wear_acs(store.mas_acs_hairties_bracelet_brown)
            
            
            hairclip = _moni_chr.get_acs_of_type("left-hair-clip")
            if hairclip:
                _moni_chr.remove_acs(hairclip)
            
            
            ribbon = _moni_chr.get_acs_of_type("ribbon")
            if ribbon:
                _moni_chr.remove_acs(ribbon)


    def _clothes_dress_newyears_exit(_moni_chr, **kwargs):
        """
        exit progpoint for dress_newyears
        """
        _moni_chr.remove_acs(store.mas_acs_flower_crown)
        _moni_chr.remove_acs(store.mas_acs_hairties_bracelet_brown)

    def _clothes_sundress_white_entry(_moni_chr, **kwargs):
        """
        Entry programming point for sundress white
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            _moni_chr.wear_acs(store.mas_acs_hairties_bracelet_brown)
            _moni_chr.wear_acs(store.mas_acs_musicnote_necklace_gold)


    def _clothes_sundress_white_exit(_moni_chr, **kwargs):
        """
        Exit programming point for sundress white
        """
        
        
        _moni_chr.remove_acs(store.mas_acs_hairties_bracelet_brown)
        _moni_chr.remove_acs(store.mas_acs_musicnote_necklace_gold)


    def _clothes_velius94_dress_whitenavyblue_entry(_moni_chr, **kwargs):
        """
        Entry prog point for navyblue dress
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            
            if (
                    not _moni_chr.is_wearing_hair_with_exprop("ribbon")
                    or _moni_chr.is_wearing_hair_with_exprop("twintails")
            ):
                _moni_chr.change_hair(store.mas_hair_def)
            
            _acs_wear_if_gifted(_moni_chr, "velius94_bunnyscrunchie_blue")






    def _acs_quetzalplushie_entry(_moni_chr, **kwargs):
        """
        Entry programming point for quetzal plushie acs
        """
        
        store.mas_showEVL('monika_plushie','EVE',_random=True)


    def _acs_quetzalplushie_exit(_moni_chr, **kwargs):
        """
        Exit programming point for quetzal plushie acs
        """
        
        _moni_chr.remove_acs(store.mas_acs_quetzalplushie_santahat)
        
        
        _moni_chr.remove_acs(store.mas_acs_quetzalplushie_antlers)
        
        
        store.mas_hideEVL('monika_plushie','EVE',derandom=True)


    def _acs_quetzalplushie_santahat_entry(_moni_chr, **kwargs):
        """
        Entry programming point for quetzal plushie santa hat acs
        """
        
        _moni_chr.wear_acs(store.mas_acs_quetzalplushie)


    def _acs_quetzalplushie_antlers_entry(_moni_chr, **kwargs):
        """
        Entry programming point for quetzal plushie antlers acs
        """
        
        _moni_chr.wear_acs(store.mas_acs_quetzalplushie)


    def _acs_heartchoc_entry(_moni_chr, **kwargs):
        """
        Entry programming point for heartchoc acs
        """
        
        
        
        
        
        
        if not (store.mas_isF14() or store.mas_isD25Season()):
            if _moni_chr.is_wearing_acs(store.mas_acs_quetzalplushie):
                _moni_chr.wear_acs(store.mas_acs_center_quetzalplushie)
        
        else:
            _moni_chr.remove_acs(store.mas_acs_quetzalplushie)


    def _acs_heartchoc_exit(_moni_chr, **kwargs):
        """
        Exit programming point for heartchoc acs
        """
        if _moni_chr.is_wearing_acs(store.mas_acs_center_quetzalplushie):
            _moni_chr.wear_acs(store.mas_acs_quetzalplushie)

init -1 python:








































    mas_hair_def = MASHair(
        "def",
        "def",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),


        ex_props={
            "ribbon": True,
            "ribbon-restore": True
        }
    )
    store.mas_sprites.init_hair(mas_hair_def)
    store.mas_selspr.init_selectable_hair(
        mas_hair_def,
        "Ponytail",
        "def",
        "hair",
        select_dlg=[
            "Do you like my ponytail, [player]?"
        ]
    )
    store.mas_selspr.unlock_hair(mas_hair_def)





    mas_hair_down = MASHair(
        "down",
        "down",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        ex_props={
            store.mas_sprites.EXP_H_NT: True,
        }



    )
    store.mas_sprites.init_hair(mas_hair_down)
    store.mas_selspr.init_selectable_hair(
        mas_hair_down,
        "Down",
        "down",
        "hair",
        select_dlg=[
            "Feels nice to let my hair down..."
        ]
    )





    mas_hair_downtiedstrand = MASHair(
        "downtiedstrand",
        "downtiedstrand",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        ex_props={
            store.mas_sprites.EXP_H_RQCP: store.mas_sprites.EXP_C_BRS,
            store.mas_sprites.EXP_H_TS: True,
            store.mas_sprites.EXP_H_NT: True,
        }
    )
    store.mas_sprites.init_hair(mas_hair_downtiedstrand)
    store.mas_selspr.init_selectable_hair(
        mas_hair_downtiedstrand,
        "Down (Tied strand)",
        "downtiedstrand",
        "hair",
        select_dlg=[
            "Feels nice to let my hair down...",
            "Looks cute, don't you think?"
        ]
    )





    mas_hair_custom = MASHair(
        "custom",
        "custom",
        MASPoseMap(),

        
        split=MASPoseMap(
            default=False,
            use_reg_for_l=True
        ),
    )
    store.mas_sprites.init_hair(mas_hair_custom)


init -1 python:




























    mas_clothes_def = MASClothes(
        "def",
        "def",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_def_entry
    )
    store.mas_sprites.init_clothes(mas_clothes_def)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_def,
        "School Uniform",
        "schooluniform",
        "clothes",
        visible_when_locked=True,
        hover_dlg=None,
        select_dlg=[
            "Ready for school!"
        ]
    )
    store.mas_selspr.unlock_clothes(mas_clothes_def)






    mas_clothes_blackdress = MASClothes(
        "blackdress",
        "blackdress",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        stay_on_start=True,
        ex_props={
            store.mas_sprites.EXP_C_BRS: True,
        }
    )
    store.mas_sprites.init_clothes(mas_clothes_blackdress)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_blackdress,
        "Black Dress",
        "blackdress",
        "clothes",
        visible_when_locked=False,
        select_dlg=[
            "Are we going somewhere special, [player]?"
        ]
    )






    mas_clothes_blazerless = MASClothes(
        "blazerless",
        "blazerless",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        stay_on_start=True,
        ex_props={
            store.mas_sprites.EXP_C_BRS: True
        },
        pose_arms=MASPoseArms(
            {
                1: MASArmBoth(
                    "crossed",
                    {
                        MASArm.LAYER_MID: True,
                    }
                ),
            }
        )
    )
    store.mas_sprites.init_clothes(mas_clothes_blazerless)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_blazerless,
        "School Uniform (Blazerless)",
        "schooluniform_blazerless",
        "clothes",
        visible_when_locked=True,
        hover_dlg=None,
        select_dlg=[
            "Ah, feels nice without the blazer!",
        ]
    )
    store.mas_selspr.unlock_clothes(mas_clothes_def)






    mas_clothes_marisa = MASClothes(
        "marisa",
        "marisa",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        pose_arms=MASPoseArms(
            {
                1: MASArmBoth(
                    "crossed",
                    {
                        MASArm.LAYER_MID: True,
                    }
                ),
                9: MASArmRight(
                    "def",
                    {
                        MASArm.LAYER_MID: True,
                    }
                ),
            }
        ),
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_marisa_entry,
        exit_pp=store.mas_sprites._clothes_marisa_exit,
        ex_props={
            store.mas_sprites.EXP_C_BRS: True,
            store.mas_sprites.EXP_C_COST: "o31",
            store.mas_sprites.EXP_C_COSP: True,
        }
    )
    store.mas_sprites.init_clothes(mas_clothes_marisa)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_marisa,
        "Witch Costume",
        "marisa",
        "clothes",
        visible_when_locked=False,
        hover_dlg=None,
        select_dlg=[
            "Just an ordinary costume, ~ze."
        ]
    )






















































    mas_clothes_santa = MASClothes(
        "santa",
        "santa",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_santa_entry,
        exit_pp=store.mas_sprites._clothes_santa_exit,
        ex_props={
            "costume": "d25"
        },
    )
    store.mas_sprites.init_clothes(mas_clothes_santa)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_santa,
        "Santa Costume",
        "santa",
        "clothes",
        visible_when_locked=False,
        hover_dlg=None,
        select_dlg=[
            "Merry Christmas!",
            "What kind of {i}presents{/i} do you want?",
            "Happy holidays!"
        ]
    )





    mas_clothes_santa_lingerie = MASClothes(
        "santa_lingerie",
        "santa_lingerie",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        stay_on_start=True,
        ex_props={
            store.mas_sprites.EXP_C_BRS: True,
            "lingerie": "d25"
        },
        entry_pp=store.mas_sprites._clothes_santa_lingerie_entry,
        exit_pp=store.mas_sprites._clothes_santa_lingerie_exit,
        pose_arms=MASPoseArms({}, def_base=False)
    )
    store.mas_sprites.init_clothes(mas_clothes_santa_lingerie)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_santa_lingerie,
        "Lingerie (Santa)",
        "santa_lingerie",
        "clothes",
        visible_when_locked=False,
        hover_dlg=None,
        select_dlg=[
            "Would you like to open your present?~",
            "What kind of {i}presents{/i} do you want?",
            "Open your present, ehehe~",
            "All I want for Christmas is you~",
            "Santa baby~",
            "What {i}else{/i} do you want to unwrap?~"
        ]
    )






    mas_clothes_dress_newyears = MASClothes(
        "new_years_dress",
        "new_years_dress",
        MASPoseMap(
            default=True,
            use_reg_for_l=True,
        ),
        entry_pp=store.mas_sprites._clothes_dress_newyears_entry,
        exit_pp=store.mas_sprites._clothes_dress_newyears_exit,
        stay_on_start=True,
        pose_arms=MASPoseArms({}, def_base=False),
        ex_props={
            store.mas_sprites.EXP_C_BRS: True,
        }
    )
    store.mas_sprites.init_clothes(mas_clothes_dress_newyears)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_dress_newyears,
        "Dress (New Years)",
        "new_years_dress",
        "clothes",
        visible_when_locked=False,
        hover_dlg=None,
        select_dlg=[
            "Are we going somewhere special, [player]?",
            "Very formal!",
            "Any special occasion, [player]?"
        ],
    )





    mas_clothes_sundress_white = MASClothes(
        "sundress_white",
        "sundress_white",
        MASPoseMap(
            default=True,
            use_reg_for_l=True,
        ),
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_sundress_white_entry,
        exit_pp=store.mas_sprites._clothes_sundress_white_exit,
        pose_arms=MASPoseArms({}, def_base=False),
        ex_props={
            store.mas_sprites.EXP_C_BRS: True,
        }
    )
    store.mas_sprites.init_clothes(mas_clothes_sundress_white)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_sundress_white,
        "Sundress (White)",
        "sundress_white",
        "clothes",
        visible_when_locked=False,
        hover_dlg=None,
        select_dlg=[
            "Are we going anywhere special today, [player]?",
            "I've always loved this outfit...",
        ],
    )





    mas_clothes_vday_lingerie = MASClothes(
        "vday_lingerie",
        "vday_lingerie",
        MASPoseMap(
            default=True,
            use_reg_for_l=True,
        ),
        stay_on_start=True,
        ex_props={
            store.mas_sprites.EXP_C_LING: True,
            store.mas_sprites.EXP_C_BRS: True
        },
        pose_arms=MASPoseArms({}, def_base=False)
    )
    store.mas_sprites.init_clothes(mas_clothes_vday_lingerie)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_vday_lingerie,
        "Lingerie (Pink Lace)",
        "vday_lingerie",
        "clothes",
        visible_when_locked=False,
        hover_dlg=None,
        select_dlg=[
            "Ehehe~",
            "Do you like what you see, [player]?"
        ]
    )

init -1 python:





























    mas_acs_mug = MASAccessory(
        "mug",
        "mug",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="mug",
        mux_type=["mug"],
        keep_on_desk=True
    )
    store.mas_sprites.init_acs(mas_acs_mug)





    mas_acs_thermos_mug = MASAccessory(
        "thermos_mug",
        "thermos_mug",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="thermos-mug"
    )
    store.mas_sprites.init_acs(mas_acs_thermos_mug)
    store.mas_selspr.init_selectable_acs(
        mas_acs_thermos_mug,
        "Thermos (Just Monika)",
        "thermos_justmonika",
        "thermos-mug"
    )





    mas_acs_ear_rose = MASAccessory(
        "ear_rose",
        "ear_rose",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        acs_type="left-hair-flower-ear",
        mux_type=[
            "left-hair-flower-ear",
            "left-hair-flower"
        ],
        ex_props={
            "left-hair-strand-eye-level": True,
        },
        priority=20,
        stay_on_start=False,
        rec_layer=MASMonika.PST_ACS,
    )
    store.mas_sprites.init_acs(mas_acs_ear_rose)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ear_rose,
        "Rose",
        "hairflower_rose",
        "left-hair-flower",
        hover_dlg=[
            "TALE AS OLD AS TIME",
        ],
        select_dlg=[
            "TRUE AS IT CAN BE",
        ]
    )





    mas_acs_hairties_bracelet_brown = MASSplitAccessory(
        "hairties_bracelet_brown",
        "hairties_bracelet_brown",
        MASPoseMap(
            p1="1",
            p2="2",
            p3="1",
            p4="4",
            p5="5",
            p6=None,
            p7="1"
        ),
        stay_on_start=True,
        acs_type="wrist-bracelet",
        mux_type=["wrist-bracelet"],
        ex_props={
            "bare wrist": True,
        },
        rec_layer=MASMonika.ASE_ACS,
        arm_split=MASPoseMap(
            default="",
            p1="10",
            p2="5",
            p3="10",
            p4="0",
            p5="10",
            p7="10",
        )
    )
    store.mas_sprites.init_acs(mas_acs_hairties_bracelet_brown)





    mas_acs_heartchoc = MASAccessory(
        "heartchoc",
        "heartchoc",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=False,
        acs_type="chocs",
        mux_type=store.mas_sprites.DEF_MUX_LD,
        keep_on_desk=False
    )
    store.mas_sprites.init_acs(mas_acs_heartchoc)





    mas_acs_hotchoc_mug = MASAccessory(
        "hotchoc_mug",
        "hotchoc_mug",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="mug",
        mux_type=["mug"],
        keep_on_desk=True
    )
    store.mas_sprites.init_acs(mas_acs_hotchoc_mug)





    mas_acs_musicnote_necklace_gold = MASSplitAccessory(
        "musicnote_necklace_gold",
        "musicnote_necklace_gold",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="necklace",
        mux_type=["necklace"],
        ex_props={
            "bare collar": True,
        },
        rec_layer=MASMonika.BSE_ACS,
        arm_split=MASPoseMap(
            default="0",
            use_reg_for_l=True
        )
    )
    store.mas_sprites.init_acs(mas_acs_musicnote_necklace_gold)





    mas_acs_marisa_strandbow = MASAccessory(
        "marisa_strandbow",
        "marisa_strandbow",
        MASPoseMap(
            default="0",
            l_default="5"
        ),
        stay_on_start=True,
        acs_type="strandbow",
        
        ex_props={
            store.mas_sprites.EXP_A_RQHP: store.mas_sprites.EXP_H_TS,
        },
        rec_layer=MASMonika.AFH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_marisa_strandbow)





    mas_acs_marisa_witchhat = MASAccessory(
        "marisa_witchhat",
        "marisa_witchhat",
        MASPoseMap(
            default="0",
            l_default="5"
        ),
        stay_on_start=True,
        acs_type="hat",
        
        ex_props={
            store.mas_sprites.EXP_A_RQHP: store.mas_sprites.EXP_H_NT,
        },
        rec_layer=MASMonika.AFH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_marisa_witchhat)
    store.mas_selspr.init_selectable_acs(
        mas_acs_marisa_witchhat,
        "Witch Hat", 
        "marisa_witchhat",
        "hat",
        select_dlg=[
            "Ze~",
            "Tea time, tea time. Even if we have coffee, it's tea time. Ehehe~",
            "Eye of newt, toe of frog...",
            "Now where did I leave that broom..."
        ]
    )






    mas_acs_holly_hairclip = MASAccessory(
        "holly_hairclip",
        "holly_hairclip",
        MASPoseMap(
            default="0",
            l_default="5"
        ),
        stay_on_start=True,
        acs_type="left-hair-clip",
        
        rec_layer=MASMonika.AFH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_holly_hairclip)
    store.mas_selspr.init_selectable_acs(
        mas_acs_holly_hairclip,
        "Hairclip (Holly)",
        "holly_hairclip",
        "left-hair-clip",
        select_dlg=[
            "Ready to deck the halls, [player]?"
        ]
    )





    mas_acs_flower_crown = MASAccessory(
        "flower_crown",
        "flower_crown",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        acs_type="front-hair-flower-crown",
        priority=20,
        stay_on_start=True,
        rec_layer=MASMonika.PST_ACS,
    )
    store.mas_sprites.init_acs(mas_acs_flower_crown)




    mas_acs_promisering = MASAccessory(
        "promisering",
        "promisering",
        MASPoseMap(
            p1=None,
            p2="2",
            p3="3",
            p4=None,
            p5="5",
            p6=None,
            p7=None,
        ),
        stay_on_start=True,
        acs_type="ring",
        ex_props={
            "bare hands": True
        }
    )
    store.mas_sprites.init_acs(mas_acs_promisering)





    mas_acs_quetzalplushie = MASAccessory(
        "quetzalplushie",
        "quetzalplushie",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=False,
        acs_type="plush_q",
        mux_type=["plush_mid"] + store.mas_sprites.DEF_MUX_LD,
        entry_pp=store.mas_sprites._acs_quetzalplushie_entry,
        exit_pp=store.mas_sprites._acs_quetzalplushie_exit,
        keep_on_desk=True
    )
    store.mas_sprites.init_acs(mas_acs_quetzalplushie)





    mas_acs_quetzalplushie_antlers = MASAccessory(
        "quetzalplushie_antlers",
        "quetzalplushie_antlers",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        priority=12,
        stay_on_start=False,
        entry_pp=store.mas_sprites._acs_quetzalplushie_antlers_entry,
        keep_on_desk=True
    )




    mas_acs_center_quetzalplushie = MASAccessory(
        "quetzalplushie_mid",
        "quetzalplushie_mid",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=False,
        acs_type="plush_mid",
        mux_type=["plush_q"],
        keep_on_desk=True
    )
    store.mas_sprites.init_acs(mas_acs_center_quetzalplushie)





    mas_acs_quetzalplushie_santahat = MASAccessory(
        "quetzalplushie_santahat",
        "quetzalplushie_santahat",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        priority=11,
        stay_on_start=False,
        entry_pp=store.mas_sprites._acs_quetzalplushie_santahat_entry,
        keep_on_desk=True
    )
    store.mas_sprites.init_acs(mas_acs_quetzalplushie_santahat)





    mas_acs_ribbon_black = MASAccessory(
        "ribbon_black",
        "ribbon_black",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_black)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_black,
        "Ribbon (Black)",
        "ribbon_black",
        "ribbon",
        hover_dlg=[
            "That's pretty formal, [player]."
        ],
        select_dlg=[
            "Are we going somewhere special, [player]?"
        ]
    )




    mas_acs_ribbon_blank = MASAccessory(
        "ribbon_blank",
        "ribbon_blank",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_blank)





    mas_acs_ribbon_blue = MASAccessory(
        "ribbon_blue",
        "ribbon_blue",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_blue)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_blue,
        "Ribbon (Blue)",
        "ribbon_blue",
        "ribbon",
        hover_dlg=[
            "Like the ocean..."
        ],
        select_dlg=[
            "Great choice, [player]!"
        ]
    )





    mas_acs_ribbon_darkpurple = MASAccessory(
        "ribbon_dark_purple",
        "ribbon_dark_purple",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_darkpurple)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_darkpurple,
        "Ribbon (Dark Purple)",
        "ribbon_dark_purple",
        "ribbon",
        hover_dlg=[
            "I love that color!"
        ],
        select_dlg=[
            "Lavender is a nice change of pace."
        ]
    )





    mas_acs_ribbon_emerald = MASAccessory(
        "ribbon_emerald",
        "ribbon_emerald",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_emerald)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_emerald,
        "Ribbon (Emerald)",
        "ribbon_emerald",
        "ribbon",
        hover_dlg=[
            "I've always loved this color...",
        ],
        select_dlg=[
            "It's just like my eyes!"
        ]
    )




    mas_acs_ribbon_def = MASAccessory(
        "ribbon_def",
        "ribbon_def",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_def)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_def,
        "Ribbon (White)",
        "ribbon_def",
        "ribbon",
        hover_dlg=[
            "Do you miss my old ribbon, [player]?"
        ],
        select_dlg=[
            "Back to the classics!"
        ]
    )





    mas_acs_ribbon_gray = MASAccessory(
        "ribbon_gray",
        "ribbon_gray",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_gray)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_gray,
        "Ribbon (Gray)",
        "ribbon_gray",
        "ribbon",
        hover_dlg=[
            "Like a warm, rainy day..."
        ],
        select_dlg=[
            "That's a really unique color, [player]."
        ]
    )





    mas_acs_ribbon_green = MASAccessory(
        "ribbon_green",
        "ribbon_green",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_green)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_green,
        "Ribbon (Green)",
        "ribbon_green",
        "ribbon",
        hover_dlg=[
            "That's a lovely color!"
        ],
        select_dlg=[
            "Green, just like my eyes!"
        ]
    )





    mas_acs_ribbon_lightpurple = MASAccessory(
        "ribbon_light_purple",
        "ribbon_light_purple",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_lightpurple)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_lightpurple,
        "Ribbon (Light Purple)",
        "ribbon_light_purple",
        "ribbon",
        hover_dlg=[
            "This purple looks pretty nice, right [player]?"
        ],
        select_dlg=[
            "Really has a spring feel to it."
        ]
    )





    mas_acs_ribbon_peach = MASAccessory(
        "ribbon_peach",
        "ribbon_peach",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_peach)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_peach,
        "Ribbon (Peach)",
        "ribbon_peach",
        "ribbon",
        hover_dlg=[
            "That's beautiful!"
        ],
        select_dlg=[
            "Just like autumn leaves..."
        ]
    )





    mas_acs_ribbon_pink = MASAccessory(
        "ribbon_pink",
        "ribbon_pink",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_pink)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_pink,
        "Ribbon (Pink)",
        "ribbon_pink",
        "ribbon",
        hover_dlg=[
            "Looks cute, right?"
        ],
        select_dlg=[
            "Good choice!"
        ]
    )





    mas_acs_ribbon_platinum = MASAccessory(
        "ribbon_platinum",
        "ribbon_platinum",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_platinum)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_platinum,
        "Ribbon (Platinum)",
        "ribbon_platinum",
        "ribbon",
        hover_dlg=[
            "That's an interesting color, [player].",
        ],
        select_dlg=[
            "I'm quite fond of it, actually."
        ]
    )





    mas_acs_ribbon_red = MASAccessory(
        "ribbon_red",
        "ribbon_red",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_red)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_red,
        "Ribbon (Red)",
        "ribbon_red",
        "ribbon",
        hover_dlg=[
            "Red is a beautiful color!"
        ],
        select_dlg=[
            "Just like roses~"
        ]
    )





    mas_acs_ribbon_ruby = MASAccessory(
        "ribbon_ruby",
        "ribbon_ruby",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_ruby)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_ruby,
        "Ribbon (Ruby)",
        "ribbon_ruby",
        "ribbon",
        hover_dlg=[
            "That's a beautiful shade of red."
        ],
        select_dlg=[
            "Doesn't it look pretty?"
        ]
    )





    mas_acs_ribbon_sapphire = MASAccessory(
        "ribbon_sapphire",
        "ribbon_sapphire",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_sapphire)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_sapphire,
        "Ribbon (Sapphire)",
        "ribbon_sapphire",
        "ribbon",
        hover_dlg=[
            "Like a clear summer sky..."
        ],
        select_dlg=[
            "Nice choice, [player]!"
        ]
    )





    mas_acs_ribbon_silver = MASAccessory(
        "ribbon_silver",
        "ribbon_silver",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_silver)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_silver,
        "Ribbon (Silver)",
        "ribbon_silver",
        "ribbon",
        hover_dlg=[
            "I like the look of this one.",
            "I've always loved silver."
        ],
        select_dlg=[
            "Nice choice, [player]."
        ]
    )





    mas_acs_ribbon_teal = MASAccessory(
        "ribbon_teal",
        "ribbon_teal",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_teal)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_teal,
        "Ribbon (Teal)",
        "ribbon_teal",
        "ribbon",
        hover_dlg=[
            "Looks really summer-y, right?"
        ],
        select_dlg=[
            "Just like a summer sky."
        ]
    )





    mas_acs_ribbon_wine = MASAccessory(
        "ribbon_wine",
        "ribbon_wine",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_wine)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_wine,
        "Ribbon (Wine)",
        "ribbon_wine",
        "ribbon",
        hover_dlg=[
            "That's a great color!"
        ],
        select_dlg=[
            "Formal! Are you taking me somewhere special, [player]?"
        ]
    )





    mas_acs_ribbon_yellow = MASAccessory(
        "ribbon_yellow",
        "ribbon_yellow",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_yellow)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_yellow,
        "Ribbon (Yellow)",
        "ribbon_yellow",
        "ribbon",
        hover_dlg=[
            "This color reminds me of a nice summer day!"
        ],
        select_dlg=[
            "Great choice, [player]!"
        ]
    )





    mas_acs_roses = MASAccessory(
        "roses",
        "roses",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        priority=11,
        stay_on_start=False,
        acs_type="flowers",
        keep_on_desk=True
    )
    store.mas_sprites.init_acs(mas_acs_roses)









default persistent._mas_acs_enable_quetzalplushie = False



default persistent._mas_acs_enable_promisering = False
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
