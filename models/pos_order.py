# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import random
class PosOrder(models.Model):
    _inherit = 'pos.order'

    add_info1 = fields.Char('Información adicional 1')
    add_info2 = fields.Char('Información adicional 2')
    add_info3 = fields.Char('Información adicional 3')
    legal_info = fields.Char('Información legal')
    numero_autorizacion = fields.Char('Numero de autorización')
    provider_authorizacion = fields.Char('Autorización de proveedor')
    reference_1 = fields.Char('Reference 1')
    reference_2 = fields.Char('Reference 2')
    reference_3 = fields.Char('Reference 3')
    transaccion_id = fields.Char('Identificador de transacción')
    transaccion_date = fields.Date('Fecha de transacción')
    comision = fields.Float('Comision')
    iva_comision = fields.Float('IVA comision')


    def send_redMas_informationn(self, order):
        validation = {'error': False, 'transaccion': False}
        logging.warning('send_redMas_information')
        logging.warning(order)
        return validation

    def check_reference(self, config_id, product_dicc):
        logging.warning('Welcome to check_reference from pos.order-----------------------')
        order_check_reference = {}
        confi_pos_config_id = self.env['pos.config'].search([('id', '=', config_id[0])])
        for pos_config_id in confi_pos_config_id:
            xml_json = pos_config_id.red_autentication('CheckReference', product_dicc)
            if xml_json != False and 'ResponseCode' in xml_json:

                if xml_json['ResponseCode'] == '000':
                    order_check_reference['ResponseMessage'] = False
            else:
                order_check_reference['ResponseMessage'] = xml_json

        return order_check_reference

#     def _process_order(self, order, draft, existing_order):
#         logging.warning('Intentando heredar ')
#         logging.warning(order)

#         product_dicc={
#           'product_id':0,
#           'reference1':'',
#           'reference2':'',
#           'reference3':'',
#           'pos_transaccion_id':'',
#           'amount':0,
#           'no_session':0,
#           'support_query':False
#         }
#         dicc_fields_data={
#         'transaccion_id':'',
#         'transaccion_date':'',
#         'provider_authorizacion':'',
#         'add_info1':'',
#         'add_info2':'',
#         'add_info3':'',
#         }
#         number = 0
#         for linea in order['data']['lines']:
#             if linea[2]:
#                 # logging.warning(linea)
#                 logging.warning(linea[2]['product_id'])
#                 producto = self.env['product.product'].search([('id', '=', linea[2]['product_id'] )])
#                 if producto and producto.red_id:
#                     if product_dicc['product_id']==0:
#                         logging.warning(producto)
#                         product_dicc['product_id']=producto.red_id
#                         product_dicc['amount']=(linea[2]['price_unit'] * linea[2]['qty'])
#                         product_dicc['reference1']= order['data']['reference1']
#                         if order['data']['reference2']:
#                             product_dicc['reference2'] = order['data']['reference2']
#                         else:
#                             product_dicc['reference2']=producto.reference2
#                         product_dicc['reference3']= order['data']['reference3']
#                         xi = 100000000
#                         xf = 999999999
#                         nr = random.randint(xi,xf)
#                         product_dicc['pos_transaccion_id']= nr
#                     if producto.support_query:
#                         product_dicc['support_query'] = True
#                     logging.warning(producto.categ_id[0].name)
#                     if producto.categ_id[0].name == 'Recarga':
#                         number = 1
#                     else:
#                         number = 2
#         #                 dicc['reference_3']=producto.reference3
#         #                 if orders['data']['uid']:
#         #                     uid = orders['data']['uid'].replace('-','')
#         #                 dicc['pos_transaccion_id']=uid[0:9]
#         #
#         sesiones = self.env['pos.session'].search([('id', '=', order['data']['pos_session_id'])])

#         if sesiones:
#             id_config = sesiones.config_id.id
#             for sesion in sesiones:
#                 pos_config = [sesion.config_id.id]
#                 product_dicc['session']=sesion.sessionid
#         if product_dicc['product_id']>0:
#             if product_dicc['support_query'] == True:
#                 value_red_mas_support_query = self.checkRedMas_supportQuery(pos_config, [product_dicc], [number])
#                 logging.warning('Producto con support query')
#                 logging.warning(value_red_mas_support_query)
#                 if value_red_mas_support_query[0] == True:
#                     res = super(PosOrder, self)._process_order(order, draft, existing_order)
#                     order_red_mas = self.env['pos.order'].search([('id', '=', res)])
#                     if value_red_mas_support_query[1]:
#                         if value_red_mas_support_query[1]['TransactionId']:
#                             order_red_mas.transaccion_id = str(value_red_mas_support_query[1]['TransactionId'])
#                         if value_red_mas_support_query[1]['TransactionDate']:
#                             order_red_mas.transaccion_date = str(value_red_mas_support_query[1]['TransactionDate'])
#                         if value_red_mas_support_query[1]['ProviderAuthorization']:
#                             order_red_mas.provider_authorizacion = str(value_red_mas_support_query[1]['ProviderAuthorization'])
#                         if 'AditionalInfo1' in value_red_mas_support_query[1]:
#                             if value_red_mas_support_query[1]['AditionalInfo1']:
#                                 order_red_mas.add_info1 = str(value_red_mas_support_query[1]['AditionalInfo1'])
#                         if 'AditionalInfo2' in value_red_mas_support_query[1]:
#                             if value_red_mas_support_query[1]['AditionalInfo2']:
#                                 order_red_mas.add_info2 = str(value_red_mas_support_query[1]['AditionalInfo2'])
#                         if 'AditionalInfo4' in value_red_mas_support_query[1]:
#                             if value_red_mas_support_query[1]['AditionalInfo4']:
#                                 order_red_mas.add_info3 = str(value_red_mas_support_query[1]['AditionalInfo4'])
#                         if 'LegalInformation' in value_red_mas_support_query[1]:
#                             if value_red_mas_support_query[1]['LegalInformation']:
#                                 order_red_mas.legal_info = str(value_red_mas_support_query[1]['LegalInformation'])
#                         if order['data']['reference1']:
#                             order_red_mas.reference_1 = order['data']['reference1']
#                         if order['data']['reference2']:
#                             order_red_mas.reference_2 = order['data']['reference2']
#                         if order['data']['reference3']:
#                             order_red_mas.reference_3 = order['data']['reference3']
#                 else:
#                     logging.warning('En algun else')
#                     logging.warning(value_red_mas_support_query)
#                     raise UserError(value_red_mas_support_query[0]['ResponseMessage'])
#             else:
#                 value_red_mas = self.checkRedMas(pos_config, [product_dicc], [number])
#                 logging.warning('No support query')
#                 logging.warning(value_red_mas)
#                 if value_red_mas[0]['ResponseMessage'] == False:
#                     res = super(PosOrder, self)._process_order(order, draft, existing_order)
#                     order_red_mas = self.env['pos.order'].search([('id', '=', res)])
#                     if value_red_mas[1]:
#                         if value_red_mas[1]['TransactionId']:
#                             order_red_mas.transaccion_id = str(value_red_mas[1]['TransactionId'])
#                         if value_red_mas[1]['TransactionDate']:
#                             order_red_mas.transaccion_date = str(value_red_mas[1]['TransactionDate'])
#                         if value_red_mas[1]['ProviderAuthorization']:
#                             order_red_mas.provider_authorizacion = str(value_red_mas[1]['ProviderAuthorization'])
#                         if 'AditionalInfo1' in value_red_mas[1]:
#                             if value_red_mas[1]['AditionalInfo1']:
#                                 order_red_mas.add_info1 = str(value_red_mas[1]['AditionalInfo1'])
#                         if 'AditionalInfo2' in value_red_mas[1]:
#                             if value_red_mas[1]['AditionalInfo2']:
#                                 order_red_mas.add_info2 = str(value_red_mas[1]['AditionalInfo2'])
#                         if 'AditionalInfo4' in value_red_mas[1]:
#                             if value_red_mas[1]['AditionalInfo4']:
#                                 order_red_mas.add_info3 = str(value_red_mas[1]['AditionalInfo4'])
#                         if 'LegalInformation' in value_red_mas[1]:
#                             if value_red_mas[1]['LegalInformation']:
#                                 order_red_mas.legal_info = str(value_red_mas[1]['LegalInformation'])
#                         if order['data']['reference1']:
#                             order_red_mas.reference_1 = order['data']['reference1']
#                         if order['data']['reference2']:
#                             order_red_mas.reference_2 = order['data']['reference2']
#                         if order['data']['reference3']:
#                             order_red_mas.reference_3 = order['data']['reference3']
#                 else:
#                     logging.warning('Entrando al else por que ps')
#                     logging.warning(value_red_mas)
#                     raise ValidationError(value_red_mas[0]['ResponseMessage'])
#         logging.warning('Que ondaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
#         logging.warning(res)
#         return res

    def send_redMas_information(self, order):
        validation = {'error': False}
        logging.warning('Intentando heredar 1 ')
        logging.warning(order)
        product_dicc={
          'product_id':0,
          'reference1':'',
          'reference2':'',
          'reference3':'',
          'pos_transaccion_id':'',
          'amount':0,
          'no_session':0,
          'support_query':False
        }
        dicc_fields_data={
        'transaccion_id':'',
        'transaccion_date':'',
        'provider_authorizacion':'',
        'add_info1':'',
        'add_info2':'',
        'add_info3':'',
        }
        number = 0
        for linea in order[0]['data']['lines']:
            if linea[2]:
                producto = self.env['product.product'].search([('id', '=', linea[2]['product_id'] )])
                if producto and producto.red_id:
                    if product_dicc['product_id']==0:
                        product_dicc['product_id']=producto.red_id
                        product_dicc['amount']=(linea[2]['price_unit'] * linea[2]['qty'])
                        if 'reference1' in order[0]['data']:
                            product_dicc['reference1']= order[0]['data']['reference1']
                        if 'data' in order[0] and 'reference2' in order[0]['data']:
                            if order[0]['data']['reference2']:
                                product_dicc['reference2'] = order[0]['data']['reference2']
                        else:
                            product_dicc['reference2']=producto.reference2
                        product_dicc['reference3']= order[0]['data']['reference3']
                        xi = 100000000
                        xf = 999999999
                        nr = random.randint(xi,xf)
                        product_dicc['pos_transaccion_id']= nr
                    if producto.support_query:
                        product_dicc['support_query'] = True
                    logging.warning(producto.categ_id[0].name)
                    if producto.categ_id[0].name == 'Recarga':
                        number = 1
                    else:
                        number = 2
        #                 dicc['reference_3']=producto.reference3
        #                 if orders['data']['uid']:
        #                     uid = orders['data']['uid'].replace('-','')
        #                 dicc['pos_transaccion_id']=uid[0:9]
        #
        sesiones = self.env['pos.session'].search([('id', '=', order[0]['data']['pos_session_id'])])

        if sesiones:
            id_config = sesiones.config_id.id
            for sesion in sesiones:
                if sesion.config_id.postoken == False:
                    return super(PosOrder, self)._process_order(order, draft, existing_order)
                pos_config = [sesion.config_id.id]
                product_dicc['session']=sesion.sessionid
        if product_dicc['product_id']>0:
            if product_dicc['support_query'] == True:
                value_red_mas_support_query = self.checkRedMas_supportQuery(pos_config, [product_dicc], [number])
                logging.warning('Producto con support query')
                logging.warning(value_red_mas_support_query)
                if value_red_mas_support_query[0] == True:
                    # res = super(PosOrder, self)._process_order(order, draft, existing_order)
                    # validation = True
                    # order_red_mas = self.env['pos.order'].search([('id', '=', res)])
                    if value_red_mas_support_query[1]:
                        if value_red_mas_support_query[1]['TransactionId']:
                            validation['TransactionId'] = str(value_red_mas_support_query[1]['TransactionId'])
                            # order_red_mas.transaccion_id = str(value_red_mas_support_query[1]['TransactionId'])
                        if value_red_mas_support_query[1]['TransactionDate']:
                            validation['TransactionDate'] = str(value_red_mas_support_query[1]['TransactionDate'])
                            # order_red_mas.transaccion_date = str(value_red_mas_support_query[1]['TransactionDate'])
                        if value_red_mas_support_query[1]['ProviderAuthorization']:
                            validation['ProviderAuthorization'] = str(value_red_mas_support_query[1]['ProviderAuthorization'])
                            # order_red_mas.provider_authorizacion = str(value_red_mas_support_query[1]['ProviderAuthorization'])
                        if 'AditionalInfo1' in value_red_mas_support_query[1]:
                            if value_red_mas_support_query[1]['AditionalInfo1']:
                                validation['AditionalInfo1'] = str(value_red_mas_support_query[1]['AditionalInfo1'])
                                # order_red_mas.add_info1 = str(value_red_mas_support_query[1]['AditionalInfo1'])
                        if 'AditionalInfo2' in value_red_mas_support_query[1]:
                            if value_red_mas_support_query[1]['AditionalInfo2']:
                                validation['AditionalInfo2'] = value_red_mas_support_query[1]['AditionalInfo2']
                                # order_red_mas.add_info2 = str(value_red_mas_support_query[1]['AditionalInfo2'])
                        if 'AditionalInfo4' in value_red_mas_support_query[1]:
                            if value_red_mas_support_query[1]['AditionalInfo4']:
                                validation['AditionalInfo4'] = value_red_mas_support_query[1]['AditionalInfo4']
                                # order_red_mas.add_info3 = str(value_red_mas_support_query[1]['AditionalInfo4'])
                        if 'LegalInformation' in value_red_mas_support_query[1]:
                            if value_red_mas_support_query[1]['LegalInformation']:
                                validation['LegalInformation'] = str(value_red_mas_support_query[1]['LegalInformation'])
                                # order_red_mas.legal_info = str(value_red_mas_support_query[1]['LegalInformation'])
                        if order[0]['data']['reference1']:
                            # order_red_mas.reference_1 = order[0]['data']['reference1']
                            validation['reference1'] = order[0]['data']['reference1']
                        if order[0]['data']['reference2']:
                            # order_red_mas.reference_2 = order[0]['data']['reference2']
                            validation['reference2'] = order[0]['data']['reference2']
                        if order[0]['data']['reference3']:
                            validation['reference3'] = order[0]['data']['reference3']
                            # order_red_mas.reference_3 = order[0]['data']['reference3']
                else:
                    logging.warning('En algun else')
                    logging.warning(value_red_mas_support_query)
                    # raise UserError(value_red_mas_support_query[0]['ResponseMessage'])
                    validation['error']= value_red_mas_support_query[0]['ResponseMessage']

            else:
                value_red_mas = self.checkRedMas(pos_config, [product_dicc], [number])
                logging.warning('No support query')
                logging.warning(value_red_mas)
                if value_red_mas[0]['ResponseMessage'] == False:
                    # res = super(PosOrder, self)._process_order(order, draft, existing_order)

                    #order_red_mas = self.env['pos.order'].search([('id', '=', res)])
                    logging.warning('not suppot query 1')
                    if value_red_mas[1]:
                        logging.warning('not suppot query 2')
                        if value_red_mas[1]['TransactionId']:
                            logging.warning('not suppot query 3')
                            validation['TransactionId'] = value_red_mas[1]['TransactionId']
                            #order_red_mas.transaccion_id = str(value_red_mas[1]['TransactionId'])
                        if value_red_mas[1]['TransactionDate']:
                            validation['TransactionDate'] = value_red_mas[1]['TransactionDate']
 #                            order_red_mas.transaccion_date = str(value_red_mas[1]['TransactionDate'])

                        if value_red_mas[1]['ProviderAuthorization']:
                            validation['ProviderAuthorization'] = value_red_mas[1]['ProviderAuthorization']
 #                            order_red_mas.provider_authorizacion = str(value_red_mas[1]['ProviderAuthorization'])

                        if 'AditionalInfo1' in value_red_mas[1]:
                            if value_red_mas[1]['AditionalInfo1']:
                                validation['AditionalInfo1'] = value_red_mas[1]['AditionalInfo1']
 #                                order_red_mas.add_info1 = str(value_red_mas[1]['AditionalInfo1'])

                        if 'AditionalInfo2' in value_red_mas[1]:
                            if value_red_mas[1]['AditionalInfo2']:
                                validation['AditionalInfo2'] = value_red_mas[1]['AditionalInfo2']
 #                                order_red_mas.add_info2 = str(value_red_mas[1]['AditionalInfo2'])

                        if 'AditionalInfo4' in value_red_mas[1]:
                            if value_red_mas[1]['AditionalInfo4']:
                                validation['AditionalInfo4'] = value_red_mas[1]['AditionalInfo4']
 #                                order_red_mas.add_info3 = str(value_red_mas[1]['AditionalInfo4'])

                        if 'LegalInformation' in value_red_mas[1]:
                            if value_red_mas[1]['LegalInformation']:
                                validation['LegalInformation']=value_red_mas[1]['LegalInformation']
 #                                order_red_mas.legal_info = str(value_red_mas[1]['LegalInformation'])

                        if order[0]['data']['reference1']:
                            validation['reference1'] = order[0]['data']['reference1']
 #                            order_red_mas.reference_1 = order[0]['data']['reference1']

                        if order[0]['data']['reference2']:
                            validation['reference2'] = order[0]['data']['reference2']
 #                        if order[0]['data']['reference2']:
 #                            order_red_mas.reference_2 = order[0]['data']['reference2']
                        if order[0]['data']['reference3']:
                            validation['reference3'] = order[0]['data']['reference3']
 #                            order_red_mas.reference_3 = order[0]['data']['reference3']
                else:
#                     raise UserError(value_red_mas[0]['ResponseMessage'])
                    validation['error'] = value_red_mas[0]['ResponseMessage']


        return validation

    def value_fields(self, dicc):
        logging.warning('Funcion value_fields')
        logging.warning(dicc)

        orders = self.env['pos.order'].search([('id', '=', dicc[0]['id_order'])])
        for order in orders:
            if len(dicc[0]) > 0:
                if 'TransactionId' in dicc[0]:
                    if dicc[0]['TransactionId']:
                        order.transaccion_id = dicc[0]['TransactionId']
                    if dicc[0]['TransactionDate']:
                        order.transaccion_date = dicc[0]['TransactionDate']
                    if dicc[0]['ProviderAuthorization']:
                        order.provider_authorizacion = dicc[0]['ProviderAuthorization']

                    if 'AditionalInfo1' in dicc[0] and dicc[0]['AditionalInfo1']:
                        order.add_info1 = dicc[0]['AditionalInfo1']
                    if 'AditionalInfo2' in dicc[0] and dicc[0]['AditionalInfo2']:
                        order.add_info2 = dicc[0]['AditionalInfo2']
                    if 'AditionalInfo4' in dicc[0] and dicc[0]['AditionalInfo4']:
                        order.add_info3 = dicc[0]['AditionalInfo4']
                    if 'LegalInformation' in dicc[0] and dicc[0]['LegalInformation']:
                        order.legal_info = dicc[0]['LegalInformation']
                    if 'reference1' in dicc[0] and dicc[0]['reference1']:
                        order.reference_1 = dicc[0]['reference1']
                    if 'reference2' in dicc[0] and dicc[0]['reference2']:
                        order.reference_2 = dicc[0]['reference2']
                    if 'reference3' in dicc[0] and dicc[0]['reference3']:
                        order.reference_3 = dicc[0]['reference3']
                    if 'comision' in dicc[0] and dicc[0]['comision']:
                        order.comision = dicc[0]['comision']
                    if 'iva_comision' in dicc[0] and dicc[0]['iva_comision']:
                        logging.warning('Entrando al iva comision :o')
                        logging.warning(float(dicc[0]['iva_comision']))
                        order.iva_comision = float(dicc[0]['iva_comision'])


        return True

    def ticket_values(self, name_order):
        dicc_values = {
        'transaccion_id':'',
        'provider_authorizacion':'',
        'reference1':'',
        'reference2':'',
        'reference3':'',
        'legal_info':'',
        'comision':0,
        'iva_comision':0
        }
        if name_order:
            orders = self.env['pos.order'].search([('pos_reference', '=', name_order[0])])

            if orders:
                for order in orders:
                    logging.warning('Me llamaron desde una funcion para el ticket::::')
                    logging.warning(order.transaccion_id)
                    if order.transaccion_id:
                        dicc_values['transaccion_id']=order.transaccion_id
                    if order.provider_authorizacion:
                        dicc_values['provider_authorizacion']=order.provider_authorizacion
                    if order.add_info1:
                        dicc_values['reference1'] = order.add_info1
                    if order.add_info2:
                        dicc_values['reference2'] = order.add_info2
                    if order.add_info3:
                        dicc_values['reference3'] = order.add_info3
                    if order.legal_info:
                        dicc_values['legal_info'] = order.legal_info
                    if order.comision:
                        dicc_values['comision'] = order.comision
                    if order.iva_comision:
                        dicc_values['iva_comision'] = order.iva_comision
        return dicc_values

    def get_balance_by_bag(self, config_id, number):
        logging.warning('Welcome to get_balance_by_bag from pos.order')
        balance = True
        confi_pos_config_id = self.env['pos.config'].search([('id', '=', config_id[0])])
        pos_order_get_balance_by = {}
        for pos_config_id in confi_pos_config_id:
            xml_json = pos_config_id.red_autentication('GetBalanceByBag', number[0])
            if xml_json != False and 'BagId' in xml_json:
                if xml_json:
                    pos_order_get_balance_by['ResponseMessage'] = False
            else:
                pos_order_get_balance_by['ResponseMessage'] = xml_json

        return pos_order_get_balance_by

    def sale(self, config_id, product_dicc):
        logging.warning('Funcion sale en pos.order------------------------------------')
        value_sale={}
        confi_pos_config_id = self.env['pos.config'].search([('id', '=', config_id[0])])
        order_check_reference = ''
        for pos_config_id in confi_pos_config_id:
            if product_dicc[0]['no_session']:
                session_x = self.env['pos.session'].search([('id','=', product_dicc[0]['no_session'])])
                product_dicc[0]['session'] = session_x.sessionid
            xml_json = pos_config_id.red_autentication('Sale', product_dicc)
            if xml_json != False and 'ResponseCode' in xml_json:
                if xml_json['ResponseCode'] == '000':
                    value_sale['ResponseMessage'] = False
            elif xml_json != False:
                value_sale['ResponseMessage'] = xml_json
            else:
                value_sale['ResponseMessage'] = 'Algo salio mal en función sale'

        return value_sale

    def checkSale(self, config_id, product_dicc):
        logging.warning('Welcome to checkSale function from pos.order--------------------')
        value_check_sale={}
        values_fields_data = None
        confi_pos_config_id = self.env['pos.config'].search([('id', '=', config_id[0])])
        order_check_reference = ''
        for pos_config_id in confi_pos_config_id:
            if product_dicc[0]['no_session']:
                session_x = self.env['pos.session'].search([('id','=', product_dicc[0]['no_session'])])
                product_dicc[0]['session'] = session_x.sessionid
            xml_json = pos_config_id.red_autentication('CheckSale', product_dicc)
            if xml_json != False and 'ResponseCode' in xml_json:
                if xml_json['ResponseCode'] == '000':
                    value_check_sale['ResponseMessage'] = False
                    values_fields_data=xml_json
            else:
                value_check_sale['ResponseMessage'] = xml_json

        return [value_check_sale, values_fields_data]

    def checkRedMas_supportQuery(self, config_id, product_dicc, number):
        logging.warning('1')
        value_red_mas_support_query = {}
        other_data = None
        # data_check_
        if config_id and number:
            logging.warning('2')
            value_get_balance_by_bag = self.get_balance_by_bag(config_id, number)
            if value_get_balance_by_bag['ResponseMessage'] ==  False:
                logging.warning('3')
                value_check_reference = self.check_reference(config_id, product_dicc)
                if value_check_reference['ResponseMessage'] == False:
                    logging.warning('4')
                    value_checkRedMas = self.checkRedMas(config_id, product_dicc, number)
                    if value_checkRedMas[0]['ResponseMessage'] == False:
                        logging.warning('5')
                        value_red_mas_support_query = True
                        other_data = value_checkRedMas[1]
                        logging.warning(other_data)
                        logging.warning('')
                        logging.warning('')
                        logging.warning('')
                    else:
                        value_red_mas_support_query = value_checkRedMas
                else:
                    value_red_mas_support_query = value_check_reference
            else:
                value_red_mas_support_query=value_get_balance_by_bag
        logging.warning('value_red_mas support_query')
        logging.warning(value_red_mas_support_query)
        if other_data != None:
            return [value_red_mas_support_query,other_data]
        else:
            return [value_red_mas_support_query]

    def checkRedMas(self, config_id, product_dicc, number):
        logging.warning('CheckRedMas 1')
        value_red_mas={}
        value_checkSale_extra = None
        if config_id and number:
            logging.warning('checkRedMas 2')
            value_get_balance_by_bag = self.get_balance_by_bag(config_id, number)
            if value_get_balance_by_bag['ResponseMessage']==False:
                logging.warning('checkRedMas 3')
                value_sale = self.sale(config_id, product_dicc)
                if value_sale['ResponseMessage']==False:
                    logging.warning('checkRedMas 4')
                    value_checkSale = self.checkSale(config_id, product_dicc)
                    if len(value_checkSale)>1:
                        if value_checkSale[0]['ResponseMessage'] == False:
                            logging.warning('checkRedMas 5')
                            value_red_mas['ResponseMessage'] = False
                            value_checkSale_extra = value_checkSale[1]
                        else:
                            value_red_mas = value_checkSale
                else:
                    value_red_mas=value_sale
            else:
                value_red_mas=value_get_balance_by_bag
        logging.warning('value_red_mas')
        logging.warning(value_red_mas)
        logging.warning('')
        logging.warning('')
        return [value_red_mas, value_checkSale_extra]
