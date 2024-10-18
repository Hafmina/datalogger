from statemachine import State, StateMachine
import time

class VehicleState(StateMachine):
    off = State(initial=True)
    running = State()
    standby = State()

    check_state = off.to(running, cond="is_moving") | running.to(standby, cond="is_stationnary") | running.to(off, cond="is_off") | standby.to(off, cond="is_off")

    last_timestamp_in_movement = 0
    last_timestamp_current_present = 0

    def is_moving(self, position):
        pass

    def is_stationnary(self, position):
        pass

    def is_off(self, current):
        timestamp = time.perf_counter()

        if current > 20:
            self.last_timestamp_current_present = timestamp
            return False

        if timestamp - self.last_timestamp_current_present > 180:
            return True

        return False