# -*- coding: utf-8 -*-
###############################################################################
#
#    Designcomplex, Thomas Klosinsky - All Rights Reserved.
#    Copyright (C) 2016 - http://designcomplex.de
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Stock Movement',
    'version': '0.1',
    'author': 'Teckzilla Solutions',
    "category": "mrp",
    "depends": ['base','purchase','stock','account','sale'],
    'data': [
            'wizard/stock_locations_view.xml',
            'wizard/change_locations_view.xml',
            'wizard/change_locations_so_view.xml',
            'account_invoice_view.xml',
            'stock_move_view.xml',
    ],
    'demo_xml': [],
    'active': False,
    'installable': True,
    'application': True,
}
creating a Supplier refund.
    Created for the purpose of sending goods back to the supplier without a preceding Purchase Order,
    this module fits very well for other purposes too where an easy and fast creation of sending back goods to the supplier with account
    balance and stock movement is needed.
    
    This module adds:
    * a button in Supplier Refund to proceed Supplier Refund with Stock Movement
    * a wizard for source and destination location selection and confirmation
    * a reference between supplier refund and stock movement with easy overview and direct access vice versa
    * normal workflow of purchase order is still possible, functions are added, not overwritten
    """,
    "depends": ['base','purchase','stock','account','sale'],
    'data': [
            'wizard/stock_locations_view.xml',
            'account_invoice_view.xml',
            'stock_move_view.xml',
    ],
    'demo_xml': [],
    'active': False,
    'installable': True,
    'application': True,
}
