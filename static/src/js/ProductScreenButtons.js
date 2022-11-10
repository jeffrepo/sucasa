odoo.define('sucasa.ProductScreenButtons', function(require) {
    'use strict';

    const { Gui } = require('point_of_sale.Gui');
    const PosComponent = require('point_of_sale.PosComponent');
    const { posbus } = require('point_of_sale.utils');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    var models = require('point_of_sale.models');

    class ButtonNumberCustomer extends PosComponent {
      constructor(){
        super(...arguments);
        useListener('click', this.onClick);
      }

      is_available() {
        const order = this.env.pos.get_order();
        return order
      }

      async onClick() {
        var order = this.env.pos.get_order();
        console.log("Este es el que vale 1");
        var value_reference1 = false;
        var value_reference2 = false;
        var value_reference3 = false;
        order.get_orderlines().forEach(function(prod){
          console.log("Que tiene productos?");
          console.log(prod);
          if(prod.product.reference1){
            value_reference1 = true;
          }else{
            value_reference1 = false;
          }
          if(prod.product.reference2){
            value_reference2 = true;
          }else{
            value_reference2 = false;
          }

          if(prod.product.reference3){
            value_reference3 = true;
          }else{
            value_reference3 = false;
          }
        });

        const { confirmed, payload: inputNote } = await this.showPopup('CustomPopup', {
            title: this.env._t('Datos verificadores'),
            value_reference1: value_reference1,
            value_reference2: value_reference2,
            value_reference3: value_reference3,
        });

        if (confirmed) {
            if (document.getElementById('reference1')){
              order.set_reference1(document.getElementById('reference1').value)
            }else{
              order.set_reference1(false)
            }

            if (document.getElementById('reference2')){
              order.set_reference2(document.getElementById('reference2').value)
            }else{
              order.set_reference2(false)
            }

            if (document.getElementById('reference3')){
              order.set_reference3(document.getElementById('reference3').value)
            }else{
              order.set_reference3(false)
            }


        };


      }

    }

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({

      initialize: function() {
        _super_order.initialize.apply(this,arguments);
        this.set_reference1();
        this.set_reference2();
        this.set_reference3();
        this.set_transaccion();
        this.set_comision();
        this.set_iva_comision();
      },

      export_as_JSON: function() {
        var json = _super_order.export_as_JSON.apply(this,arguments);
        json.reference1 = this.get_reference1();
        json.reference2 = this.get_reference2();
        json.reference3 = this.get_reference3();
        json.comision = this.get_comision();
        json.iva_comision = this.get_iva_comision();
        // json.transaccion = this.get_transaccion();
        console.log('Esta es una prueba 1');
        console.log(this.get_transaccion());

        return json;
      },

      get_reference1: function(){
        return this.get('reference1');
      },

      set_reference1: function(reference1){
        this.set({
          reference1: reference1
        });
      },

      get_reference2: function(){
        return this.get('reference2');
      },

      set_reference2: function(reference2){
        this.set({
          reference2: reference2
        });
      },

      get_reference3: function(){
        return this.get('reference3');
      },

      set_reference3: function(reference3){
        this.set({
          reference3: reference3
        });
      },

      get_transaccion: function(){
        return this.get('transaccion');
      },

      set_transaccion: function(transaccion){
        this.set({
          transaccion: transaccion
        });
      },

      get_comision: function(){
        return this.get('comision');
      },

      set_comision: function(comision){
        this.set({
          comision: comision
        });
      },

      get_iva_comision: function(){
        return this.get('iva_comision');
      },

      set_iva_comision: function(iva_comision){
        this.set({
          iva_comision: iva_comision
        });
      }

    });

    ButtonNumberCustomer.template = 'ButtonNumberCustomer';
    ProductScreen.addControlButton({

      component: ButtonNumberCustomer,
      condition: function(){
        return this.env.pos;
      }
    });

    Registries.Component.add(ButtonNumberCustomer);
    return ButtonNumberCustomer;




});
