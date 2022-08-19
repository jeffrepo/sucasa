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
            title: this.env._t('Número de teléfono y código verificador'),
        });

        if (confirmed) {
            order.set_numberPhone(document.getElementById('number_customer').value)
            order.set_verifierCode(document.getElementById('verifier_code').value)

        };


      }

    }

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({

      initialize: function() {
        _super_order.initialize.apply(this,arguments);
        this.set_numberPhone();
        this.set_verifierCode();
      },

      get_phoneNumber: function(){
        return this.get('phoneNumber');
      },

      set_numberPhone: function(phoneNumber){
        this.set({
          phoneNumber: phoneNumber
        });
      },

      get_verifierCode: function(){
        return this.get('verifierCode');
      },

      set_verifierCode: function(verifierCode){
        this.set({
          verifierCode: verifierCode
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
