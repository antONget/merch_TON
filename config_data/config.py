from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: str
    support: str
    xrocket_token: str
    community: str
    test_amount: int

@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admin_ids=env('ADMIN_IDS'),
                               support=env('SUPPORT'),
                               xrocket_token=env('XROCKET_TOKEN'),
                               community=env('COMMUNITY'),
                               test_amount=env('TEST_AMOUNT')))
