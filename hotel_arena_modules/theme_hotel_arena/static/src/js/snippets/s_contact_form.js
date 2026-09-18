/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.HAContactForm = publicWidget.Widget.extend({
    selector: '.s_ha_contact_form',
    events: {
        'submit #ha-contact-form': '_onSubmit',
    },

    _onSubmit(ev) {
        ev.preventDefault();
        const form = ev.currentTarget;
        const btn = form.querySelector('.ha-btn-submit');
        const resultDiv = form.querySelector('#ha-form-result');

        // Reset
        resultDiv.className = 'ha-form-message';
        resultDiv.style.display = 'none';
        resultDiv.textContent = '';

        // Client-side validation
        const name = form.querySelector('[name="name"]').value.trim();
        const email = form.querySelector('[name="email"]').value.trim();
        const subject = form.querySelector('[name="subject"]').value.trim();
        const message = form.querySelector('[name="message"]').value.trim();

        const errors = [];
        if (name.length < 2) errors.push('Jméno musí mít alespoň 2 znaky.');
        if (!/[^@]+@[^@]+\.[^@]+/.test(email)) errors.push('Zadejte platný email.');
        if (subject.length < 2) errors.push('Předmět musí mít alespoň 2 znaky.');
        if (message.length < 10) errors.push('Zpráva musí mít alespoň 10 znaků.');

        if (errors.length > 0) {
            resultDiv.className = 'ha-form-message ha-form-error';
            resultDiv.textContent = errors.join(' ');
            resultDiv.style.display = 'block';
            return;
        }

        // Disable button
        const origText = btn.textContent;
        btn.textContent = 'Odesílám...';
        btn.disabled = true;

        fetch('/hotel-arena/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams(new FormData(form)).toString(),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    resultDiv.className = 'ha-form-message ha-form-success';
                    resultDiv.textContent = data.message;
                    form.reset();
                } else {
                    resultDiv.className = 'ha-form-message ha-form-error';
                    resultDiv.textContent = data.message;
                }
                resultDiv.style.display = 'block';
            })
            .catch(() => {
                resultDiv.className = 'ha-form-message ha-form-error';
                resultDiv.textContent = 'Došlo k chybě při odesílání. Zkuste to prosím znovu.';
                resultDiv.style.display = 'block';
            })
            .finally(() => {
                btn.textContent = origText;
                btn.disabled = false;
            });
    },
});
