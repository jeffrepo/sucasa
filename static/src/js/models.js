odoo.define('sucasa.models', function(require) {
    'use strict';

    const models = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    const { useListener } = require('web.custom_hooks');
    // var models = require('point_of_sale.models');
    const rpc = require('web.rpc');
    var { Gui } = require('point_of_sale.Gui');
    var exports = {};
    var core = require('web.core');
    var _t = core._t;

    var posmodel_super = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({

        add_product: async function(product, options){
        console.log("ad product")
        console.log(product)
        console.log(options)
        return posmodel_super.add_product.apply(product, options);
        },
        //Check sale se manda a llamar si y solo si Sale() pasó mas de 30 segundos esperando respuesta
        check_sale: async function(orders) {
            console.log('check_sale por timout')
            console.log(orders)
            console.log('')
            console.log('')
            return await this.rpc({
                model: 'pos.order',
                method: 'check_sale',
                args: [[], [orders[0]]],
            }, {
                timeout: 800,
                shadow: true,
            }).then(function(respuesta){
                    //self.set_synch(self.get('failed') ? 'error' : 'disconnected');
                    console.log('RESPUES CHECKSALE AL INTENTAR TIMEOUT');
                    console.log(respuesta)
                    return respuesta
            })
        },


         setIntervalX: async function(callback, delay, repetitions) {
            var x = 0;
            var intervalID = setInterval(function () {

               callback();

               if (++x === repetitions) {
                   clearInterval(intervalID);
               }
            }, delay);
        },


        get_mas: async function(orders){
            var self = this;
                return await this.rpc({
                        model: 'pos.order',
                        method: 'send_redMas_information',
                        args: [[], [orders[0]]],
                    }, {
                        timeout: 10000,
                        shadow: false,
                    }).catch(function(error){
                        //self.set_synch(self.get(
                            console.log('err1')
                            return error;
                    }).then( function(response) {
                            console.log('th response')

                            return response;


                    });


        },




        //Manda a llamar Sale en el PY
        get_error_red_mas: async function(orders) {
            console.log('get_error_red_mas')
            console.log(orders)
            console.log('')
            console.log('')
            var self = this;

            return new Promise(async (resolve, reject) => {
                /////////////////////////////////////////////////////////////////////////////////////7
                try {
                          var self = this;

                          const timeout = setTimeout(async function () {
                                //resolve = undefined;
                                console.log('time out')
                                var si = self.check_set_inverval(orders, resolve, reject)
                          }, 30000); // 30 second timeout


                        const red_mas_request = await self.get_mas(orders)
                        console.log('red_mas_request')
                        console.log(red_mas_request)

                        if (resolve){
                            console.log('entra a resolve **')
                            clearTimeout(timeout);
                            resolve(red_mas_request)

                        }else{
                            console.log('realizado antes')
                        }


                }catch(error) {

                        reject(error);
                    }


            });


        },

        check_set_inverval: async function(orders,resolve,reject){
                    var self = this;
                    var delay = 7;
                    var limit = 7;
                    let i = 1;

                    console.log('START!');
                    const limitedInterval = setInterval(async function () {
                      console.log('message ${i}, appeared after ${delay * i++} seconds');
                      i++

                       var ch_sale = await self.check_sale(orders);
                        if (ch_sale){
                            if ("ResponseCode" in ch_sale){
                                if (ch_sale["ResponseCode"] == "000"){
                                    limit = i
                                    resolve(ch_sale)
                                    clearInterval(limitedInterval)

                                }else{
                                    limit = i
                                    clearInterval(limitedInterval)
                                    reject();
                                }

                            }

                        }


                       if (i == limit){
                         // resolve(true);
                           clearInterval(limitedInterval)
                       }



                    }, delay * 1000);

                   //console.log('FUERA SET INTER')
                   //console.log(limitedInterval)
                   //clearInterval(limitedInterval)
        },

        //Manda a llamar Sale en el PY
        get_error_red_mas2: function(orders) {
            console.log('get_error_red_mas')
            console.log(orders)
            console.log('')
            console.log('')
            var self = this;
            return new Promise(function(resolve,reject){

              const timeout = setTimeout(async function () {


                    resolve = undefined;
                    console.log('time out')
                    //reject(new Error('Timeout'));

                  //var interval_check_sale = await self.check_set_inverval(orders);
                  //console.log('final time out')
                  //console.log(interval_check_sale)



              }, 30000); // 30 second timeout


            self.rpc({
                model: 'pos.order',
                method: 'send_redMas_information',
                args: [[], [orders[0]]],
            }, {
                timeout: 3000,
                shadow: false,
            }).then( function (status) {
                console.log('THEN get_error_red_mas')
                console.log(status)
                console.log(resolve)
                if(resolve){
                    console.log('entro a if resolve')
                    resolve(status)
                }

            }).catch(function (data){
                console.log('CATCH get_error_red_mas')
                console.log(data)

            });


            });

        },
        refresh_sesion: async function(){
            return await this.rpc({
                model: 'pos.session',
                method: 'get_session',
                args: [[]],
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


        error_red_mas_tim: function(funcion_req,ms){

            var new_promise =  new Promise(function(resolve, reject){
                    setTimeout(function(){
                        resolve("Success!");
                    }, 4000);
            });


                  return new Promise(function(resolve, reject) {
                      setTimeout(function() {
                          console.log('SETIMEOUT')
                          reject(new Error("Data fetch failed in "+ms+" ms"))
                      }, ms)
                      console.log('fucnion tim')
                      console.log(resolve)
                      console.log(funcion_req)
                      console.log(reject)



                    funcion_req.then(function(res){
                      console.log('llega a resolve')
                      console.log('RES')
                      console.log(res)
                      resolve(res);

                      },function (type, err) { reject(); });

                  });

        },

        _save_to_server: async function(orders, options) {

          var self = this;
          var order = self.env.pos.get_order();
          console.log('_save_to_server1');

          if (orders.length){
             console.log('1')

            // make sure to stop polling when we're done
            //this.get_error_red_mas_async(orders).then(console.log)


            //setTimeout(this.get_error_red_mas(orders), 5000);
            var errt = await this.get_error_red_mas(orders);


            //this.error_red_mas_tim(this.get_error_red_mas(orders), 40000).
            //then(function(res){
             //       console.log('res then')
             //       console.log(res);
            //}).catch(function(error){
             //   console.log('error catch')
             //   console.log(error)
            //    console.log(error.message)
            //});


            //var errt = {'error': false}
            console.log(errt)
             console.log(' :D -----------------')
             console.log('')
             console.log('')
             if (errt['error'] != false){


                          console.log('ERROR RED A')
                          console.log(errt)
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

                  //if (errt['error'] != false && 'sesion_expirada' == errt['error']){
                    //  this.refresh_sesion();
                     // errt = await this.get_error_red_mas(orders);
                  //}


                  var server_id =  await posmodel_super._save_to_server.apply(this, arguments);

                  console.log('Funciona??')
                  console.log(server_id)
                  if(server_id.length){
                      errt['id_order']=server_id[0]['id']
                      errt['comision']=orders[0]['data']['comision']
                      errt['iva_comision']=orders[0]['data']['iva_comision']
                      if('amount_check_reference' in errt){
                          order.get_orderlines().forEach(function(prod){
                              if (errt['amount_check_reference']>0){
                                  console.log('Que es prod en models.js 1');
                                  console.log(prod)
                                  prod.price = errt['amount_check_reference'];
                              }

                          });


                      }
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

});
