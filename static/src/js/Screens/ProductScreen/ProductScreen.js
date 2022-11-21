odoo.define('sucasa.ProductScreen', function(require) {
    'use strict';

    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const { useListener } = require('web.custom_hooks');
    var models = require('point_of_sale.models');
    const rpc = require('web.rpc');
    var { Gui } = require('point_of_sale.Gui');

    models.load_fields('product.product', 'red_id');
    models.load_fields('product.product', 'reference1');
    models.load_fields('product.product', 'reference2');
    models.load_fields('product.product', 'reference3');
    models.load_fields('product.product', 'support_query');
    models.load_fields('pos.session', 'sessionid');
    models.load_fields('product.product', 'extra_charge_end_client');


    const SuCasaProductScreen = (ProductScreen) =>
    class extends ProductScreen{

      constructor() {
        super(...arguments);
        useListener('click-pay', this._onClickPay);
      }

      codeProducts(){
        var self = this;

        var product_dicc={
          'product_id':0,
          'reference1':'',
          'reference3':'',
          'pos_transaccion_id':'',
          'amount':0,
          'no_session':0,
          'comision':0,
          'iva_comision':0,
        }
        var order = self.env.pos.get_order();
        var value_red_id = false, support_query = false;
        var number = 0;
        order.get_orderlines().forEach(function(prod){
          if (product_dicc['product_id'] ==0){
            console.log('Datos del producto');
            console.log(prod);
            console.log(order);
            product_dicc['product_id'] = prod.product.red_id;
            product_dicc['reference1'] = order.get_reference1();
            product_dicc['reference2'] = order.get_reference2();
            product_dicc['reference3'] = order.get_reference3();
            product_dicc['amount'] = prod.price;
            product_dicc['no_session'] = order.pos_session_id;
            product_dicc['comision'] = prod.product.extra_charge_end_client;
            product_dicc['iva_comision'] = (prod.product.extra_charge_end_client - (prod.product.extra_charge_end_client/1.16)).toFixed(2)
            order.set_comision(product_dicc['comision']);
            order.set_iva_comision(product_dicc['iva_comision']);
            console.log('Queriendo ver los datos de la orden');
            console.log(order);
//             prod.set_productBarcode(prod.product.barcode);
            if(prod.product.support_query == true){
              support_query = true;
            }
            var uid = prod.order.uid.replace('-', '')
            uid=uid.replace('-','')
            // product_dicc['pos_transaccion_id'] = uid.substr(0,9)
            let min = 100000000;
            let max = 999999999;
            const r = Math.random()*(max-min) + min;
            console.log('Random Number');
            console.log(Math.floor(r));
            product_dicc['pos_transaccion_id'] = Math.floor(r);

          }
          if (prod.product.red_id){
            value_red_id = true
          }
          if(prod.product.categ_id[1] == 'Recarga'){
            number = 1;
          }else{
            number = 2;
          }
        })


      }


      _onClickPay() {
        super._onClickPay();

        this.codeProducts();

      }

    }

    Registries.Component.extend(ProductScreen, SuCasaProductScreen);

    return ProductScreen;





})
