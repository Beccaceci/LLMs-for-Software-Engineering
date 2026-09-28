#!/usr/bin/env python3
"""
Manim Scene: 3D Non-Convex Optimization Landscape and Gradient Descent Trajectories.
Designed for the Master's Course 'Large Language Models for Software Engineering' (Politecnico di Torino).

Features:
- Non-convex loss surface with saddle point and ravines.
- Contrasting optimization trajectories: Stochastic Gradient Descent (SGD) with oscillations vs. Adam / Momentum.
- Politecnico di Torino course color palette.
- Supports both static high-res still export (-s -qh) for LaTeX figures and MP4 video generation.
"""

from manim import *
import numpy as np

# ------------------------------------------------------------------------------
# Official Politecnico di Torino LLM4SE Course Palette
# ------------------------------------------------------------------------------
POLITO_NAVY = "#002D62"
STEEL_BLUE = "#2364A0"
DEEPDIVE_TEAL = "#0F7364"
INTUITION_PURPLE = "#5F2D8C"
EXAM_AMBER = "#B9550F"
THM_GREEN = "#14783C"
LIGHT_BG = "#FDFDFE"


class NonConvexLossLandscape3D(ThreeDScene):
    """
    Renders a 3D non-convex loss landscape with saddle points and compares
    optimization trajectories (SGD with high variance vs. Adam with adaptive momentum).
    """

    def construct(self):
        # Configure camera orientation
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)

        # 3D Coordinate Axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-1.5, 4, 1],
            x_length=6.5,
            y_length=6.5,
            z_length=4.5,
            axis_config={"color": GREY_B, "stroke_width": 2},
        )

        x_label = axes.get_x_axis_label(Tex(r"Parameter $w_1$").scale(0.65))
        y_label = axes.get_y_axis_label(Tex(r"Parameter $w_2$").scale(0.65))
        z_label = axes.get_z_axis_label(Tex(r"Loss $\mathcal{L}(w_1, w_2)$").scale(0.65))

        # Mathematical non-convex surface: saddle point with quadratic valley
        def loss_function(u, v):
            # Beale / Saddle-inspired smooth non-convex function
            return 0.3 * (u**2) - 0.4 * (v**2) + 0.1 * (v**4) + 0.05 * (u**2) * (v**2) + 0.8

        surface = Surface(
            lambda u, v: axes.c2p(u, v, loss_function(u, v)),
            u_range=[-2.8, 2.8],
            v_range=[-2.6, 2.6],
            resolution=(36, 36),
            should_make_jagged=False,
        )

        # Apply multi-tone color gradient matching the course palette
        surface.set_fill_by_value(
            axes=axes,
            colorscale=[
                (THM_GREEN, -0.5),
                (DEEPDIVE_TEAL, 0.5),
                (STEEL_BLUE, 1.5),
                (INTUITION_PURPLE, 2.5),
                (EXAM_AMBER, 3.8),
            ],
            axis=2,
        )
        surface.set_opacity(0.85)

        # SGD Trajectory (Oscillating across ravine walls)
        sgd_points = [
            (-2.2, 2.0),
            (-1.8, -1.6),
            (-1.4, 1.3),
            (-1.0, -1.0),
            (-0.7, 0.8),
            (-0.4, -0.5),
            (-0.1, 0.2),
            (0.0, 0.0),
        ]
        sgd_path_points = [axes.c2p(u, v, loss_function(u, v) + 0.08) for u, v in sgd_points]
        sgd_curve = VMobject(color=EXAM_AMBER, stroke_width=4)
        sgd_curve.set_points_as_corners(sgd_path_points)

        # Adam / Momentum Trajectory (Smooth descent through valley)
        adam_u = np.linspace(-2.2, 0.0, 30)
        adam_v = 2.0 * np.exp(-1.8 * (adam_u + 2.2))
        adam_path_points = [axes.c2p(u, v, loss_function(u, v) + 0.08) for u, v in zip(adam_u, adam_v)]
        adam_curve = VMobject(color=THM_GREEN, stroke_width=4.5)
        adam_curve.set_points_smoothly(adam_path_points)

        # Legend / Text Annotations
        title = Tex(r"\textbf{Non-Convex Optimization Landscape}").scale(0.8).to_corner(UL)
        sgd_legend = Tex(r"\textcolor{#B9550F}{\textbf{---}} SGD (High Variance Oscillation)").scale(0.6).next_to(title, DOWN, aligned_edge=LEFT)
        adam_legend = Tex(r"\textcolor{#14783C}{\textbf{---}} Adam / Momentum (Direct Valley Descent)").scale(0.6).next_to(sgd_legend, DOWN, aligned_edge=LEFT)

        self.add_fixed_in_frame_mobjects(title, sgd_legend, adam_legend)

        # Static scene population (for both still export and video initiation)
        self.add(axes, x_label, y_label, z_label, surface, sgd_curve, adam_curve)

        # Camera rotation for dynamic video companion (ignored during still export -s)
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(4)
        self.stop_ambient_camera_rotation()
