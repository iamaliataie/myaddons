/** @odoo-module */

import Registries from 'point_of_sale.Registries';
import ProductScreen from 'point_of_sale.ProductScreen';

const ProductScreenInherit = (product_screen) =>
  class extends product_screen {
    setup() {
      super.setup();
      console.log('Inherited Product Screen');
    }

    async _clickProduct(event) {
      super._clickProduct(event);
      const orderLines = this.currentOrder.orderlines.map((orderLine) => ({
        product_id: orderLine.product.product_tmpl_id,
        quantity: orderLine.quantity,
      }));

      const res = await this.rpc({
        model: 'pos.session',
        method: 'get_product_quantity',
        args: [odoo.pos_session_id, event.detail.product_tmpl_id, orderLines],
        context: this.env.session.user_context,
      });
      console.log(res);
      //     if (isConnectionError(error)) {
      //       return this.showPopup('OfflineErrorPopup', {
      //         title: this.env._t('Network Error'),
      //         body: this.env._t(
      //           'Product is not loaded. Tried loading the product from the server but there is a network error.'
      //         ),
      //       });
      //     } else {
      //       throw error;
      //     }
      //   }
    }
  };

Registries.Component.extend(ProductScreen, ProductScreenInherit);
