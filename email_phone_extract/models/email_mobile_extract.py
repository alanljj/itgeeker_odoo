# -*- coding: utf-8 -*-
###########################################################################
#    GeekerMaster奇客大师 www.geekermaster.com
#    Copyright 2017 ITGeeker <alanljj@gmail.com>
###########################################################################
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from openerp import models, fields, api, _
import re
from lxml import etree, html
from openerp import exceptions
import urllib2
import base64
import requests
#from PIL import Image
#from docx import Document
import zipfile
import xml.etree.ElementTree

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'
TABLE = WORD_NAMESPACE + 'tbl'
ROW = WORD_NAMESPACE + 'tr'
CELL = WORD_NAMESPACE + 'tc'

class ResPartner(models.Model):
    _inherit = "res.partner"

    duplicated_url = fields.Char('Existed Partner Link')
    duplicated_bol = fields.Boolean('Duplicated', default=False)
    duplicated_name = fields.Char('Existed Partner Info')
    cv_upload = fields.Binary(string="Upload CV")

    @api.model
    def generate_duplicate_link_email(self):
        partner_email_obj = self.env['res.partner'].search(
            [('is_company', '=', False), ('email', '=', self.email)])
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        self.duplicated_url = str(base_url) + "/web#id=" + str(partner_email_obj.id) + \
            "&view_type=form&model=res.partner&menu_id=1609&action=1618"
            # for gc menu_id=1609&action=1618
            # for demo menu_id=611&action=689
            # for local_withub10 menu_id=722&action=741
            # for tenseal menu_id=545&action=592
        self.duplicated_bol = True
        self.duplicated_name = '%s {%s %s %s}' % (partner_email_obj.name or '', partner_email_obj.function or '', partner_email_obj.parent_name or '', partner_email_obj.city or '')
        return

    @api.model
    def generate_duplicate_link_mobile(self):
        partner_mobile_obj = self.env['res.partner'].search(
            [('is_company', '=', False), ('mobile', '=', self.mobile)])
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        self.duplicated_url = str(base_url) + "/web#id=" + str(partner_mobile_obj.id) + \
            "&view_type=form&model=res.partner&menu_id=1609&action=1618"
            # need change menu and action
        self.duplicated_bol = True
        self.duplicated_name = '%s {%s %s %s}' % (partner_mobile_obj.name or '', partner_mobile_obj.function or '', partner_mobile_obj.parent_name or '', partner_mobile_obj.city or '')
        return


    # image url get
    # img_attach = fields.Html('Image', compute="_get_img_html")

    # def _get_img_html(self):
    #     attachment_id = self.env['ir.attachment'].search([
    #             ('res_model', '=', 'res.partner'),
    #             # ('res_id', '=', active_id),
    #         ], limit=1)[0]
    #     for elem in self:
    #         img_url = '/web/content/%s' % attachment_id
    #         elem.img_attach = '<img src="%s"/>' % img_url


    # not work coz required fields
    @api.one
    def open_duplicated_partner(self, cr, uid, ids, context=None):
        res = self.read(cr, uid, ids, ['duplicated_url'], context=context)
        duplicated_url = res[0]['duplicated_url']
        return{
                'type': 'ir.actions.act_url',
                'url': duplicated_url,
                'target': 'self'
            }
    # # @api.multi
    # # def open_duplicated_partner(self):
    #     partner_form = self.env.ref('base.view_partner_form', False)
    #     return {
    #         'name': 'Existed Partner',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'res.partner',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'target': 'new',
    #         'views': [(partner_form.id, 'form')],
    #         'view_id': 'partner_form.id',
    #         # 'flags': {'action_buttons': True},
    #     }


    # @api.model
    # def default_liepin_channel(self):
    # return self.env['crm.tracking.source'].search([('nick_name', '=',
    # 'liepin')], limit=1)

    # @api.multi
    # def popup(self):
    #     if self.duplicated_url:
    #         return self.env['popup.message'].warning(title='Email you input already exsited!', message='Same as %s email %s, please open existed partner to modify!\n %s'
    #         % (str(self.name), str(self.email), str(self.duplicated_url or '')))
        # return request.env['popup.message'].sudo().warning()

    # @api.one
    # def popup_notify(self):
    #     # for p in self:
    #     #     return request.env['popup.notification'].sudo().get_notifications()

    # @api.one
    # def import_docx(self):
    #     with zipfile.ZipFile(u'G:/git_withub_win/addons_pycharm/geeker_cv_parse/models/test.docx') as docx:
    #         tree = xml.etree.ElementTree.XML(docx.read('word/document.xml'))
    #         for table in tree.iter(TABLE):
    #             for row in table.iter(ROW):
    #                 for cell in row.iter(CELL):
    #                     self.cv = ''.join(node.text for node in cell.iter(TEXT))
                        # print ''.join(node.text for node in cell.iter(TEXT))

    # @api.one
    # def import_docx(self):
    #     document = Document('G:/git_withub_win/addons_pycharm/geeker_cv_parse/models/test.docx')
    #     #读取每段资料
    #     l = [ paragraph.text.encode('gb2312') for paragraph in document.paragraphs];
    #     #输出并观察结果，也可以通过其他手段处理文本即可
    #     for i in l:
    #         self.cv = i
        # 读取表格材料，并输出结果
        # tables = [table for table in document.tables];
        # for table in tables:
        #     for row in table.rows:
        #         for cell in row.cells:
        #             self.cv = cell.text.encode('utf-8'),'\t',

    # @api.onchange('cv_upload')
    # def onchange_cv_upload(self):
    #     if self.cv_upload:
    #         file_contents = base64.b64decode(self.cv_upload)
    #         # root = etree.fromstring(file_contents)
    #         self.cv2 = file_contents
            # attachment_list = self.env['ir.attachment'].search([
            #     ('res_model', '=', 'res.partner')
            #     # ('res_id', '=', active_id),
            # ], limit=1)
            # if attachment_list:
            #     for doc in attachment_list:
            #         # file_contents = base64.b64decode(attachment_list[0].read())
            #         # root = etree.fromstring(file_contents)
            #         self.cv = attachment_list
        #     my_elements = root.xpath('//sms')
        # for child in my_elements:

    # @api.onchange('attachment_ids')
    # def onchange_attachment(self):
    #     if self.attachment_ids:
    #         attachment_list = self.env['ir.attachment'].search([
    #             ('res_model', '=', 'res.partner')
    #         #     # ('res_id', '=', active_id),
    #         ], limit=1)
    #         if attachment_list:
    #             for doc in attachment_list:
    #                 index_content = attachment_list[0].index_content
    #         #         # file_contents = base64.b64decode(attachment_list[0].read())
    #         #         # root = etree.fromstring(file_contents)
    #                 self.cv3 = index_content
        #     my_elements = root.xpath('//sms')
        # for child in my_elements:

    @api.onchange('cv')
    def onchange_cv(self):
        if self.cv:
            cv_org = etree.HTML(self.cv)
            # tree = xml.etree.ElementTree.XML(cv_org)
            # for table in cv_org.iter(TABLE):
            #     for row in table.iter(ROW):
            #         for cell in row.iter(CELL):
            #             self.cv2 = ''.join(node.text for node in cell.iter(TEXT))
            # cv_org = html.fromstring(self.cv)
            # re_diagram=re.compile('<\s*div class="lens-resume"[^>]*>.*?[^<]*<\s*/\s*div\s*>', re.IGNORECASE)#diagram
            # self.cv2 = re.sub(re_diagram,'',self.cv)
            self.cv = self.env["ir.fields.converter"].filter_tags(self.cv)
            # self.cv5 = self.env["ir.fields.converter"].text_from_html(self.cv)
            # name extract
            if not self.name:
                name_path_liepin = "//span[@class='name']/text()"
                names_liepin = cv_org.xpath(name_path_liepin)
                name_path_linkedin = "//h1/text()"
                names_linkedin = cv_org.xpath(name_path_linkedin)
                if names_liepin and not self.name:
                    for n in names_liepin:
                        self.name = names_liepin[0].replace(u'姓名：', '')
                elif names_linkedin and not self.name:
                    for n in names_linkedin:
                        self.name = names_linkedin[0]
            # company extract
            if not self.parent_id:
                company_path_liepin = "//div[@class='resume-job-title']/span[@class='compony']/text()"
                companies_liepin = cv_org.xpath(company_path_liepin)
                company_path_linkedin = "//h3/text()"
                companies_linkedin = cv_org.xpath(company_path_linkedin)
                if companies_liepin:
                    for c in companies_liepin:
                        self.parent_id = self.env['res.partner'].search([('is_company', '=', True), '|','|','|', ('name', 'ilike', companies_liepin[0]), ('alias_name', 'ilike', companies_liepin[0]), ('introduction', 'ilike', companies_liepin[0]), ('comment', 'ilike', companies_liepin[0])], limit=1)
                        self.department = self.env['geeker.department'].search(['|', ('name', 'ilike', companies_liepin[0]), ('description', 'ilike', companies_liepin[0])], limit=1)
                        if not self.parent_id:
                            property_account_r = self.env['account.account'].search([('type', '=', 'receivable')])[0]
                            property_account_p = self.env['account.account'].search([('type', '=', 'payable')])[0]
                            self.parent_id.create({
                                'name': companies_liepin[0],
                                'is_company': True,
                                'comment': companies_liepin[0],
                                'property_account_receivable': property_account_r,
                                'property_account_payable': property_account_p
                            })
                        if not self.department:
                            self.department.env['geeker.department'].create({
                            'name': companies_liepin[0],
                            'description': companies_liepin[0]
                            })
                elif companies_linkedin:
                    for c in companies_linkedin:
                        self.parent_id = self.env['res.partner'].search([('is_company', '=', True), '|','|','|', ('name', 'ilike', companies_linkedin[0]), ('alias_name', 'ilike', companies_linkedin[0]), ('introduction', 'ilike', companies_linkedin[0]), ('comment', 'ilike', companies_linkedin[0])], limit=1)
                        self.department = self.env['geeker.department'].search(['|', ('name', 'ilike', companies_linkedin[0]), ('description', 'ilike', companies_linkedin[0])], limit=1)
                        if not self.parent_id:
                            property_account_r = self.env['account.account'].search([('type', '=', 'receivable')])[0]
                            property_account_p = self.env['account.account'].search([('type', '=', 'payable')])[0]
                            self.parent_id.create({
                                'name': companies_linkedin[0],
                                'is_company': True,
                                'comment': companies_linkedin[0],
                                'property_account_receivable': property_account_r,
                                'property_account_payable': property_account_p
                            })
                        if not self.department:
                            self.department.env['geeker.department'].create({
                            'name': companies_linkedin[0],
                            'description': companies_linkedin[0]
                            })

            # industry extract
            if not self.industry:
                xpath_leipin_industry = "//*[@id='workexp_anchor']/div[2]/table[1]/tbody/tr[1]/td/text()"
                industries = cv_org.xpath(xpath_leipin_industry)
                for i in industries:
                    self.industry = self.env['geeker.industry'].search(['|', '|', ('name', 'ilike', industries[0]), ('description', 'ilike', industries[0]), ('alias_name', 'ilike', industries[0])], limit=1)
                    if not self.industry:
                        self.industry.env['geeker.industry'].create({
                            'name': industries[0],
                            'sequence': 44,
                            'alias_name': industries[0]
                            })

            # function extract
            if not self.function:
                function_path_liepin = "//div[@class='job-list-title']/span/text()"
                functions_liepin = cv_org.xpath(function_path_liepin)
                function_path_linkedin = "//h2/text()"
                functions_linkedin = cv_org.xpath(function_path_linkedin)
                if functions_liepin:
                    for f in functions_liepin:
                        self.function = functions_liepin[0]
                elif functions_linkedin:
                    for f in functions_linkedin:
                        self.function = functions_linkedin[0]

            # email extract
            if not self.email:
                re_mail = re.compile(
                    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,6}\b", re.IGNORECASE)
                emails = re.findall(re_mail, self.cv)
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
                mobiles = re.findall(re_mobile, self.cv)
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

            # first link
            if not self.cddsource:
                # links = self.env["ir.fields.converter"].text_from_html_link(self.cv)
                link_path = "//a/@href"
                links = cv_org.xpath(link_path)
                for link in links:
                    self.website = links[0]
                    # links_result = links[0]
                    channel_liepin = re.compile(r"liepin", re.IGNORECASE)
                    match_liepin = channel_liepin.search(self.website)
                    channel_linkedin = re.compile(r"linkedin", re.IGNORECASE)
                    match_linkedin = channel_linkedin.search(self.website)
                    # cddsource_data = self.default_liepin_channel()
                    if match_liepin and not self.cddsource:
                        self.cddsource = self.env['crm.tracking.source'].search(
                            [('nick_name', '=', 'liepin')], limit=1)
                    elif match_linkedin and not self.cddsource:
                        self.cddsource = self.env['crm.tracking.source'].search(
                            [('nick_name', '=', 'linkedin')], limit=1)

            # thubm image
            if not self.image:
                link_path_thumb_liepin = "//img[@class='middleFace']/@src"
                links_thumb_liepin = cv_org.xpath(link_path_thumb_liepin)
                link_path_thumb_linkedin = "//div[@class=' presence-entity__image EntityPhoto-circle-8 ember-view']/@style"
                links_thumb_linkedin = cv_org.xpath(link_path_thumb_linkedin)
                if links_thumb_liepin:
                    for link in links_thumb_liepin:
                        links_thumb_liepin_result = links_thumb_liepin[0]
                        thumb_files = urllib2.urlopen(links_thumb_liepin_result)
                        # thumb_files = requests.get(links_thumb_liepin_result)
                        self.image = base64.b64encode(thumb_files.read())
                elif links_thumb_linkedin:
                    for link in links_thumb_linkedin:
                        links_thumb_linkedin_result = links_thumb_linkedin[0]
                        # image_url_rgx = r"""
                        #     url\(\s*        # Start function
                        #     (?P<url>[^)]*)  # URL string
                        #     \s*\)           # End function
                        # """
                        image_url_rgx = "https?://.+\.jpg"
                        re_pattern_img = re.compile(image_url_rgx, re.IGNORECASE)
                        # re_pattern_img = re.compile(image_url_rgx, re.IGNORECASE | re.VERBOSE)
                        img_urls = re.findall(re_pattern_img, links_thumb_linkedin_result.decode('utf-8'))
                        for i in img_urls:
                            thumb_files = urllib2.urlopen(img_urls[0])
                            self.image = base64.b64encode(thumb_files.read())

# self.env['partner.action.type'].get_default(),
# default=lambda self: self.env.context.get('move', 'in')
# self.env['crm.tracking.sourc'].search([('sequence', '=', 1)], limit=1)

    # @api.onchange('duplicated_url')
    # def onchange_duplicated_url(self):
    #     if self.duplicated_url:
    #         return self.env['popup.message'].warning(title='Email you input already exsited!', message='Same as %s email %s, please open existed partner to modify!\n %s'
    #         % (str(self.name), str(self.email), str(self.duplicated_url or '')))

    # @api.multi
    # def action_open_duplicated(self):
    #     for rec in self:
    #         client_action = {
    #         'type': 'ir.actions.act_url',
    #         'name': "Open Duplicated Partner",
    #         'target': 'current',
    #         'url': self.duplicated_url,
    #         }
    #         return client_action

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

    @api.model
    def check_mobile(self):
        mobile_check = self.env['res.partner'].search([('is_company', '=', False), ('mobile', '=', self.mobile)])
        return mobile_check

    @api.model
    def check_email(self):
        email_check = self.env['res.partner'].search([('is_company', '=', False), ('email', '=', self.email)])
        return email_check

    @api.onchange('mobile', 'email')
    def onchange_mobile(self):
        if self.mobile:
            self.mobile = self.mobile.strip().strip('"').replace(' ', '').replace('-', '')
            if self.check_mobile():
                self.generate_duplicate_link_mobile()
                # self.popup_windows()
                # raise exceptions.ValidationError(
                #     _('Atention please: Mobile %s already exist!') % (self.mobile)
                #         )
        if self.email:
            self.email = self.email.strip().strip('"').strip('.').replace(',', '.').replace('，', '.').replace('。', '.').replace('、', '.').replace('@yahoo.com.cn', '@aliyun.com').replace('@yahoo.cn', '@aliyun.com').lower()
            if self.check_email():
                self.generate_duplicate_link_email()
                # raise exceptions.ValidationError(
                #     _('Atention please: Email %s already exist!') % (self.email)
                #         )
                # partner_form = self.env.ref('base.view_partner_form', False)
                # partner_email_obj = self.env['res.partner'].search(
                #                         [('is_company', '=', False), ('email', '=', self.email)])[0]
                # return {
                #         'name': 'Existed Partner',
                #         'type': 'ir.actions.act_window',
                #         'res_model': 'res.partner',
                #         'view_type': 'form',
                #         'view_mode': 'form',
                #         'target': 'new',
                #         'views': [(partner_form.id, 'form')],
                #         'res_id': partner_email_obj,
                #         'view_id': False,
                #     }

    @api.onchange('cv2')
    def onchange_cv2(self):
        if self.cv2:
            cv_org2 = etree.HTML(self.cv2)
            self.cv2 = self.env["ir.fields.converter"].filter_tags(self.cv2)

    @api.onchange('cv3')
    def onchange_cv3(self):
        if self.cv3:
            cv_org3 = etree.HTML(self.cv3)
            self.cv3 = self.env["ir.fields.converter"].filter_tags(self.cv3)

    @api.onchange('cv4')
    def onchange_cv4(self):
        if self.cv4:
            cv_org4 = etree.HTML(self.cv4)
            self.cv4 = self.env["ir.fields.converter"].filter_tags(self.cv4)

    @api.onchange('cv5')
    def onchange_cv5(self):
        if self.cv5:
            cv_org5 = etree.HTML(self.cv5)
            self.cv5 = self.env["ir.fields.converter"].filter_tags(self.cv5)
