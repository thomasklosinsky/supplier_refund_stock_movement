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
from openerp.tools.translate import _

class stock_movement_locations(osv.osv_memory):
    _name = 'stock.movement.locations'
    
    def _get_source_location(self,cr,uid, ids, context=None):
        source_location = self.pool.get('stock.location').search(cr, uid, [('complete_name','ilike','Physical Locations / WH / Stock')])
        if source_location:
            return source_location[0]
    
    def _get_destination_location(self, cr, uid, ids, context=None):
        destination_location = self.pool.get('stock.location').search(cr, uid, [('name','ilike','Supplier')])
        if destination_location:
            return destination_location[0]
    
    def confirmed_location(self, cr, uid, ids, context=None):
        self_browse = self.browse(cr, uid, ids[0], context=context)
        account_invoice_obj = self.pool.get('account.invoice')
        stock_move_obj = self.pool.get('stock.move')
        models_data = self.pool.get('ir.model.data')
        product_template_obj = self.pool.get('product.template')
        stock_product_change_qty_obj = self.pool.get('stock.change.product.qty')
        
        
        
        invoice_browse = account_invoice_obj.browse(cr, uid, context['active_id'],context=context)
        if not invoice_browse.invoice_line:
            raise osv.except_osv(_('Error!'),_("There is no invoice lines. Add product details to generate stock moves"))
        else:
            stock_moves = []
            for invoice_id in invoice_browse.invoice_line:
                if invoice_id.quantity > invoice_id.product_id.product_tmpl_id.qty_available:
                    raise osv.except_osv(_('Error!'),_("The available quantity is less than what is expected"))
                else:
                    invoice_browse.signal_workflow('invoice_open')
                    context_change_product_qty = {
                                                  'active_model':'product.template',
                                                  'active_ids':invoice_id.product_id.product_tmpl_id.id,
                                                  'active_id':[invoice_id.product_id.product_tmpl_id.id],
                                                  }
                    rem_qty = (invoice_id.product_id.product_tmpl_id.qty_available) - (invoice_id.quantity)
                    stock_product_change_qty_id = stock_product_change_qty_obj.create(cr, uid, {'product_id':invoice_id.product_id.id,'location_id':12,'new_quantity':rem_qty})
#                     one = stock_product_change_qty_obj.browse(cr, uid, stock_product_change_qty_id)
                    res = stock_product_change_qty_obj.change_product_qty(cr, uid, [stock_product_change_qty_id],context=context_change_product_qty)
                    stock_move_vals = {
    #                                    'origin':invoice_browse.number,
                                       'product_id':invoice_id.product_id.id,
                                       'name':invoice_id.product_id.name,
                                       'product_uom':self.pool.get('product.uom').search(cr, uid, [('name', 'ilike', 'Unit(s)')])[0],
                                       'product_uom_qty':invoice_id.quantity,
                                       'location_id':self_browse.source_location_id.id,
                                       'location_dest_id':self_browse.destination_location_id.id,
                                       'state':'done',
                                       'type':'in_refund',
                                       'refund_invoice_id':context['active_id'],
                                       }
                    
                    stock_moves.append(stock_move_obj.create(cr, uid, stock_move_vals))
                account_invoice_obj.write(cr, uid, context['active_id'], {'stock_move_ids':[(6,0,stock_moves)],'move_count':len(stock_moves)})
                tree_view = tree_view = models_data.get_object_reference(cr, uid, 'stock', 'view_move_tree')
                res_id = tree_view and tree_view[1] or False
                result =  {
                            'name': _('Stock Moves'),
                            'view_type':'form',
                            'view_mode': 'tree,form',
                            'res_model': 'stock.move',
                            'type': 'ir.actions.act_window',
                            'domain':[('refund_invoice_id','=',context['active_id'])],
                            }
                
                return result
        
        
    _columns = {
                'source_location_id' : fields.many2one('stock.location',string='Source Location',required=True),
                'destination_location_id' : fields.many2one('stock.location',string='Destination Location',required=True),
                            
                }
    
    _defaults = {
                 'source_location_id' : _get_source_location,
                 'destination_location_id' : _get_destination_location,
                 
                 }
    
