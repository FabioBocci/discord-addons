from odoo import models, fields, api


class DiscordBot(models.Model):
    _name = "discord.bot"
    _description = "Discord Bot"
    _order = "name desc, id desc"

    name = fields.Char(string="Name", help="The bot’s username.", required=True, copy=False, readonly=True, index=True, tracking=True)
    discord_id = fields.Char(string="Discord ID", readonly=True, help="The bot’s unique ID.", tracking=True, copy=False)
    token = fields.Char(string="Token", help="The bot’s token.", required=True, copy=False, readonly=True, tracking=True)
    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the bot without removing it.")

    _sql_constraints = [
        ('discord_id_unique',
         'UNIQUE(discord_id)',
         "Discord id must be unique"),

        ('token_unique',
         'UNIQUE(token)',
         "The token of a bot must be unique"),
    ]

