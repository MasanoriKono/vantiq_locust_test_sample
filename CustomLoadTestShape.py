from locust import LoadTestShape

# include this class in the test driver file to apply the custom test load shape.
class CustomLoadTestShape(LoadTestShape):
    time_limit = 3600
    spawn_rate = 20
    start_user = 1000
    stage_increment = 1000
    stage_duration = 300
    cool_down_duration = 60

    def tick(self):

        run_time = self.get_run_time()

        cycle = int(run_time) // (self.stage_duration + self.cool_down_duration)

        if run_time % (self.stage_duration + self.cool_down_duration) < self.stage_duration:
            user_count = self.start_user + cycle * self.stage_increment
        else:
            user_count = 0

        return user_count, self.spawn_rate
