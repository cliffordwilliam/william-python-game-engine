class Input:
    keys_pressed = {}
    was_pressed = False

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
        if Input.was_pressed == False and Input.is_action_pressed(key) == True:
            Input.was_pressed = True
            return True
        return False

    @staticmethod
    def is_action_just_released(key):
        if Input.was_pressed == True and Input.is_action_pressed(key) == False:
            Input.was_pressed = False
            return True
        return False
