/** @odoo-module */

import Registries from 'point_of_sale.Registries';
import ProductScreen from 'point_of_sale.ProductScreen';
const { onMounted } = owl;

const ProductScreenInherit = (product_screen) =>
  class extends product_screen {
    setup() {
      onMounted(() => {
        this._computeQuanities();
      });
      return super.setup();
    }

    _computeQuanities() {
      const orderlines = this.currentOrder.orderlines;
      if (orderlines && orderlines.length) {
        orderlines.forEach((line) => {
          this.env.pos.db.product_by_id[
            line.product?.id
          ].quantity_in_location -= line.quantity;
        });
      }
    }

    async _clickProduct(event) {
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
        if (event.detail.quantity_in_location < 1) {
          return this.showPopup('ErrorPopup', {
            title: this.env._t('Out Of Stock'),
            body: this.env._t('Product is out of stock.'),
          });
        } else {
          const parentCall = super._clickProduct(event);
          this.env.pos.db.product_by_id[
            event.detail.id
          ].quantity_in_location -= 1;
          return parentCall;
        }
      }
    }

    async _updateSelectedOrderline(event) {
      const order = this.env.pos.get_order();
      const selectedLine = order.get_selected_orderline();
      // This validation must not be affected by `disallowLineQuantityChange`
      if (
        selectedLine &&
        selectedLine.isTipLine() &&
        this.env.pos.numpadMode !== 'price'
      ) {
        /**
         * You can actually type numbers from your keyboard, while a popup is shown, causing
         * the number buffer storage to be filled up with the data typed. So we force the
         * clean-up of that buffer whenever we detect this illegal action.
         */
        this._selectLine();
        if (event.detail.key === 'Backspace') {
          this._setValue('remove', event.detail.key);
        } else {
          this.showPopup('ErrorPopup', {
            title: this.env._t('Cannot modify a tip'),
            body: this.env._t('Customer tips, cannot be modified directly'),
          });
        }
      } else if (
        this.env.pos.numpadMode === 'quantity' &&
        this.env.pos.disallowLineQuantityChange()
      ) {
        if (!order.orderlines.length) return;
        let orderlines = order.orderlines;
        let lastId =
          orderlines.length !== 0 && orderlines.at(orderlines.length - 1).cid;
        let currentQuantity = this.env.pos
          .get_order()
          .get_selected_orderline()
          .get_quantity();

        if (selectedLine.noDecrease) {
          this.showPopup('ErrorPopup', {
            title: this.env._t('Invalid action'),
            body: this.env._t('You are not allowed to change this quantity'),
          });
          return;
        }
        const parsedInput =
          (event.detail.buffer && parse.float(event.detail.buffer)) || 0;
        if (lastId != selectedLine.cid) this._showDecreaseQuantityPopup();
        else if (currentQuantity < parsedInput)
          this._setValue(event.detail.buffer, event.detail.key);
        else if (parsedInput < currentQuantity)
          this._showDecreaseQuantityPopup();
      } else {
        let { buffer } = event.detail;
        let val = buffer === null ? 'remove' : buffer;
        this._setValue(val, event.detail.key);
        if (val == 'remove') {
          this._selectLine();
          this.env.pos.numpadMode = 'quantity';
        }
      }
    }

    _setValue(val, key) {
      const order_line = this.currentOrder.get_selected_orderline();
      if (order_line) {
        if (this.env.pos.numpadMode === 'quantity') {
          const product = order_line.product;
          const order_quantity = order_line.quantity;
          if (val === 'remove') {
            product.quantity_in_location += order_quantity;
            return super._setValue(val);
          }
          if (product.quantity_in_location < 1 && key !== 'Backspace') {
            return this.showPopup('ErrorPopup', {
              title: this.env._t('Out Of Stock'),
              body: this.env._t('Product is out of stock.'),
            });
          }
          if (val - order_quantity <= product.quantity_in_location) {
            this.env.pos.db.product_by_id[product.id].quantity_in_location -=
              val - order_quantity;
            return super._setValue(val);
          } else {
            const newValue = order_quantity + product.quantity_in_location;
            this.env.pos.db.product_by_id[product.id].quantity_in_location = 0;
            return super._setValue(newValue);
          }
        }
      }
    }
  };

Registries.Component.extend(ProductScreen, ProductScreenInherit);
