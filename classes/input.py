class Input:
    keys_pressed = {}
    was_pressed = {}

    @staticmethod
    def update(pressed):
        Input.keys_pressed = pressed

    @staticmethod
    def is_action_pressed(key):
        return Input.keys_pressed[key]

    @staticmethod
    def get_axis(negative_key, positive_key):
        return Input.keys_pressed[positive_key] - Input.keys_pressed[negative_key]

    @staticmethod
    def is_action_just_pressed(key):
        if key not in Input.was_pressed:
            Input.was_pressed[key] = False

        if not Input.is_action_pressed(key) and Input.was_pressed[key]:
            Input.was_pressed[key] = False

        if Input.is_action_pressed(key) and not Input.was_pressed[key]:
            Input.was_pressed[key] = True
            return True
        return False

    @staticmethod
    def is_action_just_released(key):
        if key not in Input.was_pressed:
            Input.was_pressed[key] = False

        if Input.is_action_pressed(key) and not Input.was_pressed[key]:
            Input.was_pressed[key] = True

        if not Input.is_action_pressed(key) and Input.was_pressed[key]:
            Input.was_pressed[key] = False
            return True
        return False
