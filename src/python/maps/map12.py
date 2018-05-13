def to11(engineRef):
    yield from engineRef.mapSwitchTask('map11.ika-map', (23 * 16, 17 * 16))

# Unused?
def heal(engineRef):
    engineRef.player.stats.hp = 999
    engineRef.player.stats.mp = 999
    if False:
        yield None
