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
    var dataString = obj.data ? JSON.stringify(obj.data) : "";
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.send(dataString);
}

// category catalog
function showCategoryCatalog() {
    var categoryCatalog = document.querySelector(".category-catalog");
    categoryCatalog.style.display = "block";
}


function hideCategoryCatalog() {
    var categoryCatalog = document.querySelector(".category-catalog");
    categoryCatalog.style.display = "none";
}


function createCategory() {
    var cName = document.getElementById("newCategoryName").value;
    ajaxRequest({
        method: "post",
        url: "/api/v1/article_categories",
        data: {
            name: cName
        },
        async: true,
        success: function (response) {
            var cId = response.id;
            var newCategoryNode = document.createElement("li");
            newCategoryNode.innerHTML = '<input type="checkbox" id="c' +
                cId + '" value=' + cId + '><label for="c' +
                cId + '" class="category-label" onclick="clickCategoryLabel(this)">' + cName +
                '</label><ul class="sidebar-list"></ul>';
            var sideBarItemElement = document.querySelector(".sidebar-item");
            sideBarItemElement.appendChild(newCategoryNode);
            hideCategoryCatalog();
        },
        fail: function (status) {
            alert(status);
        }
    });
}


function showModifyCatalog() {
    var cName = selectLabel = document.querySelector(".sidebar-item label.active").innerText;
    var categoryCatalog = document.querySelector(".category-catalog-modify");
    var modifyInput = document.querySelector("#latestCategoryName");
    modifyInput.value = cName;
    categoryCatalog.style.display = "block";
}

function hideModifyCatalog() {
    var categoryCatalog = document.querySelector(".category-catalog-modify");
    categoryCatalog.style.display = "none";
}

function modifyCategory() {
    var cName = document.getElementById("latestCategoryName").value;
    var selectLabel = document.querySelector(".sidebar-item label.active");
    var selectCategory = selectLabel.previousSibling;
    ajaxRequest({
        method: "put",
        url: "/api/v1/article_categories",
        data: {
            new_name: cName,
            id: selectCategory.value
        },
        async: true,
        success: function (response) {
            selectLabel.innerText = cName;
            hideModifyCatalog();
        },
        fail: function (status) {
            alert(status);
        }
    });
}


function showDeleteCatalog() {
    var categoryCatalog = document.querySelector(".category-catalog-delete");
    categoryCatalog.style.display = "block";
}


function hideDeleteCatalog() {
    var categoryCatalog = document.querySelector(".category-catalog-delete");
    categoryCatalog.style.display = "none";
}

function deleteCategory() {
    var selectCategory = document.querySelector(".sidebar-item label.active").previousSibling;

    ajaxRequest({
        method: "delete",
        url: "/api/v1/article_categories",
        data: {
            id: selectCategory.value,
        },
        async: true,
        success: function (response) {
            var selectCategoryLi = selectCategory.parentElement;
            var sideBarItemElement = document.querySelector(".sidebar-item");
            sideBarItemElement.removeChild(selectCategoryLi);
            hideDeleteCatalog();
        },
        fail: function (status) {
            alert(status);
        }
    });
}


function clickCategoryLabel(item) {
    var cLabels = document.querySelectorAll("label.category-label");
    for (var i = 0, len = cLabels.length; i < len; i++) {
        var cLabel = cLabels.item(i);
        cLabel.className = "category-label";
    }
    item.className = "category-label active";
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
                    cListHtml += '<li onclick="clickArticleItem(this);" aid=' + aId + '><div>' + aTitle + '</div></li>'
                }
                cListHtml += '</ul></li>';
            }
            var sidebarItem = document.querySelector("ul.sidebar-item");
            sidebarItem.innerHTML = cListHtml;
        },
        fail: function (status) {
            alert(status);
        }
    });
}


// article相关
function changeEditorContent(title, content, isPublished) {
    var editTitleInput = document.getElementById("titleInput");
    editTitleInput.value = title || "";
    var editContent = document.getElementById("editContent");
    editContent.value = content || "";
    var publishTip = document.getElementById("publishTip");
    if (typeof (isPublished) != "undefined") {
        publishTip.innerText = isPublished ? "已发布" : "未发布";
    } else {
        publishTip.innerText = "";
    }

    text2HTML(editContent);
}

function setArticleContent(aid) {
    ajaxRequest({
        method: "get",
        url: "/api/v1/articles/" + aid,
        aync: true,
        success: function (response) {
            changeEditorContent(response.title, response.content, response.is_published);
        },
        fail: function (status) {
            alert(status);
        }
    });
}

function clickArticleItem(item, reset = true) {
    var aItems = document.querySelectorAll(".sidebar-list li");
    for (var i = 0, len = aItems.length; i < len; i++) {
        var aItem = aItems.item(i);
        aItem.className = "";
    }
    item.className = "active";
    if (reset) {
        setArticleContent(item.getAttribute("aid"));
    } else {
        changeEditorContent(item.innerText);
    }
    var parentLabel = item.parentNode.previousSibling;
    clickCategoryLabel(parentLabel);
}


function createArticle() {
    var selectLabel = document.querySelector(".sidebar-item label.active");
    var selectCategory = selectLabel.previousSibling;
    var currentUl = selectLabel.nextSibling;
    var aTitle = "Untitled Article"
    ajaxRequest({
        method: "post",
        url: "/api/v1/articles",
        async: true,
        data: {
            category_id: selectCategory.value,
            title: aTitle
        },
        success: function (response) {
            var aId = response.id;
            var editTitleInput = document.getElementById("titleInput");
            editTitleInput.value = aTitle;
            var aLi = document.createElement("li");
            aLi.setAttribute("onclick", "clickArticleItem(this);");
            aLi.setAttribute('aid', aId);
            aLi.innerHTML = '<div>' + aTitle + '</div>'
            currentUl.appendChild(aLi);
            clickArticleItem(aLi, false);
        },
        fail: function (status) {
            alert(status);
        }
    });
}


function displayEditTip(text, className = "editor-tip") {
    var editTip = document.getElementById("editorTip");
    editTip.className = className;
    editTip.innerText = text;

    setTimeout('var editTip = document.getElementById("editorTip");editTip.innerText = "";', 3000);
}

function modifyArticle() {
    var currentArticleLi = document.querySelector(".sidebar-list li.active");
    var aId = currentArticleLi.getAttribute("aid");
    var aTitle = document.getElementById("titleInput").value;
    var aContent = document.getElementById("editContent").value;
    ajaxRequest({
        url: "/api/v1/articles/" + aId,
        method: "put",
        async: true,
        data: {
            title: aTitle,
            content: aContent,
        },
        success: function (response) {
            displayEditTip("保存成功!");
            currentArticleLi.firstChild.innerText = aTitle;

        },
        fail: function (status) {
            displayEditTip("保存失败!", "editor-tip-error");
        }
    });
}

function deleteArticle() {
    var currentArticleLi = document.querySelector(".sidebar-list li.active");
    var aId = currentArticleLi.getAttribute("aid");
    ajaxRequest({
        url: "/api/v1/articles/" + aId,
        method: "delete",
        async: true,
        success: function (response) {
            var preArticleLi = currentArticleLi.previousSibling;
            currentArticleLi.parentElement.removeChild(currentArticleLi);
            if (preArticleLi) {
                clickArticleItem(preArticleLi);
            } else {
                changeEditorContent();
            }
            hideArticleCatalog();

        },
        fail: function (status) {
            alert(status);
        }
    });
}

function publishArticle() {
    var currentArticleLi = document.querySelector(".sidebar-list li.active");
    var aId = currentArticleLi.getAttribute("aid");
    var aTitle = document.getElementById("titleInput").value;
    var aContent = document.getElementById("editContent").value;

    var showElement = document.getElementById("showContent");
    var aHtml = showElement.innerHTML;

    var tempElement = document.createElement("div");
    var showChildren = showElement.children;
    for (var i = 0; i < 4; i++) {
        var currentChild = showChildren[i];
        if (!currentChild) {
            break;
        } else {
            var newChild = currentChild.cloneNode(true);
            tempElement.appendChild(newChild);
        }
    }
    var aAbscontent = tempElement.innerHTML;

    var publishTip = document.getElementById("publishTip");

    ajaxRequest({
        url: "/api/v1/articles/" + aId + '/publish',
        method: "post",
        data: {
            title: aTitle,
            content: aContent,
            html: aHtml,
            abscontent: aAbscontent
        },
        async: true,
        success: function () {
            publishTip.innerText = "已发布";
            displayEditTip("发布成功!");
        },
        fail: function () {
            displayEditTip("发布失败!", "editor-tip-error");
        }
    });
}

function unpublishArticle() {
    var currentArticleLi = document.querySelector(".sidebar-list li.active");
    var aId = currentArticleLi.getAttribute("aid");
    var publishTip = document.getElementById("publishTip");

    ajaxRequest({
        url: "/api/v1/articles/" + aId + '/publish',
        method: "delete",
        async: true,
        success: function () {
            publishTip.innerText = "未发布";
            displayEditTip("取消发布成功!");
        },
        fail: function () {
            displayEditTip("取消发布失败!", "editor-tip-error");
        }
    });
}


function showArticleCatalog() {
    var articleCatalog = document.querySelector(".article-catalog");
    articleCatalog.style.display = "block";
}


function hideArticleCatalog() {
    var articleCatalog = document.querySelector(".article-catalog");
    articleCatalog.style.display = "none";
}

window.onload = function () {
    setCateoryList();
}