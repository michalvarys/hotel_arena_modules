import logging

_logger = logging.getLogger(__name__)

# Odoo's own stage names ("Qualified", "Won", or in Czech "Kvalifikovaný",
# "Vyhráno") are sales jargon and say little to someone handling room
# enquiries. These are set from a hook rather than XML because the records
# belong to the crm module, and an XML override of another module's record is
# ignored once that record already exists.
STAGE_NAMES = {
    'crm.stage_lead1': {'en_US': 'New enquiry',  'cs_CZ': 'Nová poptávka'},
    'crm.stage_lead2': {'en_US': 'Qualified',    'cs_CZ': 'Ověřená poptávka'},
    'crm.stage_lead3': {'en_US': 'Offer sent',   'cs_CZ': 'Nabídka odeslána'},
    'crm.stage_lead4': {'en_US': 'Booked',       'cs_CZ': 'Rezervováno'},
}


def rename_crm_stages(env):
    """Give the CRM pipeline hotel wording in every installed language."""
    active_langs = env['res.lang'].sudo().search([]).mapped('code')

    for xml_id, names in STAGE_NAMES.items():
        stage = env.ref(xml_id, raise_if_not_found=False)
        if not stage:
            continue
        for lang, value in names.items():
            if lang in active_langs:
                stage.with_context(lang=lang).sudo().name = value

    _logger.info('Hotel Arena: CRM stages renamed for %s', active_langs)
