import base64
import json
import logging

from odoo import http

from odoo.http import request, Response, JsonRequest
from odoo.tools.translate import _
from odoo.tools import date_utils
import logging
import requests
_logger = logging.getLogger(__name__)

class SucasaRoute(http.Controller):

    @http.route('/web/sucasa/create_weights', type='json', methods=['POST'],auth='none', csrf=False)
    def create_sucasa_weights(self):
        logging.warning('EXTERNAL SUCASA WEIGHT CONECTION HTTP')
        json_data = json.loads(request.httprequest.data)
        logging.warning(json_data)

        data = {"code": 300, "message": "error"}

        if ("user" in json_data) and ("password" in json_data) and ("device_id" in json_data) and ("weight" in json_data):
            if json_data["user"] == "arturo.gatica@avanguardiatech.com" and json_data["password"] =="12345":
                if int(json_data["device_id"]) > 0:
                    sucasa_weight_search = request.env["sucasa.productweight"].sudo().search([('device_id', '=', int(json_data["device_id"]))])
                    if len(sucasa_weight_search) > 0:
                        sucasa_weight_search.update({'weight': float(json_data["weight"])})
                    else:
                        dic_weight = {
                            "device_id": int(json_data["device_id"]),
                            "weight": float(json_data["weight"]),
                        }
                        sucasa_weight_id = request.env["sucasa.productweight"].sudo().create(dic_weight)
                        if sucasa_weight_id:
                            data = {"code": "00", "message": "Objecto creado"}
                        else:
                            data = {"code": 150, "message": "Objeto no creado"}
                else:
                    data = {"code": "00", "message": "Objecto recibido pero no creado"}
        return data

    #{'user': ,"password": "12345","device_id": ,"weight":}
