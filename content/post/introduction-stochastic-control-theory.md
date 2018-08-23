+++
date = "2018-08-09"
title = "Introduction to Stochastic Control Theory"
+++

I had my first contact with stochastic control theory in one of my Master's courses about Continuous Time Finance. I found the subject really interesting and decided to write my thesis about optimal dividend policy which is mainly about solving stochastic control problems.

In this post I want to give you a brief overview of stochastic control theory based on excerpts form my thesis. Let's get started.

## What is stochastic control theory?

<Remove?>
Imagine, you are an astronaut and you have to fly a rocket to the moon. Obviously, you know the direction you have to go, but there are a multitude of factors that you do not know in advance such as strong winds at take-off, small thrust differentials in your rocket and so on. You have to decide when you need to increase or decrease thrust as a consequence while all the time keeping in mind that you only have a limited amount of fuel to spend.

Imagine, you are a CEO and want to decide if you should pay dividends and if yes, what should the dividend payout ratio be? You will probably start by looking at your cash balance. Then you ask yourself: How much cash can I actually pay as dividend without risking to become insolvent? You remember that last year, raw material prices rose unexpectedly and unplanned repairs had to be made that squeezed the company wallet quite a lot, but sales of an old product also rose. Most of these events were not really foreseeable and therefore random from the company's perspective. This is where stochastic control theory comes into play. Stochastic control theory helps us find a dividend policy, i.e. a control law, so that we maximize the expected value of all future discounted dividend payments, i.e. the value function. The evolution of the company cash reserve is called the state process.

The following section closely follows the chapter "Stochastic Control Theory" from Björk (2009).

A fairly general class of stochastic control problems can be written like this:

$$\begin{align*}
  dX_t &= \mu(t, X_t, u_t)dt + \sigma(t, X_t, u_t)dW_t \\
  X_0 &= x_0,
\end{align*}$$

where `$\mu, \sigma$` are the drift and volatility of the stochastic differential equation and `$u_t$` is the control law that is used to control or steer the state process X.



\noindent
Before we continue, we need to define which type of control law we allow in our problems. It is quite natural to demand that the control law should only depend on past values of the state process. Feedback control laws are one class of control laws that satisfy this property and also the one we will consider. Formally, we can write feedback control laws the following way: 
\begin{align*}
  u&:~ \mathbb{R}_+ \times \mathbb{R}^n \to \mathbb{R}^k \\
  u_t &:=~u(t, X_t) \text{ ... feedback control law}
\end{align*}
\noindent
In most practical circumstances, the control law will likely have to obey additional control constraints. We will call the class of admissible control laws $\mathcal{U} \subset \mathbb{R}^k$ and make the following definition:
\begin{definition}
  A control law $u$ is called admissible if:
  \begin{enumerate}
    \item $u(t,x) \in \mathcal{U},~\forall t \geq 0,~\forall x \in \mathbb{R}^n$.
    \item For any starting point $(t, x)$ the stochastic differential equation 
    $$dX_t = \mu(t, X_t, u_t)dt + \sigma(t, X_t, u_t)dW_t, ~X_t = x$$
    \noindent
    has a unique solution.
  \end{enumerate}
\end{definition}

\noindent
The value function given control $u$ is given by:
\begin{align*}
  V^u &: \mathcal{U} \to \mathbb{R} \\
  V^u(t, x) &= \mathbb{E}\left[ \int_t^T F(t, X_t^u, u_t)dt + \Phi(X_T^u)|\mathcal{F}_t\right],
\end{align*}
where $F$ is a pay-off function for $t \in [0, T)$ and $\Phi$ is a pay-off function at time $t = T$, both mapping to $\mathbb{R}$\\

\noindent
The optimal value function is therefore given by:
$$V(t,x) = \sup_{u\in\mathcal{U}}V^u(t,x)$$
\noindent
or equivalently by:
$$V(t,x) = V^{u^*}(t,x).$$

\noindent
We call $u^*$ the optimal control law for the given problem. But how do we actually find the optimal value function and the associated control law? \\

\noindent
In essence, we are interested in answering two questions:
\begin{enumerate}
  \item Does an optimal control law exist?
  \item If yes, how can we find it?
\end{enumerate}

\noindent
We will focus on the second part and to find the optimal control law, we will rely on \textit{dynamic programming}. To deal with some technical problems, we make the following (sometimes rather strong) assumption:

\begin{assumption}
\label{assumption}
  The following is assumed to hold:
  \begin{enumerate}
    \item An optimal control law $u^*$ exists
    \item The optimal value function is $C^{1,2}$
    \item Interchanging limits and expectations is justified 
  \end{enumerate}
\end{assumption}

\noindent
\subsection{Dynamic programming principle}
The idea of dynamic programming can be summarized as follows:
\begin{enumerate}
  \item Consider two strategies:
  \begin{enumerate}
    \item Strategy I: Use the optimal control law $u^*$ and
    \item Strategy II: Use an arbitrary control law $u$ on $[t, t+h]$ and then switch to the optimal control law $u^*$ for the remaining time interval $(t+h, T]$.
  \end{enumerate}
  \item Compute the expected value of both strategies.
  \item Strategy II by definition cannot be better than strategy I. If we let $h \to 0$, we obtain a partial differential equation, called Hamilton-Jacobi-Bellman equation that we can use to solve our problem.
\end{enumerate}

\noindent
Strategy II is given by the control law $\tilde{u}$
$$\tilde{u}(s, y) = 
\begin{cases}
  u(s, y), & (s, y) \in [t, t+h] \times \mathbb{R}^n \\
  u^*(s, y), & (s, y) \in (t+h, T] \times \mathbb{R}^n
\end{cases}$$

\noindent
The expected value for strategy I is simply $V(t, x)$. To find the expected value for strategy II we consider the two time spans $[t, t+h)$ and $(t+h, T]$ separately:
\begin{align}
  \label{strat1}
  \mathbb{E}(\text{strategy II }[t, t+h]) &= \mathbb{E}_{t,x}\left[ \int_t^{t+h} F(s, X_s^u, u_s)\right]\\
  \label{strat2}
  \mathbb{E}(\text{strategy II }(t+h, T]) &= \mathbb{E}_{t,x}\left[ V(t+h, X_{t+h}^u)\right] ,
\end{align}
where $\mathbb{E}_{t,x}$ is short for $\mathbb{E}(.|t,x)$.  \\

\noindent
The expected value of strategy II is the sum of (\ref{strat1}) and (\ref{strat2}):
$$\mathbb{E}(\text{strategy II)} = \mathbb{E}_{t,x}\left[\int_t^{t+h} F(s, X_s^u, u_s) + V(t+h, X_{t+h}^u)\right].$$

\noindent
Comparing strategy I and II gives us:
\begin{equation}
  \label{eq:star}
  V(t, x) \geq \mathbb{E}_{t,x}\left[\int_t^{t+h} F(s, X_s^u, u_s) + V(t+h, X_{t+h}^u)\right].
\end{equation}

\noindent
Before we continue, let's define the following operator:
$$\mathcal{L}^u V(t, X_t^u) := V_x(t, X_t^u)\mu^u+\frac{1}{2}V_{xx}\sigma_u^2.$$

\noindent
Equality holds if and only if strategy II is optimal over the entire time period. Since we assumed that $V \in C^{1,2}$ we can simply apply Ito's formula to $V(t+h, X_{t+h}^u)$ in inequality (\ref{eq:star}) to get:
\begin{align*}
  V(t+h, X_{t+h}^u) &= V(t, x) + \int_t^{t+h}V_s(s, X_s^u)ds + \int_t^{t+h}V_x(s, X_s^u)dX_s \\
  &+\frac{1}{2}\underbrace{\int_t^{t+h}V_{tt}d[s]}_{\mathclap{=0 \text{ cont. + finite variation}}} + \frac{1}{2}\int_t^{t+h}V_{xx}\underbrace{d[X]_s}_{=\sigma_u^2ds} + \underbrace{\int_t^{t+h}V_{tx}d[X,s]}_{=0}\\
  &=V(t, x) + \int_t^{t+h}V_s(s, X_s^u) \\&+ \underbrace{V_x(s, X_s^u)\mu^u+\frac{1}{2}V_{xx}\sigma_u^2}_{:= \mathcal{L}^uV(s, X_s^u)} ds + \int_t^{t+h}V_x \sigma^u dW_s \\
  &= V(t, x) + \int_t^{t+h}V_s(s, X_s^u) + \mathcal{L}^u(s, X_s^u)ds + \int_t^{t+h}V_x \sigma^u dW_s \\
  \mathbb{E}_{t,x}(V(t+h, X_{t+h}^u)) &= \underbrace{V(t,x)}_{\mathclap{\mathcal{F}_t-measurable}} + \mathbb{E}_{t, x}\left[\int_t^{t+h}V_s(s, X_s^u) + \mathcal{L}^u(s, X_s^u)ds
\right] \\&+ \underbrace{\mathbb{E}_{t,x} \left[ \int_t^{t+h}V_x \sigma^u dW_s \right]}_{=0\text{ given suff. integrability}}.
\end{align*}

\noindent
It can be shown that if any component of $[A, B]_t$ is continuous (here: $s$) and any component is of finite variation (again $s$), the quadratic variation is zero.
The same logic applies to $[X,s]$. When we applied the conditional expectation, we used the fact that given $(t,x)$ we know the term $V(t,x)$ (i.e. it is $\mathcal{F}_t$-measurable), so we can bring it outside of the conditional expectation operator. Sufficient integrability means that $V_x \sigma^u$ needs to be bounded so that we get a martingale with expectation zero in our case. Plugin this result back into inequality (\ref{eq:star}) from before gives us: 

\begin{align*}
 V(t, x) &\geq \mathbb{E}_{t,x}\left[\int_t^{t+h} F(s, X_s^u, u_s) + V(t+h, X_{t+h}^u)\right]  \\
 & =\mathbb{E}_{t,x}\left[\int_t^{t+h} F(s, X_s^u, u_s) + \mathbb{E}_{t,x}[V(t+h, X_{t+h}^u)]\right] \\
 V(t, x) &\geq \mathbb{E}_{t,x}\left[\int_t^{t+h} F(.)ds + V(t, x) + \mathbb{E}_{t,x}\left[ \int_t^{t+h}V_s(s, X_s^u) + \mathcal{L}^uV(s,X_s^u)ds\right]\right] \\
 0 &\geq \mathbb{E}_{t,x}\left[\int_t^{t+h} F(.)ds  + V_s(s, X_s^u) + \mathcal{L}^uV(s,X_s^u)ds\right].
 \end{align*}
 Dividing by $h$ and taking limits yields:
 \begin{align*}
 0 & \geq \lim_{h\to 0} \frac{1}{h}\mathbb{E}_{t,x}\left[\int_t^{t+h} F(.)ds  + V_s(s, X_s^u) + \mathcal{L}^uV(s,X_s^u)ds\right].
 \end{align*}
Assuming we can interchange limits and expectation gives us:
\begin{align*}
0 &\geq \mathbb{E}_{t,x}\left[ \lim_{h\to0} \frac{1}{h}\int_t^{t+h} F(.)ds  + V_s(s, X_s^u) + \mathcal{L}^uV(s,X_s^u)ds ds\right].
\end{align*}
By the fundamental theorem of calculus we get:
\begin{align*}
0 &\geq F(t, x, u) + \frac{\partial}{\partial t}V(t,x) + \mathcal{L}^u V(t,x).
\end{align*}

\noindent
Since $u$ was arbitrary, the above inequality holds for all $u \in \mathcal{U}$ and we have equality if and only if $u = u^*$:
\begin{equation}
  \label{hamilton}
  0 = \frac{\partial}{\partial t}V(t,x) + \sup\{ F(t, x, u) + \mathcal{L}^u V(t, x)\}
\end{equation} 
with boundary condition $$V(T, x) = \Phi(x), ~\forall x \in \mathbb{R}^n.$$
The partial differential equation (\ref{hamilton}) is called \textit{Hamilton-Jacobi-Bellman equation}.

\subsection{Hamilton-Jacobi-Bellman equation}
\begin{theorem}{(Hamilton-Jacobi-Bellman equation)}
  Under Assumption \ref{assumption} the following holds:
  \begin{enumerate}
    \item V satisfies the HJB equation (\ref{hamilton}) with boundary condition $V(T, x) = \Phi(x), ~\forall x \in \mathbb{R}^n$.
    \item For each $(t, x) \in [0,T] \times \mathbb{R}^n$ the supremum in the HJBE is obtained by $u = u^*$.
  \end{enumerate}
\end{theorem}

\noindent
This means, that the optimal value function $V$ solves the Hamilton-Jacobi-Bellman equation, but not all functions that solve the HJBE need to be optimal. Solving the HJBE is therefore only necessary, but not sufficient for a solution to be optimal. However, the HJBE is also a sufficient condition for the optimal control problem in certain cases: This is known as the \textit{verification theorem} for dynamic programming. 

\begin{remark}
  Different Hamilton-Jacobi-Bellman equations need different verification theorems. For example, the HJBE associated with the optimal dividend problem is slightly different and requires a different verification theorem, which can be found e.g. in \cite{Schmidli08}. We continue to follow \cite{bjork09} and present a verification theorem for the HJBE in (\ref{hamilton}).
\end{remark}

\begin{theorem}{(Verification theorem)}
  Suppose we have $H(t,x)$ and $g(t,x)$ s.t.:
  \begin{itemize}
    \item $H$ is sufficiently integrable and solves the Hamilton-Jacobi-Bellman equation:
    \begin{align*}
    H_t(t,x) &+ \sup_{u \in \mathcal{U}}\{F(t,xu,) + \mathcal{L}^u H(t,x)\} = 0,~\forall (t,x) \in (0,T) \times \mathbb{R}^n\\
    H_T(T,x) &= \Phi(x),~\forall x \in \mathbb{R}
    \end{align*}
    \item $g$ is an admissible control law
    \item $\forall (t,x)$ the supremum in 
    $$\sup_{u \in \mathcal{U}}\{F(t,x,u) + \mathcal{L}^u H(t,x)\}$$
    is attained by $u = g(t,x)$.
  \end{itemize}
  Then the following holds:
  \begin{enumerate}
    \item The optimal value function $V$ to the control problem is given by
    $$V(t,x) = H(t,x).$$
    \item $\exists$ optimal control law $u^*$ s.t. $u^*(t,x) = g(t,x)$.
  \end{enumerate}
\end{theorem}
\begin{proof}
  Assume $H$ and $g$ are given as above. Choose some arbitrary $u \in \mathcal{U}$ and fix $(t,x)$. Define $X_t^u$ on $[t,T]$ as the solution to the stochastic differential equation:
  $$dX_s^u = \mu^u(s, X_s^u)ds + \sigma^u(s, X_s^u)dW_s,~X_t = x.$$
  Plugin this into $H$ and using Ito's formula we get:
  \begin{align*}
   H(T, X_T^u) = H(t,x) &+ \int_t^T \left[ \frac{\partial H}{\partial t}(s, X_s^u) + (\mathcal{L}^uH)(s,X_s^u)\right]ds \\
   &+ \int_t^T \nabla_x H(s,X_s^u)\sigma^u(s,X_s^u)dW_s. 
  \end{align*}
  Since $H$ solves the Hamilton-Jacobi-Bellman equation we get:
  $$\frac{\partial H}{\partial t}(s,X_s^u) + (\mathcal{L}^uH)(s,X_s^u) \leq -F^u(s, X_s^u)$$
  for all admissible $u$. Furthermore, from the boundary condition we know that $H(T, X_T^u) = \Phi(X_T^u)$ and therefore:
  \begin{align*}
    -H(t,x) &= -\Phi(X_t^u) + \overbrace{\int (.) ds}^{\leq -F^u(s, X_s^u)} + \int (.) dW_s \\
    -H(t,x) &\leq -\Phi(X_t^u) - \int_t^T F^u(s,X_s)ds + \int_t^T(.) dW_s \\
    H(t,x) &\geq \int_t^T F^u(s, X_s) ds + \Phi(X_T^u) + \int_t^T (.) dW_s\\
    \underbrace{\mathbb{E}_{t,x}(H(t,x))}_{=H(t,x)} &\geq \underbrace{\mathbb{E}_{t,x}\left[\int_t^T F^u(s, X_s^u)ds + \Phi(X_T^u) \right]}_{=V^u(t,x)} + \underbrace{\mathbb{E}_{t,x}\left[\int_t^T (.) dW_s\right]}_{=0 \text{ if } (.) \in \mathcal{L}^2}.
  \end{align*}
  Since $u$ was arbitrary we get:
  $$H(t,x) \geq \sup_{u \in \mathcal{U}}V^u(t,x) = V(t,x).$$
  To get $V(t,x) \leq H(t,x)$ and hence equality, we choose $u(t,x) = g(t,x)$. Repeating the calculations from above and using that by assumption we have that:
  $$\frac{\partial H}{\partial t}(t,x) + F^g(t,x) + \mathcal{L}^gH(t,x) = 0.$$
  We get:
  $$H(t,x) = \mathbb{E}_{t,x}\left[\int_t^T F^g(s, X_s^g)ds + \Phi(X_T^g)\right] = V^g(t,x).$$
  Since 
  $$H(t,x) \geq V(t,x) \geq V^g(t,x) = H(t,x),$$
  we are done. \qedhere
\end{proof}

## References
Björk, T (2009). *Arbitrage Theory in Continuous Time.* Oxford University Press 3 Third Edition