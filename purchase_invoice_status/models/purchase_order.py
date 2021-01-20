# Copyright 2020 - Today Coop IT Easy SCRLfs (<http://www.coopiteasy.be>)
# - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools.translate import _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    invoice_status = fields.Selection(
        selection_add=[
            ("partially_paid", _("Partially Paid")),
            ("paid", _("Paid")),
        ]
    )

    def _get_invoiced(self):
        super()._get_invoiced()
        for order in self.filtered(lambda o: o.invoice_status in "invoiced"):
            if all(i.state in "paid" for i in order.invoice_ids):
                order.invoice_status = "paid"
            elif any(
                i.state in ("paid", "in_payment") for i in order.invoice_ids
            ):
                order.invoice_status = "partially_paid"
