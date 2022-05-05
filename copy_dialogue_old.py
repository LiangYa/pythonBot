import random
import time

from service import interface_service, intent_service, dialogue_service, slot_service
from util.logger import Logger

if __name__ == '__main__':
    old_cookie = 'JSESSIONID=node0i27mrupkj4qwrcfpkzv97w715055185.node0'
    cookie = 'JSESSIONID=node01gce0nwmszjdfmeppyjlc3cyg5031599.node0'
    slot_service.copyByDialogueIdOld(350, 2248, old_cookie, 350, 2262, cookie)
    # slot_service.copyByDialogueIdOld(345, 2163, old_cookie, 350, 2217, cookie)

    Logger.info(random.randint(1, 100))

    pass
