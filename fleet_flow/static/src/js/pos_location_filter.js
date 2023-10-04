odoo.define(
  'custom_pos_location_filter.pos_location_filter',
  function (require) {
    var models = require('point_of_sale.models');
    var PosProductList = require('point_of_sale.ProductList');

    PosProductList.include({
      init: function (parent, options) {
        this._super(parent, options);
        this.location_id = null;
      },

      filter_by_location: function (location_id) {
        this.location_id = location_id;
        this.renderElement();
      },

      render_product: function (product) {
        if (this.location_id && product.location_id[0] !== this.location_id) {
          return;
        }
        this._super(product);
      },
    });
  }
);
