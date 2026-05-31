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
    var defaultLanguage = "fa";
    var supportedLanguages = { en: true, fa: true };

    /* Keep strings simple and static so the language switch remains IE8-compatible. */
    var translations = {
        fa: {
            "language.label": "زبان",
            "language.english": "English",
            "language.persian": "فارسی",
            "nav.home_alt": "خانه ATT&CK",
            "search.button": "جستجو",
            "search.placeholder": "جستجو",
            "search.core_objects": "اشیای اصلی",
            "search.core_attack_objects": "اشیای اصلی ATT&CK",
            "search.defenses": "دفاع‌ها",
            "search.cti": "اطلاعات تهدید سایبری",
            "search.reference": "مرجع",
            "search.domains": "دامنه‌ها",
            "search.reset_filters": "بازنشانی فیلترها",
            "common.all": "همه",
            "common.none": "هیچ‌کدام",
            "footer.contact": "تماس با ما",
            "footer.terms": "شرایط استفاده",
            "footer.privacy": "حریم خصوصی",
            "footer.changelog": "تغییرات وب‌سایت",
            "footer.cookie_preferences": "تنظیمات کوکی",
            "footer.copyright": "&copy;&nbsp;2015&nbsp;-&nbsp;2026، The MITRE Corporation. MITRE ATT&CK و ATT&CK نشان‌های تجاری ثبت‌شده The MITRE Corporation هستند."
        }
    };

    var textTranslations = {
        fa: {
            "Home": "خانه",
            "Search": "جستجو",
            "All": "همه",
            "None": "هیچ‌کدام",
            "ID": "شناسه",
            "ID:": "شناسه:",
            "Identifier": "شناسه",
            "Name": "نام",
            "Description": "توضیح",
            "Version": "نسخه",
            "Version:": "نسخه:",
            "Created": "ایجاد شده",
            "Created:": "ایجاد شده:",
            "Last Modified": "آخرین تغییر",
            "Last Modified:": "آخرین تغییر:",
            "Contributors": "مشارکت‌کنندگان",
            "Contributors:": "مشارکت‌کنندگان:",
            "References": "منابع",
            "Enterprise": "سازمانی",
            "Mobile": "موبایل",
            "ICS": "سامانه‌های کنترل صنعتی",
            "Blog": "وبلاگ",
            "Contribute": "مشارکت",
            "Benefactors": "حامیان",
            "Defenses": "دفاع‌ها",
            "CTI": "اطلاعات تهدید",
            "Matrices": "ماتریس‌ها",
            "MATRICES": "ماتریس‌ها",
            "Tactics": "تاکتیک‌ها",
            "TACTICS": "تاکتیک‌ها",
            "Techniques": "تکنیک‌ها",
            "TECHNIQUES": "تکنیک‌ها",
            "Sub-Techniques": "زیرتکنیک‌ها",
            "Sub-techniques": "زیرتکنیک‌ها",
            "Sub-techniques:": "زیرتکنیک‌ها:",
            "Sub-technique of:": "زیرتکنیکِ:",
            "No sub-techniques": "زیرتکنیکی وجود ندارد",
            "Mitigations": "راهکارهای کاهش خطر",
            "MITIGATIONS": "راهکارهای کاهش خطر",
            "Assets": "دارایی‌ها",
            "Targeted Assets": "دارایی‌های هدف",
            "Data Sources": "منابع داده",
            "Data Components": "مولفه‌های داده",
            "Detection Strategies": "راهبردهای تشخیص",
            "Analytics": "تحلیل‌ها",
            "Groups": "گروه‌ها",
            "GROUPS": "گروه‌ها",
            "Software": "نرم‌افزار",
            "SOFTWARE": "نرم‌افزار",
            "Campaigns": "کارزارها",
            "Resources": "منابع",
            "Overview": "نمای کلی",
            "Platform": "سکو",
            "Platform:": "سکو:",
            "Platforms": "سکوها",
            "Platforms:": "سکوها:",
            "Domains": "دامنه‌ها",
            "Procedure Examples": "نمونه‌های رویه",
            "Tactic": "تاکتیک",
            "Tactic:": "تاکتیک:",
            "Tactics:": "تاکتیک‌ها:",
            "Tactic Type:": "نوع تاکتیک:",
            "System Requirements:": "نیازمندی‌های سیستم:",
            "Permissions Required:": "مجوزهای مورد نیاز:",
            "Effective Permissions:": "مجوزهای موثر:",
            "Supports Remote:": "پشتیبانی از اجرای راه دور:",
            "Requires Network:": "نیازمند شبکه:",
            "Defense Bypassed:": "دفاع دور زده شده:",
            "Impact Type:": "نوع اثر:",
            "CAPEC ID:": "شناسه CAPEC:",
            "MTC ID:": "شناسه MTC:",
            "Version Permalink": "پیوند پایدار نسخه"
        }
    };

    var monthTranslations = {
        fa: {
            "January": "ژانویه",
            "February": "فوریه",
            "March": "مارس",
            "April": "آوریل",
            "May": "مه",
            "June": "ژوئن",
            "July": "ژوئیه",
            "August": "اوت",
            "September": "سپتامبر",
            "October": "اکتبر",
            "November": "نوامبر",
            "December": "دسامبر"
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

    function translateMonthNames(language, value) {
        var dict = monthTranslations[language];
        var month;

        if (!dict) {
            return value;
        }

        for (month in dict) {
            if (dict.hasOwnProperty(month)) {
                value = value.replace(new RegExp("\\b" + month + "\\b", "g"), dict[month]);
            }
        }

        return value;
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
            } else {
                node.nodeValue = translateMonthNames(language, value);
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
