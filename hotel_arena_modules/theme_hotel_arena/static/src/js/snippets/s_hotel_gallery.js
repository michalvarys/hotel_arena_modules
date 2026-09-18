/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.HAHotelGallery = publicWidget.Widget.extend({
    selector: '.s_ha_gallery',
    events: {
        'click .ha-gallery-item': '_onItemClick',
    },

    start() {
        this._super(...arguments);
        this._images = [];
        this._currentIndex = 0;

        // Collect all gallery images
        this.el.querySelectorAll('.ha-gallery-item img').forEach((img) => {
            this._images.push(img.src);
        });
    },

    _onItemClick(ev) {
        ev.preventDefault();
        const item = ev.currentTarget;
        const img = item.querySelector('img');
        if (!img) return;

        this._currentIndex = this._images.indexOf(img.src);
        this._openLightbox(img.src);
    },

    _openLightbox(src) {
        // Remove existing lightbox if any
        const existing = document.querySelector('.ha-lightbox');
        if (existing) existing.remove();

        const total = this._images.length;
        const current = this._currentIndex + 1;

        const lightbox = document.createElement('div');
        lightbox.className = 'ha-lightbox active';
        lightbox.innerHTML = `
            <span class="ha-lightbox-close">&times;</span>
            <img class="ha-lightbox-img" src="${src}" alt="Gallery"/>
            <span class="ha-lightbox-nav prev"><i class="fa fa-chevron-left"></i></span>
            <span class="ha-lightbox-nav next"><i class="fa fa-chevron-right"></i></span>
            <div class="ha-lightbox-counter">${current} / ${total}</div>
        `;

        document.body.appendChild(lightbox);

        // Events
        lightbox.querySelector('.ha-lightbox-close').addEventListener('click', () => {
            lightbox.remove();
        });

        lightbox.querySelector('.ha-lightbox-nav.prev').addEventListener('click', () => {
            this._currentIndex = (this._currentIndex - 1 + total) % total;
            this._updateLightbox(lightbox);
        });

        lightbox.querySelector('.ha-lightbox-nav.next').addEventListener('click', () => {
            this._currentIndex = (this._currentIndex + 1) % total;
            this._updateLightbox(lightbox);
        });

        // Close on backdrop click
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) lightbox.remove();
        });

        // Keyboard navigation
        this._keyHandler = (e) => {
            if (e.key === 'Escape') lightbox.remove();
            if (e.key === 'ArrowLeft') {
                this._currentIndex = (this._currentIndex - 1 + total) % total;
                this._updateLightbox(lightbox);
            }
            if (e.key === 'ArrowRight') {
                this._currentIndex = (this._currentIndex + 1) % total;
                this._updateLightbox(lightbox);
            }
        };
        document.addEventListener('keydown', this._keyHandler);
    },

    _updateLightbox(lightbox) {
        const img = lightbox.querySelector('.ha-lightbox-img');
        const counter = lightbox.querySelector('.ha-lightbox-counter');
        img.src = this._images[this._currentIndex];
        counter.textContent = `${this._currentIndex + 1} / ${this._images.length}`;
    },

    destroy() {
        if (this._keyHandler) {
            document.removeEventListener('keydown', this._keyHandler);
        }
        const lightbox = document.querySelector('.ha-lightbox');
        if (lightbox) lightbox.remove();
        this._super(...arguments);
    },
});
