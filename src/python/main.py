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
        systemFontData=getSystemFontData()
    )

if __name__ == '__main__':
    main()
