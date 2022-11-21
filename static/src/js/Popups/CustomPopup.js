/** @odoo-module **/
import rpc from 'web.rpc';
import { Gui } from 'point_of_sale.Gui';
import PosComponent from 'point_of_sale.PosComponent';
import AbstractAwaitablePopup from 'point_of_sale.AbstractAwaitablePopup';
import Registries from 'point_of_sale.Registries';
import ProductItem from 'point_of_sale.ProductItem';
const { useListener } = require('web.custom_hooks');
const { _t } = require('web.core');
class CustomPopup extends AbstractAwaitablePopup {

  constructor() {
    super(...arguments);
    console.log('En un contructor de SUCASA');
  }


}

//Create a custom popup

CustomPopup.template = 'CustomPopup';
CustomPopup.defaultProps = {

  confirmText: _t('Ok'),

  cancelText: 'Cancel',

  title: 'Número de teléfono',

  body: '',
};


Registries.Component.add(CustomPopup);
export default CustomPopup;
