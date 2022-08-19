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

    ],
    'assets':{
        'point_of_sale.assets': [
            'sucasa/static/src/js/Screens/ProductScreen/ProductScreen.js',
            'sucasa/static/src/js/ProductScreenButtons.js',
            'sucasa/static/src/js/Popups/CustomPopup.js'
        ],
        'web.assets_qweb':[
            'sucasa/static/src/xml/ProductScreenButtonsViews.xml',
            'sucasa/static/src/xml/ViewsPopups/CustomPopupView.xml'
        ]
    },
    'installable': True,
    'auto_install': False,
}
