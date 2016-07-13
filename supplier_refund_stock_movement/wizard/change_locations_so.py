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
from openerp.tools.translate import _

class change_wizard_so_temp(osv.osv_memory):
    _name = 'change.wizard.so.temp'
    _columns = {
                'so_id':fields.many2one('sale.order',string='Sale Order'),
                'customer_id':fields.many2one('res.partner',string='Customer'),
                'change_temp_id':fields.many2one('change.company.so.wizard',string='Change Company')
                }

class change_company_so_wizard(osv.osv_memory):
    _name = 'change.company.so.wizard'
    
    def change_location_so(self, cr, uid, ids, context=None):
        self_browse = self.browse(cr, uid, ids[0], context=context)
        sale_order_obj = self.pool.get('sale.order')
         
        dest_comp = self_browse.dest_comp_id.id
        for change_wizard_temp_id in self_browse.so_ids:
            for so_id in change_wizard_temp_id.so_id:
                o = so_id.write({'company_id':dest_comp})
        return {'type': 'ir.actions.act_window_close'}
         
     
    def on_change_company_so(self, cr, uid, ids, company_id, context=None):
        result = []
        if company_id:
            sale_order_obj = self.pool.get('sale.order')
            res = sale_order_obj.search(cr, uid, [('company_id','=',company_id),('state','=','draft')],context=context)
            if res:
                for res_id in res:
                    change_temp_so_dict = {
                                        'so_id':sale_order_obj.browse(cr, id, res_id),
                                        'customer_id':sale_order_obj.browse(cr, uid, res_id).partner_id.id,
                                        }
                    result.append(change_temp_so_dict)
            else:
                raise osv.except_osv(_('No Invoice Found!'),_("Either sale for this company is not in draft state. Or do not belong to this company"))
        return {'value':{'so_ids':result}}
#             
        

    _columns = {
                'so_ids' : fields.one2many('change.wizard.so.temp','change_temp_id',string='Sale Orders'),
                'company_id' : fields.many2one('res.company',string='Company',required=True),
                'dest_comp_id':fields.many2one('res.company', string='Destination Company', required=True),
                }
    
    _defaults = {
                 'company_id':lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'account.analytic.line', context=c),
                 }
    
