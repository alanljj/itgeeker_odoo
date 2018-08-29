# -*- coding: utf-8 -*-
###########################################################################
#    GeekerMaster奇客大师 www.geekermaster.com
#    Copyright 2018 ITGeeker <alanljj@gmail.com>
###########################################################################
{
    'name': 'Tree list highlighted',
    'version': '8.0.1.0.0',
    'category': 'ITGeeker',
    "price": 1.99,
    "currency": "EUR",
    'summary': 'odoo list view table tr hover background color',
    'author': 'ITGeeker',
    'website': 'https://www.itgeeker.net',
    'images': ['static/description/main_screen.png'],
    'description': """
    The purpose of this module is to deploy your own custome theme in GeekerMaster!\n
    1.0.3 add web_form_sticky_header, stick header for form\n
    """,
    'depends': ['website'],
    'data': [
        'views/website_templates.xml',
    ],
    'application': True,
    'installable': True,
}
