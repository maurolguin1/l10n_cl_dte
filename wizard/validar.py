# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import UserError
import logging
import base64
_logger = logging.getLogger(__name__)


class ValidarDTEWizard(models.TransientModel):
    _name = 'sii.dte.validar.wizard'
    _description = 'SII XML from Provider'

    action = fields.Selection([
            ('response','Acuse de recibo') ,
            ('receipt','Recibo de mercaderías'),
            ('validate','Aprobar comercialmente'),
            ], string="Acción", default="response")

    @api.multi
    def confirm(self):
        context = dict(self._context or {})
        active_id = context.get('active_id', []) or []
        inv = self.env['account.invoice'].browse(active_id)
        if self.action == 'response':
            inv.do_receipt_deliver()
        if self.action == 'receipt':
            inv.do_receipt()
        if self.action == 'validate':
            inv.do_validar_comercial()