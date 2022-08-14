odoo.define('sucasa.screens', function (require) {
"use strict";

var screens = require('point_of_sale.screens');
var models = require('point_of_sale.models');
// var pos_db = require('point_of_sale.DB');
var rpc = require('web.rpc');
var PosBaseWidget = require('point_of_sale.BaseWidget');
var core = require('web.core');
var _t = core._t;


screens.ActionpadWidget.include({
  renderElement: function(){
      console.log('Am here');
      PosBaseWidget.prototype.renderElement.call(this);
      var self = this;
      this._super();

      this.$('.pay').click(function(){
          console.log('Vamonos')
      });
      this.$('.set-customer').click(function(){
          console.log('Que pedo?')
      });

  },
});






})
