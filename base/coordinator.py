from base.definitions.types import State


class ScintController:
    def __init__(self):
        self.current_state = State.CONTROLLER

    def get_current_state(self):
        return self.current_state

    def transition_to_locator(self):
        if self.current_state == State.CONTROLLER:
            # Perform any necessary cleanup for current state
            # Transition to the locator state
            self.current_state = State.LOCATOR
        else:
            raise ValueError("Invalid state transition")

    def transition_to_processor(self):
        if self.current_state == State.LOCATOR:
            # Perform any necessary cleanup for current state
            # Transition to the processor state
            self.current_state = State.PROCESSOR
        else:
            raise ValueError("Invalid state transition")

    def transition_to_transformer(self):
        if self.current_state == State.PROCESSOR:
            # Perform any necessary cleanup for current state
            # Transition to the transformer state
            self.current_state = State.TRANSFORMER
        else:
            raise ValueError("Invalid state transition")

    def transition_to_controller(self):
        if self.current_state in [
            State.LOCATOR,
            State.PROCESSOR,
            State.TRANSFORMER,
        ]:
            # Perform any necessary cleanup for current state
            # Transition back to controller state
            self.current_state = State.CONTROLLER
        else:
            raise ValueError("Invalid state transition")

    def handle_user_interaction(self, user_input):
        if self.current_state == State.CONTROLLER:
            # Handle user interaction in the controller state
            print("Handling user interaction in the controller")
        elif self.current_state == State.LOCATOR:
            # Handle user interaction in the locator state
            print("Handling user interaction in the locator")
        elif self.current_state == State.PROCESSOR:
            # Handle user interaction in the processor state
            print("Handling user interaction in the processor")
        elif self.current_state == State.TRANSFORMER:
            # Handle user interaction in the transformer state
            print("Handling user interaction in the transformer")
        else:
            raise ValueError("Invalid state")

    def handle_cleanup_and_setup_for_transition(self, old_state, new_state):
        """
        This method should be called whenever a transition occurs.
        It will call any necessary cleanup methods for old_state and setup methods for new_state.
        """
        pass  # To be implemented based on your application's needs.
