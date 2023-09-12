import random
import time

from service import interface_service, intent_service, dialogue_service, slot_service
from util.logger import Logger

if __name__ == '__main__':
    old_cookie = 'JSESSIONID=node01cynpu7dri9fxgbnvht399c6w645375.node0'
    cookie = 'JSESSIONID=node01c3w4gksswuxi4gjc1s8ql6xr19348685.node0'
    slot_service.copyByDialogueIdOld(358, 2298, old_cookie, 360, 2306, cookie)
    # slot_service.copyByDialogueIdOld(345, 2163, old_cookie, 350, 2217, cookie)

    # Logger.info(random.randint(1, 100))

    pass
