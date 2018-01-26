# -*- coding: utf-8 -*-
###########################################################################
#    GeekerMaster奇客大师 www.geekermaster.com
#    Copyright 2017 ITGeeker <alanljj@gmail.com>
###########################################################################
from openerp import models, fields, api, _
import re
from lxml import etree, html


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.onchange('comment')
    def onchange_comment(self):
        # email extract
        if not self.email:
            re_mail = re.compile(
                r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,6}\b", re.IGNORECASE)
            emails = re.findall(re_mail, self.comment)
            for e in emails:
                # if not self.email:
                self.email = emails[0]
                existed_email = self.search(
                    [('is_company', '=', False), ('email', '=', emails[0])])
                if existed_email:
                    self.generate_duplicate_link_email()
                else:
                    self.duplicated_bol = False
                # partner_email_obj = self.env['res.partner'].search(
                #     [('is_company', '=', False), ('email', '=', emails[0])])[0]
                # base_url = self.env['ir.config_parameter'].get_param('web.base.url')
                # # url = ("%s" + "/web#id=" + "%s" +
                # # "&view_type=form&model=res.partner&menu_id=722&action=741")
                # # % (base_url, partner_email_obj.id)
                # self.duplicated_url = str(base_url) + "/web#id=" + str(partner_email_obj.id) + \
                #     "&view_type=form&model=res.partner&menu_id=1609&action=1618"
                # self.duplicated_bol = True
                # self.duplicated_name = '%s {%s %s %s}' % (partner_email_obj.name or '', partner_email_obj.function or '', partner_email_obj.parent_name or '', partner_email_obj.city or '')
                # if self.duplicated_url:
                #     return self.env['popup.message'].warning(title='Email you input already exsited!', message='Same as %s email %s, please open existed partner to modify!\n %s'
                #         % (str(self.name), str(self.email), str(self.duplicated_url or '')))
                # raise exceptions.ValidationError(
                # _('Atention please: Email %s already exist!\n \
                #     Same as %s [%s] from %s \n \
                #     %s/web#id=%s&view_type=form&model=res.partner&menu_id=722&action=741') %
                # # # self.name or '', self.function or 'unknown position',
                # (emails[0],
                #     partner_email_obj.name, partner_email_obj.function or '', partner_email_obj.parent_name or 'unknown company',
                #     base_url, partner_email_obj.id))

        # mobile extract
        if not self.mobile:
            re_mobile = re.compile(
                r"1[34578][012356789]\d{8}|134[012345678]\d{7}", re.IGNORECASE)
            mobiles = re.findall(re_mobile, self.comment)
            for m in mobiles:
                self.mobile = mobiles[0]
                existed_mobile = self.search([('is_company', '=', False), ('mobile', '=', mobiles[0])])
                if existed_mobile:
                    self.generate_duplicate_link_mobile()
                else:
                    self.duplicated_bol = False

                # partner_mobile_obj = self.env['res.partner'].search([('is_company', '=', False), ('mobile', '=', mobiles[0])])[0]
                # base_url = self.env['ir.config_parameter'].get_param('web.base.url')
                # self.duplicated_url = str(base_url) + "/web#id=" + str(partner_mobile_obj.id) + \
                #     "&view_type=form&model=res.partner&menu_id=1609&action=1618"
                # self.duplicated_bol = True
                # self.duplicated_name = '%s {%s %s %s}' % (partner_mobile_obj.name or '', partner_mobile_obj.function or '', partner_mobile_obj.parent_name or '', partner_mobile_obj.city or '')
                # if self.duplicated_url:
                #     return self.env['popup.message'].warning(title='Mobile you input already exsited!', message='Same as %s email %s, please open existed partner to modify!\n %s'
                #         % (str(self.name), str(self.mobile), str(self.duplicated_url or '')))

            #     raise exceptions.ValidationError(
            #     _('Atention please: Mobile %s already exist!\n \
            #         Same as %s [%s] from %s \n \
            #         %s/web#id=%s&view_type=form&model=res.partner&menu_id=722&action=741') %
            #     (mobiles[0],
            #         partner_mobile_obj.name, partner_mobile_obj.function or '', partner_mobile_obj.parent_name or 'unknown company',
            #         base_url, partner_mobile_obj.id))
