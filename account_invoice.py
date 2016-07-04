# -*- coding: utf-8 -*-
##############################################################################
#
#   Designcomplex - Thomas Klosinsky - all rights reserved.
#   Copyright 2016
#   www.designcomplex.de - thomas@designcomplex.de
#   This software is licensed unter LGPL-3 and is distributed without
#   warranty
#   For further information see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    stock_move_ids = fields.One2many('stock.move','refund_invoice_id',string='Stock Moves')
    move_count = fields.Integer(string="Stock Moves")
        
    @api.multi
    def view_related_stock_moves(self):
        stock_moves = []
        for stock_move_id in self.stock_move_ids:
            stock_moves.append(stock_move_id.id)
        result =  {
                    'name': _('Stock Moves'),
                    'view_type':'form',
                    'view_mode': 'tree,form',
                    'res_model': 'stock.move',
                    'type': 'ir.actions.act_window',
                    'domain':[('refund_invoice_id','=',self._ids[0])],
                    }
        
        return result
    
    @api.multi
    def invoice_open_two(self):
        account_invoice_obj = self.pool.get('account.invoice') 
        res = account_invoice_obj.action_date_assign(self._cr, self._uid, self._ids[0],self._context)
        res = super(account_invoice, self).action_move_create()
        res = account_invoice_obj.action_number(self._cr, self._uid, self._ids[0],self._context)
        res = account_invoice_obj.invoice_validate(self._cr, self._uid, self._ids[0],self._context)
        return res
