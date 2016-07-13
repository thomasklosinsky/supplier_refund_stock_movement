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

class change_wizard_temp(osv.osv_memory):
    _name = 'change.wizard.temp'
    _columns = {
                'invoice_id':fields.many2one('account.invoice',string='Invoices'),
                'type':fields.selection([('out_invoice','Customer Invoice'),
                    ('in_invoice','Supplier Invoice'),
                    ('out_refund','Customer Refund'),
                    ('in_refund','Supplier Refund')],string="Invoice Type"),
                'source':fields.char('Source'),
                'customer_id':fields.many2one('res.partner',string='Customer'),
                'change_temp_id':fields.many2one('change.company.wizard',string='Change Company')
                }
    
class change_company_wizard(osv.osv_memory):
    _name = 'change.company.wizard'
    
    def change_location(self, cr, uid, ids, context=None):
        self_browse = self.browse(cr, uid, ids[0], context=context)
        account_invoice_obj = self.pool.get('account.invoice')
        
        dest_comp = self_browse.dest_comp_id.id
        for change_wizard_temp_id in self_browse.invoice_ids:
            for invoice_id in change_wizard_temp_id.invoice_id:
                o = invoice_id.write({'company_id':dest_comp})
        return {'type': 'ir.actions.act_window_close'}
        
    
    def on_change_company(self, cr, uid, ids, company_id, context=None):
        result = []
        if company_id:
            account_invoice_obj = self.pool.get('account.invoice')
            res = account_invoice_obj.search(cr, uid, [('company_id','=',company_id),('state','=','draft')],context=context)
            if res:
                for res_id in res:
                    change_temp_dict = {
                                        'invoice_id':account_invoice_obj.browse(cr, id, res_id),
                                        'type':account_invoice_obj.browse(cr, uid, res_id).type,
                                        'source':account_invoice_obj.browse(cr, uid, res_id).origin,
                                        'customer_id':account_invoice_obj.browse(cr, uid, res_id).partner_id.id,
                                        }
                    result.append(change_temp_dict)
            else:
                raise osv.except_osv(_('No Invoice Found!'),_("Either invoice for this company is not in draft state. Or do not belong to this company"))
        return {'value':{'invoice_ids':result}}
            
        

    _columns = {
                'invoice_ids' : fields.one2many('change.wizard.temp','change_temp_id',string='Invoices'),
                'company_id' : fields.many2one('res.company',string='Company',required=True),
                'dest_comp_id':fields.many2one('res.company', string='Destination Company', required=True),
                }
    
    _defaults = {
                 'company_id':lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'account.analytic.line', context=c),
                 }
    
