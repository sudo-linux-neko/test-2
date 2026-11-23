# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Vaibhav Agarwal

from manim import *
from actors import BaseActor, ActorStyle, SpeechBubble

class MeowTest(Scene):
    def construct(self):
        # 1. 创建一个卡通风格的 Actor，放在左下角
        actor = BaseActor(style=ActorStyle.CARTOON)
        actor.to_edge(LEFT).to_edge(DOWN)

        # 2. 将 Actor 加入场景并播放挥手动画
        self.play(FadeIn(actor))
        self.play(actor.wave())

        # 3. 创建一个对话气泡，附着在 Actor 上并播放生长动画
        bubble = SpeechBubble("Meow! This is Manim!")
        bubble.attach_to(actor)
        self.play(bubble.grow_animation())

        self.wait(2)
