import { Engine, Image, PyEngine } from "./winter.js";

// Some neat-O special effects

function _blurScreen(engine: Engine, factor: number) {
    // Grabs the screen, blurs it up a bit, then returns the image.
    // Returns tinier images.  Use scaleblit to bring them back.

    // Grossly inefficient.

    const w = Math.floor(engine.video.xres * factor)
    const h = Math.floor(engine.video.yres * factor)

    const bleh = engine.video.grabImage(0, 0, engine.video.xres, engine.video.yres)
    engine.video.scaleBlit(bleh, 0, 0, w, h)
    engine.video.freeImage(bleh)
    return engine.video.grabImage(0, 0, w, h)
}

export function createBlurImages(engineRef: PyEngine) {
    const engine = engineRef.getEngine()
    const BLEH = 1
    const images = []
    let i = 1.0
    while (i < 2) {
        const img = _blurScreen(engine, 1.0 / i)
        images.push(img)
        engine.video.scaleBlit(img, -BLEH, -BLEH, engine.video.xres + BLEH * 2, engine.video.yres + BLEH * 2)

        i += 0.1
    }

    return images
}

export function freeBlurImages(engineRef: PyEngine, images: Image[]) {
    const engine = engineRef.getEngine()
    images.forEach(img => {
        engine.video.freeImage(img)
    })
}

export function *blurFadeTask(engineRef: PyEngine, time: number, startImages: Image[], endImages: Image[]) {
    const engine = engineRef.getEngine()
    let now = engine.getTime()
    const startTime = now
    const endTime = now + time
    while (now < endTime) {
        const imageIndex = Math.floor((now - startTime) * startImages.length / time)
        const opacity = (now - startTime) / time

        engine.video.scaleBlit(startImages[imageIndex], 0, 0, engine.video.xres, engine.video.yres)
        engine.video.tintScaleBlit(endImages[endImages.length - (imageIndex + 1)], 0, 0, engine.video.xres, engine.video.yres, opacity)

        engine.video.showPage()
        yield null
        now = engine.getTime()
    }
}

function *_fadeTask(engineRef: PyEngine, time: number, startAlpha: number, endAlpha: number, draw: ()=>void) {
    const engine = engineRef.getEngine()
    const deltaAlpha = endAlpha - startAlpha

    let now = engine.getTime()
    const startTime = now
    const endtime = now + time

    while (now < endtime) {
        draw()
        const alpha = startAlpha + deltaAlpha * (now - startTime) / time
        engine.video.drawRect(0, 0, engine.video.xres, engine.video.yres, 0, 0, 0, alpha)

        engine.video.showPage()
        yield null
        now = engine.getTime()
    }
}

export function *fadeInTask(engineRef: PyEngine, time: number, draw: ()=>void) {
    yield *_fadeTask(engineRef, time, 1.0, 0.0, draw)
}

export function *fadeOutTask(engineRef: PyEngine, time: number, draw: ()=>void) {
    yield *_fadeTask(engineRef, time, 0.0, 1.0, draw)
}
