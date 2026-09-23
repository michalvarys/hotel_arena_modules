from odoo import models

# Homepage SEO. The Czech text is carried over verbatim from the old
# arenahotel.cz, which is the wording the site currently ranks on; Odoo would
# otherwise ship "Home" / "This is the homepage of the website" and drop the
# "ubytování Chomutov" keyword entirely. The old site had no description in
# English, German or Russian at all, so those are written here.
#
# en_US is the source slot, so English is the value the record is created with
# and the other languages are written as translations on top.
HOME_META = {
    'en_US': {
        'website_meta_title': 'Chomutov accommodation - Hotel Arena',
        'website_meta_description': (
            'Looking for modern, comfortable accommodation in Chomutov? Hotel Arena '
            'offers quality rooms and a convenient location. Book your stay today!'
        ),
        'website_meta_keywords': (
            'hotel by Chomutov zoo, weekend break chomutov, family accommodation '
            'chomutov, hotel chomutov, hotel with restaurant chomutov, corporate accommodation'
        ),
    },
    'cs_CZ': {
        'website_meta_title': 'Ubytování Chomutov - Hotel Arena',
        'website_meta_description': (
            'Hledáte moderní a pohodlné ubytování v Chomutově? Arena Hotel nabízí '
            'kvalitní pokoje a výhodnou polohu. Rezervujte si svůj pobyt ještě dnes!'
        ),
        'website_meta_keywords': (
            'hotel u ZOO Chomutov, víkendový pobyt chomutov, ubytování pro rodiny '
            'chomutov, hotel chomutov, hotel s restaurací chomutov, ubytování pro firmy'
        ),
    },
    'de_DE': {
        'website_meta_title': 'Unterkunft Komotau - Hotel Arena',
        'website_meta_description': (
            'Suchen Sie eine moderne und komfortable Unterkunft in Komotau? Das Hotel '
            'Arena bietet hochwertige Zimmer und eine günstige Lage. Buchen Sie noch heute!'
        ),
        'website_meta_keywords': (
            'hotel beim zoo komotau, wochenendaufenthalt komotau, familienunterkunft '
            'komotau, hotel komotau, hotel mit restaurant komotau, firmenunterkunft'
        ),
    },
    'ru_RU': {
        'website_meta_title': 'Проживание в Хомутове - Hotel Arena',
        'website_meta_description': (
            'Ищете современное и комфортное жильё в Хомутове? Hotel Arena предлагает '
            'качественные номера и удобное расположение. Забронируйте проживание уже сегодня!'
        ),
        'website_meta_keywords': (
            'отель у зоопарка хомутов, выходные в хомутове, семейное проживание хомутов, '
            'отель хомутов, отель с рестораном хомутов, проживание для компаний'
        ),
    },
}


# Per-page browser titles. Odoo falls back to the view's `name`, which is not a
# translatable column, so every language would otherwise share the English one.
# The wording follows the old arenahotel.cz; /ubytovani had no counterpart there
# (the rooms sat on its homepage), so those four are written here.
PAGE_TITLES = {
    '/ubytovani': {
        'en_US': 'Accommodation - Hotel Arena',
        'cs_CZ': 'Ubytování - Hotel Arena',
        'de_DE': 'Unterbringung - Hotel Arena',
        'ru_RU': 'Проживание - Hotel Arena',
    },
    '/o-hotelu': {
        'en_US': 'About us - Hotel Arena',
        'cs_CZ': 'O hotelu - Hotel Arena',
        'de_DE': 'Über das Hotel - Hotel Arena',
        'ru_RU': 'Об отеле - Hotel Arena',
    },
    '/restaurace-a-bar': {
        'en_US': 'Restaurant and bar - Hotel Arena',
        'cs_CZ': 'Restaurace a bar - Hotel Arena',
        'de_DE': 'Restaurant und Bar - Hotel Arena',
        'ru_RU': 'Ресторан и бар - Hotel Arena',
    },
    '/galerie': {
        'en_US': 'Gallery - Hotel Arena',
        'cs_CZ': 'Galerie - Hotel Arena',
        'de_DE': 'Galerie - Hotel Arena',
        'ru_RU': 'Галерея - Hotel Arena',
    },
    '/cenik': {
        'en_US': 'Pricelist - Hotel Arena',
        'cs_CZ': 'Ceník - Hotel Arena',
        'de_DE': 'Preisliste - Hotel Arena',
        'ru_RU': 'Прейскурант - Hotel Arena',
    },
    '/kontakt': {
        'en_US': 'Contact - Hotel Arena',
        'cs_CZ': 'Kontakt - Hotel Arena',
        'de_DE': 'Kontakt - Hotel Arena',
        'ru_RU': 'Контакт - Hotel Arena',
    },
}


class ThemeHotelArena(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_hotel_arena_post_copy(self, mod):
        # Disable default header
        self.disable_view('website.template_header_default')
        # Enable custom header
        self.enable_view('theme_hotel_arena.ha_header')
        # Odoo's default footer block ships placeholder contacts
        # (info@yourcompany.com); ha_footer carries the real ones.
        self.disable_view('website.template_footer_links')

        website = self.env['website'].get_current_website()
        Menu = self.env['website.menu']

        # Odoo creates its own menu entries ("Home", "Contact us") next to the
        # theme's, so '/' ends up listed twice. Deduplicate by URL rather than
        # by label: the labels are translatable, and matching on a Czech string
        # broke the moment the menu was moved to an English source.
        menus = Menu.search([('website_id', '=', website.id)], order='sequence, id')
        seen = set()
        for menu in menus:
            if not menu.url:
                continue
            if menu.url in seen:
                menu.unlink()
            else:
                seen.add(menu.url)

        Menu.search([
            ('website_id', '=', website.id),
            ('url', '=', '/contactus'),
        ]).unlink()

        # Unpublish default contactus page (we use /kontakt instead)
        contactus_page = self.env['website.page'].search([
            ('website_id', '=', website.id),
            ('url', '=', '/contactus'),
        ], limit=1)
        if contactus_page:
            contactus_page.is_published = False

        # Homepage SEO, written per language.
        homepage = self.env['website.page'].search([
            ('url', '=', '/'),
            ('view_id.key', '=', 'website.homepage'),
        ], limit=1)
        active = {code for code, _name in self.env['res.lang'].get_installed()}

        if homepage:
            for lang, values in HOME_META.items():
                if lang in active:
                    homepage.with_context(lang=lang).write(values)

        Page = self.env['website.page']
        for url, titles in PAGE_TITLES.items():
            page = Page.search([
                ('website_id', '=', website.id),
                ('url', '=', url),
            ], limit=1)
            if not page:
                continue
            for lang, title in titles.items():
                if lang in active:
                    page.with_context(lang=lang).write({'website_meta_title': title})
