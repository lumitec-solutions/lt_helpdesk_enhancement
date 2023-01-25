##############################################################################
# Copyright (c) 2022 lumitec GmbH (https://www.lumitec.solutions)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################

from odoo import models, fields, _, api
from odoo.exceptions import UserError



class SignSendRequest(models.TransientModel):
    _inherit = "sign.send.request"

    ticket_id = fields.Many2one('helpdesk.ticket', string="Ticket")

    @api.model
    def default_get(self, fields):
        res = super(SignSendRequest, self).default_get(fields)
        if not res.get('template_id'):
            return res
        template = self.env['sign.template'].browse(res['template_id'])
        res['has_default_template'] = bool(template)
        invalid_selections = template.sign_item_ids.filtered(
            lambda item: item.type_id.item_type == 'selection' and not item.option_ids)
        if invalid_selections:
            raise UserError(_("One or more selection items have no associated options"))
        if 'filename' in fields:
            res['filename'] = template.display_name
        if 'subject' in fields:
            res['subject'] = _("Signature Request - %(file_name)s", file_name=template.attachment_id.name)
        roles = template.sign_item_ids.responsible_id

        if 'signers_count' in fields or 'signer_ids' in fields or 'signer_id' in fields:
            if 'signers_count' in fields:
                res['signers_count'] = len(roles)
            if 'signer_ids' in fields:
                res['signer_ids'] = [(0, 0, {
                    'role_id': role.id,
                    'partner_id': False,
                }) for role in roles]
            if self.env.context.get('sign_directly_without_mail'):
                if len(roles) == 1 and 'signer_ids' in fields and res.get('signer_ids'):
                    res['signer_ids'][0][2]['partner_id'] = self.env.user.partner_id.id
                elif not roles and 'signer_id' in fields:
                    res['signer_id'] = self.env.user.partner_id.id
        if self._context.get('helpdesk_ticket') == True:
            if 'ticket_id' in fields:
                res['ticket_id'] = self._context.get('ticket_id')

        return res

    @api.onchange('template_id')
    def _onchange_template_id(self):
        self.signer_id = False
        self.filename = self.template_id.display_name
        self.subject = _("Signature Request - %s") % (self.template_id.attachment_id.name or '')
        roles = self.template_id.mapped('sign_item_ids.responsible_id')
        signer_ids = []
        if self._context.get('helpdesk_ticket') == True:
            signer_ids = [(0, 0, {
                'role_id': role.id,
                'partner_id': self._context.get('partner'),
            }) for role in roles]
        else:
            signer_ids = [(0, 0, {
                'role_id': role.id,
                'partner_id': False,
            }) for role in roles]
        if self.env.context.get('sign_directly_without_mail'):
            if len(roles) == 1:
                signer_ids[0][2]['partner_id'] = self.env.user.partner_id.id
            elif not roles:
                self.signer_id = self.env.user.partner_id.id
        self.signer_ids = [(5, 0, 0)] + signer_ids
        self.signers_count = len(roles)

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
