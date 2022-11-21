# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from lxml import etree
from odoo.exceptions import UserError, ValidationError
from lxml.builder import ElementMaker
import xml.etree.ElementTree as ET
import requests
import base64
import logging
import xmltodict, json

class SucasaProductWight(models.Model):
    _name = 'sucasa.productweight'

    weight = fields.Float('Product weight', digits = (12,3))
    device_id = fields.Integer('Device id')


class SucasaConsultaProducto(models.Model):
    _name = 'sucasa.consulta_producto'

    name = fields.Char('Codigo barra')
    producto_id = fields.Many2one('product.template','Producto')
    color = fields.Integer()


    @api.depends('name','producto_id')
    def _oncha_name(self):
        for record in self:
            record.write({})
            logging.warning(record.producto_id)
            logging.warning(self._origin)
            logging.warning(self.env.context)
            logging.warning('hola')



    @api.onchange('name','producto_id')
    def _onchange_name(self):
        self.write({})
        logging.warning('HOLA')
        logging.warning(self.producto_id)

        # logging.warning(self.name)

class SucasaCarrier(models.Model):
    _name = 'sucasa.carrier'

    CarrierId = fields.Integer("CarrierId")
    name = fields.Char('Nombre')

class PayNotification(models.Model):
    _name = 'sucasa.pay_notification'

    config_id = fields.Many2one('pos.config', 'Punto de venta')
    amount = fields.Float('Monto')
    bank = fields.Many2one('res.bank', 'Bancos')
    document_number = fields.Char('Numero de documento')
    document_date = fields.Date('Fecha de documento')
    origin_account_number = fields.Char('Numero de cuenta original')
    payment_method = fields.Many2one('pos.payment.method' ,'Metodo de pago')
    bagId = fields.Integer('Bolsa')
    state = fields.Selection(
        [('draft', 'New'), ('paid', 'Paid')],
        'Status', readonly=True, copy=False, default='draft')

    def button_pay (self):
        logging.warning('Haciendo click en el boton pagar')

        response_code_payment_method = ''
        response_code_banks = ''

        if self.config_id:
            xml_json = self.config_id.red_autentication('GetAvailablePaymentMethods', False)
            if 'ResponseCode' in xml_json:
                response_code_payment_method = int(xml_json['ResponseCode'])
        if self.config_id:
            xml_json = self.config_id.red_autentication('GetAvailableBanks', False)
            if 'ResponseCode' in xml_json:
                response_code_banks = int(xml_json['ResponseCode'])

        logging.warning('BANCOS')
        logging.warning(response_code_banks)

        if (response_code_payment_method and response_code_banks) == 000:
            logging.warning('Se ha tenido buena respuesta de los metodos anteriores')
            if self.config_id:
                dicc_fields = {
                'amount':self.amount,
                'bank':self.bank.name,
                'document_number':self.document_number,
                'document_date':self.document_date.strftime('%Y%m%d'),
                'origin_account_number':self.origin_account_number,
                'payment_method':self.payment_method.name,
                'bag_id':self.bagId
                }

                xml_json = self.config_id.red_autentication('SubmitPayNotification', dicc_fields)
                if xml_json:
                    if 'ResponseCode' in xml_json:
                        response_code = int(xml_json['ResponseCode'])
                        if response_code == 000:
                            logging.warning(self.state)
                            self.state = 'paid'

        return True
