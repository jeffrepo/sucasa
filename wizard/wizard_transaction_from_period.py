# -*- coding: utf-8 -*-

from odoo import models, fields, api
import xlsxwriter
import base64
import io
import logging

class TransactionFromPeriodWizard(models.TransientModel):
    _name = 'sucasa.transaction_from_period.wizard'
    _description = "Wizard para obtención de datos de ..."

    start_date = fields.Date('Fecha inicio', required=True)
    final_date = fields.Date('Fecha fin', required=True)
    point_of_sale = fields.Many2one('pos.config', string='Punto de venta', required=True)
    product_category = fields.Many2one('product.category', string="Categoria", required=True)
    name = fields.Char('Nombre archivo', size=32)
    archivo = fields.Binary('Archivo', filters='.xls')

    def print_report(self):
        data = {
             'ids': [],
             'model': 'sucasa.transaction_from_period.wizard',
             'form': self.read()[0]
        }
        return self.env.ref('sucasa.action_reporte_sucasa').report_action([], data=data)


    def print_report_excel(self):
        for w in self:
            logging.warning('Formato de fecha')
            start_date = w.start_date.strftime('%Y%m%d')
            final_date = w.final_date.strftime('%Y%m%d')
            store_id_selected = w.point_of_sale.storeid
            pos_id_selected = w.point_of_sale.posid
            product_category = w.product_category.ProductCategoryId
            point_of_sale = w.point_of_sale

            values=[start_date, final_date, store_id_selected, pos_id_selected, product_category, point_of_sale]
            response = self.get_transaction_from_period(values)

            f = io.BytesIO()
            libro = xlsxwriter.Workbook(f)
            hoja = libro.add_worksheet('Reporte')

            if response:
                formato_titulo = libro.add_format({'size': 18, 'color':'#ffffff', 'align':'center', 'fg_color':'#F39C12', 'bold':True})
                formato_subtitulo = libro.add_format({'size': 11, 'color':'#ffffff', 'align':'center', 'fg_color':'#F5B041', 'border':1})
                formato_datos_wizard = libro.add_format({'size': 11, 'color':'#ffffff', 'align':'center', 'fg_color':'#5D6D7E', 'border':1})

                #Tamaño de la fila
                hoja.set_row (0, 30)

                #Tamaño de las columnas
                hoja.set_column('A:S', 20)

                hoja.merge_range('A1:R1', 'Transacción del período', formato_titulo)

                hoja.write(2,0, 'Fecha inicio: ', formato_datos_wizard)
                hoja.write(2,1, str(w.start_date.strftime('%d/%m/%Y')))
                hoja.write(2,3, 'Fecha final: ', formato_datos_wizard)
                hoja.write(2,4, str(w.final_date.strftime('%d/%m/%Y')))
                hoja.write(2,6, 'Punto de venta ', formato_datos_wizard)
                hoja.write(2,7, str(w.point_of_sale.name))
                hoja.write(2,9, 'Categoria: ', formato_datos_wizard)
                hoja.write(2,10, str(w.product_category.name))

                hoja.write(4,0, 'TransactionId', formato_subtitulo)
                hoja.write(4,1, 'ClientId', formato_subtitulo)
                hoja.write(4,2, 'PosId', formato_subtitulo)
                hoja.write(4,3, 'TransactionDate', formato_subtitulo)
                hoja.write(4,4, 'ProductName', formato_subtitulo)
                hoja.write(4,5, 'CarrierName', formato_subtitulo)
                hoja.write(4,6, 'Amount', formato_subtitulo)
                hoja.write(4,7, 'TotalCharge', formato_subtitulo)
                hoja.write(4,8, 'Authorization', formato_subtitulo)
                hoja.write(4,9, 'ResponseCode', formato_subtitulo)
                hoja.write(4,10, 'InternalResponseMessage', formato_subtitulo)
                hoja.write(4,11, 'POSTransactionId', formato_subtitulo)
                hoja.write(4,12, 'StoreName', formato_subtitulo)
                hoja.write(4,13, 'CashierFirsName', formato_subtitulo)
                hoja.write(4,14, 'CashierLastName', formato_subtitulo)
                hoja.write(4,15, 'ClientUtility', formato_subtitulo)
                hoja.write(4,16, 'StoreId', formato_subtitulo)
                hoja.write(4,17, 'ProductCategoryId', formato_subtitulo)

                logging.warning('Que es response')
                logging.warning(response)
                logging.warning(str(response)[0])
                logging.warning('')
                fila = 5
                if str(response)[0] == '[':
                    for r in response:
                        logging.warning(r)
                        if r['TransactionId']:
                            hoja.write(fila,0, r['TransactionId'])
                        if r['ClientId']:
                            hoja.write(fila,1, r['ClientId'])
                        if r['PosId']:
                            hoja.write(fila,2, r['PosId'])
                        if r['TransactionDate']:
                            hoja.write(fila,3, r['TransactionDate'])
                        if r['ProductName']:
                            hoja.write(fila,4, r['ProductName'])
                        if r['CarrierName']:
                            hoja.write(fila,5, r['CarrierName'])
                        if r['Amount']:
                            hoja.write(fila,6, r['Amount'])
                        if r['TotalCharge']:
                            hoja.write(fila,7, r['TotalCharge'])
                        if r['Authorization']:
                            hoja.write(fila,8, r['Authorization'])
                        if r['ResponseCode']:
                            hoja.write(fila,9, r['ResponseCode'])
                        if r['InternalResponseMessage']:
                            hoja.write(fila,10, r['InternalResponseMessage'])
                        if r['POSTransactionId']:
                            hoja.write(fila,11, r['POSTransactionId'])
                        if r['StoreName']:
                            hoja.write(fila,12, r['StoreName'])
                        if r['CashierFirsName']:
                            hoja.write(fila,13, r['CashierFirsName'])
                        if r['CashierLastName']:
                            hoja.write(fila,14, r['CashierLastName'])
                        if r['ClientUtility']:
                            hoja.write(fila,15, r['ClientUtility'])
                        if r['StoreId']:
                            hoja.write(fila,16, r['StoreId'])
                        if r['ProductCategoryId']:
                            hoja.write(fila,17, r['ProductCategoryId'])

                        fila+=1
                elif str(response)[0] == '{':
                    if 'TransactionId' in response:
                        hoja.write(fila,0, response['TransactionId'])
                    if 'ClientId' in response:
                        hoja.write(fila,1, response['ClientId'])
                    if 'PosId' in response:
                        hoja.write(fila,2, response['PosId'])
                    if 'TransactionDate' in response:
                        hoja.write(fila,3, response['TransactionDate'])
                    if 'ProductName' in response:
                        hoja.write(fila,4, response['ProductName'])
                    if 'CarrierName' in response:
                        hoja.write(fila,5, response['CarrierName'])
                    if 'Amount' in response:
                        hoja.write(fila,6, response['Amount'])
                    if 'TotalCharge' in response:
                        hoja.write(fila,7, response['TotalCharge'])
                    if 'Authorization' in response:
                        hoja.write(fila,8, response['Authorization'])
                    if 'ResponseCode' in response:
                        hoja.write(fila,9, response['ResponseCode'])
                    if 'InternalResponseMessage' in response:
                        hoja.write(fila,10, response['InternalResponseMessage'])
                    if 'POSTransactionId' in response:
                        hoja.write(fila,11, response['POSTransactionId'])
                    if 'StoreName' in response:
                        hoja.write(fila,12, response['StoreName'])
                    if 'CashierFirsName' in response:
                        hoja.write(fila,13, response['CashierFirsName'])
                    if 'CashierLastName' in response:
                        hoja.write(fila,14, response['CashierLastName'])
                    if 'ClientUtility' in response:
                        hoja.write(fila,15, response['ClientUtility'])
                    if 'StoreId' in response:
                        hoja.write(fila,16, response['StoreId'])
                    if 'ProductCategoryId' in response:
                        hoja.write(fila,17, response['ProductCategoryId'])

            libro.close()
            datos = base64.b64encode(f.getvalue())
            self.write({'archivo':datos, 'name':'Reporte.xlsx'})

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sucasa.transaction_from_period.wizard',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def get_transaction_from_period(self, values):
        logging.warning('Valores recibidos')
        logging.warning(values)

        for point in values[5]:
            xml_json = point.red_autentication('GetTransactionFromPeriod', values)
            logging.warning('antes if xml_json')
            logging.warning(xml_json)
            if xml_json:
                if xml_json != 'Transacción exitosa':
                    logging.warning('Recibimos algo')
                    logging.warning(xml_json)
                else:
                    xml_json = False
            else:
                xml_json = False
        return xml_json
