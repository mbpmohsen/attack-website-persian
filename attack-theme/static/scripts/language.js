/*
 * IE8-compatible language selector and static UI translator.
 *
 * The site is generated as static HTML, so language preference is read from the
 * `lang` query parameter first and then from a cookie. The selector persists
 * the choice in a cookie and reloads the page with the selected query value.
 * Keep this file ES3-compatible: no addEventListener, JSON, array helpers, or
 * other ES5+ features.
 */
(function () {
    var cookieName = "attack_language";
    var defaultLanguage = "en";
    var supportedLanguages = { en: true, fa: true };

    /*
     * Persian strings are intentionally marked TODO-FA where they need review
     * by a fluent human translator. This satisfies the placeholder requirement
     * without pretending the generated translations are final.
     */
    var translations = {
        fa: {
            "language.label": "زبان [TODO-FA]",
            "language.english": "English",
            "language.persian": "فارسی [TODO-FA]",
            "nav.home_alt": "خانه ATT&CK [TODO-FA]",
            "search.button": "جستجو [TODO-FA]",
            "search.placeholder": "جستجو [TODO-FA]",
            "search.core_objects": "اشیای اصلی [TODO-FA]",
            "search.core_attack_objects": "اشیای اصلی ATT&CK [TODO-FA]",
            "search.defenses": "دفاع‌ها [TODO-FA]",
            "search.cti": "اطلاعات تهدید [TODO-FA]",
            "search.reference": "مرجع [TODO-FA]",
            "search.domains": "دامنه‌ها [TODO-FA]",
            "search.reset_filters": "بازنشانی پالایه‌ها [TODO-FA]",
            "common.all": "همه [TODO-FA]",
            "common.none": "هیچ‌کدام [TODO-FA]",
            "footer.contact": "تماس با ما [TODO-FA]",
            "footer.terms": "شرایط استفاده [TODO-FA]",
            "footer.privacy": "حریم خصوصی [TODO-FA]",
            "footer.changelog": "تغییرات وب‌سایت [TODO-FA]",
            "footer.cookie_preferences": "تنظیمات کوکی [TODO-FA]",
            "footer.copyright": "&copy;&nbsp;2015&nbsp;-&nbsp;2026، The MITRE Corporation. MITRE ATT&CK و ATT&CK نشان‌های تجاری ثبت‌شده The MITRE Corporation هستند. [TODO-FA]"
        }
    };

    var textTranslations = {
        fa: {
            "Home": "خانه [TODO-FA]",
            "Search": "جستجو [TODO-FA]",
            "All": "همه [TODO-FA]",
            "None": "هیچ‌کدام [TODO-FA]",
            "ID": "شناسه [TODO-FA]",
            "ID:": "شناسه: [TODO-FA]",
            "Name": "نام [TODO-FA]",
            "Description": "توضیح [TODO-FA]",
            "Version": "نسخه [TODO-FA]",
            "Created": "ایجاد شده [TODO-FA]",
            "Last Modified": "آخرین تغییر [TODO-FA]",
            "Contributors": "مشارکت‌کنندگان [TODO-FA]",
            "References": "منابع [TODO-FA]",
            "Enterprise": "سازمانی [TODO-FA]",
            "Mobile": "موبایل [TODO-FA]",
            "ICS": "سامانه‌های کنترل صنعتی [TODO-FA]",
            "Matrices": "ماتریس‌ها [TODO-FA]",
            "Tactics": "تاکتیک‌ها [TODO-FA]",
            "Techniques": "تکنیک‌ها [TODO-FA]",
            "Sub-Techniques": "زیرتکنیک‌ها [TODO-FA]",
            "Mitigations": "کاهش‌دهنده‌ها [TODO-FA]",
            "Assets": "دارایی‌ها [TODO-FA]",
            "Data Sources": "منابع داده [TODO-FA]",
            "Data Components": "مولفه‌های داده [TODO-FA]",
            "Detection Strategies": "راهبردهای تشخیص [TODO-FA]",
            "Analytics": "تحلیل‌ها [TODO-FA]",
            "Groups": "گروه‌ها [TODO-FA]",
            "Software": "نرم‌افزار [TODO-FA]",
            "Campaigns": "کارزارها [TODO-FA]",
            "Resources": "منابع [TODO-FA]",
            "Overview": "نمای کلی [TODO-FA]",
            "Platform": "سکو [TODO-FA]",
            "Domains": "دامنه‌ها [TODO-FA]"
        }
    };

    function trim(value) {
        return String(value).replace(/^\s+|\s+$/g, "");
    }

    function getQueryLanguage() {
        var query = window.location.search;
        var parts;
        var pair;
        var i;

        if (!query || query.length < 2) {
            return "";
        }

        parts = query.substring(1).split("&");
        for (i = 0; i < parts.length; i += 1) {
            pair = parts[i].split("=");
            if (decodeURIComponent(pair[0]) === "lang") {
                return decodeURIComponent(pair[1] || "");
            }
        }
        return "";
    }

    function getCookie(name) {
        var cookies = document.cookie ? document.cookie.split(";") : [];
        var prefix = name + "=";
        var item;
        var i;

        for (i = 0; i < cookies.length; i += 1) {
            item = trim(cookies[i]);
            if (item.indexOf(prefix) === 0) {
                return decodeURIComponent(item.substring(prefix.length));
            }
        }
        return "";
    }

    function setCookie(name, value) {
        var expires = new Date();
        expires.setFullYear(expires.getFullYear() + 1);
        document.cookie = name + "=" + encodeURIComponent(value) + "; expires=" + expires.toUTCString() + "; path=/";
    }

    function normalizeLanguage(language) {
        if (supportedLanguages[language]) {
            return language;
        }
        return defaultLanguage;
    }

    function getCurrentLanguage() {
        return normalizeLanguage(getQueryLanguage() || getCookie(cookieName) || defaultLanguage);
    }

    function setDocumentDirection(language) {
        var root = document.documentElement;
        root.setAttribute("lang", language);
        root.setAttribute("dir", language === "fa" ? "rtl" : "ltr");
    }

    function translateByKey(language) {
        var dict = translations[language];
        var elements;
        var element;
        var key;
        var attrPairs;
        var attrPair;
        var i;
        var j;

        if (!dict) {
            return;
        }

        elements = document.getElementsByTagName("*");
        for (i = 0; i < elements.length; i += 1) {
            element = elements[i];
            key = element.getAttribute("data-i18n");
            if (key && dict[key]) {
                element.innerHTML = dict[key];
            }

            attrPairs = element.getAttribute("data-i18n-attr");
            if (attrPairs) {
                attrPairs = attrPairs.split(",");
                for (j = 0; j < attrPairs.length; j += 1) {
                    attrPair = attrPairs[j].split(":");
                    if (attrPair.length === 2 && dict[attrPair[1]]) {
                        element.setAttribute(attrPair[0], dict[attrPair[1]]);
                    }
                }
            }
        }
    }

    function getTextTranslation(language, value) {
        var dict = textTranslations[language];
        var stixDict = window.attackStixTextTranslations && window.attackStixTextTranslations[language];

        if (dict && dict[value]) {
            return dict[value];
        }
        if (stixDict && stixDict[value]) {
            return stixDict[value];
        }
        return "";
    }

    function normalizeTranslationKey(value) {
        return trim(String(value).replace(/\[\d+\]/g, "").replace(/\s+/g, " "));
    }

    function hasClassName(element, className) {
        return (" " + element.className + " ").indexOf(" " + className + " ") > -1;
    }

    function getElementText(element) {
        if (typeof element.textContent === "string") {
            return element.textContent;
        }
        return element.innerText || "";
    }

    function translateDescriptionBlocks(language) {
        var dict = window.attackStixDescriptionTranslations && window.attackStixDescriptionTranslations[language];
        var elements;
        var element;
        var key;
        var i;

        if (!dict) {
            return;
        }

        elements = document.getElementsByTagName("div");
        for (i = 0; i < elements.length; i += 1) {
            element = elements[i];
            if (hasClassName(element, "description-body")) {
                key = normalizeTranslationKey(getElementText(element));
                if (dict[key]) {
                    element.innerHTML = dict[key];
                }
            }
        }
    }

    function translateTextNodes(node, language) {
        var child;
        var next;
        var tagName;
        var value;
        var cleanValue;
        var leading;
        var trailing;
        var translation;

        if (!node) {
            return;
        }

        if (node.nodeType === 3) {
            value = node.nodeValue;
            cleanValue = trim(value);
            translation = getTextTranslation(language, cleanValue);
            if (translation) {
                leading = value.match(/^\s*/)[0];
                trailing = value.match(/\s*$/)[0];
                node.nodeValue = leading + translation + trailing;
            }
            return;
        }

        if (node.nodeType !== 1) {
            return;
        }

        tagName = node.tagName ? node.tagName.toLowerCase() : "";
        if (tagName === "script" || tagName === "style" || tagName === "textarea") {
            return;
        }

        child = node.firstChild;
        while (child) {
            next = child.nextSibling;
            translateTextNodes(child, language);
            child = next;
        }
    }

    function setSelectorValue(language) {
        var selector = document.getElementById("language-selector");
        if (selector) {
            selector.value = language;
        }
    }

    function buildLanguageUrl(language) {
        var location = window.location;
        var path = location.pathname;
        var query = location.search ? location.search.substring(1).split("&") : [];
        var hash = location.hash || "";
        var found = false;
        var parts = [];
        var pair;
        var i;

        for (i = 0; i < query.length; i += 1) {
            if (!query[i]) {
                continue;
            }
            pair = query[i].split("=");
            if (decodeURIComponent(pair[0]) === "lang") {
                parts[parts.length] = "lang=" + encodeURIComponent(language);
                found = true;
            } else {
                parts[parts.length] = query[i];
            }
        }

        if (!found) {
            parts[parts.length] = "lang=" + encodeURIComponent(language);
        }

        return path + "?" + parts.join("&") + hash;
    }

    function bindSelector(language) {
        var selector = document.getElementById("language-selector");
        if (!selector) {
            return;
        }

        selector.onchange = function () {
            var selectedLanguage = normalizeLanguage(selector.value);
            setCookie(cookieName, selectedLanguage);
            window.location.href = buildLanguageUrl(selectedLanguage);
        };
    }

    function applyLanguage() {
        var language = getCurrentLanguage();
        setCookie(cookieName, language);
        setDocumentDirection(language);
        translateByKey(language);
        translateDescriptionBlocks(language);
        translateTextNodes(document.body, language);
        setSelectorValue(language);
        bindSelector(language);
    }

    if (document.attachEvent) {
        document.attachEvent("onreadystatechange", function () {
            if (document.readyState === "complete") {
                applyLanguage();
            }
        });
    } else if (document.addEventListener) {
        document.addEventListener("DOMContentLoaded", applyLanguage, false);
    } else {
        window.onload = applyLanguage;
    }

    window.attackApplyLanguage = applyLanguage;
}());
