# -*- coding: utf-8 -*-
###########################################################################
#    GeekerMaster奇客大师 www.geekermaster.com
#    Copyright 2017 ITGeeker <alanljj@gmail.com>
###########################################################################
from openerp import models, fields, api, _
import re
from lxml import etree, html
from openerp import exceptions


class ResPartner(models.Model):
    _inherit = "res.partner"

    # @api.model
    # def default_liepin_channel(self):
    #     return self.env['crm.tracking.source'].search([('nick_name', '=', 'liepin')], limit=1)

    @api.multi
    def open_duplicated_partner(self):
        partner_form = self.env.ref('base.view_partner_form', False)
        return {
            'name': 'Existed Partner',
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'views': [(partner_form.id, 'form')],
            'view_id': 'partner_form.id',
            'flags': {'action_buttons': True},
        }

    @api.onchange('cv')
    def onchange_cv(self):
        if self.cv:
            self.cv5 = self.env["ir.fields.converter"].text_from_html(self.cv)
            cv_org = etree.HTML(self.cv)
            # name extract
            names_path = "//span[@class='name']/text()"
            names = cv_org.xpath(names_path)
            for n in names:
                self.name = names[0].replace(u'姓名：', '')
            # company extract
            xpath_liepin_company = "//div[@class='resume-job-title']/span[@class='compony']/text()"
            companies = cv_org.xpath(xpath_liepin_company)
            for company in companies:
                self.parent_id = self.env['res.partner'].search([('is_company', '=', True),'|','|', ('name', 'ilike', companies[0]), ('alias_name', 'ilike', companies[0]),('introduction', 'ilike', companies[0])])
                if not self.parent_id:
                    self.parent_id.create({
                                            'name':companies[0],
                                            'is_company': True
                                            })
                    # super(AdvanceRule, self).write(vals)
                # self.alias_name = companies[0]
            # company extract
            xpath_leipin_industry = "//*[@id='workexp_anchor']/div[2]/table[1]/tbody/tr[1]/td/text()"
            industries = cv_org.xpath(xpath_leipin_industry)
            for industry in industries:
                self.industyry = self.env['geeker.industry'].search(['|','|', ('name', 'ilike', industries[0]), ('description', 'ilike', industries[0]),('alias_name', 'ilike', industries[0])])
                if not self.industyry:
                    self.industyry = self.env['geeker.industry'].create({'name':industries[0]})

            # function extract
            functions_path = "//div[@class='job-list-title']/span/text()"
            functions = cv_org.xpath(functions_path)
            for n in functions:
                self.function = functions[0]
            # email extract
            re_mail = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,6}\b", re.IGNORECASE)
            emails = re.findall(re_mail, self.cv)
            for e in emails:
                # if not self.email:
                self.email = emails[0]
                existed_email = self.search([('is_company', '=', False), ('email', '=', emails[0])])
                if existed_email:
                    partner_email_obj = self.env['res.partner'].search([('is_company', '=', False), ('email', '=', emails[0])])[0]
                    base_url = self.env['ir.config_parameter'].get_param('web.base.url')
                    raise exceptions.ValidationError(
                    _('Atention please: Email %s already exist!\n \
                        Same as %s [%s] from %s \n \
                        %s/web#id=%s&view_type=form&model=res.partner&menu_id=611&action=689') %
                        # for withub win: menu_id=722&action=741
                        # for master_gc: menu_id=1609&action=1618
                        # for demo_gm: menu_id=611&action=689
                        # Link:<a href="%s">link name</a>
                    # self.name or '', self.function or 'unknown position',
                    (emails[0],
                        partner_email_obj.name, partner_email_obj.function or '', partner_email_obj.parent_name or 'unknown company',
                        base_url, partner_email_obj.id))
                    # return {
                    #         'name': _('Duplicated Talent'),
                    #         'view_type': 'form',
                    #         'view_mode': 'form',
                    #         'res_model': 'res.partner',
                    #         'type': 'ir.actions.act_window',
                    #         'views': [(base.view_partner_form,'form')],
                    #         'target': 'new',
                    #        }

            # mobile extract
            re_mobile = re.compile(r"1[34578][012356789]\d{8}|134[012345678]\d{7}", re.IGNORECASE)
            mobiles = re.findall(re_mobile, self.cv)
            for m in mobiles:
                # if not self.mobile:
                self.mobile = mobiles[0]
                existed_mobile = self.search([('is_company', '=', False), ('mobile', '=', mobiles[0])])
                if existed_mobile:
                    partner_mobile_obj = self.env['res.partner'].search([('is_company', '=', False), ('mobile', '=', mobiles[0])])[0]
                    base_url = self.env['ir.config_parameter'].get_param('web.base.url')
                    raise exceptions.ValidationError(
                    _('Atention please: Mobile %s already exist!\n \
                        Same as %s [%s] from %s \n \
                        %s/web#id=%s&view_type=form&model=res.partner&menu_id=722&action=741') %
                    (mobiles[0],
                        partner_mobile_obj.name, partner_mobile_obj.function or '', partner_mobile_obj.parent_name or 'unknown company',
                        base_url, partner_mobile_obj.id))

            # first link
            links = self.env["ir.fields.converter"].text_from_html_link(self.cv)
            for link in links:
                self.website = links[0]
                # links_result = links[0]
                pattern_source_channel = re.compile(r"liepin", re.IGNORECASE)
                match_liepin = pattern_source_channel.search(self.website)
                # cddsource_data = self.default_liepin_channel()
                if match_liepin and not self.cddsource:
                    self.cddsource = self.env['crm.tracking.source'].search([('nick_name', '=', 'liepin')], limit=1)
                    # self.alias_name = cddsource_data
                    # self.cddsource = cddsource_data
# self.env['partner.action.type'].get_default(),
# default=lambda self: self.env.context.get('move', 'in')
# self.env['crm.tracking.sourc'].search([('sequence', '=', 1)], limit=1)

    # @api.one
    # # @api.constrains("email", "mobile")
    # def _check_email_mobile(self):
    #     if self.email:
    #         existed_emails = self.search([('is_company', '=', False), ('email', '=', self.email)])
    #         if existed_emails:
    #             raise exceptions.ValidationError(
    #                 _("Field '%s' already exist") % one.email)

    # @api.multi
    # @api.constrains("email", "mobile")
    # def _check_email_mobile(self):
        # for one in self:
        #     if one.email:
        #         emails = one.search([('email', '=', one.email)])
        #         if len(emails) > 1:
        #             raise exceptions.ValidationError(
        #                 _("Field '%s' already exist") % one.email)
            # if not one.env.context.get('skip_check'):
            #     lines = one.search([('export_id', '=', one.export_id.id),
            #                         ('name', '=', one.name)])
            #     if len(lines) > 1:
            #         raise exceptions.ValidationError(
            #             _("Field '%s' already exists") % one.name)
