# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Vaibhav Agarwal

from manim import *
import numpy as np
from scipy.stats import norm
from manim_voiceover import VoiceoverScene
from kokoro_mv import KokoroService

# --- Configuration ---
VOICE = "af_nicole"  # Professional American Female voice

# Cinematic Color Palette
BG_COLOR = "#0A0E17"      # Deep cinematic midnight
TEAL = "#00E5FF"          # Glowing primary accent
GOLD = "#FFC107"          # Warm secondary accent
TEXT_COLOR = "#EAEAEA"    # Soft white for readability
MUTED = "#8892A4"         # For secondary information

config.background_color = BG_COLOR
config.frame_rate = 30  # Standard for 720p HD


class BlackScholesCinematic(ThreeDScene, VoiceoverScene):
    def construct(self):
        self.set_speech_service(KokoroService(voice=VOICE))

        # ==========================================
        # SCENE 1: THE HOOK & THE PROBLEM (≈1 min)
        # ==========================================
        with self.voiceover(
            text="What is the fair price of a financial option? For decades, this was one of the most difficult questions in finance. An option is a contract giving you the right, but not the obligation, to buy or sell an asset at a specific price, called the strike price, on a specific date. But how do you put a price on a right? This is the problem that three economists solved, and in doing so, they transformed Wall Street forever."
        ) as tracker:
            # Kinetic typography for the hook
            line1 = Text("What is the", font_size=52, color=TEXT_COLOR, weight=LIGHT)
            line2 = Text("fair price", font_size=72, color=TEAL, weight=BOLD)
            line3 = Text("of an option?", font_size=52, color=TEXT_COLOR, weight=LIGHT)
            
            hook = VGroup(line1, line2, line3).arrange(DOWN, buff=0.3)
            
            self.play(FadeIn(line1, shift=UP), run_time=tracker.duration * 0.2)
            self.play(Write(line2), run_time=tracker.duration * 0.3)
            self.play(FadeIn(line3, shift=DOWN), run_time=tracker.duration * 0.2)
            self.wait(tracker.duration * 0.3)
            self.play(FadeOut(hook))

        # Transition to payoff diagram
        with self.voiceover(
            text="Let's visualize a simple call option. The horizontal axis is the stock price at expiration. The vertical axis is your payoff. If the stock price finishes below the strike price, the option is worthless. But if it rises above the strike, your payoff grows, dollar for dollar. This is the famous hockey stick payoff."
        ) as tracker:
            axes = Axes(
                x_range=[0, 150, 25], y_range=[0, 60, 20],
                axis_config={"color": MUTED, "include_numbers": True},
                x_length=9, y_length=5
            ).to_edge(DOWN, buff=0.8)
            
            x_label = Text("Stock Price at Expiration (S)", font_size=22, color=TEXT_COLOR).next_to(axes.x_axis, DOWN)
            y_label = Text("Option Payoff", font_size=22, color=TEXT_COLOR).next_to(axes.y_axis, LEFT)

            strike_price = 100
            payoff_func = lambda x: max(x - strike_price, 0)
            payoff_curve = axes.plot(payoff_func, color=TEAL, x_range=[0, 150], stroke_width=5)
            
            strike_line = axes.get_vertical_line(
                axes.c2p(strike_price, 0), color=GOLD, line_func=DashedLine
            )
            strike_label = Text("Strike Price (K)", font_size=20, color=GOLD).next_to(strike_line, UP)

            self.play(Create(axes), Write(x_label), Write(y_label), run_time=tracker.duration * 0.3)
            self.play(Create(payoff_curve), Create(strike_line), Write(strike_label), run_time=tracker.duration * 0.4)
            self.wait(tracker.duration * 0.3)
            self.play(FadeOut(axes), FadeOut(x_label), FadeOut(y_label), FadeOut(payoff_curve), FadeOut(strike_line), FadeOut(strike_label))

        # ==========================================
        # SCENE 2: HISTORICAL CONTEXT (≈1.5 min)
        # ==========================================
        with self.voiceover(
            text="In the early 1970s, Fischer Black, Myron Scholes, and Robert Merton achieved a major breakthrough. They didn't just find a formula; they discovered a fundamental principle of finance. Their insight was that you could perfectly hedge an option by continuously trading the underlying stock. By creating a riskless portfolio, they could price the option using the risk-free rate. This idea, known as no-arbitrage, earned Scholes and Merton the Nobel Prize in Economics in 1997. Fischer Black had passed away, but his name lives on in the model."
        ) as tracker:
            # Timeline visualization
            timeline = NumberLine(
                x_range=[1965, 2000, 5],
                length=10,
                color=MUTED,
                include_numbers=True,
                label_direction=DOWN
            ).to_edge(UP, buff=1.5)

            # Key events
            events = VGroup(
                Dot(timeline.n2p(1973), color=TEAL, radius=0.1),
                Dot(timeline.n2p(1997), color=GOLD, radius=0.1),
            )
            event_labels = VGroup(
                Text("1973: The Formula", font_size=20, color=TEAL).next_to(events[0], UP, buff=0.3),
                Text("1997: Nobel Prize", font_size=20, color=GOLD).next_to(events[1], UP, buff=0.3),
            )

            self.play(Create(timeline), run_time=tracker.duration * 0.3)
            self.play(FadeIn(events[0], scale=0.5), Write(event_labels[0]), run_time=tracker.duration * 0.3)
            self.play(FadeIn(events[1], scale=0.5), Write(event_labels[1]), run_time=tracker.duration * 0.3)
            self.wait(tracker.duration * 0.1)
            self.play(FadeOut(timeline), FadeOut(events), FadeOut(event_labels))

        # ==========================================
        # SCENE 3: THE ASSUMPTIONS (≈1.5 min)
        # ==========================================
        with self.voiceover(
            text="The Black-Scholes model is built on a set of elegant, albeit strict, assumptions. First, the stock price follows a geometric Brownian motion with constant drift and volatility. Second, there are no transaction costs or taxes. Third, the risk-free interest rate is constant and known. Fourth, the stock pays no dividends during the option's life. And fifth, trading is continuous, and short-selling is allowed. These assumptions create a perfect, frictionless market where a unique price can be derived."
        ) as tracker:
            title = Text("The Assumptions", font_size=44, color=TEAL, weight=BOLD).to_edge(UP, buff=0.8)
            
            assumptions = VGroup(
                Text("1.  Geometric Brownian Motion", font_size=28, color=TEXT_COLOR),
                Text("2.  No Transaction Costs or Taxes", font_size=28, color=TEXT_COLOR),
                Text("3.  Constant Risk-Free Rate", font_size=28, color=TEXT_COLOR),
                Text("4.  No Dividends", font_size=28, color=TEXT_COLOR),
                Text("5.  Continuous Trading & Short-Selling", font_size=28, color=TEXT_COLOR),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).next_to(title, DOWN, buff=1)

            self.play(Write(title), run_time=tracker.duration * 0.2)
            self.play(
                LaggedStart(*[FadeIn(line, shift=RIGHT) for line in assumptions], lag_ratio=0.15),
                run_time=tracker.duration * 0.7
            )
            self.wait(tracker.duration * 0.1)
            self.play(FadeOut(title), FadeOut(assumptions))

        # ==========================================
        # SCENE 4: BROWNIAN MOTION (≈1 min)
        # ==========================================
        with self.voiceover(
            text="At the heart of the model is the idea that stock prices wander randomly, like a particle in a fluid. This is called geometric Brownian motion. While the exact path is unpredictable, the logarithm of the price is normally distributed. This means we can model the probability of future prices using a bell curve. Let's simulate a few possible paths a stock might take over one year."
        ) as tracker:
            # GBM simulation
            np.random.seed(42)
            S0, mu, sigma, T, N = 100, 0.08, 0.25, 1.0, 252
            dt = T / N
            t = np.linspace(0, T, N)

            gbm_axes = Axes(
                x_range=[0, 1, 0.25], y_range=[50, 200, 50],
                axis_config={"color": MUTED},
                x_length=10, y_length=5
            ).to_edge(DOWN, buff=1.0)
            
            gbm_labels = VGroup(
                Text("Time (Years)", font_size=20, color=TEXT_COLOR).next_to(gbm_axes.x_axis, DOWN),
                Text("Stock Price", font_size=20, color=TEXT_COLOR).next_to(gbm_axes.y_axis, LEFT)
            )

            paths = VGroup()
            for _ in range(8):
                W = np.cumsum(np.random.standard_normal(size=N)) * np.sqrt(dt)
                X = (mu - 0.5 * sigma**2) * t + sigma * W
                S = S0 * np.exp(X)
                path = gbm_axes.plot_line_graph(
                    t, S, add_vertex_dots=False,
                    line_color=TEAL, stroke_width=2, stroke_opacity=0.7
                )
                paths.add(path)

            self.play(Create(gbm_axes), Write(gbm_labels), run_time=tracker.duration * 0.3)
            self.play(
                LaggedStart(*[Create(p) for p in paths], lag_ratio=0.1),
                run_time=tracker.duration * 0.7
            )
            self.wait(0.5)
            self.play(FadeOut(gbm_axes), FadeOut(gbm_labels), FadeOut(paths))

        # ==========================================
        # SCENE 5: THE FORMULA (≈1.5 min)
        # ==========================================
        with self.voiceover(
            text="From these assumptions, they derived a closed-form solution: the Black-Scholes formula. For a European call option, it is C equals S times N of d1, minus K times e to the power of negative rT, times N of d2. Here, S is the current stock price, K is the strike price, r is the risk-free rate, T is the time to expiration, and sigma is the volatility. N of x is the cumulative distribution function of the standard normal distribution. The terms d1 and d2 combine these variables into a standardized measure of how far the stock price is from the strike."
        ) as tracker:
            # Main formula
            formula = MathTex(
                "C", "=", "S", "N(d_1)", "-", "K", "e^{-rT}", "N(d_2)",
                font_size=72
            ).set_color_by_tex_to_color_map({
                "C": TEAL, "S": GOLD, "K": TEAL, "r": GOLD, "T": GOLD
            })
            formula.to_edge(UP, buff=1.5)

            # Definitions of d1 and d2
            d1_def = MathTex(
                "d_1 = \\frac{\\ln(S/K) + (r + \\frac{1}{2}\\sigma^2)T}{\\sigma \\sqrt{T}}",
                font_size=40
            ).next_to(formula, DOWN, buff=0.8)
            
            d2_def = MathTex(
                "d_2 = d_1 - \\sigma \\sqrt{T}",
                font_size=40
            ).next_to(d1_def, DOWN, buff=0.4)

            # Variable legend
            legend = VGroup(
                MathTex("S", font_size=28, color=GOLD), Text(" = Stock Price", font_size=24, color=TEXT_COLOR),
                MathTex("K", font_size=28, color=TEAL), Text(" = Strike Price", font_size=24, color=TEXT_COLOR),
                MathTex("r", font_size=28, color=GOLD), Text(" = Risk-Free Rate", font_size=24, color=TEXT_COLOR),
                MathTex("T", font_size=28, color=GOLD), Text(" = Time to Expiration", font_size=24, color=TEXT_COLOR),
                MathTex("\\sigma", font_size=28, color=TEAL), Text(" = Volatility", font_size=24, color=TEXT_COLOR),
            ).arrange_in_grid(rows=5, cols=2, buff=0.3).to_edge(DOWN, buff=0.5)

            self.play(Write(formula), run_time=tracker.duration * 0.3)
            self.play(Write(d1_def), Write(d2_def), run_time=tracker.duration * 0.3)
            self.play(FadeIn(legend, shift=UP), run_time=tracker.duration * 0.3)
            self.wait(tracker.duration * 0.1)
            self.play(FadeOut(formula), FadeOut(d1_def), FadeOut(d2_def), FadeOut(legend))

        # ==========================================
        # SCENE 6: 3D PAYOFF SURFACE (≈1.5 min)
        # ==========================================
        with self.voiceover(
            text="Let's bring this formula to life. This 3D surface shows the call price as a function of two variables: the current stock price on the x-axis, and the time to expiration on the y-axis. Notice how the option value increases as the stock price rises. It also increases with more time to expiration, because more time means more uncertainty, and more potential for the stock to move favorably. As time runs out, the surface drops toward the intrinsic payoff we saw earlier. This is the Black-Scholes model in motion."
        ) as tracker:
            # 3D Axes
            axes_3d = ThreeDAxes(
                x_range=[50, 150, 25], y_range=[0, 1, 0.25], z_range=[0, 60, 20],
                x_length=8, y_length=5, z_length=4,
                axis_config={"color": MUTED}
            ).to_edge(DOWN, buff=0.5)
            
            x_label = axes_3d.get_x_axis_label("S")
            y_label = axes_3d.get_y_axis_label("T")
            z_label = axes_3d.get_z_axis_label("C")

            # Black-Scholes call price function
            def bs_call(S, K, T, r, sigma):
                d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
                d2 = d1 - sigma * np.sqrt(T)
                return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

            K, r, sigma = 100, 0.05, 0.25

            surface = Surface(
                lambda u, v: axes_3d.c2p(u, v, bs_call(u, K, v, r, sigma)),
                u_range=[60, 140],
                v_range=[0.01, 1.0],
                resolution=(24, 24),
                fill_color=TEAL,
                fill_opacity=0.55,
                stroke_color=GOLD,
                stroke_width=0.5
            )

            # Set cinematic camera orientation
            self.set_camera_orientation(phi=70 * DEGREES, theta=-50 * DEGREES)
            
            self.play(Create(axes_3d), Write(x_label), Write(y_label), Write(z_label), run_time=tracker.duration * 0.3)
            self.play(Create(surface), run_time=tracker.duration * 0.5)
            
            # Ambient rotation for cinematic effect
            self.begin_ambient_camera_rotation(rate=0.08)
            self.wait(tracker.duration * 0.2)
            self.stop_ambient_camera_rotation()
            
            self.play(FadeOut(axes_3d), FadeOut(surface), FadeOut(x_label), FadeOut(y_label), FadeOut(z_label))

        # ==========================================
        # SCENE 7: THE GREEKS (≈1.5 min)
        # ==========================================
        with self.voiceover(
            text="The model also gives us the Greeks: Delta, Gamma, Theta, Vega, and Rho. These are the risk management tools of the options trader. Delta measures the change in option price for a one-dollar move in the stock. Gamma measures how fast Delta changes. Theta measures the decay of the option's value as time passes. Vega measures sensitivity to volatility. And Rho measures sensitivity to interest rates. Together, these Greeks allow traders to build and hedge complex portfolios with precision."
        ) as tracker:
            greeks_title = Text("The Greeks", font_size=48, color=GOLD, weight=BOLD).to_edge(UP, buff=1)
            
            greeks_data = [
                (r"\Delta", "Delta", "Sensitivity to Stock Price", TEAL),
                (r"\Gamma", "Gamma", "Sensitivity to Delta", GOLD),
                (r"\Theta", "Theta", "Sensitivity to Time Decay", MUTED),
                (r"\nu",    "Vega",  "Sensitivity to Volatility", TEAL),
                (r"\rho",   "Rho",   "Sensitivity to Interest Rates", GOLD),
            ]

            greek_rows = VGroup()
            for symbol, name, desc, color in greeks_data:
                symbol_mobj = MathTex(symbol, font_size=40, color=color)
                name_mobj = Text(name, font_size=30, color=TEXT_COLOR, weight=BOLD)
                desc_mobj = Text(desc, font_size=24, color=MUTED)
                row = VGroup(symbol_mobj, name_mobj, desc_mobj).arrange(RIGHT, buff=0.5, aligned_edge=LEFT)
                greek_rows.add(row)

            greek_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(greeks_title, DOWN, buff=1)

            self.play(Write(greeks_title), run_time=tracker.duration * 0.2)
            self.play(
                LaggedStart(*[FadeIn(row, shift=UP) for row in greek_rows], lag_ratio=0.15),
                run_time=tracker.duration * 0.7
            )
            self.wait(tracker.duration * 0.1)
            self.play(FadeOut(greeks_title), FadeOut(greek_rows))

        # ==========================================
        # SCENE 8: LIMITATIONS (≈1 min)
        # ==========================================
        with self.voiceover(
            text="Of course, the real world is not as perfect as the model's assumptions. Markets can jump, volatility is not constant, and transaction costs exist. The 1987 stock market crash, known as Black Monday, exposed some of these limitations when the model's prices diverged dramatically from reality. This led to the development of more advanced models, like stochastic volatility and jump-diffusion models. But the Black-Scholes model remains the foundation, the benchmark against which all other models are measured."
        ) as tracker:
            title = Text("Real-World Limitations", font_size=40, color=GOLD, weight=BOLD).to_edge(UP, buff=1)
            
            limitations = VGroup(
                Text("•  Volatility is not constant", font_size=28, color=TEXT_COLOR),
                Text("•  Markets can gap or jump", font_size=28, color=TEXT_COLOR),
                Text("•  Transaction costs exist", font_size=28, color=TEXT_COLOR),
                Text("•  Assumes continuous trading", font_size=28, color=TEXT_COLOR),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).next_to(title, DOWN, buff=1)

            self.play(Write(title), run_time=tracker.duration * 0.2)
            self.play(
                LaggedStart(*[FadeIn(line, shift=LEFT) for line in limitations], lag_ratio=0.15),
                run_time=tracker.duration * 0.7
            )
            self.wait(tracker.duration * 0.1)
            self.play(FadeOut(title), FadeOut(limitations))

        # ==========================================
        # SCENE 9: CONCLUSION (≈30 sec)
        # ==========================================
        with self.voiceover(
            text="The Black-Scholes model transformed finance. It gave the world a common language for pricing risk. While its assumptions don't always hold, its legacy is undeniable. It earned a Nobel Prize, spawned a multi-trillion-dollar derivatives industry, and forever changed how we understand uncertainty. The fair price of an option is no longer a mystery. It is a formula, a model, and a monument to human ingenuity."
        ) as tracker:
            conclusion = VGroup(
                Text("The Black-Scholes Model", font_size=56, color=TEAL, weight=BOLD),
                Text("1973 — Present", font_size=32, color=GOLD),
                Text("Nobel Prize in Economics, 1997", font_size=28, color=MUTED),
                Text("Transforming Risk into Mathematics", font_size=24, color=TEXT_COLOR, slant=ITALIC),
            ).arrange(DOWN, buff=0.8)

            self.play(Write(conclusion), run_time=tracker.duration)
            self.wait(1)
            self.play(FadeOut(conclusion))
