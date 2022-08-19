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

      fCheckReference(red_id, product_dicc){
        if(red_id){
          rpc.query({
                model: 'pos.order',
                method: 'check_reference',
                args: [[],[this.env.pos.config_id], [product_dicc]],
              },{

          }).then(function (check_reference){
            console.log('Estamos llamando a una función');
            console.log(check_reference);

          });
        }
        return true;
      }

      fGetBalanceByBag(number){
        if(number){
          var getBalanceByBag
          rpc.query({
            model: 'pos.order',
            method: 'get_balance_by_bag',
            args:[[], [this.env.pos.config_id], [number]]
          },{
          }).then(function (get_balance_by){
            getBalanceByBag = get_balance_by;
            console.log('Ya casi');
            console.log(getBalanceByBag);
            if(getBalanceByBag){
              return true;
            }else{
              return false;
            }

          });


        }else {
          return false;
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
        var value_red_id = false;
        var number = 0;
        order.get_orderlines().forEach(function(prod){
          if (product_dicc['product_id'] ==0){
            product_dicc['product_id'] = prod.product.red_id;
            product_dicc['reference1'] = order.get_phoneNumber();
            product_dicc['reference3'] = order.get_verifierCode();
            var uid = prod.order.uid.replace('-', '')
            uid=uid.replace('-','')
            product_dicc['pos_transaccion_id'] = uid.substr(0,9)
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

        console.log('Product dicc');
        console.log(product_dicc)
        if(value_red_id == true){
          var check_reference = this.fCheckReference(value_red_id, product_dicc);
          var get_balance_by_bag = this.fGetBalanceByBag(number);
          if(check_reference){
            if(get_balance_by_bag){
                return true
            }

          }
        }else {
          return false
        }


      }


      _onClickPay() {
          var valueProducts = this.codeProducts();
          console.log('valueProducts');
          console.log(valueProducts);
          if(valueProducts == true){
            this.showScreen('PaymentScreen');
            super._onClickPay();
          }else{
            this.showScreen('ProductScreen');
          }



      }

    }

    Registries.Component.extend(ProductScreen, SuCasaProductScreen);

    return ProductScreen;





})
