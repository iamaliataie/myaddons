/** @odoo-module */

import { KanbanController } from "@web/views/kanban/kanban_controller";
import { registry } from '@web/core/registry';
import { kanbanView } from '@web/views/kanban/kanban_view';

export class VanKanbanController extends KanbanController {
   setup() {
       super.setup();
   }
   loadProducts() {
       this.actionService.doAction({
          type: 'ir.actions.act_window',
          res_model: 'fleetflow.van',
          name:'Open Wizard',
          view_mode: 'form',
          view_type: 'form',
          views: [[false, 'form']],
          target: 'new',
          res_id: false,
      });
   }
   unloadProducts() {
       this.actionService.doAction({
          type: 'ir.actions.act_window',
          res_model: 'fleetflow.van',
          name:'Open Wizard',
          view_mode: 'form',
          view_type: 'form',
          views: [[false, 'form']],
          target: 'new',
          res_id: false,
      });
   }
}
registry.category("views").add("button_in_kanban", {
   ...kanbanView,
   Controller: VanKanbanController,
   buttonTemplate: "button_van.KanbanView.Buttons",
});