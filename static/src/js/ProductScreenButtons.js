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

        const { confirmed, payload: inputNote } = await this.showPopup('CustomPopup', {
            title: this.env._t('Datos verificadores'),
        });

        if (confirmed) {
            order.set_reference1(document.getElementById('reference1').value)
            order.set_reference2(document.getElementById('reference2').value)
            order.set_reference3(document.getElementById('reference3').value)

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
      },

      export_as_JSON: function() {
        var json = _super_order.export_as_JSON.apply(this,arguments);
        json.reference1 = this.get_reference1();
        json.reference2 = this.get_reference2();
        json.reference3 = this.get_reference3();

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
