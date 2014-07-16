# zerocycle.ingest.accounts
# Accounts Report Reader
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Jul 16 18:12:52 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: accounts.py [] benjamin@bengfort.com $

"""
Accounts report reader
"""

##########################################################################
## Imports
##########################################################################

from zerocycle.db.models import *
from zerocycle.exceptions import *
from zerocycle.ingest.base import CSVReportReader

##########################################################################
## AccountsReportReader
##########################################################################

class AccountsReportReader(CSVReportReader):

    def __init__(self, *args, **kwargs):
        kwargs['header'] = kwargs.get('header', True)
        super(AccountsReportReader, self).__init__(*args, **kwargs)

    def handle_item(self, item):
        """
        Constructs a Route item from the dictionary being passed in.
        """
        return Route(name=item['ROUTE NAME'], locations=int(item['SERVICE LOCATIONS']))

if __name__ == '__main__':
    import os
    FIXTURE = os.path.join(os.path.dirname(__file__), "../../fixtures/accounts.csv")
    reader = AccountsReportReader(FIXTURE)
    for item in reader:
        print "%s" % item
