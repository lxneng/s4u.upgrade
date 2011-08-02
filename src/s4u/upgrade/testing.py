from s4u.upgrade import _upgrade_steps
from s4u.upgrade import _context_providers


def reset_upgrade_data():
    del _upgrade_steps[:]
    _context_providers.clear()
