function Json2Html(arr, parent) {
    for (let i = 0; i < arr.length; i++) {
        parent.appendChild(__Json2Html(arr[i]));
    }
    return parent;
}

function __Json2Html(obj) {
    if (typeof(obj) == "string") {
        return new Text(obj);
    } else {
        let node = document.createElement(obj.tag);
        for (let i = 0; i < obj.attrs.length; i++) {
            let attr = obj.attrs[i];
            node.setAttribute(attr.name, attr.value);
        }
        for (let i = 0; i < obj.children.length; i++) {
            node.appendChild(__Json2Html(obj.children[i]));
        }
        return node;
    }
}