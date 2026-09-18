from odoo import models


class ThemeHotelArena(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_hotel_arena_post_copy(self, mod):
        # Disable default header
        self.disable_view('website.template_header_default')
        # Enable custom header
        self.enable_view('theme_hotel_arena.ha_header')
        # Enable footer links
        self.enable_view('website.template_footer_links')

        # Remove default Odoo menu items that duplicate our theme menus
        website = self.env['website'].get_current_website()
        Menu = self.env['website.menu']
        for url in ['/', '/contactus']:
            menus = Menu.search([
                ('website_id', '=', website.id),
                ('url', '=', url),
            ])
            if menus:
                menus.unlink()

        # Unpublish default contactus page (we use /kontakt instead)
        contactus_page = self.env['website.page'].search([
            ('website_id', '=', website.id),
            ('url', '=', '/contactus'),
        ], limit=1)
        if contactus_page:
            contactus_page.is_published = False
