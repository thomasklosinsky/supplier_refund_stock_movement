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

from openerp.osv import fields, osv

class stock_move(osv.osv):
    _inherit = 'stock.move'
    
    _columns = {
                'refund_invoice_id':fields.many2one('account.invoice',string='Refund Invoice Ref.'),
                'type':fields.selection([
                        ('out_invoice','Customer Invoice'),
                        ('in_invoice','Supplier Invoice'),
                        ('out_refund','Customer Refund'),
                        ('in_refund','Supplier Refund'),
                    ], string='Type')
                }