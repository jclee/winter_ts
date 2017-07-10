"use strict";

const child_process = require('child_process');
const express = require('express');
const path = require('path');

const port = (process.env.PORT || 9001);

// Path to the root of the repository
const root = path.join(__dirname, '../..');

const app = express();

app.use(express.static(path.join(__dirname, 'static')));
app.use(express.static(path.join(root, 'build')));

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

const server = app.listen(port, function() {
    console.log("started on port", port);
});
