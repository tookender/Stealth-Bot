import io
import copy
import errors
import typing
import inspect
import difflib
import discord
import itertools
import traceback

from helpers import helpers
from ._base import EventsBase
from discord.ext import commands
from helpers.context import CustomContext
from helpers.paginator import PersistentExceptionView

def join_literals(annotation: inspect.Parameter.annotation, return_list: bool = False):
    if typing.get_origin(annotation) is typing.Literal:
        arguments = annotation.__args__

        if return_list is False:
            return '[' + '|'.join(arguments) + ']'

        else:
            return list(arguments)

    return None


def conv_n(tuple_acc):
    returning = ""
    op_list_v = []
    op_list_n = list(tuple_acc)

    for i in range(len(op_list_n)):
        op_list_v.append(op_list_n[i].__name__.replace("Converter", ""))

    for i in range(len(op_list_v)):
        if i + 3 <= len(op_list_v):
            returning += f"{op_list_v[i].lower()}, "

        elif i + 2 <= len(op_list_v):
            returning += f"{op_list_v[i].lower()} or "

        else:
            returning += f"{op_list_v[i].lower()}"

    return returning


class ErrorHandler(EventsBase):

    @commands.Cog.listener('on_command_error')
    async def error_handler(self, ctx: CustomContext, error):
        owners = [564890536947875868, 555818548291829792]

        error = getattr(error, "original", error)

        if isinstance(error, errors.MuteRoleNotFound):
            pass

        elif isinstance(error, errors.MuteRoleAlreadyExists):
            pass

        #### NORMAL ERRORS ####

        elif isinstance(error, errors.Forbidden):
            pass

        elif isinstance(error, errors.InvalidThread):
            pass

        elif isinstance(error, errors.AuthorBlacklisted):
            pass

        elif isinstance(error, errors.BotMaintenance):
            pass

        elif isinstance(error, errors.NoBannedMembers):
            pass

        elif isinstance(error, helpers.NotSH):
            pass

        elif isinstance(error, helpers.NotSPvP):
            pass

        elif isinstance(error, errors.TooLongPrefix):
            pass

        elif isinstance(error, errors.TooManyPrefixes):
            pass

        elif isinstance(error, errors.EmptyTodoList):
            pass

        elif isinstance(error, errors.NoSpotifyStatus):
            pass

        elif isinstance(error, errors.PrefixAlreadyExists):
            pass

        elif isinstance(error, errors.PrefixDoesntExist):
            pass

        elif isinstance(error, errors.CommandDoesntExist):
            pass

        elif isinstance(error, commands.CommandOnCooldown):
            pass

        elif isinstance(error, discord.Forbidden):
            pass

        elif isinstance(error, discord.HTTPException):
            pass

        elif isinstance(error, commands.MissingPermissions):
            pass

        elif isinstance(error, commands.BotMissingPermissions):
            pass

        elif isinstance(error, commands.NotOwner):
            pass

        elif isinstance(error, commands.DisabledCommand):
            pass

        elif isinstance(error, commands.CheckAnyFailure):
            pass

        elif isinstance(error, commands.TooManyArguments):
            pass

        elif isinstance(error, commands.BadLiteralArgument):
            pass

        elif isinstance(error, commands.BadArgument):
            pass

        elif isinstance(error, commands.BadUnionArgument):
            pass

        elif isinstance(error, commands.MemberNotFound):
            pass

        elif isinstance(error, commands.MessageNotFound):
            pass

        elif isinstance(error, commands.GuildNotFound):
            pass

        elif isinstance(error, commands.ChannelNotFound):
            pass

        elif isinstance(error, commands.UserNotFound):
            pass

        elif isinstance(error, commands.EmojiNotFound):
            pass

        elif isinstance(error, commands.ChannelNotReadable):
            pass

        elif isinstance(error, commands.NSFWChannelRequired):
            pass

        elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
            pass

        elif isinstance(error, commands.RoleNotFound):
            pass

        elif isinstance(error, commands.MissingRole):
            pass

        elif isinstance(error, commands.ExtensionFailed):
            pass

        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            pass

        elif isinstance(error, commands.ExtensionNotFound):
            pass

        elif isinstance(error, IndexError):
            pass

        elif isinstance(error, KeyError):
            pass

        else:
            name = None
            icon_url = None
            message = None

            channel = self.bot.get_channel(914145662520659998)

            traceback_string = "".join(traceback.format_exception(etype=None, value=error, tb=error.__traceback__))

            embed = discord.Embed( description=f"An unexpected error occurred.\nThe developers have been notified about this and will fix it ASAP.")
            embed.set_author(name="Unexpected error occurred", icon_url='https://i.imgur.com/9gQ6A5Y.png')

            await ctx.send(embed=embed)

            return await self.send_unexpected_error(ctx, error)

        traceback_string = "".join(traceback.format_exception(etype=None, value=error, tb=error.__traceback__))

        embed = discord.Embed(title=f"<:error:888779034408927242> Command {ctx.command.name} raised an error", description=f"""
```prolog
{traceback_string}
```
        """)

        return await ctx.send(embed=embed, footer=False)

    @commands.Cog.listener()
    async def on_command(self, ctx: CustomContext):
        if ctx.guild.id in self.bot.disable_commands_guilds:
            try:
                if self.bot.disable_commands_guilds[ctx.guild.id] is True:
                    return

            except KeyError:
                pass

        await self.bot.db.execute(
            "INSERT INTO commands (guild_id, user_id, command, timestamp) VALUES ($1, $2, $3, $4)",
            getattr(ctx.guild, 'id', None), ctx.author.id, ctx.command.qualified_name, ctx.message.created_at)