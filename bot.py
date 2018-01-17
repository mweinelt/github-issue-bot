import re

import irc3
import requests
from requests.compat import urljoin

issue_pattern = re.compile(r"(?:^|\s)#(\d+)", re.MULTILINE)
issue_endpoint = 'https://api.github.com/repos/freifunk-gluon/gluon/issues/'


@irc3.plugin
class GithubIssues:
    def __init__(self, bot):
        self.bot = bot

    @irc3.event(irc3.rfc.PRIVMSG)
    def has_issue(self, target, data, **kwargs):
        issues = set(issue_pattern.findall(data))
        for issue_id in issues:
            response = requests.get(urljoin(issue_endpoint, issue_id))

            if response.status_code == 404:
                continue

            blob = response.json()

            self.bot.privmsg(
                target,
                "[{number}] {title} (by {user[login]}) -- {html_url}".format(
                    **blob
                )
            )


def main():
    config = dict(
        nick='gluon',
        host='irc.hackint.org', port='6697', ssl='True', ssl_verify='CERT_NONE',
        max_lag=240,
        autojoins=['#gluon'],
        includes=[
            'irc3.plugins.core',
            __name__,
        ]
    )

    bot = irc3.IrcBot.from_config(config)
    bot.run(forever=True)


if __name__ == '__main__':
    main()
