# We don't just launch into system.py directly, since it confuses brython when
# modules imported by system try to circularly import system.
#
# TODO: Fix circular imports

import ika
import system


def main():
    ika.Run(
        task=system.mainTask(),
        mapsPath='winter/maps.json',
        imagePaths=[
            'gfx/gba.png',
            'gfx/isabigfatbitch.png',
            #'gfx/mountains.png',
            'gfx/title.png',
            #'gfx/ui/barhp0.png',
            #'gfx/ui/barhp1.png',
            #'gfx/ui/barhp2.png',
            #'gfx/ui/barhp3.png',
            #'gfx/ui/barmp0.png',
            #'gfx/ui/barmp1.png',
            #'gfx/ui/barmp2.png',
            #'gfx/ui/barmp3.png',
            #'gfx/ui/divider.png',
            #'gfx/ui/font.png',
            #'gfx/ui/font2.png',
            #'gfx/ui/icon_att.png',
            #'gfx/ui/icon_mag.png',
            #'gfx/ui/icon_mres.png',
            #'gfx/ui/icon_pres.png',
            #'gfx/ui/icon_speed.png',
            #'gfx/ui/item_dynamite.png',
            #'gfx/ui/item_sword.png',
            #'gfx/ui/meter.png',
            'gfx/ui/pointer.png',
            #'gfx/ui/rune_apoplexy.png',
            #'gfx/ui/rune_quicken.png',
            #'gfx/ui/rune_shield.png',
            #'gfx/ui/rune_squall.png',
            #'gfx/ui/rune_strike.png',
            #'gfx/ui/rune_surge.png',
            #'gfx/ui/rune_trinity.png',
            #'gfx/ui/text_attributes.png',
            #'gfx/ui/text_equip.png',
            #'gfx/ui/text_exp.png',
            #'gfx/ui/text_hp.png',
            #'gfx/ui/text_items.png',
            #'gfx/ui/text_lvl.png',
            #'gfx/ui/text_menu.png',
            #'gfx/ui/text_mp.png',
            #'gfx/ui/text_spells.png',
            #'gfx/ui/text_stats.png',
            #'gfx/ui/win2_background.png',
            #'gfx/ui/win2_bottom.png',
            #'gfx/ui/win2_bottom_left.png',
            #'gfx/ui/win2_bottom_right.png',
            #'gfx/ui/win2_right.png',
            #'gfx/ui/win2_top.png',
            #'gfx/ui/win2_top_left.png',
            #'gfx/ui/win2_top_right.png',
            'gfx/ui/win_background.png',
            'gfx/ui/win_bottom.png',
            'gfx/ui/win_bottom_left.png',
            'gfx/ui/win_bottom_right.png',
            'gfx/ui/win_left.png',
            'gfx/ui/win_right.png',
            'gfx/ui/win_top.png',
            'gfx/ui/win_top_left.png',
            'gfx/ui/win_top_right.png',
            'gfx/yourmother.png',
            'winter/snowy.png',
            'winter/system_font.png',
        ],
    )

if __name__ == '__main__':
    main()
