# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _, SUPERUSER_ID

class ProductTemplate(models.Model):
    _inherit = "product.template"

    red_id = fields.Integer("ProductId")
    reference1 = fields.Char("Reference 1")
    reference2 = fields.Char("Reference 2")
    reference3 = fields.Char('Reference 3')
    lenght_ref1 = fields.Integer("Lenght Ref1")
    lenght_ref2 = fields.Integer("Lenght Ref2")
    lenght_ref3 = fields.Integer("Lenght Ref3")
    regex_ref2 = fields.Char("RegexRef2")
    validate_ref1 = fields.Char("ValidateRef1")
    validate_ref2 = fields.Char("ValidateRef2")
    validate_ref3 = fields.Char("ValidateRef3")
    carrier_id = fields.Many2one("sucasa.carrier","Carrier")
    legal_information = fields.Char("Lega Information")
    support_query = fields.Boolean(string='Support Query') 
