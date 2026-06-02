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
            "home.get_started": "شروع کنید",
            "home.take_tour": "راهنما",
            "home.contribute": "مشارکت",
            "home.blog": "وبلاگ",
            "home.random_page": "صفحه تصادفی",
            "matrix.techniques_count": "تکنیک",
            "home.intro_1": "MITRE ATT&CK<sup>&reg;</sup> یک پایگاه دانش جهانی و در دسترس از تاکتیک‌ها و تکنیک‌های مهاجمان است که بر پایه مشاهده‌های دنیای واقعی ساخته شده است. پایگاه دانش ATT&CK به عنوان پایه‌ای برای توسعه مدل‌ها و روش‌شناسی‌های تهدید در بخش خصوصی، دولت و جامعه محصولات و خدمات امنیت سایبری استفاده می‌شود.",
            "home.intro_2": "MITRE با ایجاد ATT&CK ماموریت خود برای حل مسئله‌ها در مسیر جهانی امن‌تر را دنبال می‌کند؛ با گرد هم آوردن جامعه‌ها برای توسعه امنیت سایبری موثرتر. ATT&CK باز است و هر فرد یا سازمانی می‌تواند بدون هزینه از آن استفاده کند.",
            "home.custom_instance": "این یک نمونه سفارشی از وب‌سایت ATT&CK است که از <a href=\"https://github.com/mitre-attack/attack-website\">کد منبع منتشرشده توسط ATT&CK در GitHub</a> ساخته شده است. این نمونه وابستگی رسمی به ATT&CK ندارد. نمونه رسمی وب‌سایت ATT&CK در <a href=\"https://attack.mitre.org\">attack.mitre.org</a> در دسترس است.",
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
            "Reference": "منبع",
            "Use": "استفاده",
            "Detects": "تشخیص می‌دهد",
            "Field": "فیلد",
            "Channel": "کانال",
            "Log Sources": "منابع لاگ",
            "Mutable Elements": "عناصر قابل تغییر",
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
            "Matrix": "ماتریس",
            "ATT&CK Matrix for Enterprise": "ماتریس سازمانی ATT&CK",
            "layout: side": "چیدمان: کناری",
            "side": "کناری",
            "flat": "تخت",
            "show sub-techniques": "نمایش زیرتکنیک‌ها",
            "hide sub-techniques": "پنهان کردن زیرتکنیک‌ها",
            "help": "راهنما",
            "Tactics": "تاکتیک‌ها",
            "TACTICS": "تاکتیک‌ها",
            "Enterprise Tactics": "تاکتیک‌های سازمانی",
            "Mobile Tactics": "تاکتیک‌های موبایل",
            "ICS Tactics": "تاکتیک‌های سامانه‌های کنترل صنعتی",
            "Tactics:": "تاکتیک‌ها:",
            "Techniques": "تکنیک‌ها",
            "TECHNIQUES": "تکنیک‌ها",
            "Technique": "تکنیک",
            "Enterprise Techniques": "تکنیک‌های سازمانی",
            "Mobile Techniques": "تکنیک‌های موبایل",
            "ICS Techniques": "تکنیک‌های سامانه‌های کنترل صنعتی",
            "Techniques:": "تکنیک‌ها:",
            "Sub-Techniques": "زیرتکنیک‌ها",
            "Sub-technique": "زیرتکنیک",
            "Sub-techniques": "زیرتکنیک‌ها",
            "Sub-techniques:": "زیرتکنیک‌ها:",
            "Sub-technique of:": "زیرتکنیکِ:",
            "No sub-techniques": "زیرتکنیکی وجود ندارد",
            "Mitigations": "راهکارهای کاهش خطر",
            "MITIGATIONS": "راهکارهای کاهش خطر",
            "Enterprise Mitigations": "راهکارهای کاهش خطر سازمانی",
            "Mobile Mitigations": "راهکارهای کاهش خطر موبایل",
            "ICS Mitigations": "راهکارهای کاهش خطر سامانه‌های کنترل صنعتی",
            "Mitigations:": "راهکارهای کاهش خطر:",
            "Techniques Addressed by Mitigation": "تکنیک‌های پوشش‌داده‌شده توسط راهکار کاهش خطر",
            "Mitigation": "راهکار کاهش خطر",
            "Assets": "دارایی‌ها",
            "ASSETS": "دارایی‌ها",
            "Asset": "دارایی",
            "Assets:": "دارایی‌ها:",
            "Targeted Assets": "دارایی‌های هدف",
            "Related Assets": "دارایی‌های مرتبط",
            "Data Sources": "منابع داده",
            "DATA SOURCES": "منابع داده",
            "Data Source": "منبع داده",
            "Data Components": "مولفه‌های داده",
            "DATA COMPONENTS": "مولفه‌های داده",
            "Data Component": "مولفه داده",
            "Data Components:": "مولفه‌های داده:",
            "Detection Strategies": "راهبردهای تشخیص",
            "DETECTION STRATEGIES": "راهبردهای تشخیص",
            "Detection Strategy": "راهبرد تشخیص",
            "Detection Strategies:": "راهبردهای تشخیص:",
            "Technique Detected": "تکنیک تشخیص‌داده‌شده",
            "Technique Detected:": "تکنیک تشخیص‌داده‌شده:",
            "Analytics": "تحلیل‌ها",
            "ANALYTICS": "تحلیل‌ها",
            "Analytic ID": "شناسه تحلیل",
            "Analytic Description": "توضیح تحلیل",
            "Analytics:": "تحلیل‌ها:",
            "Groups": "گروه‌ها",
            "GROUPS": "گروه‌ها",
            "Group": "گروه",
            "Groups:": "گروه‌ها:",
            "Associated Groups": "گروه‌های مرتبط",
            "Associated Group Descriptions": "توضیح گروه‌های مرتبط",
            "Software": "نرم‌افزار",
            "SOFTWARE": "نرم‌افزار",
            "Software:": "نرم‌افزار:",
            "Associated Software": "نرم‌افزارهای مرتبط",
            "Associated Software Descriptions": "توضیح نرم‌افزارهای مرتبط",
            "Groups That Use This Software": "گروه‌هایی که از این نرم‌افزار استفاده می‌کنند",
            "Campaigns": "کارزارها",
            "CAMPAIGNS": "کارزارها",
            "Campaign": "کارزار",
            "Campaigns:": "کارزارها:",
            "Associated Campaigns": "کارزارهای مرتبط",
            "Associated Campaign Descriptions": "توضیح کارزارهای مرتبط",
            "Resources": "منابع",
            "RESOURCES": "منابع",
            "Overview": "نمای کلی",
            "Platform": "سکو",
            "Platform:": "سکو:",
            "Platforms": "سکوها",
            "Platforms:": "سکوها:",
            "Sector": "بخش",
            "Sector:": "بخش:",
            "Sectors": "بخش‌ها",
            "Sectors:": "بخش‌ها:",
            "Domains": "دامنه‌ها",
            "Domain": "دامنه",
            "First Seen": "اولین مشاهده",
            "First Seen:": "اولین مشاهده:",
            "Last Seen": "آخرین مشاهده",
            "Last Seen:": "آخرین مشاهده:",
            "Procedure Examples": "نمونه‌های رویه",
            "Examples": "نمونه‌ها",
            "Tactic": "تاکتیک",
            "Tactic:": "تاکتیک:",
            "Tactic Type:": "نوع تاکتیک:",
            "Type": "نوع",
            "Type:": "نوع:",
            "Security Control": "کنترل امنیتی",
            "Security Controls": "کنترل‌های امنیتی",
            "Security Control:": "کنترل امنیتی:",
            "Security Controls:": "کنترل‌های امنیتی:",
            "Collection Layer": "لایه جمع‌آوری",
            "Collection Layers": "لایه‌های جمع‌آوری",
            "Collection Layer:": "لایه جمع‌آوری:",
            "Collection Layers:": "لایه‌های جمع‌آوری:",
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
