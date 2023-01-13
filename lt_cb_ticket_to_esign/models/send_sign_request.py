##############################################################################
# Copyright (c) 2022 lumitec GmbH (https://www.lumitec.solutions)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################
from odoo import models, fields


class SignSendRequest(models.TransientModel):
    _inherit = "sign.send.request"

    ticket_id = fields.Many2one('helpdesk.ticket', string="Ticket")

    def create_request(self, send=True, without_mail=False):
        template_id = self.template_id.id
        if self.signers_count:
            signers = [{'partner_id': signer.partner_id.id, 'role': signer.role_id.id} for signer in self.signer_ids]
        else:
            signers = [{'partner_id': self.signer_id.id, 'role': self.env.ref('sign.sign_item_role_default').id}]
        followers = self.follower_ids.ids
        reference = self.filename
        subject = self.subject
        message = self.message
        message_cc = self.message_cc
        attachment_ids = self.attachment_ids
        ticket_id = self.ticket_id.id
        return self.env['sign.request'].initialize_new(
            template_id=template_id,
            signers=signers,
            followers=followers,
            reference=reference,
            subject=subject,
            ticket_id=ticket_id,
            message=message,
            message_cc=message_cc,
            attachment_ids=attachment_ids,
            send=send,
            without_mail=without_mail,
        )
