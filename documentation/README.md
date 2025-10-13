# PAT-Analytics Documentation  
This document will provide all the math that is being used in PAT.
# Table of Contents
- [PAT-Analytics Documentation](#pat-analytics-documentation)
- [Table of Contents](#table-of-contents)
- [Basics](#basics)
  - [How to upload this document](#how-to-upload-this-document)
  - [Notation](#notation)
  - [Setting Things Up](#setting-things-up)
  - [No Quantity](#no-quantity)
  - [Floating Weights](#floating-weights)
    - [Case 1: *No Rebalancing*](#case-1-no-rebalancing)
    - [Case 2 : *Rebalancing*](#case-2--rebalancing)
# Basics  
## How to upload this document  
Github does not natively support KaTeX so we can't just upload this document :c . After editing  
## Notation
$$
\begin{aligned}
X &:= \{\text{all tradable instruments (universe)}\} \\
\\

\end{aligned}
$$
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
V(x,t) = p(x,t) q(x,t - \Delta t)
$$  
Since you will look at how much of an instrument you have at time $t - \Delta t$, multiply it by the current price, and recieve current value.  

Or the **total market value** of the portfolio $P_t$ as:
$$
V_p(t) = \sum_{i \in X} V(x,t)
$$ 
The **weight** of instrument $x \in X$ at time $t$:  
$$
w(x,t) = \dfrac{V(x,t)}{\sum_{i \in P_t} V(i,t)} \in \mathbb{R_{\geq 0}}
$$  
The **gross return** of instrument $x \in X$ from time $t$ to $t + \Delta t$  
$$
R(x,t) = \dfrac{p(x,t + \Delta t)}{p(x, t)} \in \mathbb{R_{\geq 0}}
$$  
Finally **net return** is  
$$
r(x,t) = \dfrac{p(x,t + \Delta t) - p(x,t)}{p(x, t)} = R(x,t) - 1\in \mathbb{R_{\geq 0}}
$$
The most convinient of these to work with is the $w$ and $R$. 


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
p(x, t + \Delta t) = p(x,t)R(x,t)
$$
Let $\Delta q_x = q(x, t + \Delta t) - q(x,t)$. So, 
$$
\begin{aligned}
V(x,t + \Delta t)   &= p(x,t + \Delta t)q(x,t + \Delta t)  \\
                    &= [p(x,t)R(x,t)][q(x,t) + \Delta q_x] \\
                    &= p(x,t)R(x,t)q(x,t) + p(x,t)R(x,t)\Delta q_x \\
                    &= V(x,t)R(x,t) + p(x,t)R(x,t)\Delta q_x 
\end{aligned}
$$
  
### Case 1: *No Rebalancing*  
If we do not rebalance, no buy or sell is happening, i.e $q(x,t) = q(x, t + \Delta t) \to \Delta q_x = 0$
$$
\begin{aligned}
w(x, t + \Delta t) &= \dfrac{V(x,t + \Delta t)}{\sum_{i \in X} V(i, t + \Delta t)} \\
\\
    &= \dfrac{V(x,t)R(x,t) + p(x,t)R(x,t)\Delta q_x}{\sum_{i \in X} V(i,t)R(i,t) + p(i,t)R(i,t)\Delta q_i} \\
\\
    &= \dfrac{V(x,t)R(x,t)}{\sum_{i \in X} V(i,t)R(i,t)} \\
\\
    &= \dfrac{w(x,t) V_p(t)R(x,t)}{\sum_{i \in X} w(i,t) V_p(t) R(i,t)} \\
\\
    &= \dfrac{w(x,t)R(x,t)}{\sum_{i \in X} w(i,t) R(i,t)}
\end{aligned}
$$
In conclusion, we evolve $w$ by time step $\Delta t$ by 
$$
\boxed{w(x, t + \Delta t) = \dfrac{w(x,t)R(x,t)}{\sum_{i \in X} w(i,t) R(i,t)}}
$$
### Case 2 : *Rebalancing*
If we do have rebalancing on this time step ($t + \Delta \equiv 0 (\text{mod } \delta)$), then we are going to be buying/selling shares. We will define target $V_p(t + \Delta t)$ based off of information at $V_p(t)$.  
$$
\begin{aligned}
V_p^{pre}(t + \Delta t) &= \sum_{i \in P_t} p_i(x, t + \Delta t)q(x, t) \\
\\
V_p^{post}(t + \Delta t) &= \sum_{i \in P_t} p_i(x, t + \Delta t)q(x, t + \Delta t) \\
\\
V_p(t + \Delta t) &= V_p^{post}(t + \Delta t)
\end{aligned}
$$
Now, 
$$
\begin{aligned}
w(x, t + \Delta t) &= w_0(x) \\
\end{aligned}
$$
Now, to update our quantity, set up the equation
$$
\begin{aligned}
\Delta q_x &= q(x, t + \Delta t) - q(x,t) \\
\\
&= \dfrac{w_0(x) V_p(t + \Delta t)}{p(x, t + \Delta t)} - \dfrac{w(x, t) V_p(x,t)}{p(x,t)} \\
\\
&= \dfrac{}{}
\end{aligned}
$$

