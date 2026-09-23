/** @odoo-module **/

/**
 * Point the booking links at the visitor's own language.
 *
 * The booking engine takes the language from the path (/JJZW/de?...) and
 * redirects to the matching storefront (de-DE, en-US, ru-RU, cs-CZ). The
 * obvious way to do that would be a t-attf-href in the arch — but any QWeb
 * directive inside #wrap strips the container's editor branding, and without
 * it Odoo offers no drop zone: 45 of 67 blocks greyed out on the homepage
 * while /cenik, which carries no booking link, stayed fine.
 *
 * So the arch keeps a plain static href and the language is swapped in here,
 * which leaves the page fully editable.
 */

import publicWidget from '@web/legacy/js/public/public_widget';

const LANGS = {
    cs: 'cs',
    en: 'en',
    de: 'de',
    ru: 'ru',
};

publicWidget.registry.HABookingLang = publicWidget.Widget.extend({
    selector: '#wrapwrap',

    start() {
        // <html lang> is "cs-CZ", "de-DE", ...; the engine wants the short form.
        const htmlLang = (document.documentElement.getAttribute('lang') || '').slice(0, 2).toLowerCase();
        const code = LANGS[htmlLang];
        if (!code || code === 'cs') {
            // Czech is what the arch already carries; nothing to rewrite.
            return this._super(...arguments);
        }

        document.querySelectorAll('a[data-book-lang]').forEach((a) => {
            const href = a.getAttribute('href') || '';
            const next = href.replace(/(\/JJZW\/)[a-z]{2}(\?)/, `$1${code}$2`);
            if (next !== href) {
                a.setAttribute('href', next);
            }
        });

        return this._super(...arguments);
    },
});

export default publicWidget.registry.HABookingLang;
