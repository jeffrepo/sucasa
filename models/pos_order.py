# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

class PosOrder(models.Model):
    _inherit = 'pos.order'

    numero_autorizacion = fields.Char('Numero de autorización')

    def check_reference(self, config_id, product_dicc):
        confi_pos_config_id = self.env['pos.config'].search([('id', '=', config_id[0])])
        order_check_reference = ''
        for pos_config_id in confi_pos_config_id:
            xml_json = pos_config_id.red_autentication('CheckReference', product_dicc)
            if xml_json != False and 'CheckReference' in xml_json:
                if xml_json['CheckReference']:
                    order_check_reference = xml_json['CheckReference']
        logging.warning('pos.order check_reference()---------------------------')
        logging.warning(order_check_reference)
        return True

    def _process_order(self, orders, draft, existing_order):
        logging.warning('Intentando heredar ')
        logging.warning(orders)
        uid = ''
        dicc = {
        'product_id':0,
        'amount':0,
        'reference_1':'',
        'reference_2':'',
        'reference_3':'',
        'pos_transaccion_id':'',
        'sesion':'',
        }
        for linea in orders['data']['lines']:
            if linea[2]:
                logging.warning(linea[2]['product_id'])
                producto = self.env['product.product'].search([('id', '=', linea[2]['product_id'] )])
                if producto and producto.red_id:
                    if dicc['product_id']==0:
                        dicc['product_id']=producto.red_id
                        dicc['amount']=(linea[2]['price_unit'] * linea[2]['qty'])
                        dicc['reference1']= producto.reference1
                        dicc['reference_2']= producto.reference2
                        dicc['reference_3']=producto.reference3
                        if orders['data']['uid']:
                            uid = orders['data']['uid'].replace('-','')
                        dicc['pos_transaccion_id']=uid[0:9]

        sesiones = self.env['pos.session'].search([('id', '=', orders['data']['pos_session_id'])])

        if sesiones:
            logging.warning('Sesion--')
            logging.warning(sesiones.config_id.id)
            id_config = sesiones.config_id.id
            for sesion in sesiones:
                dicc['sesion']=sesion.sessionid
                logging.warning('Siguiente parte')
                xml_json = sesion.config_id.red_autentication('Sale', dicc)
                logging.warning('despues de xml_json')
                logging.warning(xml_json)
                if xml_json != False and 'CheckReference' in xml_json:
                    if xml_json['Sale']:
                        pos_config_id._process_order = xml_json['Sale']


        res = super(PosOrder, self)._process_order(orders, draft, existing_order)
        return res

    def get_balance_by_bag(self, config_id, number):
        confi_pos_config_id = self.env['pos.config'].search([('id', '=', config_id[0])])
        pos_order_get_balance_by = False
        for pos_config_id in confi_pos_config_id:
            xml_json = pos_config_id.red_autentication('GetBalanceByBag', number[0])
            if xml_json != False and 'BagId' in xml_json:
                if xml_json:
                    pos_order_get_balance_by = xml_json
        logging.warning('Que estoy trayendo desde x lugar 2')
        logging.warning(pos_order_get_balance_by)
        if pos_order_get_balance_by:
            return True
        else:
            return False
