/** @odoo-module */

import Registries from 'point_of_sale.Registries';
import ProductScreen from 'point_of_sale.ProductScreen';
import { Orderline } from 'point_of_sale.models';

const ProductScreenInherit = (product_screen) =>
  class extends product_screen {
    setup() {
      super.setup();
      console.log('Inherited Product Screen');
      console.log(this.env.pos.db);
    }

    async __checkProductQuantity(product, order_lines) {
      const res = await this.rpc({
        model: 'pos.session',
        method: 'get_product_quantity',
        args: [odoo.pos_session_id, event.detail.product_tmpl_id, orderLines],
        context: this.env.session.user_context,
      });
      if (res) {
        super._clickProduct(event);
      } else {
        return this.showPopup('OfflineErrorPopup', {
          title: this.env._t('Out Of Stock'),
          body: this.env._t('Product is out of stock.'),
        });
      }
    }

    async _clickProduct(event) {
      console.log('%cClickproduct called', 'color:lime;font-weight:bold');
      // const orderLines = this.currentOrder.orderlines.map((orderLine) => ({
      //   product_id: orderLine.product.product_tmpl_id,
      //   quantity: orderLine.quantity,
      // }));

      let productHasOrderline = false;
      this.currentOrder.orderlines.forEach((line) => {
        if (line.product.product_tmpl_id === event.detail.product_tmpl_id) {
          productHasOrderline = true;
        }
      });

      if (!productHasOrderline) {
        this.env.pos.db.product_by_id[
          event.detail.id
        ].quantity_in_location -= 1;
        return super._clickProduct(event);
      } else {
        const currentOrderline = this.currentOrder.get_selected_orderline();
        const quantity = currentOrderline.quantity;
        console.log(`%c${quantity}`, 'color:pink');
        if (event.detail.quantity_in_location < 1) {
          return this.showPopup('OfflineErrorPopup', {
            title: this.env._t('Out Of Stock'),
            body: this.env._t('Product is out of stock.'),
          });
        } else {
          const parentCall = super._clickProduct(event);
          this.env.pos.db.product_by_id[
            event.detail.id
          ].quantity_in_location -= 1;
          // console.log();
          return parentCall;
        }
      }
    }
    _setValue(val) {
      console.log('%cSet value called', 'color:navy;font-weight:bold');
      return super._setValue(val);
      // if (this.currentOrder.get_selected_orderline()) {
      //   if (this.env.pos.numpadMode === 'quantity') {
      //     const result = this.currentOrder
      //       .get_selected_orderline()
      //       .set_quantity(val);
      //     if (!result) NumberBuffer.reset();
      //   } else if (this.env.pos.numpadMode === 'discount') {
      //     this.currentOrder.get_selected_orderline().set_discount(val);
      //   } else if (this.env.pos.numpadMode === 'price') {
      //     var selected_orderline = this.currentOrder.get_selected_orderline();
      //     selected_orderline.price_manually_set = true;
      //     selected_orderline.set_unit_price(val);
      //   }
      // }
    }
  };

// const PosOrderlineInherit = (pos_orderline) =>
//   class extends pos_orderline {
//     constructor(obj, options) {
//       super(obj, options);
//       console.log('%cWorking', 'color:red');
//     }

//     async set_quantity(quantity, keep_price) {
//       console.log(`%c${quantity} ==== ${keep_price}`, 'color:green');
//       if (isNaN(quantity)) {
//         return super.set_quantity(quantity, keep_price);
//       } else {
//         const res = await this.rpc({
//           model: 'pos.session',
//           method: 'get_product_quantity',
//           args: [odoo.pos_session_id, this.product.product_tmpl_id, quantity],
//         });
//         console.log('%c-----------+>', res, 'color:purple');
//         if (res) {
//           return super.set_quantity(quantity, keep_price);
//         } else {
//           return this.showPopup('OfflineErrorPopup', {
//             title: this.env._t('Out Of Stock'),
//             body: this.env._t('Product is out of stock.'),
//           });
//         }
//       }
//     }
//   };

Registries.Component.extend(ProductScreen, ProductScreenInherit);
