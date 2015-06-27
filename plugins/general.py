import codecs
import urllib.request
import urllib.parse
from wrappers import *
import json


@plugin(desc="general")
class general():
    itersplit = re.compile(r'"([^"]*)"|([^ ]+)')

    @adv_command
    def pm(self, arg, target):
        """redirects the output to a private message"""
        try:
            while 1:
                x = yield
                if x is not None:
                    x = x.copy()
                    x.params = arg.nick
                    target.send(x)
        except GeneratorExit:
            target.close()


    @command("repeat")
    def rep(self, message):
        cnt, *msg = message.text.split()
        cnt = int(cnt)
        if cnt > 100:
            raise Exception("too many")
        for i in range(int(cnt)):
            yield message.reply(" ".join(msg))

    @command("for")
    @command("iterate")
    def iter(self, message):
        for x in message.data:
            yield message.reply(x)

    @command("reverse")
    def reverse(self, message):
        "reverse the message"
        return message.reply(message.data[::-1])

    @command("echo")
    def echo(self, message):
        "repeats the input, useful for formatting"
        return message.reply(message.data)

    @command("caps")
    @command("upper")
    def uper(self, message):
        "turns the message into upper case"
        return message.reply(message.data.upper())

    @command("lower")
    def lower(self, message):
        "turns the message into lower case"
        return message.reply(message.data.lower())

    @command("rot13")
    def rot13(self, message):
        "applies rot13 to the message"
        return message.reply(codecs.encode(message.data, 'rot_13'), codecs.encode(message.text, 'rot_13'))

    @command("camel")
    def camel(self, message):
        "turns the message into camel case"
        return message.reply(message.data.title())

    @command
    def action(self, message):
        ret = message.copy()
        ret.ctcp = "ACTION"
        return ret


    @adv_command
    def tail(self, arg, target):
        lines = []
        no = int(arg.text or 1)
        try:
            while 1:
                x = yield
                if x is not None:
                    lines.append(x)
        except GeneratorExit:
            if lines:
                for x in lines[-no:]:
                    target.send(x)
            target.close()



    @command
    def strip(self, message):
        "strip the message of any whitespace"
        return message.reply(message.data.strip())

    @adv_command
    def split(self, arg, target):
        splitby = arg.text or " "
        try:
            while 1:
                x = yield
                if x is None:
                    target.send(arg.reply(arg.data.split()))
                else:
                    target.send(x.reply(x.data.split(splitby)))
        except GeneratorExit:
            target.close()


    @command
    def quote(self, message):
        """capture the N number of previous messages and and output it as data"""
        try:
            count = int(message.text or 1)
        except:
            raise Exception("needs an integer for number of lines")

        lines = list(self.bot.message_buffer[message.server][message.params])[1:count + 1][::-1]
        count = len(lines)
        lines = "\n".join([x.to_pretty() for x in lines])

        return message.reply(lines, "captured %s lines!" % count)

    @adv_command
    def sprunge(self, arg, target):
        """redirect output to a sprunge and return the link"""
        lines = []
        arg = arg
        try:
            while 1:
                x = yield
                if x is None:
                    lines.append(str(arg.text))
                else:
                    lines.append(str(x.data))
        except GeneratorExit:
            if lines:
                data = {'sprunge': '\n'.join(lines)}
                response = urllib.request.urlopen(urllib.request.Request('http://sprunge.us',
                                                                         urllib.parse.urlencode(data).encode(
                                                                             'utf-8'))).read().decode()
                target.send(arg.reply(response))
            target.close()

    @adv_command
    def cat(self, arg, target):
        """concat all messages to one line joined by arg.text or ' '"""
        data = []
        try:
            while 1:
                x = yield
                if x is None:
                    pass
                else:
                    data.append(x.data)
        except GeneratorExit:
            target.send(arg.reply(data))
            target.close()


    @adv_command
    def wc(self, arg, target):
        count = 0
        try:
            while 1:
                x = yield
                if x is None:
                    pass
                else:
                    count += 1
        except GeneratorExit:
            target.send(arg.reply(count))
            target.close()




    @on_load
    def alaiasload(self):
        try:
            with open('aliases.json', 'r') as infile:
                aliases = json.load(infile)
                for cmd, alias in aliases.items():
                    self.bot.aliases[cmd] = alias
        except FileNotFoundError:
            pass

    @on_unload
    def aliassave(self):
        with open('aliases.json', 'w') as outfile:
            json.dump(self.bot.aliases, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    @regex("^.?botsnack")
    def botsnack(self, message):
        return message.reply("am I supposed to be impressed by this offering?")
