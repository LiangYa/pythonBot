import random
import time

from service import interface_service, intent_service, dialogue_service, slot_service
from util.logger import Logger

if __name__ == '__main__':
    old_cookie = 'JSESSIONID=node0x7674gllzzugkqt8imil3m944239185.node0'
    cookie = 'JSESSIONID=node01sq24gc9w817e1b1llafk1aw3v3439935.node0'
    slot_service.copyByDialogueIdOld(187, 822, old_cookie, 187, 2286, cookie)
    # slot_service.copyByDialogueIdOld(345, 2163, old_cookie, 350, 2217, cookie)

    Logger.info(random.randint(1, 100))

    pass
