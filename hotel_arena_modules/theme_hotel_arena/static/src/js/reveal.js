/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.HARevealOnScroll = publicWidget.Widget.extend({
    selector: '#wrapwrap',

    start() {
        this._super(...arguments);
        const reveals = this.el.querySelectorAll('.reveal');
        if (!reveals.length) return;

        this._observer = new IntersectionObserver(
            (entries) => {
                for (const entry of entries) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                        this._observer.unobserve(entry.target);
                    }
                }
            },
            { threshold: 0.1, rootMargin: '0px 0px -30px 0px' }
        );

        for (const el of reveals) {
            this._observer.observe(el);
        }
    },

    destroy() {
        if (this._observer) {
            this._observer.disconnect();
        }
        this._super(...arguments);
    },
});
