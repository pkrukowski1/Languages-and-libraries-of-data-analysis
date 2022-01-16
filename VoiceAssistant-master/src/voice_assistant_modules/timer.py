import datetime


class Timer():
    def get_curr_time(self):
        return datetime.datetime.now()

if __name__=="__main__":
    print(Timer().get_curr_time())