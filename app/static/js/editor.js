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

function ajaxRequest(obj) {
    var req = new XMLHttpRequest();
    req.responseType = "json";
    req.onreadystatechange = function () {
        if (req.readyState == 4) {
            if (req.status == 200) {
                obj.success(req.response)
            } else {
                obj.fail(req.status)
            }
        }
    };
    req.open(obj.method, obj.url, obj.async || true);
    req.send();
}

function clickCategoryLabel (item) {
    var cLabels = document.querySelectorAll("label.category-label");
    for (var i=0, len=cLabels.length; i < len; i++) {
        var cLabel = cLabels.item(i);
        cLabel.className = "category-label";
    }
    item.className = "category-label active";
}

function clickArticleItem (item) {
    var aItems = document.querySelectorAll(".sidebar-list li");
    for (var i=0, len=aItems.length; i < len; i++) {
        var aItem = aItems.item(i);
        aItem.className = "";
    }
    item.className = "active";
}

// category相关
function setCateoryList() {
    ajaxRequest({
        method: "get",
        url: "/api/v1/article_categories",
        async: true,
        success: function (response) {
            var categoryData = response.data;
            var cListHtml = "";
            for (var ci = 0, clen = categoryData.length; ci < clen; ci++) {
                var c = categoryData[ci];
                var cId = c.id;
                var cName = c.name;
                var cArticles = c.articles;
                cListHtml += '<li><input type="checkbox" id="c' +
                    cId + '" value=' + cId + '><label for="c' +
                    cId + '" class="category-label" onclick="clickCategoryLabel(this)">' + cName +
                    '</label><ul class="sidebar-list">';

                for (var ai = 0, alen = cArticles.length; ai < alen; ai++) {
                    var a = cArticles[ai];
                    var aId = a.id;
                    var aTitle = a.title;
                    cListHtml += '<li onclick="clickArticleItem(this)"><div aid=' + aId + '>' + aTitle + '</div>'
                }
                cListHtml += '</ul></li>';
                console.log(cId);
            }
            var sidebarItem = document.querySelector("ul.sidebar-item");
            sidebarItem.innerHTML = cListHtml;
        },
        fail: function (status) {
            alert(status);
        }
    });
}

window.onload = function () {
    setCateoryList();
}