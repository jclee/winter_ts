const greet = () => {
    return "Hello, world";
}

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

declare var brython: any;

removeChildren(document.body);
addPythonScript('system.py');
brython();
