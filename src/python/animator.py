from browser import window

def Animator():
    return window.Animator.new()

def makeAnim(strand, delay):
    """Quicky function to make a proper strand, given a
       list of frames, and a delay between each."""

    return list(zip(strand, [delay] * len(strand)))
