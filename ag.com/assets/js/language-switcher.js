(function () {
    var TRANSLATE_SCRIPT_ID = 'jhs-google-translate-script';
    var TRANSLATE_HOLDER_ID = 'google_translate_element';
    var SUPPORTED_LANGUAGES = 'en,kn,hi,te,ta,fi';

    function expireCookie(name, path) {
        document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=' + path;
    }

    function clearPersistedTranslateState() {
        try {
            expireCookie('googtrans', '/');
            expireCookie('googtrans', '');
            expireCookie('googtrans', '/;domain=' + window.location.hostname);
            if (window.location.hostname.indexOf('www.') === 0) {
                expireCookie('googtrans', '/;domain=' + window.location.hostname.replace('www.', ''));
            }
        } catch (e) {}
    }

    function getLanguageSelects() {
        return Array.prototype.slice.call(
            document.querySelectorAll('#languageSelect, #languageSelector, .currency-menu select.form-select.nice-select')
        );
    }

    function syncNiceSelectLabel(select, lang) {
        try {
            var niceSelect = select.nextElementSibling;
            if (!niceSelect || !niceSelect.classList || !niceSelect.classList.contains('nice-select')) {
                return;
            }

            var optionNode = niceSelect.querySelector('.option[data-value="' + lang + '"]');
            var currentNode = niceSelect.querySelector('.current');

            if (optionNode && currentNode) {
                currentNode.textContent = optionNode.textContent;
                niceSelect.querySelectorAll('.option').forEach(function (item) {
                    item.classList.remove('selected', 'focus');
                });
                optionNode.classList.add('selected', 'focus');
            }
        } catch (e) {}
    }

    function setSelectValues(lang) {
        getLanguageSelects().forEach(function (select) {
            try {
                select.value = lang;
                syncNiceSelectLabel(select, lang);
            } catch (e) {}
        });
    }

    function applyLanguage(lang) {
        var combo = document.querySelector('.goog-te-combo');
        if (!combo) {
            return false;
        }

        combo.value = lang;
        combo.dispatchEvent(new Event('change'));
        setSelectValues(lang);
        return true;
    }

    function redirectFallback(lang) {
        var targetLang = lang || 'en';
        if (targetLang === 'en') {
            return;
        }

        var translatedUrl = 'https://translate.google.com/translate?sl=en&tl=' +
            encodeURIComponent(targetLang) +
            '&u=' + encodeURIComponent(window.location.href);
        window.location.href = translatedUrl;
    }

    window.changeLanguage = function (lang) {
        var targetLang = lang || 'en';

        if (targetLang === 'en') {
            setSelectValues('en');
            clearPersistedTranslateState();

            var comboEn = document.querySelector('.goog-te-combo');
            if (comboEn) {
                comboEn.value = '';
                comboEn.dispatchEvent(new Event('change'));
            }

            var wasTranslated =
                document.documentElement.classList.contains('translated-ltr') ||
                document.body.classList.contains('translated-ltr') ||
                document.cookie.indexOf('googtrans=') !== -1;

            if (wasTranslated) {
                window.location.reload();
            }
            return;
        }

        if (applyLanguage(targetLang)) {
            return;
        }

        var retryCount = 0;
        var retryTimer = setInterval(function () {
            retryCount += 1;
            if (applyLanguage(targetLang)) {
                clearInterval(retryTimer);
                return;
            }

            if (retryCount > 25) {
                clearInterval(retryTimer);
                redirectFallback(targetLang);
            }
        }, 200);
    };

    function attachSelectHandlers() {
        getLanguageSelects().forEach(function (select) {
            if (select.dataset.langBound === '1') {
                return;
            }

            select.dataset.langBound = '1';
            select.addEventListener('change', function (event) {
                if (event && typeof event.preventDefault === 'function') {
                    event.preventDefault();
                }

                var selectedLang = select.value || 'en';
                window.changeLanguage(selectedLang);
            });
        });

        if (!document.documentElement.dataset.niceSelectLangBound) {
            document.documentElement.dataset.niceSelectLangBound = '1';
            document.addEventListener('click', function (event) {
                var option = event.target.closest('.nice-select .option');
                if (!option) {
                    return;
                }

                var selectedLang = option.getAttribute('data-value') || option.dataset.value;
                if (selectedLang) {
                    window.changeLanguage(selectedLang);
                }
            });
        }
    }

    window.jhsGoogleTranslateInit = function () {
        if (!window.google || !google.translate || !google.translate.TranslateElement) {
            return;
        }

        if (!document.getElementById(TRANSLATE_HOLDER_ID)) {
            var holder = document.createElement('div');
            holder.id = TRANSLATE_HOLDER_ID;
            holder.style.display = 'none';
            document.body.appendChild(holder);
        }

        if (!document.documentElement.dataset.translateReady) {
            new google.translate.TranslateElement(
                {
                    pageLanguage: 'en',
                    includedLanguages: SUPPORTED_LANGUAGES,
                    autoDisplay: false
                },
                TRANSLATE_HOLDER_ID
            );
            document.documentElement.dataset.translateReady = '1';
        }

        attachSelectHandlers();

        // Force default language to English on every page load.
        setSelectValues('en');
    };

    function ensureTranslateScript() {
        if (document.getElementById(TRANSLATE_SCRIPT_ID)) {
            return;
        }

        var script = document.createElement('script');
        script.id = TRANSLATE_SCRIPT_ID;
        script.src = 'https://translate.google.com/translate_a/element.js?cb=jhsGoogleTranslateInit';
        script.async = true;
        document.head.appendChild(script);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            clearPersistedTranslateState();
            setSelectValues('en');
            attachSelectHandlers();
            ensureTranslateScript();
        });
    } else {
        clearPersistedTranslateState();
        setSelectValues('en');
        attachSelectHandlers();
        ensureTranslateScript();
    }
})();
