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
    'installable': True,
    'auto_install': False,
}
