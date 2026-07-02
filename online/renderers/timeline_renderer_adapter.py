class TimelineRendererAdapter:

    def __init__(self, timeline, renderer):
        self.timeline = timeline
        self.renderer = renderer

    def render_at(self, t: int):
        frame = self.timeline.get_frame(t)
        self.renderer.render_frame(frame)
