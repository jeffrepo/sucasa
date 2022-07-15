# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging

class ResPartner(models.Model):
    _inherit = "res.partner"

    clientid = fields.Char(string="Identificador de cliente")
