# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Vaibhav Agarwal

from manim import *
import numpy as np
from scipy.stats import norm
from manim_voiceover import VoiceoverScene
from kokoro_mv import KokoroService

# --- Configuration ---
# Use a professional American Female voice.
# Other options: "am_adam", "af_bella", "bm_george", etc.
VOICE = "af_nicole"

# Color Palette
BG_COLOR = "#0B0E14"  # Deep midnight blue
TEAL = "#00F0FF"      # Primary accent
GOLD = "#FFD700"      # Secondary accent
TEXT_COLOR = "#E0E0E0"

config.background_color = BG_COLOR

class BlackScholesExplainer(VoiceoverScene):
    def construct(self):
        # Initialize the Kokoro TTS service
        self.set_speech_service(KokoroService(voice=VOICE))

        # ==========================================
        # SCENE 1: INTRODUCTION & THE PROBLEM
        # ==========================================
        with self.voiceover(text="What is the fair price of a financial option? For decades, this was one of the most difficult questions in finance.") as tracker:
            title = Text("The Black-Scholes Model", font_size=48, color=TEAL, weight=BOLD)
            subtitle = Text("The Nobel-Prize Winning Formula for Options Pricing", font_size=24, color=TEXT_COLOR)
            title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.5)
            self.play(Write(title), FadeIn(subtitle, shift=UP), run_time=tracker.duration)
            self.wait(0.5)
            self.play(FadeOut(title_group))

        with self.voiceover(text="An option is a contract that gives you the right, but not the obligation, to buy or sell an asset at a specific price, called the strike price, on a specific date.") as tracker:
            # Visualize a simple payoff diagram
            axes = Axes(
                x_range=[0, 150, 25], y_range=[0, 50, 10],
                axis_config={"color": TEXT_COLOR},
                x_length=8, y_length=4.5
            ).to_edge(DOWN, buff=1)
            labels = axes.get_axis_labels(x_label="Stock Price (S)", y_label="Payoff")
            
            # Payoff for a call option: max(S - K, 0) with K=100
            strike_price = 100
            call_payoff = axes.plot(
                lambda x: max(x - strike_price, 0),
                color=TEAL, x_range=[0, 150]
            )
            strike_line = axes.get_vertical_line(axes.c2p(strike_price, 0), color=GOLD, line_func=DashedLine)
            strike_label = Text("Strike Price (K)", font_size=20, color=GOLD).next_to(strike_line, UP)

            self.play(Create(axes), Write(labels), run_time=tracker.duration * 0.6)
            self.play(Create(call_payoff), Create(strike_line), Write(strike_label), run_time=tracker.duration * 0.4)
            self.wait(0.5)

        # ==========================================
        # SCENE 2: THE ASSUMPTIONS & BROWNIAN MOTION
        # ==========================================
        with self.voiceover(text="The Black-Scholes model, developed in 1973 by Fischer Black, Robert Merton, and Myron Scholes, made a revolutionary assumption: that stock prices follow a geometric Brownian motion with constant drift and volatility.") as tracker:
            self.play(FadeOut(axes), FadeOut(labels), FadeOut(call_payoff), FadeOut(strike_line), FadeOut(strike_label))
            
            assumption_title = Text("Key Assumptions", font_size=36, color=TEAL).to_edge(UP)
            assumptions = VGroup(
                Text("• No dividends during the option's life", font_size=22, color=TEXT_COLOR),
                Text("• Markets are efficient (random walk)", font_size=22, color=TEXT_COLOR),
                Text("• No transaction costs or taxes", font_size=22, color=TEXT_COLOR),
                Text("• Constant risk-free rate and volatility", font_size=22, color=TEXT_COLOR),
                Text("• European-style exercise only", font_size=22, color=TEXT_COLOR)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(assumption_title, DOWN, buff=1)

            self.play(Write(assumption_title), run_time=tracker.duration * 0.3)
            self.play(LaggedStart(*[FadeIn(line, shift=RIGHT) for line in assumptions], lag_ratio=0.2), run_time=tracker.duration * 0.7)
            self.wait(0.5)

        with self.voiceover(text="This means the stock price wanders randomly, but its percentage returns are normally distributed. We can simulate this as a 'random walk' on a logarithmic scale.") as tracker:
            self.play(FadeOut(assumption_title), FadeOut(assumptions))
            
            # Simulate Geometric Brownian Motion
            np.random.seed(42)
            S0, mu, sigma, T, N = 100, 0.05, 0.2, 1.0, 252
            dt = T / N
            t = np.linspace(0, T, N)
            W = np.random.standard_normal(size=N)
            W = np.cumsum(W) * np.sqrt(dt)
            X = (mu - 0.5 * sigma**2) * t + sigma * W
            S = S0 * np.exp(X)

            gbm_axes = Axes(
                x_range=[0, 1, 0.25], y_range=[0, 200, 50],
                axis_config={"color": TEXT_COLOR},
                x_length=10, y_length=5
            ).to_edge(DOWN, buff=0.8)
            gbm_labels = gbm_axes.get_axis_labels(x_label="Time (Years)", y_label="Stock Price (S)")

            # Plot multiple paths
            paths = VGroup()
            for _ in range(5):
                W_sim = np.cumsum(np.random.standard_normal(size=N)) * np.sqrt(dt)
                X_sim = (mu - 0.5 * sigma**2) * t + sigma * W_sim
                S_sim = S0 * np.exp(X_sim)
                path = gbm_axes.plot_line_graph(t, S_sim, add_vertex_dots=False, line_color=TEAL, stroke_width=2)
                paths.add(path)
            
            self.play(Create(gbm_axes), Write(gbm_labels), run_time=tracker.duration * 0.3)
            self.play(LaggedStart(*[Create(path) for path in paths], lag_ratio=0.1), run_time=tracker.duration * 0.7)
            self.wait(0.5)

        # ==========================================
        # SCENE 3: THE FORMULA & 3D PAYOFF SURFACE
        # ==========================================
        with self.voiceover(text="From these assumptions, they derived a closed-form solution: the Black-Scholes formula. For a European call option, it is C equals S times N of d1, minus K times e to the power of negative rT, times N of d2.") as tracker:
            self.play(FadeOut(gbm_axes), FadeOut(gbm_labels), FadeOut(paths))
            
            formula = MathTex(
                "C", "=", "S", "N(d_1)", "-", "K", "e^{-rT}", "N(d_2)",
                font_size=60
            ).set_color_by_tex_to_color_map({
                "C": TEAL, "S": GOLD, "K": TEAL, "r": GOLD, "T": GOLD
            })
            formula.to_edge(UP, buff=1.5)
            
            # d1 and d2 definitions
            d1_def = MathTex(
                "d_1 = \\frac{\\ln(S/K) + (r + \\frac{1}{2}\\sigma^2)T}{\\sigma \\sqrt{T}}",
                font_size=36
            ).next_to(formula, DOWN, buff=0.8)
            d2_def = MathTex(
                "d_2 = d_1 - \\sigma \\sqrt{T}",
                font_size=36
            ).next_to(d1_def, DOWN, buff=0.4)

            self.play(Write(formula), run_time=tracker.duration * 0.5)
            self.play(Write(d1_def), Write(d2_def), run_time=tracker.duration * 0.5)
            self.wait(1)

        with self.voiceover(text="Let's visualize this. Here is the call price as a surface, depending on the current stock price and the time to expiration. Notice how the value increases with a higher stock price and decreases as time runs out.") as tracker:
            # 3D Payoff Surface
            axes_3d = ThreeDAxes(
                x_range=[50, 150, 25], y_range=[0, 1, 0.25], z_range=[0, 60, 20],
                x_length=8, y_length=5, z_length=4,
                axis_config={"color": TEXT_COLOR}
            ).to_edge(DOWN, buff=0.5)
            
            # Axes labels
            x_label = axes_3d.get_x_axis_label("S")
            y_label = axes_3d.get_y_axis_label("T")
            z_label = axes_3d.get_z_axis_label("C")

            # Define Black-Scholes call price function
            def bs_call(S, K, T, r, sigma):
                d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
                d2 = d1 - sigma * np.sqrt(T)
                return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

            K, r, sigma = 100, 0.05, 0.2
            
            # Create surface
            surface = Surface(
                lambda u, v: axes_3d.c2p(u, v, bs_call(u, K, v, r, sigma)),
                u_range=[60, 140],
                v_range=[0.01, 1.0], # Avoid T=0 to prevent division by zero
                resolution=(20, 20),
                fill_color=TEAL,
                fill_opacity=0.6,
                stroke_color=GOLD,
                stroke_width=0.5
            )

            # Camera should be angled to see the surface
            self.move_camera(phi=65 * DEGREES, theta=-45 * DEGREES)
            
            self.play(Create(axes_3d), Write(x_label), Write(y_label), Write(z_label), run_time=tracker.duration * 0.3)
            self.play(Create(surface), run_time=tracker.duration * 0.7)
            self.wait(2)

        # ==========================================
        # SCENE 4: THE GREEKS & CONCLUSION
        # ==========================================
        with self.voiceover(text="The model also gives us the 'Greeks'—Delta, Gamma, Theta, Vega, and Rho—which measure how sensitive the option price is to changes in each variable. These are the tools traders use to manage risk.") as tracker:
            self.play(FadeOut(axes_3d), FadeOut(surface), FadeOut(x_label), FadeOut(y_label), FadeOut(z_label), FadeOut(formula), FadeOut(d1_def), FadeOut(d2_def))
            
            greeks_title = Text("The Greeks", font_size=40, color=GOLD).to_edge(UP)
            greeks_list = VGroup(
                Text("Δ  Delta   —  Sensitivity to Stock Price", font_size=24, color=TEXT_COLOR),
                Text("Γ  Gamma  —  Sensitivity to Delta", font_size=24, color=TEXT_COLOR),
                Text("Θ  Theta   —  Sensitivity to Time", font_size=24, color=TEXT_COLOR),
                Text("ν  Vega    —  Sensitivity to Volatility", font_size=24, color=TEXT_COLOR),
                Text("ρ  Rho     —  Sensitivity to Interest Rate", font_size=24, color=TEXT_COLOR)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).next_to(greeks_title, DOWN, buff=1)

            self.play(Write(greeks_title), run_time=tracker.duration * 0.3)
            self.play(LaggedStart(*[FadeIn(g, shift=UP) for g in greeks_list], lag_ratio=0.15), run_time=tracker.duration * 0.7)
            self.wait(1)

        with self.voiceover(text="While its assumptions don't always hold in the real world, the Black-Scholes model remains the foundation of modern quantitative finance, earning its creators a Nobel Prize and transforming how we understand risk.") as tracker:
            self.play(FadeOut(greeks_title), FadeOut(greeks_list))
            
            conclusion = VGroup(
                Text("The Black-Scholes Model", font_size=48, color=TEAL, weight=BOLD),
                Text("1973 — Present", font_size=28, color=GOLD),
                Text("Nobel Prize in Economics, 1997", font_size=24, color=TEXT_COLOR)
            ).arrange(DOWN, buff=0.8)
            
            self.play(Write(conclusion), run_time=tracker.duration)
            self.wait(1)
            self.play(FadeOut(conclusion))
