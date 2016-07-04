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

{
    'name': 'Supplier Refund Stock Movement',
    'version': '0.1',
    'author': 'Designcomplex',
    'price': 49.00,
    'license': 'LGPL-3',
    'currency': 'EUR',
    "category": "mrp",
    'summary':'Adding Stock Movements to Supplier Refunds',
    'description':"""
    Supplier Refund > Stock Movement
    ================================
    This module adds the possibility to directly make a stock movement when creating a Supplier refund.
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
