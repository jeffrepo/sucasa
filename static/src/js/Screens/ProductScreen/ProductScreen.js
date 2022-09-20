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


    const SuCasaProductScreen = (ProductScreen) =>
    class extends ProductScreen{

      constructor() {
        super(...arguments);
        useListener('click-pay', this._onClickPay);
      }

      // fCheckReference(red_id, product_dicc){
      //   if(red_id){
      //     rpc.query({
      //           model: 'pos.order',
      //           method: 'check_reference',
      //           args: [[],[this.env.pos.config_id], [product_dicc]],
      //         },{
      //
      //     }).then(function (check_reference){
      //       console.log('Estamos llamando a una función');
      //       console.log(check_reference);
      //
      //     });
      //   }
      //   return true;
      // }
      //
      // fGetBalanceByBag(number){
      //
      //   if(number){
      //     var getBalanceByBag
      //     rpc.query({
      //       model: 'pos.order',
      //       method: 'get_balance_by_bag',
      //       args:[[], [this.env.pos.config_id], [number]]
      //     },{
      //     }).then(function (get_balance_by){
      //       getBalanceByBag = get_balance_by;
      //       console.log('Ya casi');
      //       console.log(getBalanceByBag);
      //       if(getBalanceByBag){
      //         return true;
      //       }else{
      //         return false;
      //       }
      //
      //     });
      //
      //
      //   }else {
      //     return false;
      //   }
      // }

      codeProducts(){
        var self = this;

        var product_dicc={
          'product_id':0,
          'reference1':'',
          'reference3':'',
          'pos_transaccion_id':'',
          'amount':0,
          'no_session':0,
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

        // console.log('Product dicc');
        // console.log(product_dicc);
        // if(value_red_id){
        //
        //   // var get_balance_by_bag = this.fGetBalanceByBag(number);
        //
        //   if(support_query){
        //
        //     // var check_reference = this.fCheckReference(value_red_id, product_dicc);
        //     console.log('Antes del RPC');
        //     rpc.query({
        //       model: 'pos.order',
        //       method: 'checkRedMas_supportQuery',
        //       args:[[], [this.env.pos.config_id], [product_dicc], [number]]
        //     },{
        //     }).then(function (response){
        //       console.log('Que trajo RESPONSE ----------------');
        //       console.log(response);
        //       if(response['ResponseMessage'] == false){
        //         console.log('Entro?');
        //         self.showScreen('PaymentScreen');
        //       }else{
        //         Gui.showPopup('ConfirmPopup', {
        //           title: self.env._t('ResponseMessage'),
        //           body:response['ResponseMessage'],
        //         }).then(({ confirmed }) => {
        //
        //
        //
        //         });
        //       }
        //
        //
        //     });
        //
        //   }else{
        //     console.log('Antes del RPC');
        //     console.log(product_dicc);
        //     console.log('');
        //     console.log('');
        //     rpc.query({
        //       model: 'pos.order',
        //       method: 'checkRedMas',
        //       args:[[], [this.env.pos.config_id], [product_dicc], [number]]
        //     },{
        //     }).then(function (response){
        //       console.log('Que trajo RESPONSE');
        //       console.log(response);
        //       if(response['ResponseMessage']==false){
        //         console.log('Entro?');
        //         self.showScreen('PaymentScreen');
        //       }else{
        //         Gui.showPopup('ConfirmPopup', {
        //           title: self.env._t('ResponseMessage'),
        //           body:response['ResponseMessage'],
        //         }).then(({ confirmed }) => {
        //
        //
        //
        //         });
        //       }
        //
        //     });
        //
        //   }
        //
        // }else{
        //   console.log('Producto sin problemas');
        //   self.showScreen('PaymentScreen');
        // }


      }


      _onClickPay() {
        super._onClickPay();
        // this.showScreen('ProductScreen');
        this.codeProducts();



      }

    }

    Registries.Component.extend(ProductScreen, SuCasaProductScreen);

    return ProductScreen;





})
