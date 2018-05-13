# We don't just launch into system.py directly, since it confuses brython when
# modules imported by system try to circularly import system.
#
# TODO: Fix circular imports

import ika
import system

def main():
    ika.Run(
        task=system.mainTask(),
    )

if __name__ == '__main__':
    main()
