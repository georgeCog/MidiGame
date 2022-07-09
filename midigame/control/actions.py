from .system import SystemController

sc = SystemController()

def presses_key(key, actor):
    actor.activated_action = sc.get_presser(key)
    actor.deactivated_action = sc.get_releaser(key)
    return actor
