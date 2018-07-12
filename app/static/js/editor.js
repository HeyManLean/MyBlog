// marked相关

var renderer = new marked.Renderer()

marked.setOptions({
    renderer: renderer,
    gfm: true,
    tables: true,
    breaks: false,
    pedantic: false,
    sanitize: false,
    smartLists: true,
    smartypants: false,
    langPrefix: "",
    highlight: function (code) {
        return hljs.highlightAuto(code).value;
    }
});
renderer.code = function (code, language) {
    var lang = language;
    if (!lang) {
        lang = 'python';
    }
    var highlighted = hljs.highlight(lang, code).value;
    return '<pre class="hljs"><code class="hljs ' + lang + '">' + highlighted + '</code></pre>';
};


function text2HTML(target) {
    var markedHtml = marked(target.value);
    document.querySelector("#showContent").innerHTML = markedHtml;
}

// category相关
function setCateoryList() {
    
}