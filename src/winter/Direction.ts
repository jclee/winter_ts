// TODO: consider using "const enum" once enum no longer used by Python?
export enum Direction {
    Left = 0,
    Right = 1,
    Up = 2,
    Down = 3,
    UpLeft = 4,
    UpRight = 5,
    DownLeft = 6,
    DownRight = 7,
}

export interface Delta {
    x: number
    y: number
}

// x/y displacements for each direction
const _deltas = {
    [Direction.Left]:      { x: -1, y:  0},
    [Direction.Right]:     { x:  1, y:  0},
    [Direction.Up]:        { x:  0, y: -1},
    [Direction.Down]:      { x:  0, y:  1},
    [Direction.UpLeft]:    { x: -1, y: -1},
    [Direction.UpRight]:   { x:  1, y: -1},
    [Direction.DownLeft]:  { x: -1, y:  1},
    [Direction.DownRight]: { x:  1, y:  1},
}

export const toDelta = (d:Direction): Delta => {
    return _deltas[d]
}

// opposite directions
const _invert = {
    [Direction.Left]:      Direction.Right,
    [Direction.Right]:     Direction.Left,
    [Direction.Up]:        Direction.Down,
    [Direction.Down]:      Direction.Up,
    [Direction.UpLeft]:    Direction.DownRight,
    [Direction.UpRight]:   Direction.DownLeft,
    [Direction.DownLeft]:  Direction.UpRight,
    [Direction.DownRight]: Direction.DownLeft,
}

export const invert = (d: Direction):Direction => {
    return _invert[d]
}

const _invertX = {
    [Direction.Left]:      Direction.Right,
    [Direction.Right]:     Direction.Left,
    [Direction.Up]:        Direction.Up,
    [Direction.Down]:      Direction.Down,
    [Direction.UpLeft]:    Direction.UpRight,
    [Direction.UpRight]:   Direction.UpLeft,
    [Direction.DownLeft]:  Direction.DownRight,
    [Direction.DownRight]: Direction.DownLeft,
}

const _invertY = {
    [Direction.Left]:      Direction.Left,
    [Direction.Right]:     Direction.Right,
    [Direction.Up]:        Direction.Down,
    [Direction.Down]:      Direction.Up,
    [Direction.UpLeft]:    Direction.DownLeft,
    [Direction.UpRight]:   Direction.DownRight,
    [Direction.DownLeft]:  Direction.UpLeft,
    [Direction.DownRight]: Direction.UpRight,
}

export const fromDelta = (dx: number, dy: number): Direction => {
    // -_-;

    if (dy === 0) {
        return (dx > 0) ? Direction.Right : Direction.Left
    } else if (dx === 0) {
        return (dy > 0) ? Direction.Down : Direction.Up
    } else {
        const m = Math.abs(dy / dx)
        let d: Direction
        if (m > 0.8) {
            d = Direction.Down
        } else if (m > 0.2) {
            d = Direction.DownRight
        } else {
            d = Direction.Right
        }

        if (dx < 0) {
            d = _invertX[d]
        }
        if (dy < 0) {
            d = _invertY[d]
        }
        return d
    }
}
