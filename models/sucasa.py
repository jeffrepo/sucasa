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



class SucasaCarrier(models.Model):
    _name = 'sucasa.carrier'

    CarrierId = fields.Integer("CarrierId")
    name = fields.Char('Nombre')
