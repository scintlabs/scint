from scint.framework.entities.composer import Composer


class Bulletin(Composer):
    def __init__(self, context, *args, **kwargs):
        super().__init__(context, *args, **kwargs)
