# Part of Ygen. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, http, _
import logging

_logger = logging.getLogger(__name__)


class DiscordUser(models.Model):
    _name = "discord.user"
    _inherit = 'mail.thread'
    _description = "Discord User"
    _order = "display_name desc, id desc"

    name = fields.Char(string="Username", help="The user’s username.", required=True, copy=False, readonly=True, index=True, tracking=True)
    display_name = fields.Char(string="Display Name", help="For regular users this is just their username, but if they have a guild specific nickname then that is returned instead.", required=True, copy=False, readonly=True, index=True, tracking=True)
    discord_id = fields.Char(string="Discord ID", readonly=True, help="The user’s unique ID.", tracking=True, copy=False)
    bot = fields.Boolean(string="Bot", readonly=True, help="Specifies if the user is a bot account.", default=False, copy=False)
    discriminator = fields.Char(string="Discriminator", readonly=True, help="The user’s discriminator. This is given when the username has conflicts.", tracking=True, copy=False)
    mention = fields.Char(string="Mention", readonly=True, index=True, help="The string that allows you to mention the user.", tracking=True, copy=False)
    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the channel without removing it.")

    _sql_constraints = [
        ('discord_id_unique',
         'UNIQUE(discord_id)',
         "Discord id must be unique"),

        ('mention_unique',
         'UNIQUE(mention)',
         "The mention of a user must be unique"),

        ('name_unique',
         'UNIQUE(name)',
         "The username of a user must be unique"),
    ]

    @api.model
    def UpdateOrCreate(self, vals):
        keys = vals.keys()
        Users = self.env[self._name]
        for user_key in keys:
            user = self.search([('discord_id', '=', user_key)], limit=1)
            if user:
                user.write(vals[user_key])
            else:
                user = self.create(vals[user_key])
            Users |= user
        return Users



class DiscordMember(models.Model):
    _name = "discord.member"
    _inherit = 'mail.thread'
    _description = "Discord Member"
    _order = "display_name desc, id desc"

    guild_id = fields.Many2one('discord.guild', string="Guild", readonly=True, index=True, help="The guild the member belongs to.")
    user_id = fields.Many2one('discord.user', string="User", readonly=True, index=True, help="The user the member represents.")
    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the channel without removing it.")

    name = fields.Char(related='user_id.name', string="Username", help="The user’s username.", readonly=True, index=True, tracking=True)
    display_name = fields.Char(related='user_id.display_name', string="Display Name", help="For regular users this is just their username, but if they have a guild specific nickname then that is returned instead.", readonly=True, index=True, tracking=True)
    discord_id = fields.Char(related='user_id.discord_id', string="Discord ID", readonly=True, help="The user’s unique ID.", tracking=True)
    bot = fields.Boolean(related='user_id.bot', string="Bot", readonly=True, help="Specifies if the user is a bot account.", default=False)
    discriminator = fields.Char(related='user_id.discriminator', string="Discriminator", readonly=True, help="The user’s discriminator. This is given when the username has conflicts.", tracking=True)
    mention = fields.Char(related='user_id.mention', string="Mention", readonly=True, index=True, help="The string that allows you to mention the user.", tracking=True)

    def UpdateOrCreate(self, vals):
        keys = vals.keys()
        Members = self.env[self._name]
        for member_key in keys:
            member = self.search([('discord_id', '=', member_key)], limit=1)
            if member:
                member.write(vals[member_key])
            else:
                member = self.create(vals[member_key])
            Members |= member
        return Members
