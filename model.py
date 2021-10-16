import numpy as np
from scipy.optimize import minimize
from scipy.optimize import Bounds
import pandas as pd
import plotly.express as px


class OCP:
    """
    Solves optimal-control problem via
    a single-shooting approach
    """

    def __init__(self, N, upper_bound):
        self.N = N
        self.upper_bound = upper_bound
        self.t = np.linspace(0, 1, self.N + 1)

    def ode_model(self, x, u):
        alpha, v, beta, gamma, delta = 0.0581, 0.1, 0.2, 16.66, 0.25
        mass_rhs = alpha / v * np.exp(gamma * x[1] / (1 + x[1])) * (1 - x[0])
        return np.array([mass_rhs, mass_rhs * delta + beta / v * (u - x[1])])

    def runge_kutta_step(self, fun, xn, h, args):
        if args is not None:
            fun = lambda x, fun=fun: fun(x, *args)
        k1 = fun(xn)
        k2 = fun(xn + 0.5 * h * k1)
        k3 = fun(xn + 0.5 * h * k2)
        k4 = fun(xn + h * k3)
        return xn + h / 6.0 * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    def simulation(self, control_sequence):
        x = np.zeros((self.N + 1, 2))
        x[0, :] = np.array([0.0, 0.0])
        h = 1.0 / self.N
        for i in range(self.N):
            x[i + 1, :] = self.runge_kutta_step(
                self.ode_model, x[i, :], h, args=(control_sequence[i],)
            )
        return x

    def objective(self, w):
        x = self.simulation(w)
        return -x[-1, 0]

    def inequality(self, w):
        x = self.simulation(w)
        return -x[:, 1] + self.upper_bound

    def iterate(self, iter):
        w0 = np.zeros(self.N)
        res = minimize(
            self.objective,
            w0,
            method="SLSQP",
            constraints={"type": "ineq", "fun": self.inequality},
            bounds=Bounds(-0.2, 0.2),
            tol=1e-10,
            options={"maxiter": iter, "disp": False},
        )
        x = self.simulation(res.x)
        return self.t, x, res.x

    def solve(self, max_iter):
        df_list = []
        for i in range(max_iter + 1):
            t, x, w = self.iterate(i + 1)
            df = pd.DataFrame(
                {
                    "z": t,
                    "x_1": x[:, 0],
                    "x_2": x[:, 1],
                    "u": np.insert(w, 0, w[0]),
                    "iteration": np.repeat(i, len(t)),
                }
            )
            df_list.append(df)

        return pd.concat(df_list, ignore_index=True)

    def plot(self, df):
        fig = px.line(
            df,
            x="z",
            y=["x_1", "x_2", "u"],
            line_shape="hv",
            animation_frame="iteration",
            template="seaborn",
            markers=True,
        )

        fig.for_each_trace(
            lambda trace: trace.update(line_shape="spline")
            if (trace.name == "x_1") or (trace.name == "x_2")
            else ()
        )

        for frame in range(len(fig.frames)):
            fig.frames[frame].data[0].update(line_shape="spline")
            fig.frames[frame].data[1].update(line_shape="spline")

        return fig
