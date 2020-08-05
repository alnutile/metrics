from datetime import datetime, timedelta


class SecondsDiff:
    def clamp(self, t, start, end):
        "Return `t` clamped to the range [`start`, `end`]."
        return max(start, min(end, t))

    def day_part(self, t):
        "Return timedelta between midnight and `t`."
        return t - t.replace(hour=0, minute=0, second=0)

    def office_time_between(self, a, b, start=timedelta(hours=9),
                            stop=timedelta(hours=17)):
        """
        a = start
        b = end
        Return the total office time between `a` and `b` as a timedelta
        object. Office time consists of weekdays from `start` to `stop`
        (default: 08:00 to 17:00).
        """
        zero = timedelta(0)
        assert(zero <= start <= stop <= timedelta(1))
        office_day = stop - start
        days = (b - a).days + 1
        weeks = days // 7
        a_weekday = a.weekday()
        b_weekday = b.weekday()
        extra = (max(0, 5 - a_weekday) + min(5, 1 + b_weekday)) % 5
        weekdays = weeks * 5 + extra
        total = office_day * weekdays
        if a.weekday() < 5:
            total -= self.clamp(self.day_part(a) - start, zero, office_day)
        if b.weekday() < 5:
            total -= self.clamp(stop - self.day_part(b), zero, office_day)
        return total
