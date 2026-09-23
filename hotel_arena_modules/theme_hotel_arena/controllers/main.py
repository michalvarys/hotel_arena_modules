import re
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

# Fallback only. The live address is the system parameter below, so reception
# can be re-pointed from Settings > Technical > System Parameters.
RECEPTION_EMAIL = 'recepce@arenahotel.cz'
RECEPTION_EMAIL_PARAM = 'hotel_arena.contact_email'


class HotelArenaController(http.Controller):

    @http.route('/hotel-arena/contact', type='http', auth='public',
                methods=['POST'], website=True, csrf=True)
    def contact_form_submit(self, **kwargs):
        name = kwargs.get('name', '').strip()
        email = kwargs.get('email', '').strip()
        phone = kwargs.get('phone', '').strip()
        subject = kwargs.get('subject', '').strip()
        message = kwargs.get('message', '').strip()

        errors = []
        if len(name) < 2:
            errors.append('Jméno musí mít alespoň 2 znaky.')
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            errors.append('Zadejte platný email.')
        if len(subject) < 2:
            errors.append('Předmět musí mít alespoň 2 znaky.')
        if len(message) < 10:
            errors.append('Zpráva musí mít alespoň 10 znaků.')

        if errors:
            return request.make_json_response(
                {'success': False, 'message': ' '.join(errors)},
                status=400,
            )

        # The lead is what actually captures the enquiry; the mail is only a
        # heads-up for reception. They are done independently on purpose, so a
        # dead SMTP server cannot swallow a booking request.
        lead = self._create_lead(name, email, phone, subject, message)
        self._notify_reception(name, email, phone, subject, message, lead)

        if not lead:
            # Nothing was stored and mail is best-effort — do not claim success.
            return request.make_json_response(
                {'success': False,
                 'message': 'Zprávu se nepodařilo odeslat. '
                            'Zavolejte nám prosím na +420 474 721 290.'},
                status=500,
            )

        return request.make_json_response(
            {'success': True, 'message': 'Zpráva byla úspěšně odeslána. Děkujeme!'}
        )

    def _find_or_create_partner(self, name, email, phone):
        """Reuse the guest's contact if we already know the e-mail, else add it.

        Without this the enquiry only carried the name as loose text on the
        lead and no contact was ever created, so repeat guests stayed
        invisible in the address book.
        """
        Partner = request.env['res.partner'].sudo()
        try:
            partner = Partner.search([('email', '=ilike', email)], limit=1)
            if partner:
                # Fill in a phone number we did not have before, but never
                # overwrite details reception may have corrected by hand.
                if phone and not partner.phone:
                    partner.phone = phone
                return partner
            return Partner.create({
                'name': name,
                'email': email,
                'phone': phone or False,
                'company_type': 'person',
                'comment': 'Vytvořeno z kontaktního formuláře na webu.',
            })
        except Exception:
            _logger.exception('Hotel Arena: could not create contact.')
            return None

    def _create_lead(self, name, email, phone, subject, message):
        """File the enquiry as a CRM opportunity. Returns the lead or None."""
        if not request.env.registry.get('crm.lead'):
            _logger.warning('Hotel Arena: CRM not installed, enquiry not stored.')
            return None

        partner = self._find_or_create_partner(name, email, phone)
        values = {
            'name': '[Web] %s' % subject,
            'contact_name': name,
            'email_from': email,
            'phone': phone,
            'description': message,
            'type': 'opportunity',
        }
        if partner:
            values['partner_id'] = partner.id

        try:
            return request.env['crm.lead'].sudo().create(values)
        except Exception:
            _logger.exception('Hotel Arena: could not create CRM lead.')
            return None

    def _reception_email(self):
        """Address configured in Odoo, falling back to the hotel's own."""
        param = request.env['ir.config_parameter'].sudo()
        return (param.get_param(RECEPTION_EMAIL_PARAM) or '').strip() \
            or RECEPTION_EMAIL

    def _notify_reception(self, name, email, phone, subject, message, lead):
        """Best-effort notification. Never raises — the lead already holds it."""
        company = request.env.company
        recipient = self._reception_email()
        body = [
            '<p><strong>Jméno:</strong> %s</p>' % name,
            '<p><strong>E-mail:</strong> %s</p>' % email,
            '<p><strong>Telefon:</strong> %s</p>' % (phone or '—'),
            '<p><strong>Předmět:</strong> %s</p>' % subject,
            '<p><strong>Zpráva:</strong></p><p>%s</p>' % message,
        ]
        if lead:
            body.append('<p>Poptávka je uložena v CRM (č. %s).</p>' % lead.id)

        try:
            mail = request.env['mail.mail'].sudo().create({
                'subject': '[Hotel Arena Web] %s' % subject,
                'body_html': ''.join(body),
                # Send as ourselves and let reception reply to the guest —
                # putting the guest's address in From trips SPF/DMARC.
                'email_from': company.email or recipient,
                'reply_to': email,
                'email_to': recipient,
            })
            mail.send(raise_exception=False)
        except Exception:
            _logger.exception('Hotel Arena: reception notification failed.')
