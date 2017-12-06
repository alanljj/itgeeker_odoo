# -*- coding: utf-8 -*-
###########################################################################
#    GeekerMaster奇客大师 www.geekermaster.com
#    Copyright 2017 ITGeeker <alanljj@gmail.com>
###########################################################################
{
    "name": "Auto fill Email and Phone",
    "version": "8.0.1.0.0",
    "author": "ITGeeker",
    "website": "http://www.itgeeker.net",
    "images": ["static/description/icon.png"],
    "category": "ITGeeker",
    "price": 49.99,
    "currency": "EUR",
    "summary": "CV contact extract and parse",
    "description": '''
    remove html style\n
    ''',
    "depends": [
        "base",
        # "html_image_url_extractor",
        "html_text",
        "geeker_crm_tracking_source",
        "geeker_industry",
        "geeker_partner",
        # "popup_message",
    ],
    "data": [
        "views/geeker_cv_parse.xml",
    ],
    "demo": [],
    "test": [],
    "js": [],
    "css": [],
    "qweb": [],
    "auto_install": False,
    "installable": True
}
