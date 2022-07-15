# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from odoo.exceptions import UserError, ValidationError

class PosSession(models.Model):
    _inherit = 'pos.session'

    sessionid = fields.Char('SessionId')
    # Se ejecuta manualmente cuando sea necesario
    def _get_all_product_extend_list_session(self):
        for session in self:
            session.config_id._get_all_product_extend_list()
        return True

    #Se ejecuta manualmente
    def _get_session(self):
        for session in self:
            xml_json = session.config_id.red_autentication('GetSession')
        return True
