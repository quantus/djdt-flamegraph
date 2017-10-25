import collections
import signal
import threading
from time import time

from . import flamegraph

from flask_debugtoolbar.panels import DebugPanel


class FlamegraphPanel(DebugPanel):
    name = 'Flamegraph'

    user_activate = True

    using_main_thread = False

    def __init__(self, jinja_env, context={}):
        DebugPanel.__init__(self, jinja_env, context=context)

        self.using_main_thread = isinstance(
            threading.current_thread(),
            threading._MainThread
        )
        if not self.using_main_thread:
            self.is_active = False

    def content(self):
        if not self.using_main_thread:
            return (
                "The flamegraph only works on main thread. Remember to "
                "disable Werkzeug reloader with --no-reload switch."
            )
        if not self.is_active:
            return "The flamegraph is not activated, activate it to use it"

        return flamegraph.stats_to_svg(self.sampler.get_stats())

    def title(self):
        if not self.is_active:
            return "Flamegraph not active"
        return ''

    def nav_title(self):
        return 'Flamegraph'

    def nav_subtitle(self):
        if not self.is_active:
            return "in-active"
        return ''

    def url(self):
        return ''

    def has_content(self):
        return bool(self.sampler)

    def process_view(self, request, view_func, view_kwargs):
        if not self.is_active or not self.using_main_thread:
            return

        def func(*args, **kwargs):
            self.sampler = Sampler()
            self.sampler.start(kwargs)
            ret = view_func(*args, **kwargs)
            self.sampler.stop()
            return ret
        return func


class Sampler(object):
    def __init__(self, interval=0.001):
        self.stack_counts = collections.defaultdict(int)
        self.interval = interval

    def _sample(self, signum, frame):
        now = time()

        stack = []
        while frame is not None:
            formatted_frame = '{}({})'.format(frame.f_code.co_name,
                                              frame.f_globals.get('__name__'))
            stack.append(formatted_frame)
            frame = frame.f_back

        formatted_stack = ';'.join(reversed(stack))
        self.stack_counts[formatted_stack] += 1

        delta = now - self._last
        if delta > 5 * self.interval:
            # Last sample happened a long time ago, most likely we were "stuck"
            # in some external module.
            missed = delta / self.interval
            formatted_stack = (
                formatted_stack.rpartition(';')[0] + ';NATIVE CODE EXECUTION'
            )
            self.stack_counts[formatted_stack] += missed - 1
        self._last = now

    def get_stats(self):
        return '\n'.join(
            '%s %d' % (key, value) for key, value in
            sorted(self.stack_counts.items())
        )

    def start(self, info):
        self._info = info
        self._start = self._last = time()
        signal.signal(signal.SIGALRM, self._sample)
        signal.siginterrupt(signal.SIGALRM, False)
        signal.setitimer(signal.ITIMER_REAL, self.interval, self.interval)

    def stop(self):
        signal.setitimer(signal.ITIMER_REAL, 0, 0)
