##############################################################################
# Copyright (c) 2022 lumitec GmbH (https://www.lumitec.solutions)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################
from odoo import models, fields,api
from odoo.http import request



class SignTemplate(models.Model):
    _inherit = 'sign.template'

    # ticket_id = fields.Many2one('helpdesk.ticket', string="Ticket")
    # partner_id = fields.Many2one('res.partner', string="Customer")
    helpdesk_ticket_template = fields.Boolean(string="Helpdesk Ticket Template", default=False)




