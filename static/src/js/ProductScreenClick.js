odoo.define('sucasa.ProductScreenClick', function(require) {
    "use strict";

    const ProductScreenClick = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    var models = require('point_of_sale.models');

    models.load_fields('pos.config', 'device_id');
    
    const DevProductScreenClick = ProductScreenClick => class extends ProductScreenClick {
        //@Override
        
        constructor() {
            super(...arguments);
           
        }
        
        async _getAddProductOptions(product, base_code) {
            console.log('_getAddProductOptions')
            console.log(product)
            console.log(base_code)
            var super_product_options = await super._getAddProductOptions(product,base_code)
            if (product.to_weight){
                var device_id = this.env.pos.config.device_id
                console.log(device_id)
                var weight = await this._getSucasaWeight(device_id)
                super_product_options.quantity = weight
                return super_product_options
            }else{
                return super_product_options
            }
        }
        
        
        async _getSucasaWeight(device_id){
            var self = this;
                return await this.rpc({
                        model: 'pos.order',
                        method: 'get_sucasa_product_weight',
                        args: [[], [device_id]],
                    }, {
                        timeout: 10000,
                        shadow: false,
                    }).catch(function(error){
                        //self.set_synch(self.get(              
                            console.log('err1')
                            return error;
                    }).then( function(response) {
                            console.log('th response')
                            console.log(response)
                            return response;


                    }); 
        
        
        }



    }

    Registries.Component.extend(ProductScreenClick, DevProductScreenClick);

    return ProductScreenClick;
});