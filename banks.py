from twbank import TWBank
from stdchartered import STDCharteredBank

supported_banks = {'BOT': TWBank, 'SCB': STDCharteredBank}

def get_bank(name):
    return supported_banks[name]() if name in supported_banks else None

def get_bank_ids():
    return supported_banks.keys()

