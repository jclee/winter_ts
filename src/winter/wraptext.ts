import { Font } from "./winter.js";

// Miscillany
// coded by Andy Friesen
// copyright whenever.  All rights reserved.
//
// This source code may be used for any purpose, provided that
// the original author is never misrepresented in any way.
//
// There is no warranty, express or implied on the functionality, or
// suitability of this code for any purpose.

// wraps the text to the given pixel width, using the font specified.
// returns a list of strings

export function wrapText(text: string, maxWidth: number, font: Font) {
    const result: string[] = []
    let pos = 0
    let lastSpace = 0

    while (text.length > 0) {
        // find a space, tab, or newline.  whichever comes first.
        // if the word can be appended to the current line, append it.
        // if not, and the current line is not empty, put it on a new line.
        // if the word is longer than a single line, hack it wherever, and make the hunk its own line.

        // find the next space, tab, or newline.
        if (pos >= text.length) {    // hit the end of the string?
            result.push(text) // we're done.  add the last of it to the list
            break             // and break out
        }

        if (text[pos] === ' ') {
            lastSpace = pos
        }

        if (text[pos] === '\n') {      // newline.  Chop.
            result.push(text.slice(0, pos))
            text = text.slice(pos + 1)
            pos = 0
            lastSpace = 0
            continue
        }

        const l = font.stringWidth(text.slice(0, pos))

        if (l >= maxWidth) {        // too wide.  Go back to the last whitespace character, and chop
            if (lastSpace > 0) {
                result.push(text.slice(0, lastSpace))
                text = text.slice(lastSpace + 1)
                pos = 0
                lastSpace = 0
            } else {                       // no last space!  Hack right here, since the word is obviously too goddamn long.
                result.push(text.slice(0, pos))
                text = text.slice(pos + 1)
            }
            continue
        }

        pos += 1
    }

    return result
}
