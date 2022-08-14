# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

class PosOrder(models.Model):
    _inherit = 'pos.order'

    numero_autorizacion = fields.Char('Numero de autorización')

    def check_reference(self, config_id, product_dicc):
        confi_pos_config_id = self.env['pos.config'].search([('id', '=', config_id[0])])

        for pos_config_id in confi_pos_config_id:
            xml_json = pos_config_id.red_autentication('CheckReference', product_dicc)
            logging.warning('Desde pos.order')
            logging.warning(xml_json)
            if xml_json != False and 'CheckReference' in xml_json:
                logging.warning('Primera parte')
                if xml_json['CheckReference']:
                    logging.warning(xml_json)
                    pos_config_id.check_reference = xml_json['CheckReference']
        return True
