from openerp import models, fields, api, tools
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime
from lxml import etree
import base64

class esms_import(models.TransientModel):

    _name = "esms.import"

    smsfile = fields.Binary(string="Load SMS Backup", required=True)


    attachments = self.env['ir.attachment'].search(
            [('db_datas', '!=', False)], limit=limit)
imported_attachment = self.env['ir.attachment'].search([
                ('res_model', '=', 'res.users'),
                ('res_id', '=', imported_user.id),
            ])

    @api.one
    def read_smsbackup(self):
        file_contents = base64.b64decode(self.smsfile)
        root = etree.fromstring(file_contents)
        my_elements = root.xpath('//sms')
    for child in my_elements:
        attributes = child.attrib
            body = attributes["body"]
            type = attributes["type"]
            from_address = ""
            to_address = ""

            if type == "2":
                direction = "O"
                from_address = attributes["address"]

            elif type == "1":
                direction = "I"
                to_address = attributes["address"]


            self.env['esms.history'].create({'from_mobile': from_address, 'to_mobile':to_mobile, 'sms_content':body, 'direction':direction})

            def related_attachment(session, thejob):
    attachment_id = thejob.args[1]

    action = {
        'name': _("Attachment"),
        'type': 'ir.actions.act_window',
        'res_model': "ir.attachment",
        'view_type': 'form',
        'view_mode': 'form',
        'res_id': attachment_id,
    }
    return action
