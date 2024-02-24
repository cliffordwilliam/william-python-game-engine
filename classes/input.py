class Input:
    keys_pressed = {}

    @staticmethod
    def update(pressed):
        Input.keys_pressed = pressed

    @staticmethod
    def is_action_pressed(key):
        return Input.keys_pressed[key]

    @staticmethod
    def get_axis(negative_key, positive_key):
        return Input.keys_pressed[positive_key] - Input.keys_pressed[negative_key]
