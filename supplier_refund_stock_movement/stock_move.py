# -*- coding: utf-8 -*-
##############################################################################
#
#    Designcomplex, Thomas Klosinsky - All Rights Reserved.
#    Copyright (C) 2016 - http://designcomplex.de
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
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