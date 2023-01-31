##############################################################################
# Copyright (c) 2022 lumitec GmbH (https://www.lumitec.solutions)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################
from odoo import models, fields, api, Command


class SignRequest(models.Model):
    _inherit = 'sign.request'

    ticket_id = fields.Many2one('helpdesk.ticket', string="Ticket")

    @api.model
    def initialize_new(self, template_id, signers, followers, reference, subject, ticket_id, message, message_cc=None, attachment_ids=None, send=True, without_mail=False):
        sign_users = self.env['res.users'].search([('partner_id', 'in', [signer['partner_id'] for signer in signers])]).filtered(lambda u: u.has_group('sign.group_sign_employee'))
        sign_request = self.create({'template_id': template_id,
                                    'reference': reference,
                                    'subject': subject,
                                    'message': message,
                                    'message_cc': message_cc,
                                    'ticket_id': ticket_id})
        if attachment_ids:
            attachment_ids.write({'res_model': sign_request._name, 'res_id': sign_request.id})
            sign_request.write({'attachment_ids': [Command.set(attachment_ids.ids)]})
        sign_request.message_subscribe(partner_ids=followers)
        sign_request.activity_update(sign_users)
        sign_request.set_signers(signers)
        if send:
            sign_request.action_sent()
        if without_mail:
            sign_request.action_sent_without_mail()
        return {
            'id': sign_request.id,
            'token': sign_request.access_token,
            'sign_token': sign_request.request_item_ids.filtered(lambda r: r.partner_id == self.env.user.partner_id)[:1].access_token,
        }
