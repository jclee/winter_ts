"use strict";

const child_process = require('child_process');
const express = require('express');
const http = require('http');
const reload = require('reload');
const path = require('path');
const watch = require('watch');

const port = (process.env.PORT || 9001);

// Path to the root of the repository
const root = path.join(__dirname, '../..');

const app = express();

app.use(express.static(path.join(__dirname, 'static')));
app.use(express.static(path.join(root, 'build')));
app.use(express.static(path.join(__dirname, '../python')));
app.use('/brython.js', express.static(path.join(root, 'node_modules/brython/brython.js')));

const server = http.createServer(app);

const rebuildTypescript = () => {
    console.log("Running typescript compiler...");
    const result = child_process.spawnSync('tsc');
    if (result.status != 0) {
        console.error();
        console.error(
            result.stdout.toString('utf8'),
            result.stderr.toString('utf8')
        );
        if (result.error !== undefined) {
            console.error("error:", result.error);
        }
        return false;
    }
    return true;
};
if (!rebuildTypescript()) {
    // May want non-zero return code here for some applications...
    process.exit(0);
}

const reloadServer = reload(app, { verbose: true });

watch.watchTree(path.join(__dirname, 'static'), (f, curr, prev) => {
    reloadServer.reload();
});

watch.watchTree(path.join(root, 'src/python'), (f, curr, prev) => {
    reloadServer.reload();
});

watch.watchTree(path.join(root, 'src/winter'), (f, curr, prev) => {
    if (rebuildTypescript()) {
        reloadServer.reload();
    }
});

// Open Local Dev Server in Browser
const openBrowser = (url) => {
    if (process.platform === 'darwin') {
        try {
            // Try our best to reuse existing tab
            // on OS X Google Chrome with AppleScript
            child_process.execSync('ps cax | grep "Google Chrome"');
            child_process.execSync(
                'osascript '
                + path.resolve(root, 's/chrome.applescript')
                + ' '
                + url
            );
            return;
        } catch (err) {
            // Ignore errors.
        }
    }
    // Fallback to opn
    // (It will always open new tab)
    const opn = require('opn');
    opn(url);
}
openBrowser('http://localhost:' + port + '/');

server.listen(port, () => {
    console.log("started on port", port);
});
