# Introduction
The total wind can be decomposed into geostrophic and ageostrophic components, with the latter responsible for the entire divergence of the total wind. 
Diagnosing the ageostrophic component is, therefore, essential for understanding atmospheric dynamics and weather evolution.
The diagnostic euqation of ageostropic wind is as follows:
$$
\vec{V_a} = \frac{1}{f} \vec{k} \times \frac{\partial \vec{V}}{\partial t} 
           + \frac{1}{f} \vec{k} \times \left[ (\vec{V} \cdot \nabla) \vec{V} \right] 
           + \frac{R \omega}{p f^2} \nabla_p T 
           - \frac{1}{f} \vec{k} \times \vec{F_h} 
           + \frac{1}{f} \vec{k} \times \left( \omega \frac{\partial \vec{V_a}}{\partial p} \right)
$$

# Steps
## data
u,v,w,z,t data on several pressure levels (3 at least), times (3 at least) and considerable lat lon range (big enough to separate 1000km scale)

## calculate Ageostropic Wind
## calculate terms

