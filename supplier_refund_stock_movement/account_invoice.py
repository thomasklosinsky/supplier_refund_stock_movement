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
        for inv in self:
            return self.signal_workflow('invoice_open')
