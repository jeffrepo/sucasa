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



class PosConfig(models.Model):
    _inherit = 'pos.config'

    clientid = fields.Char('Identificar de cliente')
    clerkcode = fields.Char('Codigo cajero')
    storeid = fields.Char('Identificador de sucursal')
    posid = fields.Char('Identificador de caja')
    postoken = fields.Char('Token')

    # def eli_park(self):
    #

    def response_codes(self):
        codes = {
            "200": 'Sesion expirada',
            "201": 'No pudo validar sesion',
            "202": 'Ha ocurrido un error registrando el token. Favor de comunicarse a soporte técnico RPM.',
            "203": 'Caja no disponible para registro de token.',
            "204": 'Token inválido para la caja proporcionada'
        }
        return codes

    # carriers disponibles se ejecuta 1 vez al dia acciones automatizada
    def _get_available_carriers(self):
        odoo_carriers_dic = {}
        # odoo_carriers = self.env['sucasa.carrier'].search([()])
        pos_config_ids = self.env['pos.config'].search([('clientid','!=', False),('storeid','!=', False),('posid','!=', False),('clerkcode','!=',False),('postoken','!=', False)])
        if pos_config_ids:
            for pos in pos_config_ids:
                xml_json = pos.red_autentication('GetAvailableCarriers')
                if "Carrier" in xml_json:
                    if len(xml_json["Carrier"]) > 0:
                        odoo_carriers_ids = self.env['sucasa.carrier'].search([])
                        odoo_carriers_dic = {}
                        if len(odoo_carriers_ids) > 0:
                            for c in odoo_carriers_ids:
                                if c.CarrierId:
                                    odoo_carriers_dic[c.CarrierId] = c

                        for carrier in xml_json["Carrier"]:
                            if int(carrier["CarrierId"]) not in odoo_carriers_dic:
                                carrier_id = self.env['sucasa.carrier'].create({'CarrierId': int(carrier["CarrierId"]), 'name': carrier["CarrierName"] })
                                logging.warning(carrier_id)
                            else:
                                odoo_carriers_dic[int(carrier["CarrierId"])].update({'name': carrier["CarrierName"]})
                logging.warning(xml_json)
        return odoo_carriers_dic

    # categoria de productos por cliente se ejecuta 1 vez al dia
    def _get_product_categories_by_client_id(self):
        odoo_categ_dic = {}
        pos_config_ids = self.env['pos.config'].search([('clientid','!=', False),('storeid','!=', False),('posid','!=', False),('clerkcode','!=',False),('postoken','!=', False)])
        if pos_config_ids:
            for pos in pos_config_ids:
                xml_json = pos.red_autentication('GetProductsCategoriesByClientId')
                logging.warning(xml_json)
                if "ProductCategories" in xml_json:
                    if len(xml_json["ProductCategories"]) > 0:
                        odoo_categ_ids = self.env['product.category'].search([('ProductCategoryId','!=', False)])
                        odoo_categ_dic = {}
                        if len(odoo_categ_ids) > 0:
                            for c in odoo_categ_ids:
                                if c.ProductCategoryId:
                                    odoo_categ_dic[c.ProductCategoryId] = c

                        for category in xml_json["ProductCategories"]:
                            if int(category["ProductCategoryId"]) not in odoo_categ_dic:
                                category_id = self.env['product.category'].create({'ProductCategoryId': category["ProductCategoryId"] ,'name': category["ProductCategoryName"]})
                            else:
                                odoo_categ_dic[int(category["ProductCategoryId"])].update({'name': category["ProductCategoryName"]})
        return odoo_categ_dic

    # Se ejecuta por cada transacción en el punto de venta antes y despues
    # para ver el saldo de cada punto
    def _get_balance_by_bag(self, config_id):
        saldo = 0
        pos_config_id = self.env['pos.config'].search([('id','=',config_id)])
        if pos_config_id:
            saldo = pos_config_id.red_autentication('GetBalanceByBag')
            if saldo <= 0:
                logging.warning('error')
        return saldo

    # Se ejecuta 1 vez al dia , se ejecuta antes de  SubmitPayNotification (_submit_pay_notification)
    def _get_available_payment_methods(self):
        payment_methods = {}
        return payment_methods

    # Se ejecuta 1 vez al dia, se ejecuta antes de SubmitPayNotification (_submit_pay_notification)
    def _get_available_banks(self):
        banks = {}
        return banks

    def _submit_pay_notification(self):
        submit = False
        return submit

    # Se ejecuta una vez al dia y manda a llamar _get_available_carriers y _get_product_categories_by_client_id
    def _get_all_product_extend_list(self):
        products = {}
        pos_config_ids = self.env['pos.config'].search([('clientid','!=', False),('storeid','!=', False),('posid','!=', False),('clerkcode','!=',False),('postoken','!=', False)])
        if pos_config_ids:
            odoo_carriers_dic = self._get_available_carriers()
            odoo_categ_dic = self._get_product_categories_by_client_id()
            for pos in pos_config_ids:
                xml_json = pos.red_autentication('GetAllProductExtendList')
                logging.warning(xml_json)
                if "ProductExtended" in xml_json:
                    if len(xml_json) > 0:
                        odoo_product_ids = self.env['product.template'].search([('red_id','!=', False)])
                        odoo_product_dic = {}
                        if len(odoo_product_ids) > 0:
                            for p in odoo_product_ids:
                                odoo_product_dic[p.red_id] = p

                        for product in xml_json["ProductExtended"]:
                            if int(product["ProductId"]) not in odoo_product_dic:
                                logging.warning(product)
                                product_dic = {'red_id': product["ProductId"],
                                'name': product["ProductName"],
                                'available_in_pos': True,
                                'lenght_ref1': product["LenghtRef1"],
                                'lenght_ref2': product["LenghtRef2"],
                                'lenght_ref3': product["LenghtRef3"],
                                'validate_ref1': product["ValidateRef1"],
                                'validate_ref2': product["ValidateRef2"],
                                'validate_ref3': product["ValidateRef3"],
                                'list_price': product["Amount"],
                                'legal_information': product["LegalInformation"]}

                                if "Reference1" in product:
                                    product_dic["reference1"] = product["Reference1"]
                                if "Reference2" in product:
                                    product_dic["reference2"] = product["Reference2"]

                                if "CategoryId" in product:
                                    product_dic["categ_id"] = odoo_categ_dic[int(product["CategoryId"])].id if int(product["CategoryId"]) in odoo_categ_dic else False
                                if "carrier_id" in product:
                                    product_dic["carrier_id"] = odoo_carriers_dic[int(product["CarrierId"])].id if int(product["CarrierId"]) in odoo_carriers_dic else False


                                product_template_id = self.env['product.template'].create(product_dic)
                            else:
                                product_dic = {
                                'name': product["ProductName"],
                                'available_in_pos': True,
                                'lenght_ref1': product["LenghtRef1"],
                                'lenght_ref2': product["LenghtRef2"],
                                'lenght_ref3': product["LenghtRef3"],
                                'validate_ref1': product["ValidateRef1"],
                                'validate_ref2': product["ValidateRef2"],
                                'validate_ref3': product["ValidateRef3"],
                                'list_price': product["Amount"],
                                'carrier_id': odoo_carriers_dic[int(product["CarrierId"])].id,
                                'legal_information': product["LegalInformation"]}
                                if "Reference1" in product:
                                    product_dic["reference1"] = product["Reference1"]
                                if "Reference2" in product:
                                    product_dic["reference2"] = product["Reference2"]


                                if "CategoryId" in product:
                                    product_dic["categ_id"] = odoo_categ_dic[int(product["CategoryId"])].id if int(product["CategoryId"]) in odoo_categ_dic else False
                                if "carrier_id" in product:
                                    product_dic["carrier_id"] = odoo_carriers_dic[int(product["CarrierId"])].id if int(product["CarrierId"]) in odoo_carriers_dic else False

                                odoo_product_dic[int(product["ProductId"])].update(product_dic)
        return products

    def red_autentication(self,method):
        for pos in self:
            data = False
            attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
            SOAPN_NS = "{http://schemas.xmlsoap.org/soap/envelope/}"
            NSMAP = {
                 'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
            }
            SOAP_NS = 'http://schemas.xmlsoap.org/soap/envelope/'
            ns_map = {'soapenv': SOAP_NS}


            Envelope = etree.Element(etree.QName(SOAP_NS, 'Envelope'), nsmap=ns_map)
            TagBody = etree.SubElement(Envelope,SOAPN_NS+"Body",{})
            TagMethod = etree.SubElement(TagBody, method, {'xmlns':"http://rpmmx.net/"})
            TagPosCredentials = etree.SubElement(TagMethod, "posCredentials", {})
            TagClientId = etree.SubElement(TagPosCredentials, "ClientId",nsmap=ns_map)
            TagClientId.text = pos.clientid
            TagStoreId = etree.SubElement(TagPosCredentials, "StoreId",{})
            TagStoreId.text = pos.storeid
            TagPosId = etree.SubElement(TagPosCredentials, "PosId",{})
            TagPosId.text = pos.posid
            TagClerkCode = etree.SubElement(TagPosCredentials, "ClerkCode",{})
            TagClerkCode.text = pos.clerkcode
            TagPosToken = etree.SubElement(TagPosCredentials, "PosToken",{})
            TagPosToken.text = pos.postoken

            xmls = etree.tostring(Envelope, encoding="UTF-8")
            xmls = xmls.decode("utf-8").replace("&amp;", "&").encode("utf-8")
            xmls_base64 = base64.b64encode(xmls)
            logging.warning(xmls)

            url = "https://wspruebas.cedixvirtual.mx/redmas_plat/WebService/SaleService.asmx"

            headers = {"content-type": "text/xml; charset=utf-8", 'Host': "wspruebas.cedixvirtual.mx"}
            response = requests.post(url, data = xmls, headers = headers)
            if response:
                if response.status_code == 200:
                    if response.content:
                        new_xml = xmltodict.parse(response.content)
                        logging.warning(json.dumps(new_xml))
                        new_json1 = json.dumps(new_xml)
                        new_json = json.loads(new_json1)
                        if new_json:
                            if "soap:Envelope" in new_json:
                                if "soap:Body" in new_json["soap:Envelope"]:
                                    if method == "GetAvailableCarriers":
                                        if "GetAvailableCarriersResponse" in new_json["soap:Envelope"]["soap:Body"]:
                                            if "GetAvailableCarriersResult" in new_json["soap:Envelope"]["soap:Body"]["GetAvailableCarriersResponse"]:
                                                if "ResponseCode" in new_json["soap:Envelope"]["soap:Body"]["GetAvailableCarriersResponse"]["GetAvailableCarriersResult"]:
                                                    response_code = new_json["soap:Envelope"]["soap:Body"]["GetAvailableCarriersResponse"]["GetAvailableCarriersResult"]["ResponseCode"]
                                                    if int(response_code) == 000:
                                                        logging.warning('transaccion exitosa')
                                                        if "CarrierList" in new_json["soap:Envelope"]["soap:Body"]["GetAvailableCarriersResponse"]["GetAvailableCarriersResult"]:
                                                            data =  new_json["soap:Envelope"]["soap:Body"]["GetAvailableCarriersResponse"]["GetAvailableCarriersResult"]["CarrierList"]
                                                            # logging.warning(new_json["soap:Envelope"]["soap:Body"]["GetAvailableCarriersResponse"]["GetAvailableCarriersResult"]["CarrierList"])

                                    if method == "GetProductsCategoriesByClientId":
                                        if "GetProductsCategoriesByClientIdResponse" in new_json["soap:Envelope"]["soap:Body"]:
                                            if "GetProductsCategoriesByClientIdResult" in new_json["soap:Envelope"]["soap:Body"]["GetProductsCategoriesByClientIdResponse"]:
                                                if "ResponseCode" in new_json["soap:Envelope"]["soap:Body"]["GetProductsCategoriesByClientIdResponse"]["GetProductsCategoriesByClientIdResult"]:
                                                    response_code = new_json["soap:Envelope"]["soap:Body"]["GetProductsCategoriesByClientIdResponse"]["GetProductsCategoriesByClientIdResult"]["ResponseCode"]
                                                    if int(response_code) == 000:
                                                        logging.warning('transaccion exitosa')
                                                        if "ProductCategories" in new_json["soap:Envelope"]["soap:Body"]["GetProductsCategoriesByClientIdResponse"]["GetProductsCategoriesByClientIdResult"]:
                                                            data = new_json["soap:Envelope"]["soap:Body"]["GetProductsCategoriesByClientIdResponse"]["GetProductsCategoriesByClientIdResult"]["ProductCategories"]
                                                            # logging.warning(new_json["soap:Envelope"]["soap:Body"]["GetProductsCategoriesByClientIdResponse"]["GetProductsCategoriesByClientIdResult"]["ProductCategories"])
                                        # logging.warning('GetProductsCategoriesByClientId')

                                    if method == "GetBalanceByBag":
                                        if "GetBlanceByBagResponse" in new_json["soap:Envelope"]["soap:Body"]:
                                            if "GetBlanceByBagResult" in new_json["soap:Envelope"]["soap:Body"]["GetBlanceByBagResponse"]:
                                                if "ResponseCode" in new_json["soap:Envelope"]["soap:Body"]["GetBlanceByBagResponse"]["GetBlanceByBagResult"]:
                                                    response_code = new_json["soap:Envelope"]["soap:Body"]["GetBlanceByBagResponse"]["GetBlanceByBagResult"]["ResponseCode"]
                                                    if int(response_code) == 000:
                                                        logging.warning('GetBalanceByBag')
                                                        balance = new_json["soap:Envelope"]["soap:Body"]["GetBlanceByBagResponse"]["GetBlanceByBagResult"]["balance"]
                                                        logging.warning(balance)
                                                        data = balance
                                    if method == "GetAllProductExtendList":
                                        if "GetAllProductExtendListResponse" in new_json["soap:Envelope"]["soap:Body"]:
                                            if "GetAllProductExtendListResult" in new_json["soap:Envelope"]["soap:Body"]["GetAllProductExtendListResponse"]:
                                                if "ResponseCode" in new_json["soap:Envelope"]["soap:Body"]["GetAllProductExtendListResponse"]["GetAllProductExtendListResult"]:
                                                    response_code = new_json["soap:Envelope"]["soap:Body"]["GetAllProductExtendListResponse"]["GetAllProductExtendListResult"]["ResponseCode"]
                                                    if int(response_code) == 000:
                                                        data = new_json["soap:Envelope"]["soap:Body"]["GetAllProductExtendListResponse"]["GetAllProductExtendListResult"]["ProductExtendedList"]

                                    if method == "GetSession":
                                        if "GetSessionResponse" in new_json["soap:Envelope"]["soap:Body"]:
                                            if "GetSessionResult" in new_json["soap:Envelope"]["soap:Body"]["GetSessionResponse"]:
                                                if "ResponseCode" in new_json["soap:Envelope"]["soap:Body"]["GetSessionResponse"]["GetSessionResult"]:
                                                    response_code = new_json["soap:Envelope"]["soap:Body"]["GetSessionResponse"]["GetSessionResult"]["ResponseCode"]
                                                    if int(response_code) == 000:
                                                        data = new_json["soap:Envelope"]["soap:Body"]["GetSessionResponse"]["GetSessionResult"]

                                    if method == 'RegisterPosTokenResponse':
                                        if "RegisterPosTokenResponse" in new_json["soap:Envelope"]["soap:Body"]:
                                            if "RegisterPosTokenResult" in new_json["soap:Envelope"]["soap:Body"]["RegisterPosTokenResponse"]:
                                                if "ResponseCode" in new_json["soap:Envelope"]["soap:Body"]["RegisterPosTokenResponse"]["RegisterPosTokenResult"]:
                                                    response_code = new_json["soap:Envelope"]["soap:Body"]["RegisterPosTokenResponse"]["RegisterPosTokenResult"]["ResponseCode"]
                                                    if response_code == 000:
                                                        logging.warning('transaccion exitosa')
                                                        registered = True
                                                    else:
                                                        response_codes = self.response_codes()
                                                        logging.warning(response_code)
                                                        logging.warning(response_codes)
                                                        if response_code in response_codes:
                                                            raise UserError(str(response_codes[response_code]))
                                                        else:
                                                            raise UserError('Error codigo no encontrado')
                else:
                    raise UserError(str('Error de conexion'))

            logging.warning(response)
        return data

    # Autenticacion registrando token
    def register_pos_token(self):
        registered = False

        attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")

        SOAPN_NS = "{http://schemas.xmlsoap.org/soap/envelope/}"

        NSMAP = {
             'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
        }

        # GTDocumento = etree.Element(DTE_NS+"GTDocumento", {attr_qname: 'http://www.sat.gob.gt/dte/fel/0.1.0'}, Version="0.1", nsmap=NSMAP)


        SOAP_NS = 'http://schemas.xmlsoap.org/soap/envelope/'
        ns_map = {'soapenv': SOAP_NS}


        Envelope = etree.Element(etree.QName(SOAP_NS, 'Envelope'), nsmap=ns_map)
        # TagHeader = etree.SubElement(Envelope,SOAPN_NS+"Header",{})
        TagBody = etree.SubElement(Envelope,SOAPN_NS+"Body",{})
        TagRegistedPosToken = etree.SubElement(TagBody, "RegisterPosToken", {'xmlns':"http://rpmmx.net/"})
        TagPosCredentials = etree.SubElement(TagRegistedPosToken, "posCredentials", {})
        TagClientId = etree.SubElement(TagPosCredentials, "ClientId",nsmap=ns_map)
        # TagClientId.text = "429894"
        TagClientId.text = self.clientid
        TagStoreId = etree.SubElement(TagPosCredentials, "StoreId",{})
        # TagStoreId.text = "1"
        TagStoreId.text = self.storeid
        TagPosId = etree.SubElement(TagPosCredentials, "PosId",{})
        # TagPosId.text = "73581"
        TagPosId.text = self.posid
        TagClerkCode = etree.SubElement(TagPosCredentials, "ClerkCode",{})
        # TagClerkCode.text = "08062022"
        TagClerkCode.text = self.clerkcode
        TagPosToken = etree.SubElement(TagPosCredentials, "PosToken",{})
        # TagPosToken.text = "23bb77dc-ca16-4cd3-a652-237ce4e02021"
        TagPosToken.text = self.postoken

        xmls = etree.tostring(Envelope, encoding="UTF-8")
        xmls = xmls.decode("utf-8").replace("&amp;", "&").encode("utf-8")
        xmls_base64 = base64.b64encode(xmls)
        logging.warning(xmls)

# {"soap:Envelope":
# 	 {"@xmlns:soap": "http://schemas.xmlsoap.org/soap/envelope/", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance", "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
#      "soap:Body":
#         {"RegisterPosTokenResponse":
#             {"@xmlns": "http://rpmmx.net/", "RegisterPosTokenResult":
#                 {"ResponseCode": "203", "ResponseMessage": "Caja no disponible para registro de token."}
#             }
#         }
#     }
# }

        url = "https://wspruebas.cedixvirtual.mx/redmas_plat/WebService/SaleService.asmx"

        headers = {"content-type": "text/xml; charset=utf-8", 'Host': "wspruebas.cedixvirtual.mx"}
        response = requests.post(url, data = xmls, headers = headers)
        if response:
            if response.status_code == 200:
                if response.content:
                    new_xml = xmltodict.parse(response.content)
                    logging.warning(json.dumps(new_xml))
                    new_json1 = json.dumps(new_xml)
                    new_json = json.loads(new_json1)
                    if new_json:
                        if "soap:Envelope" in new_json:
                            if "soap:Body" in new_json["soap:Envelope"]:
                                if "RegisterPosTokenResponse" in new_json["soap:Envelope"]["soap:Body"]:
                                    if "RegisterPosTokenResult" in new_json["soap:Envelope"]["soap:Body"]["RegisterPosTokenResponse"]:
                                        if "ResponseCode" in new_json["soap:Envelope"]["soap:Body"]["RegisterPosTokenResponse"]["RegisterPosTokenResult"]:
                                            response_code = new_json["soap:Envelope"]["soap:Body"]["RegisterPosTokenResponse"]["RegisterPosTokenResult"]["ResponseCode"]
                                            if response_code == 000:
                                                logging.warning('transaccion exitosa')
                                                registered = True
                                            else:
                                                response_codes = self.response_codes()
                                                logging.warning(response_code)
                                                logging.warning(response_codes)
                                                if response_code in response_codes:
                                                    raise UserError(str(response_codes[response_code]))
                                                else:
                                                    raise UserError('Error codigo no encontrado')
            else:
                raise UserError(str('Error de conexion'))

        logging.warning(response)
        return registered
