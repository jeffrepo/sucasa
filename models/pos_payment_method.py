from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'
    _description = 'New payment methods'


    def actualizar_catalogos(self, pos_config_id):
        logging.warning('Welcome to actualizar_catalogos')
        logging.warning(self)
        list_payment_name = []
        if pos_config_id:
            xml_json = pos_config_id.red_autentication('GetAvailablePaymentMethods', False)
            for payment in xml_json['PaymentMethods']['string']:
                for pay in self:
                    list_payment_name.append(pay.name)
                if payment not in list_payment_name:
                    if payment == 'Efectivo':
                        self.create({
                        'name':payment,
                        'is_cash_count':True
                        })
                    else:
                        self.create({
                        'name':payment
                        })
        logging.warning('')
        logging.warning('')
        return True
