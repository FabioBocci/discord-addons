from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)


class DiscordCommand(models.Model):
    _name = "discord.command"
    _description = "Discord Command"
    _order = "name desc, id desc"

    name = fields.Char(string="Name", help="The command’s name.", required=True, index=True)
    description = fields.Char(string="Description", help="The command’s description.", required=True, index=True)

    bot_id = fields.Many2one('discord.bot', string="Bot", index=True, help="The bot the command belongs to.")
    # guild_id = fields.Many2one('discord.guild', string="Guild", index=True, help="The guild the command belongs to.")

    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the command without removing it.")

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The name of a command must be unique"),
    ]

    @api.model
    def _get_commands(self):
        return self.search([('active', '=', True)])

    @api.model
    def _get_command(self, name):
        return self.search([('name', '=', name), ('active', '=', True)], limit=1)

    @api.model
    def _register_commands(self):
        commands = self._get_commands()
        for command in commands:
            command._register_command()

    def _register_command(self):

        # TODO implement this
        url = self.bot_id._get_url() + 'applications/%s/commands' % self.bot_id.application_id

        headers = self.bot_id._get_headers()

        body = {
            "name": self.name,
            "description": self.description,
            "type": 1,
        }
        # TODO handle subcommands and options

        try:
            result = requests.post(url, headers=headers, json=body)
            if result.status_code == 200:
                return result.json()
            result.close()
        except Exception as e:
            _logger.warning(e)
        return False
