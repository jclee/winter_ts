# We don't just launch into system.py directly, since it confuses brython when
# modules imported by system try to circularly import system.
#
# TODO: Fix circular imports

import ika
import system

def getSystemFontData():
    return {
        'subsets': [
            (
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
                42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57,
                58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73,
                74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89,
                90, 91, 92, 93, 94, 95, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            ),
            (
                96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96,
                96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96,
                96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108,
                109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120,
                121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132,
                133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144,
                145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156,
                157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168,
                169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180,
                181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 96, 96,
                96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96,
                96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96,
                96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96,
                96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96,
                96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96,
                96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96,
                96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96,
                96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96
            )
        ],
        'widths': [
            7, 4, 7, 7, 7, 7, 7, 5, 5, 5, 7, 7, 4, 7, 4, 7, 7, 6, 7, 7, 7, 7,
            7, 7, 7, 7, 4, 4, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 7, 7,
            7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 4, 7,
            7, 7, 7, 7, 7, 7, 7, 4, 7, 7, 4, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9,
            7, 7, 7, 7, 7, 7, 7, 7, 7, 4, 7, 7, 7, 7, 7, 5, 5, 5, 7, 7, 4, 7,
            4, 7, 7, 6, 7, 7, 7, 7, 7, 7, 7, 7, 4, 4, 7, 7, 7, 7, 7, 7, 7, 7,
            7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
            7, 7, 7, 7, 7, 7, 4, 7, 7, 7, 7, 7, 7, 7, 7, 4, 7, 7, 4, 9, 7, 7,
            7, 7, 7, 7, 7, 7, 7, 9, 7, 7, 7, 7, 7, 7, 7, 7
        ],

        'heights': [
            10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
            10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
            10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
            10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
            10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
            10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
            10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
            10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
            10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
            10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
            10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
            10, 10, 10, 10, 10
        ]
    }


def main():
    ika.Run(
        task=system.mainTask(),
        mapsPath='winter/maps.json',
        spritesPath='winter/sprites.json',
        imagePaths=[
            'winter/gfx/gba.png',
            'winter/gfx/isabigfatbitch.png',
            #'winter/gfx/mountains.png',
            'winter/gfx/title.png',
            #'winter/gfx/ui/barhp0.png',
            #'winter/gfx/ui/barhp1.png',
            #'winter/gfx/ui/barhp2.png',
            #'winter/gfx/ui/barhp3.png',
            #'winter/gfx/ui/barmp0.png',
            #'winter/gfx/ui/barmp1.png',
            #'winter/gfx/ui/barmp2.png',
            #'winter/gfx/ui/barmp3.png',
            #'winter/gfx/ui/divider.png',
            #'winter/gfx/ui/font.png',
            #'winter/gfx/ui/font2.png',
            #'winter/gfx/ui/icon_att.png',
            #'winter/gfx/ui/icon_mag.png',
            #'winter/gfx/ui/icon_mres.png',
            #'winter/gfx/ui/icon_pres.png',
            #'winter/gfx/ui/icon_speed.png',
            #'winter/gfx/ui/item_dynamite.png',
            #'winter/gfx/ui/item_sword.png',
            #'winter/gfx/ui/meter.png',
            'winter/gfx/ui/pointer.png',
            #'winter/gfx/ui/rune_apoplexy.png',
            #'winter/gfx/ui/rune_quicken.png',
            #'winter/gfx/ui/rune_shield.png',
            #'winter/gfx/ui/rune_squall.png',
            #'winter/gfx/ui/rune_strike.png',
            #'winter/gfx/ui/rune_surge.png',
            #'winter/gfx/ui/rune_trinity.png',
            #'winter/gfx/ui/text_attributes.png',
            #'winter/gfx/ui/text_equip.png',
            #'winter/gfx/ui/text_exp.png',
            #'winter/gfx/ui/text_hp.png',
            #'winter/gfx/ui/text_items.png',
            #'winter/gfx/ui/text_lvl.png',
            #'winter/gfx/ui/text_menu.png',
            #'winter/gfx/ui/text_mp.png',
            #'winter/gfx/ui/text_spells.png',
            #'winter/gfx/ui/text_stats.png',
            #'winter/gfx/ui/win2_background.png',
            #'winter/gfx/ui/win2_bottom.png',
            #'winter/gfx/ui/win2_bottom_left.png',
            #'winter/gfx/ui/win2_bottom_right.png',
            #'winter/gfx/ui/win2_right.png',
            #'winter/gfx/ui/win2_top.png',
            #'winter/gfx/ui/win2_top_left.png',
            #'winter/gfx/ui/win2_top_right.png',
            'winter/gfx/ui/win_background.png',
            'winter/gfx/ui/win_bottom.png',
            'winter/gfx/ui/win_bottom_left.png',
            'winter/gfx/ui/win_bottom_right.png',
            'winter/gfx/ui/win_left.png',
            'winter/gfx/ui/win_right.png',
            'winter/gfx/ui/win_top.png',
            'winter/gfx/ui/win_top_left.png',
            'winter/gfx/ui/win_top_right.png',
            'winter/gfx/yourmother.png',
            'winter/snowy.png',
            'winter/sprite/anklebiter.png',
            'winter/sprite/boulder.png',
            'winter/sprite/carnivore.png',
            'winter/sprite/devourer.png',
            'winter/sprite/dragonpup.png',
            'winter/sprite/dynamite.png',
            'winter/sprite/firerune.png',
            'winter/sprite/gorilla.png',
            'winter/sprite/grandpa.png',
            'winter/sprite/guardrune.png',
            'winter/sprite/hellhound.png',
            'winter/sprite/hgap.png',
            'winter/sprite/ice.png',
            'winter/sprite/icecave.png',
            'winter/sprite/icechunks.png',
            'winter/sprite/kid1.png',
            'winter/sprite/kid2.png',
            'winter/sprite/kid3.png',
            'winter/sprite/powerrune.png',
            'winter/sprite/protagonist.png',
            'winter/sprite/razormane.png',
            'winter/sprite/rend.png',
            'winter/sprite/savepoint.png',
            'winter/sprite/serpent.png',
            'winter/sprite/soulreaver.png',
            'winter/sprite/strengthrune.png',
            'winter/sprite/vgap.png',
            'winter/sprite/waterrune.png',
            'winter/sprite/windrune.png',
            'winter/sprite/yeti.png',
            'winter/system_font.png',
        ],
        systemFontData=getSystemFontData()
    )

if __name__ == '__main__':
    main()
