const removeChildren = (node : HTMLElement) => {
    while (node.firstChild) {
        node.removeChild(node.firstChild);
    }
};
const addPythonScript = (path : string) => {
    const s = document.createElement('script');
    s.type = 'text/python';
    s.src = path;
    document.body.appendChild(s);
};

const enum BrythonDebugLevel {
    None = 0,
    ShowErrors = 1,
    Translate = 2,
    TranslateAll = 10,
}

interface BrythonOptions {
    debug: BrythonDebugLevel;
}

declare var brython: (options: BrythonOptions) => void;

removeChildren(document.body);
addPythonScript('main.py');
brython({
    debug: BrythonDebugLevel.ShowErrors,
});
