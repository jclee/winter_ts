"use strict";
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = y[op[0] & 2 ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [0, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var __values = (this && this.__values) || function (o) {
    var m = typeof Symbol === "function" && o[Symbol.iterator], i = 0;
    if (m) return m.call(o);
    return {
        next: function () {
            if (o && i >= o.length) o = void 0;
            return { value: o && o[i++], done: !o };
        }
    };
};
var __read = (this && this.__read) || function (o, n) {
    var m = typeof Symbol === "function" && o[Symbol.iterator];
    if (!m) return o;
    var i = m.call(o), r, ar = [], e;
    try {
        while ((n === void 0 || n-- > 0) && !(r = i.next()).done) ar.push(r.value);
    }
    catch (error) { e = { error: error }; }
    finally {
        try {
            if (r && !r.done && (m = i["return"])) m.call(i);
        }
        finally { if (e) throw e.error; }
    }
    return ar;
};
var WinterSnow = (function () {
    function WinterSnow(xres, yres, count, velocity, colorValue) {
        this.xres = xres;
        this.yres = yres;
        this.count = count;
        this.velocity = velocity;
        this.flakes = [];
        for (var i = 0; i < this.count; ++i) {
            this.flakes.push({ x: 0, y: 0, vx: 0, life: 0 });
        }
        var r = colorValue & 0xff;
        var g = (colorValue >> 8) & 0xff;
        var b = (colorValue >> 16) & 0xff;
        this.colorPrefix = 'rgba(' + r + ', ' + g + ', ' + b + ', ';
        this.yRange = this.yres + velocity[1] * WinterSnow.MaxLife;
    }
    WinterSnow.prototype.reinitFlake = function (s) {
        s.x = Math.floor(Math.random() * this.xres);
        s.y = this.yres - Math.floor(Math.random() * this.yRange);
        s.vx = Math.floor(Math.random() * 3) - 1;
        s.life = Math.floor(Math.random() * WinterSnow.MaxLife);
    };
    WinterSnow.prototype.update = function () {
        for (var i = 0; i < this.count; ++i) {
            var p = this.flakes[i];
            p.x += p.vx + this.velocity[0];
            p.y += 1 + this.velocity[1];
            p.life -= 1;
            if (p.x < 0
                || p.x >= this.xres
                || p.y >= this.yres
                || p.life <= 0) {
                this.reinitFlake(p);
            }
        }
    };
    WinterSnow.prototype.draw = function (canvasEl) {
        var ctx = canvasEl.getContext('2d');
        if (ctx === null) {
            return;
        }
        ctx.imageSmoothingEnabled = false;
        try {
            for (var _a = __values(this.flakes), _b = _a.next(); !_b.done; _b = _a.next()) {
                var p = _b.value;
                var a = Math.sin(p.life / WinterSnow.MaxLife * Math.PI);
                ctx.fillStyle = this.colorPrefix + a + ')';
                ctx.fillRect(Math.floor(p.x), Math.floor(p.y), 1, 1);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_b && !_b.done && (_c = _a.return)) _c.call(_a);
            }
            finally { if (e_1) throw e_1.error; }
        }
        var e_1, _c;
    };
    WinterSnow.MaxLife = 50;
    return WinterSnow;
}());
window.WinterSnow = WinterSnow;
var Point = (function () {
    function Point() {
    }
    return Point;
}());
var Canvas = (function () {
    function Canvas(width, height, _el, _ctx) {
        this.width = width;
        this.height = height;
        this._el = _el;
        this._ctx = _ctx;
    }
    return Canvas;
}());
var RGB = function (r, g, b, a) {
    return ((Math.floor(r) & 0xff)
        | ((Math.floor(g) & 0xff) << 8)
        | ((Math.floor(b) & 0xff) << 16)
        | ((Math.floor(a) & 0xff) << 24));
};
window.RGB = RGB;
var _RGBAToCSS = function (colorValue) {
    var r = colorValue & 0xff;
    var g = (colorValue >> 8) & 0xff;
    var b = (colorValue >> 16) & 0xff;
    var a = ((colorValue >> 24) & 0xff) / 255.0;
    return "rgba(" + r + ", " + g + ", " + b + ", " + a + ")";
};
var _makeCanvasAndContext = function (width, height) {
    var el = window.document.createElement('canvas');
    el.width = width;
    el.height = height;
    var ctx = el.getContext('2d');
    if (ctx === null) {
        throw new Error("Couldn't get 2D context");
    }
    ctx.mozImageSmoothingEnabled = false;
    ctx.webkitImageSmoothingEnabled = false;
    ctx.imageSmoothingEnabled = false;
    ctx.save();
    return [el, ctx];
};
var Entity = (function () {
    function Entity(x, y, layer, spritename, name, spriteData, engine) {
        this.x = x;
        this.y = y;
        this.layer = layer;
        this.spritename = spritename;
        this.name = name;
        this._getEngine = function () { return engine; };
        this.specframe = -1;
        this.name = name;
        this.speed = 100;
        this.isobs = true;
        this.mapobs = true;
        this.entobs = true;
        this.spritewidth = spriteData.width;
        this.spriteheight = spriteData.height;
        this.hotx = spriteData.hotspotX;
        this.hoty = spriteData.hotspotY;
        this.hotwidth = spriteData.hotspotWidth;
        this.hotheight = spriteData.hotspotHeight;
        this._direction = 'down';
        this.isMoving = false;
        this._delayCount = 0;
        this._speedCount = 0;
        this.destLocation = new Point();
        this.destVector = new Point();
    }
    Entity.prototype.MoveTo = function (x, y) {
        this.destLocation.x = x;
        this.destLocation.y = y;
        this.destVector.x = x - this.x;
        this.destVector.y = y - this.y;
        this._delayCount = 0;
        this.isMoving = this.destVector.x != 0 || this.destVector.y != 0;
    };
    Entity.prototype.Stop = function () {
        this.destLocation.x = this.x;
        this.destLocation.y = this.y;
        this.destVector.x = 0;
        this.destVector.y = 0;
        this.isMoving = false;
    };
    Entity.prototype.Update = function () {
        var newDir = '';
        if (this._delayCount > 0) {
            this._delayCount -= 1;
        }
        else if (this.destVector.x != 0 || this.destVector.y != 0) {
            var startX = this.destLocation.x - this.destVector.x;
            var startY = this.destLocation.y - this.destVector.y;
            var dx = this.x - this.destLocation.x;
            var dy = this.y - this.destLocation.y;
            if (dx == 0) {
                if (this.y > this.destLocation.y) {
                    newDir = 'up';
                }
                else if (this.y < this.destLocation.y) {
                    newDir = 'down';
                }
                else {
                    newDir = '';
                }
            }
            else if (dy == 0) {
                if (this.x > this.destLocation.x) {
                    newDir = 'left';
                }
                else if (this.x < this.destLocation.x) {
                    newDir = 'right';
                }
                else {
                    newDir = '';
                }
            }
            else {
                var m = this.destVector.y / this.destVector.x;
                var targetY = Math.floor(Math.floor((this.x - startX) * m) + startY);
                var deltaY = Math.abs(this.y - targetY);
                if (deltaY == 0) {
                    var tempX;
                    if (this.x > this.destLocation.x) {
                        newDir = 'left';
                        tempX = this.x - 1;
                    }
                    else {
                        newDir = 'right';
                        tempX = this.x + 1;
                    }
                    targetY = Math.floor((tempX - startX) * m) + startY;
                    deltaY = Math.abs(this.y - targetY);
                }
                if (deltaY == 1) {
                    if (this.y > this.destLocation.y) {
                        if (this.x > this.destLocation.x) {
                            newDir = 'upleft';
                        }
                        else {
                            newDir = 'upright';
                        }
                    }
                    else {
                        if (this.x > this.destLocation.x) {
                            newDir = 'downleft';
                        }
                        else {
                            newDir = 'downright';
                        }
                    }
                }
                else if (deltaY > 1) {
                    if (this.y > this.destLocation.y) {
                        newDir = 'up';
                    }
                    else {
                        newDir = 'down';
                    }
                }
            }
        }
        if (newDir == '') {
            this.Stop();
        }
        else {
            this._Move(newDir);
        }
    };
    Entity.prototype._MoveDiagonally = function (d) {
        var d1 = '';
        var d2 = '';
        if (d == 'upleft') {
            ;
            _a = __read(['up', 'left'], 2), d1 = _a[0], d2 = _a[1];
        }
        else if (d == 'upright') {
            ;
            _b = __read(['up', 'right'], 2), d1 = _b[0], d2 = _b[1];
        }
        else if (d == 'downleft') {
            ;
            _c = __read(['down', 'left'], 2), d1 = _c[0], d2 = _c[1];
        }
        else if (d == 'downright') {
            ;
            _d = __read(['down', 'right'], 2), d1 = _d[0], d2 = _d[1];
        }
        else {
            return d;
        }
        var newX = this.x + (d2 == 'left' ? -1 : 1);
        var newY = this.y + (d1 == 'up' ? -1 : 1);
        if (this._isObstructedAt(this.x, newY)) {
            d1 = '';
        }
        if (this._isObstructedAt(newX, this.y)) {
            d2 = '';
        }
        if (d1 == '') {
            return d2;
        }
        if (d2 == '') {
            return d1;
        }
        if (d1 == 'up') {
            return (d2 == 'left' ? 'upleft' : 'upright');
        }
        else {
            return (d2 == 'left' ? 'downleft' : 'downright');
        }
        var _a, _b, _c, _d;
    };
    Entity.prototype._Move = function (newDir) {
        var moveDir = this._MoveDiagonally(newDir);
        this._direction = newDir;
        this.isMoving = true;
        var newX = this.x;
        var newY = this.y;
        if (moveDir == 'up') {
            newY -= 1;
        }
        else if (moveDir == 'down') {
            newY += 1;
        }
        else if (moveDir == 'left') {
            newX -= 1;
        }
        else if (moveDir == 'right') {
            newX += 1;
        }
        else if (moveDir == 'upleft') {
            newY -= 1;
            newX -= 1;
        }
        else if (moveDir == 'upright') {
            newY -= 1;
            newX += 1;
        }
        else if (moveDir == 'downleft') {
            newY += 1;
            newX -= 1;
        }
        else if (moveDir == 'downright') {
            newY += 1;
            newX += 1;
        }
        if (this._isObstructedAt(newX, newY)) {
            this.Stop();
            return;
        }
        this.x = newX;
        this.y = newY;
    };
    Entity.prototype._isObstructedAt = function (x, y) {
        var engine = this._getEngine();
        return ((this.mapobs && engine.detectMapCollision(x, y, this.hotwidth, this.hotheight, this.layer))
            || (this.entobs && engine.detectEntityCollision(this.name, x, y, this.hotwidth, this.hotheight, this.layer)));
    };
    Entity.prototype.Touches = function (otherEnt) {
        var x1 = this.x;
        var y1 = this.y;
        var w = this.hotwidth;
        var h = this.hotheight;
        if (x1 > otherEnt.x + otherEnt.hotwidth ||
            y1 > otherEnt.y + otherEnt.hotheight ||
            x1 + w < otherEnt.x ||
            y1 + h < otherEnt.y) {
            return false;
        }
        else {
            return true;
        }
    };
    return Entity;
}());
var FontClass = (function () {
    function FontClass(_engine) {
        this._engine = _engine;
        this.height = 10;
    }
    FontClass.prototype.CenterPrint = function (x, y, text) {
        this.Print(x - this.StringWidth(text) / 2, y, text);
    };
    FontClass.prototype.StringWidth = function (s) {
        var w = 0;
        try {
            for (var _a = __values(this._genGlyphs(s)), _b = _a.next(); !_b.done; _b = _a.next()) {
                var glyph = _b.value;
                w += glyph.width;
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (_b && !_b.done && (_c = _a.return)) _c.call(_a);
            }
            finally { if (e_2) throw e_2.error; }
        }
        return w;
        var e_2, _c;
    };
    FontClass.prototype.PrintWithOpacity = function (x, y, text, opacity) {
        var ctx = this._engine.ctx;
        ctx.save();
        ctx.globalAlpha = opacity / 255.0;
        this.Print(x, y, text);
        ctx.restore();
    };
    FontClass.prototype.Print = function (x, y, text) {
        var imageEl = this._engine.getImageEl('system_font.png');
        var cursorX = Math.floor(x);
        var cursorY = Math.floor(y);
        try {
            for (var _a = __values(this._genGlyphs(text)), _b = _a.next(); !_b.done; _b = _a.next()) {
                var glyph = _b.value;
                this._engine.ctx.drawImage(imageEl, glyph.tileX, glyph.tileY, glyph.width, glyph.height, cursorX, cursorY, glyph.width, glyph.height);
                cursorX += glyph.width;
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (_b && !_b.done && (_c = _a.return)) _c.call(_a);
            }
            finally { if (e_3) throw e_3.error; }
        }
        var e_3, _c;
    };
    FontClass.prototype._genGlyphs = function (text) {
        var subsets, widths, heights, index, subsetIndex, ch, subsetCh, glyphIndex;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    subsets = this._engine.systemFontData.subsets;
                    widths = this._engine.systemFontData.widths;
                    heights = this._engine.systemFontData.heights;
                    index = 0;
                    subsetIndex = 0;
                    _a.label = 1;
                case 1:
                    if (!(index < text.length)) return [3, 3];
                    ch = text.charAt(index);
                    index += 1;
                    if (ch === '\n' || ch === '\t') {
                        throw new Error("String codes not implemented");
                    }
                    if (ch == '~' && index < text.length) {
                        subsetCh = text.charAt(index);
                        if (subsetCh >= '0' && subsetCh <= '9') {
                            index += 1;
                            subsetIndex = subsetCh.charCodeAt(0) - '0'.charCodeAt(0);
                            return [3, 1];
                        }
                    }
                    glyphIndex = subsets[subsetIndex][ch.charCodeAt(0)];
                    return [4, {
                            width: widths[glyphIndex],
                            height: heights[glyphIndex],
                            tileX: (glyphIndex % 16) * 9,
                            tileY: Math.floor(glyphIndex / 16) * 10,
                        }];
                case 2:
                    _a.sent();
                    return [3, 1];
                case 3: return [2];
            }
        });
    };
    return FontClass;
}());
window.FontClass = FontClass;
var MapClass = (function () {
    function MapClass(_engine, _video) {
        this._engine = _engine;
        this._video = _video;
        this._spriteID = 0;
        this.entities = {};
        this.mapEntityNames_ = [];
    }
    Object.defineProperty(MapClass.prototype, "xwin", {
        get: function () {
            return this._xwin;
        },
        set: function (x) {
            this._setCamera(x, this._ywin);
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(MapClass.prototype, "ywin", {
        get: function () {
            return this._ywin;
        },
        set: function (y) {
            this._setCamera(this._xwin, y);
        },
        enumerable: true,
        configurable: true
    });
    MapClass.prototype._setCamera = function (x, y) {
        var mapData = this._engine.getMapData(this._currentMapName);
        var dimensions = mapData.header.dimensions;
        var width = dimensions.width;
        var height = dimensions.height;
        if (width > 0) {
            this._xwin = Math.max(0, Math.min(width - this._video.xres - 1, x));
        }
        else {
            this._xwin = x;
        }
        if (height > 0) {
            this._ywin = Math.max(0, Math.min(height - this._video.yres - 1, y));
        }
        else {
            this._ywin = y;
        }
    };
    MapClass.prototype.Render = function () {
        var mapData = this._engine.getMapData(this._currentMapName);
        var tileW = 16;
        var tileH = 16;
        var tilesPerRow = 16;
        var layerCount = mapData.layers.length;
        var layerEnts = [];
        for (var i = 0; i < layerCount; ++i) {
            layerEnts.push([]);
        }
        for (var key in this.entities) {
            var ent = this.entities[key];
            layerEnts[ent.layer].push([ent.y, ent]);
        }
        try {
            for (var layerEnts_1 = __values(layerEnts), layerEnts_1_1 = layerEnts_1.next(); !layerEnts_1_1.done; layerEnts_1_1 = layerEnts_1.next()) {
                var layerEnt = layerEnts_1_1.value;
                layerEnt.sort();
            }
        }
        catch (e_4_1) { e_4 = { error: e_4_1 }; }
        finally {
            try {
                if (layerEnts_1_1 && !layerEnts_1_1.done && (_a = layerEnts_1.return)) _a.call(layerEnts_1);
            }
            finally { if (e_4) throw e_4.error; }
        }
        var imageEl = this._engine.getImageEl('snowy.png');
        for (var i = 0; i < layerCount; ++i) {
            var layer = mapData.layers[i];
            var xw = Math.floor(this._xwin * layer.parallax.mulx / layer.parallax.divx);
            var yw = Math.floor(this._ywin * layer.parallax.muly / layer.parallax.divy);
            var firstX = Math.floor(xw / tileW);
            var firstY = Math.floor(yw / tileH);
            var adjustX = xw % tileW;
            var adjustY = yw % tileH;
            var w = layer.dimensions.width;
            var h = layer.dimensions.height;
            var lenX = Math.floor(this._video.xres / tileW) + 1;
            var lenY = Math.floor(this._video.yres / tileH) + 2;
            if (firstX < 0) {
                lenX -= -firstX;
                adjustX += firstX * tileW;
                firstX = 0;
            }
            if (firstY < 0) {
                lenY -= -firstY;
                adjustY += firstY * tileH;
                firstY = 0;
            }
            if (firstX + lenX > w) {
                lenX = w - firstX;
            }
            if (firstY + lenY > h) {
                lenY = h - firstY;
            }
            var localLayerData = this._localLayerDatas[i];
            for (var y = 0; y < lenY; ++y) {
                for (var x = 0; x < lenX; ++x) {
                    var index = (firstY + y) * w + (firstX + x);
                    var tileIndex = localLayerData[index];
                    var tileX = (tileIndex % tilesPerRow) * tileW;
                    var tileY = Math.floor(tileIndex / tilesPerRow) * tileH;
                    this._engine.ctx.drawImage(imageEl, tileX, tileY, tileW, tileH, x * tileW - adjustX, y * tileH - adjustY, tileW, tileH);
                }
            }
            try {
                for (var _b = __values(layerEnts[i]), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var _d = __read(_c.value, 2), _ = _d[0], ent = _d[1];
                    var spritePath = 'sprite/' + ent.spritename.replace('.ika-sprite', '.png');
                    var spriteImageEl = this._engine.getImageEl(spritePath);
                    var frameIndex = Math.max(0, ent.specframe);
                    var frameX = (frameIndex % 8) * ent.spritewidth;
                    var frameY = Math.floor(frameIndex / 8) * ent.spriteheight;
                    this._engine.ctx.drawImage(spriteImageEl, frameX, frameY, ent.spritewidth, ent.spriteheight, ent.x - ent.hotx - xw, ent.y - ent.hoty - yw, ent.spritewidth, ent.spriteheight);
                }
            }
            catch (e_5_1) { e_5 = { error: e_5_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_e = _b.return)) _e.call(_b);
                }
                finally { if (e_5) throw e_5.error; }
            }
        }
        var e_4, _a, e_5, _e;
    };
    MapClass.prototype.SetTile = function (x, y, layerIndex, tileIndex) {
        var mapData = this._engine.getMapData(this._currentMapName);
        var layer = mapData.layers[layerIndex];
        var localLayerData = this._localLayerDatas[layerIndex];
        var index = y * layer.dimensions.width + x;
        localLayerData[index] = tileIndex;
    };
    MapClass.prototype.SetObs = function (x, y, layerIndex, obs) {
        var mapData = this._engine.getMapData(this._currentMapName);
        var layer = mapData.layers[layerIndex];
        var localLayerObstructions = this._localLayerObstructions[layerIndex];
        var index = y * layer.dimensions.width + x;
        localLayerObstructions[index] = obs;
    };
    MapClass.prototype.Switch = function (path) {
        this.clearMapEntities();
        this._currentMapName = path.replace('maps/', '').replace('.ika-map', '');
        this._xwin = 0;
        this._ywin = 0;
        var mapData = this._engine.getMapData(this._currentMapName);
        this.layercount = mapData.layers.length;
        this._localLayerDatas = [];
        this._localLayerObstructions = [];
        for (var i = 0; i < mapData.layers.length; ++i) {
            var layer = mapData.layers[i];
            this._localLayerDatas.push(layer.data.slice(0));
            this._localLayerObstructions.push(layer.obstructions.slice(0));
        }
        for (var i = 0; i < mapData.layers.length; ++i) {
            var layer = mapData.layers[i];
            try {
                for (var _a = __values(layer.entities), _b = _a.next(); !_b.done; _b = _a.next()) {
                    var entity = _b.value;
                    var spriteData = this._engine.sprites[entity.sprite];
                    var ent = new Entity(entity.x, entity.y, i, entity.sprite, entity.label, spriteData, this._engine);
                    this.entities[ent.name] = ent;
                    this.mapEntityNames_.push(ent.name);
                }
            }
            catch (e_6_1) { e_6 = { error: e_6_1 }; }
            finally {
                try {
                    if (_b && !_b.done && (_c = _a.return)) _c.call(_a);
                }
                finally { if (e_6) throw e_6.error; }
            }
        }
        var e_6, _c;
    };
    MapClass.prototype.GetMetaData = function () {
        var mapData = this._engine.getMapData(this._currentMapName);
        return mapData.information.meta;
    };
    MapClass.prototype.GetZones = function (layerIndex) {
        var zoneTuples = [];
        var mapData = this._engine.getMapData(this._currentMapName);
        try {
            for (var _a = __values(mapData.layers[layerIndex].zones), _b = _a.next(); !_b.done; _b = _a.next()) {
                var zone = _b.value;
                var scriptName = null;
                try {
                    for (var _c = __values(mapData.zones), _d = _c.next(); !_d.done; _d = _c.next()) {
                        var zoneMetadata = _d.value;
                        if (zoneMetadata.label === zone.label) {
                            scriptName = zoneMetadata.script;
                            break;
                        }
                    }
                }
                catch (e_7_1) { e_7 = { error: e_7_1 }; }
                finally {
                    try {
                        if (_d && !_d.done && (_e = _c.return)) _e.call(_c);
                    }
                    finally { if (e_7) throw e_7.error; }
                }
                zoneTuples.push([
                    zone.x,
                    zone.y,
                    zone.width,
                    zone.height,
                    scriptName
                ]);
            }
        }
        catch (e_8_1) { e_8 = { error: e_8_1 }; }
        finally {
            try {
                if (_b && !_b.done && (_f = _a.return)) _f.call(_a);
            }
            finally { if (e_8) throw e_8.error; }
        }
        return zoneTuples;
        var e_8, _f, e_7, _e;
    };
    MapClass.prototype.FindLayerByName = function (name) {
        var mapData = this._engine.getMapData(this._currentMapName);
        for (var i = 0; i < mapData.layers.length; ++i) {
            var layer = mapData.layers[i];
            if (layer.label === name) {
                return i;
            }
        }
        return null;
    };
    MapClass.prototype.addEntity = function (x, y, layer, spritename) {
        this._spriteID += 1;
        var name = "sprite_" + this._spriteID;
        var spriteData = this._engine.sprites[spritename];
        var ent = new Entity(x, y, layer, spritename, name, spriteData, this._engine);
        this.entities[ent.name] = ent;
        return ent;
    };
    MapClass.prototype.RemoveEntity = function (entity) {
        delete this.entities[entity.name];
    };
    MapClass.prototype.clearMapEntities = function () {
        try {
            for (var _a = __values(this.mapEntityNames_), _b = _a.next(); !_b.done; _b = _a.next()) {
                var name_1 = _b.value;
                delete this.entities[name_1];
            }
        }
        catch (e_9_1) { e_9 = { error: e_9_1 }; }
        finally {
            try {
                if (_b && !_b.done && (_c = _a.return)) _c.call(_a);
            }
            finally { if (e_9) throw e_9.error; }
        }
        this.mapEntityNames_ = [];
        var e_9, _c;
    };
    MapClass.prototype.EntitiesAt = function (x, y, width, height, layer) {
        var x2 = x + width;
        var y2 = y + height;
        var found = [];
        for (var key in this.entities) {
            var ent = this.entities[key];
            if (ent.layer != layer) {
                continue;
            }
            if (x > ent.x + ent.hotwidth) {
                continue;
            }
            if (y > ent.y + ent.hotheight) {
                continue;
            }
            if (x2 < ent.x) {
                continue;
            }
            if (y2 < ent.y) {
                continue;
            }
            found.push(ent);
        }
        return found;
    };
    MapClass.prototype.ProcessEntities = function () {
        var _TIME_RATE = 100;
        for (var key in this.entities) {
            var ent = this.entities[key];
            ent._speedCount += ent.speed;
            while (ent._speedCount >= _TIME_RATE) {
                ent.Update();
                ent._speedCount -= _TIME_RATE;
            }
        }
    };
    return MapClass;
}());
window.MapClass = MapClass;
var VideoClass = (function () {
    function VideoClass(engine) {
        this.xres = 320;
        this.yres = 240;
        this._getEngine = function () { return engine; };
    }
    VideoClass.prototype._assertBlendmodeSupported = function (blendmode) {
        var Opaque = 0;
        var Matte = 1;
        if (blendmode !== undefined && blendmode != Opaque && blendmode != Matte) {
            throw new Error("Unsupported blendmode");
        }
    };
    VideoClass.prototype.Blit = function (image, x, y, blendmode) {
        this._assertBlendmodeSupported(blendmode);
        this._getEngine().ctx.drawImage(image._el, x, y);
    };
    VideoClass.prototype.ClearScreen = function () {
        this._getEngine().ctx.fillStyle = 'rgb(0, 0, 0)';
        this._getEngine().ctx.fillRect(0, 0, this._getEngine().width, this._getEngine().height);
    };
    VideoClass.prototype.ResetClipScreen = function () {
        this._getEngine().ctx.restore();
        this._getEngine().ctx.save();
    };
    VideoClass.prototype.ClipScreen = function (left, top, right, bottom) {
        this.ResetClipScreen();
        if (left !== undefined && top !== undefined && right !== undefined && bottom !== undefined) {
            this._getEngine().ctx.rect(left, top, right - left, bottom - top);
            this._getEngine().ctx.clip();
        }
    };
    VideoClass.prototype.DrawPixel = function (x, y, colour, blendmode) {
        this._assertBlendmodeSupported(blendmode);
        this._getEngine().ctx.fillStyle = _RGBAToCSS(colour);
        this._getEngine().ctx.fillRect(x, y, 1, 1);
    };
    VideoClass.prototype.DrawRect = function (x1, y1, x2, y2, colour, fill, blendmode) {
        this._assertBlendmodeSupported(blendmode);
        if (fill) {
            this._getEngine().ctx.fillStyle = _RGBAToCSS(colour);
            this._getEngine().ctx.fillRect(x1, y1, x2 - x1 + 1, y2 - y1 + 1);
        }
        else {
            throw new Error("unfilled DrawRect not implemented");
        }
    };
    VideoClass.prototype.GrabImage = function (x1, y1, x2, y2) {
        var width = x2 - x1;
        var height = y2 - y1;
        var canvasEl;
        var ctx;
        _a = __read(_makeCanvasAndContext(width, height), 2), canvasEl = _a[0], ctx = _a[1];
        ctx.drawImage(this._getEngine().canvasEl, -x1, -y1);
        return new Canvas(width, height, canvasEl, ctx);
        var _a;
    };
    VideoClass.prototype.ScaleBlit = function (image, x, y, width, height, blendmode) {
        this._assertBlendmodeSupported(blendmode);
        this._getEngine().ctx.drawImage(image._el, 0, 0, image.width, image.height, x, y, width, height);
    };
    VideoClass.prototype.ShowPage = function () {
        this._getEngine().displayCtx.drawImage(this._getEngine().canvasEl, 0, 0);
    };
    VideoClass.prototype.TintBlit = function (image, x, y, tintColor, blendMode) {
        this._getEngine().ctx.save();
        this._getEngine().ctx.globalAlpha = ((tintColor >> 24) & 0xff) / 255.0;
        this.Blit(image, x, y, blendMode);
        this._getEngine().ctx.restore();
    };
    VideoClass.prototype.TintDistortBlit = function (image, upLeft, _upRight, downRight, _downLeft, blendmode) {
        this._getEngine().ctx.save();
        var tintColor = upLeft[2];
        this._getEngine().ctx.globalAlpha = ((tintColor >> 24) & 0xff) / 255.0;
        this.ScaleBlit(image, upLeft[0], upLeft[1], downRight[0] - upLeft[0], downRight[1] - upLeft[1], blendmode);
        this._getEngine().ctx.restore();
    };
    VideoClass.prototype.DrawTriangle = function (v1, v2, v3) {
        var ctx = this._getEngine().ctx;
        var dx = v3[0] - v2[0];
        var dy = v3[1] - v2[1];
        var len = Math.sqrt(dx * dx + dy * dy);
        var ndx = dx / len;
        var ndy = dy / len;
        var dx1 = v1[0] - v2[0];
        var dy1 = v1[1] - v2[1];
        var projLen = dx1 * ndx + dy1 * ndy;
        var projx = ndx * projLen;
        var projy = ndy * projLen;
        var x2 = dx1 - projx;
        var y2 = dy1 - projy;
        var gradientEndX = v1[0] - x2;
        var gradientEndY = v1[1] - y2;
        var gradient = ctx.createLinearGradient(v1[0], v1[1], gradientEndX, gradientEndY);
        gradient.addColorStop(0, 'rgb(0, 0, 0)');
        gradient.addColorStop(1, 'rgb(0, 0, 0, 0)');
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.moveTo(v1[0], v1[1]);
        ctx.lineTo(v2[0], v2[1]);
        ctx.lineTo(v3[0], v3[1]);
        ctx.fill();
    };
    return VideoClass;
}());
window.VideoClass = VideoClass;
var Engine = (function () {
    function Engine(_getKey) {
        this._getKey = _getKey;
        this.imageEls = {};
        this.maps = {};
        this.sprites = {};
        this._video = new VideoClass(this);
        this.map = new MapClass(this, this._video);
    }
    Engine.prototype.run = function (taskFn, mapsPath, spritesPath, imagePaths, systemFontData) {
        var _this = this;
        this.startMsec = Date.now();
        this.width = 320;
        this.height = 240;
        this.systemFontData = systemFontData;
        _a = __read(_makeCanvasAndContext(this.width, this.height), 2), this.canvasEl = _a[0], this.ctx = _a[1];
        _b = __read(_makeCanvasAndContext(this.width, this.height), 2), this.displayCanvasEl = _b[0], this.displayCtx = _b[1];
        var style = this.displayCanvasEl.style;
        style.border = "1px solid";
        style.imageRendering = "optimizeSpeed";
        style.imageRendering = "-moz-crisp-edges";
        style.imageRendering = "pixelated";
        style.width = "" + this.width * 2;
        style.height = "" + this.height * 2;
        style.display = "block";
        style.marginLeft = "auto";
        style.marginRight = "auto";
        window.document.body.appendChild(this.displayCanvasEl);
        window.document.body.style.backgroundColor = "#dddddd";
        var promises = [];
        var _loop_1 = function (path) {
            var loadImage = function (resolve, _reject) {
                var imageEl = window.document.createElement('img');
                imageEl.addEventListener('load', resolve);
                imageEl.src = path;
                _this.imageEls[path] = imageEl;
                imageEl.style.position = "absolute";
                imageEl.style.top = "0";
                imageEl.style.left = "0";
                imageEl.style.opacity = "0";
                window.document.body.appendChild(imageEl);
            };
            promises.push(new Promise(loadImage));
        };
        try {
            for (var imagePaths_1 = __values(imagePaths), imagePaths_1_1 = imagePaths_1.next(); !imagePaths_1_1.done; imagePaths_1_1 = imagePaths_1.next()) {
                var path = imagePaths_1_1.value;
                _loop_1(path);
            }
        }
        catch (e_10_1) { e_10 = { error: e_10_1 }; }
        finally {
            try {
                if (imagePaths_1_1 && !imagePaths_1_1.done && (_c = imagePaths_1.return)) _c.call(imagePaths_1);
            }
            finally { if (e_10) throw e_10.error; }
        }
        var loadJson = function (path) {
            var fn = function (resolve, _reject) {
                var xhr = new XMLHttpRequest();
                var onLoad = function () {
                    var json = JSON.parse(xhr.responseText);
                    resolve(json);
                };
                xhr.addEventListener('load', onLoad);
                xhr.open('GET', path);
                xhr.send();
            };
            return new Promise(fn);
        };
        var setMapJson = function (json) {
            _this.maps = json;
        };
        var setSpriteJson = function (json) {
            _this.sprites = json;
        };
        promises.push(loadJson(mapsPath).then(setMapJson));
        promises.push(loadJson(spritesPath).then(setSpriteJson));
        var _KeycodeMap = {
            'ArrowUp': 'UP',
            'ArrowDown': 'DOWN',
            'ArrowRight': 'RIGHT',
            'ArrowLeft': 'LEFT',
            'Enter': 'ENTER',
            'Escape': 'ESCAPE',
            ' ': 'SPACE',
            'Z': 'Z',
            'z': 'Z',
            'X': 'X',
            'x': 'X',
            'C': 'C',
            'c': 'C',
            'V': 'V',
            'v': 'V',
            'B': 'B',
            'b': 'B',
            'N': 'N',
            'n': 'N',
            'M': 'M',
            'm': 'M',
        };
        var onKeyDown = function (event) {
            if (event.defaultPrevented) {
                return;
            }
            if (!(event.key in _KeycodeMap)) {
                return;
            }
            var control = _this._getKey(_KeycodeMap[event.key]);
            control._pressed = 1;
            control._position = 1;
            event.preventDefault();
        };
        var onKeyUp = function (event) {
            if (event.defaultPrevented) {
                return;
            }
            if (!(event.key in _KeycodeMap)) {
                return;
            }
            var control = _this._getKey(_KeycodeMap[event.key]);
            control._position = 0;
            event.preventDefault();
        };
        window.addEventListener('keydown', onKeyDown, true);
        window.addEventListener('keyup', onKeyUp, true);
        var runFrame = function (_timestamp) {
            if (taskFn()) {
                window.requestAnimationFrame(runFrame);
            }
            else {
                console.log("Engine done.");
            }
        };
        var startEngine = function () {
            console.log("Starting engine...");
            window.requestAnimationFrame(runFrame);
        };
        Promise.all(promises).then(startEngine);
        var _a, _b, e_10, _c;
    };
    Engine.prototype.getMapData = function (mapName) {
        var mapData = this.maps[mapName];
        if (!mapData) {
            throw new Error("Map data not found");
        }
        return mapData;
    };
    Engine.prototype.getImageEl = function (imagePath) {
        var imageEl = this.imageEls['winter/' + imagePath];
        if (!imageEl) {
            throw new Error("Image element not found:" + imagePath);
        }
        return imageEl;
    };
    Engine.prototype.getImage = function (imagePath) {
        var el = this.getImageEl(imagePath);
        return {
            _el: el,
            width: el.width,
            height: el.height,
        };
    };
    Engine.prototype.detectEntityCollision = function (entName, x, y, w, h, layerIndex) {
        var ents = this.map.EntitiesAt(x + 1, y + 1, w - 2, h - 2, layerIndex);
        try {
            for (var ents_1 = __values(ents), ents_1_1 = ents_1.next(); !ents_1_1.done; ents_1_1 = ents_1.next()) {
                var ent = ents_1_1.value;
                if (ent.isobs && ent.name != entName) {
                    return true;
                }
            }
        }
        catch (e_11_1) { e_11 = { error: e_11_1 }; }
        finally {
            try {
                if (ents_1_1 && !ents_1_1.done && (_a = ents_1.return)) _a.call(ents_1);
            }
            finally { if (e_11) throw e_11.error; }
        }
        return false;
        var e_11, _a;
    };
    Engine.prototype.detectMapCollision = function (x, y, w, h, layerIndex) {
        var tileW = 16;
        var tileH = 16;
        var mapData = this.getMapData(this.map._currentMapName);
        var layer = mapData.layers[layerIndex];
        var layerWidth = layer.dimensions.width;
        var layerHeight = layer.dimensions.height;
        var y2 = Math.floor((y + h - 1) / tileH);
        var x2 = Math.floor((x + w - 1) / tileW);
        x = Math.floor(x / tileW);
        y = Math.floor(y / tileH);
        if (x < 0 || y < 0 || x2 >= layerWidth || y2 >= layerHeight) {
            return true;
        }
        var localLayerObstructions = this.map._localLayerObstructions[layerIndex];
        for (var cy = y; cy <= y2; ++cy) {
            for (var cx = x; cx <= x2; ++cx) {
                var obsIndex = cy * layerWidth + cx;
                if (obsIndex < localLayerObstructions.length) {
                    if (localLayerObstructions[obsIndex] != 0) {
                        return true;
                    }
                }
            }
        }
        return false;
    };
    return Engine;
}());
window.Engine = Engine;
var removeChildren = function (node) {
    while (node.firstChild) {
        node.removeChild(node.firstChild);
    }
};
var addPythonScript = function (path) {
    var s = document.createElement('script');
    s.type = 'text/python';
    s.src = path;
    document.body.appendChild(s);
};
removeChildren(document.body);
addPythonScript('main.py');
brython({
    debug: 1,
});
//# sourceMappingURL=winter.js.map