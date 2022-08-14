# -*- coding: utf-8 -*-


{
    'name': 'SU CASA',
    'version': '1.0',
    'category': 'Hidden',
    'sequence': 6,
    'summary': 'Módulo para SU CASA',
    'description': """

""",
    'depends': ['base','point_of_sale','product'],
    'data': [
        'views/pos_config_view.xml',
        'views/sucasa_view.xml',
        'views/pos_session_view.xml',
        # 'security/ir.model.access.csv',
    ],
    'assets':{
        'point_of_sale.assets': [
            # 'pos_ticket_mx/static/src/css/pos_ticket_mx.css',
            # 'pos_ticket_mx/static/src/js/qrcode.js',
            # 'pos_ticket_mx/static/src/js/Screens/PaymentScreen/PaymentScreen.js',
            # 'pos_ticket_mx/static/src/js/Screens/ReceiptScreen/OrderReceipt.js',
            'sucasa/static/src/js/Screens/ProductScreen/ProductScreen.js',
        ],
        'web.assets_qweb':[
            # 'pos_ticket_mx/static/src/xml/**/*',
        ],
    },
    'installable': True,
    'auto_install': False,
}
