# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from odoo.exceptions import UserError, ValidationError

class PosSession(models.Model):
    _inherit = 'pos.session'

    sessionid = fields.Char('SessionId')
    
    # Se ejecuta manualmente cuando sea necesario
    def get_all_product_extend_list_session(self):
        for session in self:
            session.config_id._get_all_product_extend_list()
        return True

    #Se ejecuta manualmente
    def get_session(self):
        for session in self:
            if session.config_id.postoken:
                xml_json = session.config_id.red_autentication('GetSession', False)
                logging.warning(xml_json)
                if xml_json and "SessionId" in xml_json:
                    if xml_json["SessionId"]:
                        session.sessionid = xml_json["SessionId"]
        return True

    def action_pos_session_open(self):
        res = False
        logging.warning('action_pos_session_open')
        logging.warning(self.config_id.clerkcode)
        if self.config_id.postoken == False or self.config_id.clerkcode == False:
            res = super(PosSession, self).action_pos_session_open()
        else:
            self.get_session()
            # logging.warning('button action pos session open')
            # logging.warning(self.config_id)
            # logging.warning(self.payment_method_ids.actualizar_catalogos(self.config_id))
            self.config_id.get_available_banks(self.config_id)
            self.get_all_product_extend_list_session()
            self.payment_method_ids.actualizar_catalogos(self.config_id)
            res = super(PosSession, self).action_pos_session_open()
        return res
    
    def activate_session(self):
        logging.warning('Sesión automatica')
        open_sessions = self.env['pos.session'].search([('state', '=', 'opened')])
        logging.warning(open_sessions)
        for session in open_sessions:
            logging.warning('Sesión abierta :D')
            if session.sessionid:
                session.get_session()
                logging.warning('Ya se cambio el token')
        return True