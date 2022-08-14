odoo.define('sucasa.ProductScreen', function(require) {
    'use strict';

    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const { useListener } = require('web.custom_hooks');
    var models = require('point_of_sale.models');
    const rpc = require('web.rpc');

    models.load_fields('product.product', 'red_id');
    models.load_fields('product.product', 'reference1');
    models.load_fields('product.product', 'reference3');


    const SuCasaProductScreen = (ProductScreen) =>
    class extends ProductScreen{

      constructor() {
        super(...arguments);
        useListener('click-pay', this._onClickPay);
      }

      _onClickPay() {
          var valueProducts = this.codeProducts();
          super._onClickPay();
          console.log('Que es codeProducts()');
          console.log(valueProducts);
          if(valueProducts == true){
            this.showScreen('PaymentScreen');
          }

      }

      codeProducts(){
        var self = this;

        var product_dicc={
          'product_id':0,
          'reference1':'',
          'reference3':'',
          'pos_transaccion_id':'',
        }
        var order = self.env.pos.get_order();
        console.log(self.product_template)
        var value_red_id = false;
        order.get_orderlines().forEach(function(prod){
          if (product_dicc['product_id'] ==0){
            console.log('PRODUCTO')
            console.log(prod)
            product_dicc['product_id'] = prod.product.red_id;
            product_dicc['reference1'] = prod.product.reference1;
            product_dicc['reference3'] = prod.product.reference3;
            var uid = prod.order.uid.replace('-', '')
            console.log(uid.replace('-',''))
            uid=uid.replace('-','')
            product_dicc['pos_transaccion_id'] = uid.substr(0,9)
          }

          // if (prod.product.red_id){
          //   value_red_id = true
          // }
        })

        console.log(product_dicc)
        rpc.query({
              model: 'pos.order',
              method: 'check_reference',
              args: [[],[this.env.pos.config_id], [product_dicc]],
            },{

        }).then(function (check_reference){
          console.log('Otra vez check_reference')
          console.log(check_reference);
          if(value_red_id == true){
            return true
          }else {
            return false
          }
        })







      }




    }

    Registries.Component.extend(ProductScreen, SuCasaProductScreen);

    return ProductScreen;











})
