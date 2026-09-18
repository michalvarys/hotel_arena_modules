import re
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


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

        try:
            if request.env.registry.get('crm.lead'):
                request.env['crm.lead'].sudo().create({
                    'name': subject,
                    'contact_name': name,
                    'email_from': email,
                    'phone': phone,
                    'description': message,
                    'type': 'opportunity',
                })
            else:
                mail_values = {
                    'subject': f'[Hotel Arena Web] {subject}',
                    'body_html': (
                        f'<p><strong>Jméno:</strong> {name}</p>'
                        f'<p><strong>Email:</strong> {email}</p>'
                        f'<p><strong>Telefon:</strong> {phone}</p>'
                        f'<p><strong>Zpráva:</strong></p><p>{message}</p>'
                    ),
                    'email_from': email,
                    'email_to': 'recepce@arenahotel.cz',
                }
                request.env['mail.mail'].sudo().create(mail_values).send()
        except Exception as e:
            _logger.exception('Hotel Arena contact form error: %s', e)
            return request.make_json_response(
                {'success': False, 'message': 'Došlo k chybě při odesílání.'},
                status=500,
            )

        return request.make_json_response(
            {'success': True, 'message': 'Zpráva byla úspěšně odeslána. Děkujeme!'}
        )
