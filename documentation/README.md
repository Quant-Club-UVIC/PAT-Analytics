# PAT-Analytics Documentation  
This document will provide all the math that is being used in PAT.
# Table of Contents
- [PAT-Analytics Documentation](#pat-analytics-documentation)
- [Table of Contents](#table-of-contents)
- [Basics](#basics)
  - [Setting Things Up](#setting-things-up)
  - [No Quantity](#no-quantity)
  - [Floating Weights](#floating-weights)
# Basics
## Setting Things Up  
Define  
$$
X = \{ \text{all positions(tradable instruments)} \}
$$  
We have a portfolio at time $t$, $P_t \subseteq X$, the set of positions one is holding at time $t$. So we can define  
$$
P : \mathbb{R_{\geq 0}} \to \mathbb{P}(X)  \\
t \mapsto P_t
$$  
Now, if we want to get  
Amount of **shares** of instrument $x \in X$ at time $t \in \mathbb{R_{\geq 0}}$:  
$$
q(x,t) \in \mathbb{R_{\geq 0}}
$$
We can define  $P_t = \{x \in X | q(x,t) \not = 0 \}$  
The **price** of instrument $x \in X$ at time $t$:  
$$
p(x,t) \in \mathbb{R_{\geq 0}}
$$  
We can define the **value** of an instrument $x \in X$ at time $t$:  
$$
V(x,t) = p(x,t) q(x,t)
$$  
Or the **total market value** of the portfolio $P_t$ as:
$$
V_p(t) = \sum_{i \in X} V(x,t)
$$ 
The **weight** of instrument $x \in X$ at time $t$:  
$$
w(x,t) = \dfrac{V(x,t)}{\sum_{i \in P_t} V(i,t)} \in \mathbb{R_{\geq 0}}
$$  
The **return** of instrument $x \in X$ from time $t$ to $t + \Delta t$  
$$
r(x,t) = \dfrac{p(x,t + \Delta t)}{p(x, t)} \in \mathbb{R_{\geq 0}}
$$  
The most convinient of these to work with is the $w$ and $r$. 


## No Quantity  
What do we do if the user does not specify the amount of shares of an instrument they have, but only their starting weight. Consider, 
$$
\begin{aligned}
    w(x, t_0) &= \dfrac{p(x, t_0)q(x, t_0)}{V_p(t_0)} \\
    \\
    q(x , t_0)&= \dfrac{w(x,t_0)  V_p(t_0)}{p(x, t_0)}
\end{aligned}
$$
So we can just set $V_p$ to some constant and solve!

## Floating Weights  
Sometimes users will only tell us what they want, $x$, their desired weight $w$, and how often they want to rebalance $\delta \in \mathbb{R_{\geq 0}}$, to a target weight $w_0 : X \to \mathbb{R_{\geq 0}}$. Note that 
$$
p(x, t + \Delta t) = p(x,t)r(x,t)
$$
Let $\Delta q_x = q(x, t + \Delta t) - q(x,t)$. So, 
$$
\begin{aligned}
V(x,t + \Delta t)   &= p(x,t + \Delta t)q(x,t + \Delta t)  \\
                    &= [p(x,t)r(x,t)][q(x,t) + \Delta q_x] \\
                    &= p(x,t)r(x,t)q(x,t) + p(x,t)r(x,t)\Delta q_x \\
                    &= V(x,t)r(x,t) + p(x,t)r(x,t)\Delta q_x
\end{aligned}
$$
So the way our weight changes with *no* rebalancing is
$$
\begin{aligned}
w(x, t + \Delta t) &= \dfrac{V(x,t + \Delta t)}{\sum_{i \in X} V(i, t + \Delta t)} \\
\\
    &= \dfrac{V(x,t)r(x,t) + p(x,t)r(x,t)\Delta q_x}{\sum_{i \in X} V(i,t)r(i,t) + p(i,t)r(i,t)\Delta q_i} \\
\\
    &= \dfrac{V(x,t)r(x,t) + p(x,t)r(x,t)\Delta q_x}{\sum_{i \in X} V(i,t)r(i,t) + \sum_{i \in X} p(i,t)r(i,t)\Delta q_i} \\
\end{aligned}
$$
If we do have rebalancing on this time step, then  
$$
\begin{aligned}
w(x, t + \Delta t) = w_0(x)
\end{aligned}
$$

