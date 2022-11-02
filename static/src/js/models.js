odoo.define('sucasa.models', function(require) {
    'use strict';

    const models = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    const { useListener } = require('web.custom_hooks');
    // var models = require('point_of_sale.models');
    const rpc = require('web.rpc');
    var { Gui } = require('point_of_sale.Gui');
    var exports = {};

    var posmodel_super = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({



        get_error_red_mas: async function(orders) {
            console.log('orders 1')
            console.log(orders)
            console.log('')
            console.log('')
            return await this.rpc({
                model: 'pos.order',
                method: 'send_redMas_information',
                args: [[], [orders[0]]],
            });
        },


        sending_values_red_mas: async function(dicc){
            console.log('Enviando datos a función value_fields python')
            return await this.rpc({
                model: 'pos.order',
                method: 'value_fields',
                args: [[], [dicc]],
            });
        },

        _save_to_server: async function(orders, options) {

          var self = this;
          var order = self.env.pos.get_order();
          console.log('_save_to_server1');

          if (orders.length){
             console.log('1')
             var errt = await this.get_error_red_mas(orders);
             console.log(errt)
             console.log(' :D -----------------')
             console.log('')
             console.log('')
             if (errt['error'] != false){


                  Gui.showPopup('ErrorPopup', {
                      title: 'Error',
                      body: errt['error'],
                  });
              }else{
                  console.log('Todo bien :D');
                  console.log(orders)
                  console.log(order)
                  console.log('')
                  console.log('')
                  console.log('')

                  var server_id = await posmodel_super._save_to_server.apply(this, arguments);

                  console.log('Funciona??')
                  console.log(server_id)
                  if(server_id.length){
                      errt['id_order']=server_id[0]['id']
                      errt['comision']=orders[0]['data']['comision']
                      errt['iva_comision']=orders[0]['data']['iva_comision']
                      console.log(errt);
                      console.log('..........');
                      var errt = await this.sending_values_red_mas(errt);
                  }

                  return server_id;
              }
          }else{
              return await posmodel_super._save_to_server.apply(this, arguments);
          }


        }





    });
    
    
    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        export_for_printing: function() {
            var line = _super_orderline.export_for_printing.apply(this,arguments);
            line.barcode = this.get_product().barcode;
            return line;
        },
    });
    
//     var _super_order_line = models.Orderline.prototype;

//     models.Orderline = models.Orderline.extend({
//         export_as_JSON : function(){
//             console.log('EXPORT AS JSON SUCASA');;
//             var new_json = _super_order_line.export_as_JSON.apply(this);
// //             new_json['barcode'] = this.get_productBarcode() ? this.get_productBarcode() : false;
//             console.log(this.get_product());
            
//             return new_json;
//         },
// //         initialize: function() {
// //             _super_order_line.initialize.apply(this,arguments);
// //             this.set_productBarcode();
// //         },
// //         get_productBarcode: function(){
// //             return this.get('barcode');
// //         },

// //         set_productBarcode: function(barcode){
// //             this.set({
// //               barcode: barcode
// //             });
// //         },

//         export_for_printing: function(){
// //             _super_order_line.export_for_printing.apply(this,arguments);
//             var new_json = _super_order_line.export_as_JSON.apply(this);
//             console.log('Buscando barcode')
//             console.log(this.get_product())
// //             new_json['barcode']= this.get_product().barcode;
//             return new_json; 
//         },
//     });

});
