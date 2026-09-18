{
    'name': 'Hotel Arena Theme',
    'summary': 'Odoo 18 dark theme for Hotel Arena Chomutov - elegant hotel website with red accent design',
    'description': """
        Complete hotel website theme with dark design (Playfair Display + DM Sans).
        Features:
        - Dark theme with red (#F07070) accent and crimson (#8B1A2B) gradient
        - Fixed transparent nav with blur-on-scroll effect
        - Full-screen hero slider with parallax zoom
        - Room cards with 3:4 aspect ratio and hover overlays
        - Numbered feature list with image
        - Exterior showcase with statistics
        - Restaurante Brasileiro branded section (green/gold)
        - Concierge services grid
        - Location section with grayscale map
        - Photo gallery with lightbox
        - Contact form with AJAX submission
        - Reveal-on-scroll animations
        - Responsive design (mobile-first, 4 breakpoints)
    """,
    'category': 'Theme/Hotel',
    'version': '18.0.1.0.0',
    'author': 'VaryShop',
    'website': 'https://arenahotel.cz',
    'license': 'LGPL-3',
    'depends': [
        'theme_common',
        'website',
        'settings_hotel_arena',
    ],
    'data': [
        # 1. Generate primary template (MUST be first)
        'data/generate_primary_template.xml',
        # 2. Asset registration (SCSS bundles)
        'data/ir_asset.xml',
        # 3. Layout (header, footer)
        'views/layout.xml',
        # 4. Image library
        'views/images_library.xml',
        # 5. Snippets
        'views/snippets/s_hero_slider.xml',
        'views/snippets/s_parallax_section.xml',
        'views/snippets/s_about_hotel.xml',
        'views/snippets/s_rooms_preview.xml',
        'views/snippets/s_rooms_listing.xml',
        'views/snippets/s_room_prices.xml',
        'views/snippets/s_hotel_features.xml',
        'views/snippets/s_hotel_gallery.xml',
        'views/snippets/s_restaurant.xml',
        'views/snippets/s_breakfast.xml',
        'views/snippets/s_contact_form.xml',
        # 6. Snippet registry
        'views/snippets/snippets_registry.xml',
        # 7. Pages
        'views/pages.xml',
        # 8. Homepage (inherit on website.homepage, NOT theme template)
        'data/homepage.xml',
        # 9. Menu data
        'data/website_menu_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'theme_hotel_arena/static/src/scss/theme.scss',
            'theme_hotel_arena/static/src/scss/header.scss',
            'theme_hotel_arena/static/src/scss/footer.scss',
            'theme_hotel_arena/static/src/scss/rooms.scss',
            'theme_hotel_arena/static/src/scss/gallery.scss',
            'theme_hotel_arena/static/src/scss/contact.scss',
            'theme_hotel_arena/static/src/scss/responsive.scss',
            'theme_hotel_arena/static/src/js/reveal.js',
            'theme_hotel_arena/static/src/js/snippets/s_hotel_gallery.js',
            'theme_hotel_arena/static/src/js/snippets/s_contact_form.js',
        ],
    },
    'configurator_snippets': {
        'homepage': [
            's_hero_slider',
            's_home_about',
            's_home_restaurant',
            's_rooms_preview',
            's_concierge_services',
            's_hotel_gallery',
        ],
    },
    'images': [
        'static/description/icon.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
