{
    'name': 'Hotel Arena Settings',
    'summary': 'Base configuration for Hotel Arena website: languages, website settings',
    'category': 'Website',
    'version': '18.0.1.0.0',
    'author': 'VaryShop',
    'license': 'LGPL-3',
    'depends': [
        'website',
        # Contact form enquiries are filed as CRM leads, so nothing is lost
        # when outgoing mail is down. See theme_hotel_arena/controllers.
        'crm',
    ],
    'data': [
        'data/website_config_data.xml',
        'data/seo_redirects.xml',
        'data/crm_data.xml',
    ],
    'post_init_hook': 'rename_crm_stages',
    'installable': True,
    'auto_install': False,
    'application': False,
}
