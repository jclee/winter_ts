# We don't just launch into system.py directly, since it confuses brython when
# modules imported by system try to circularly import system.
#
# TODO: Fix circular imports
import system
