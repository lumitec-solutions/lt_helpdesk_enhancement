##############################################################################
# Copyright (c) 2022 lumitec GmbH (https://www.lumitec.solutions)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################
{
    'name': 'Ticket should Trigger eSign',
    'summary': 'Ticket should Trigger eSign',
    'author': "lumitec GmbH",
    'website': "https://www.lumitec.solutions",
    'category': '',
    'version': '15.0.1.0.0',
    'license': 'OPL-1',
    'depends': [
        'base',
        'helpdesk',
        'sign',
    ],
    'data': [
        'data/cron.xml',
        'views/helpdesk_ticket.xml',
        'views/send_sign_request.xml',
        'views/sign_request.xml',
        'views/sign_template.xml',
         ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
