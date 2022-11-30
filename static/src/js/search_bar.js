odoo.define('sucasa.search_bar', function (require) {
  'use strict';


  const SearchBar = require('web.SearchBar');
  const utils = require('web.utils');
  const { patch } = require('web.utils');


  patch(SearchBar.prototype, 'sucasa.mypatch2', {
    _onSearchInput(ev) {
      console.log(this)
      if (this && this.env && this.env.action && this.env.action.xml_id && this.env.action.xml_id == "sucasa.sucasa_product_template_action"){
          setTimeout(function(){
             window.location.reload(1);
          }, 2000);
      }
      this._super(ev);

    }
});
});
