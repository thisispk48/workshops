# Pixels, Projections and Principal Components
### Linear Algebra at Work in Modern Image Processing

> **Audience:** MSc Big Data Analytics (BDA)  
> **Topic:** Linear Algebra at Work in Modern Image Processing

---

# Part 1: The Geometry of Projections

## 1.1 The Intuition: Projections as Shadows

Before looking at any formulas, imagine a physical setup:

A flashlight shines directly from above, perpendicular to a line or surface. An object or arrow floating in space casts a **shadow** onto that line or surface.

The **projection** is simply this shadow vector $\mathbf{p}$.

To construct any vector in physics or geometry, we only ever need two ingredients:
1. **Length:** How long is the shadow?
2. **Direction:** Which way does the shadow point?

$$\text{Projection Vector} = (\text{Length of Shadow}) \times (\text{Unit Direction})$$

---

## 1.2 Projecting a 2D Vector onto a 1D Line

Let $\mathbf{v}$ be a vector we want to project onto the line running along another vector $\mathbf{x}$.

<div align="center">

![2D Vector Projection](./assets/1_2_fig_vector_projection.png)

*Figure 1.2: Orthogonal projection of vector $\mathbf{v}$ onto vector $\mathbf{x}$, showing the perpendicular error line $\mathbf{e}$.*

👉 **[Open Interactive 2D Visualization in Browser](https://thisispk48.github.io/workshops/20260926_sju_26bda_pca/assets/1_2_fig_vector_projection.html)**

</div>

### Step A: Finding the Shadow Length

From basic right-triangle trigonometry:

$$\text{Shadow Length} = \|\mathbf{v}\| \cos(\theta)$$

Now recall the geometric definition of the **dot product**:

$$\mathbf{v} \cdot \mathbf{x} = \|\mathbf{v}\| \|\mathbf{x}\| \cos(\theta)$$

Notice that $\|\mathbf{v}\| \cos(\theta)$ is already sitting inside the dot product. The only extra term is $\|\mathbf{x}\|$. Therefore, dividing by the length of $\mathbf{x}$ isolates the exact shadow length:

$$\text{Shadow Length} = \frac{\mathbf{v} \cdot \mathbf{x}}{\|\mathbf{x}\|}$$

### Step B: Finding the Direction

The shadow lies on the line spanned by $\mathbf{x}$. To capture purely its direction without altering length, we normalize $\mathbf{x}$ into a **unit vector**:

$$\text{Unit Direction} = \frac{\mathbf{x}}{\|\mathbf{x}\|}$$

### Step C: Multiplying Length by Direction

Combine the two parts:

$$\mathbf{p} = \left( \frac{\mathbf{v} \cdot \mathbf{x}}{\|\mathbf{x}\|} \right) \left( \frac{\mathbf{x}}{\|\mathbf{x}\|} \right) = \left( \frac{\mathbf{v} \cdot \mathbf{x}}{\|\mathbf{x}\|^2} \right) \mathbf{x}$$

In matrix vector notation (with column vectors, where $\mathbf{v} \cdot \mathbf{x} = \mathbf{x}^T \mathbf{v}$ and $\|\mathbf{x}\|^2 = \mathbf{x}^T \mathbf{x}$):

$$\mathbf{p} = \left( \frac{\mathbf{x}^T \mathbf{v}}{\mathbf{x}^T \mathbf{x}} \right) \mathbf{x}$$

---

### Step D: Deriving the 1D Projection Matrix $\mathbf{P}$

We want a single matrix $\mathbf{P}$ such that multiplying any vector $\mathbf{v}$ by $\mathbf{P}$ immediately gives its projection:

$$\mathbf{p} = \mathbf{P} \mathbf{v}$$

Notice that the scalar term $(\mathbf{x}^T \mathbf{v})$ can be commuted:

$$\mathbf{p} = \frac{\mathbf{x} (\mathbf{x}^T \mathbf{v})}{\mathbf{x}^T \mathbf{x}} = \left[ \frac{\mathbf{x} \mathbf{x}^T}{\mathbf{x}^T \mathbf{x}} \right] \mathbf{v}$$

We have successfully factored out $\mathbf{v}$ to the right! The term in the brackets is our **Projection Matrix**:

$$\mathbf{P} = \frac{\mathbf{x} \mathbf{x}^T}{\mathbf{x}^T \mathbf{x}}$$

#### Dimension Check:
- **Numerator ($\mathbf{x} \mathbf{x}^T$):** $(n \times 1) \times (1 \times n) = (n \times n)$ **Matrix** (Outer product).
- **Denominator ($\mathbf{x}^T \mathbf{x}$):** $(1 \times n) \times (n \times 1) = (1 \times 1)$ **Scalar** (Inner / Dot product).
- If $\mathbf{x}$ is already a unit vector ($\|\mathbf{x}\| = 1$), then $\mathbf{x}^T \mathbf{x} = 1$, which simplifies to:

$$\mathbf{P} = \mathbf{x} \mathbf{x}^T$$

---

### Example 1.2.1: Projecting $\mathbf{v} = [2, 4]^T$ onto the $45^\circ$ Diagonal Line

Let the direction line be $\mathbf{x} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$ (the $45^\circ$ diagonal line $y = x$).

1. **Outer product matrix ($\mathbf{x}\mathbf{x}^T$):**
   $$\mathbf{x} \mathbf{x}^T = \begin{bmatrix} 1 \\ 1 \end{bmatrix} \begin{bmatrix} 1 & 1 \end{bmatrix} = \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}$$

2. **Squared length ($\mathbf{x}^T\mathbf{x}$):**
   $$\mathbf{x}^T \mathbf{x} = 1^2 + 1^2 = 2$$

3. **Projection Matrix $\mathbf{P}$:**
   $$\mathbf{P} = \frac{1}{2} \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix} = \begin{bmatrix} 0.5 & 0.5 \\ 0.5 & 0.5 \end{bmatrix}$$

4. **Calculate the Shadow Vector $\mathbf{p}$:**
   $$\mathbf{p} = \mathbf{P} \mathbf{v} = \begin{bmatrix} 0.5 & 0.5 \\ 0.5 & 0.5 \end{bmatrix} \begin{bmatrix} 2 \\ 4 \end{bmatrix} = \begin{bmatrix} 0.5(2) + 0.5(4) \\ 0.5(2) + 0.5(4) \end{bmatrix} = \begin{bmatrix} 3 \\ 3 \end{bmatrix}$$

5. **Calculate the Error Drop Line $\mathbf{e}$:**
   $$\mathbf{e} = \mathbf{v} - \mathbf{p} = \begin{bmatrix} 2 \\ 4 \end{bmatrix} - \begin{bmatrix} 3 \\ 3 \end{bmatrix} = \begin{bmatrix} -1 \\ 1 \end{bmatrix}$$

6. **Orthogonality Check:**
   - **Dot product check:** $\mathbf{x}^T \mathbf{e} = (1)(-1) + (1)(1) = 0$.
   - **Slope check:** Line $y = x$ has slope $m_1 = +1$. The drop line $\mathbf{e}$ has slope $m_2 = \frac{1}{-1} = -1$. Because $m_1 \times m_2 = -1$, the drop hits at exactly $90^\circ$!

<div align="center">

![Example 1.2.1 Projection](./assets/1_2_1_example_diagonal_projection.png)

*Example 1.2.1: Orthogonal projection of $\mathbf{v} = [2, 4]^T$ onto line $\mathbf{x} = [1, 1]^T$, yielding shadow $\mathbf{p} = [3, 3]^T$ and error $\mathbf{e} = [-1, 1]^T$.*

👉 **[Open Interactive Example 1.2.1 in Browser](https://thisispk48.github.io/workshops/20260926_sju_26bda_pca/assets/1_2_1_example_diagonal_projection.html)**

</div>

---

## 1.3 Abstracting Up: What Subspaces Can We Project Onto?

When we projected onto vector $\mathbf{x}$, we were really projecting onto the **1-dimensional subspace** (the infinite straight line) spanned by $\mathbf{x}$.

In any vector space, all valid linear subspaces must pass through the origin $(0, 0, \dots, 0)$.

### The Subspaces of 2D Space ($\mathbb{R}^2$):

| Dimension | Geometry | Description | Projection Matrix $\mathbf{P}$ |
| :--- | :--- | :--- | :--- |
| **0D** | **The Origin** | The single point $(0, 0)$ | $\mathbf{0} = \begin{bmatrix} 0 & 0 \\ 0 & 0 \end{bmatrix}$ *(total loss of info)* |
| **1D** | **Any Line through Origin** | Line spanned by direction $\mathbf{x}$ | $\mathbf{P} = \frac{\mathbf{x}\mathbf{x}^T}{\mathbf{x}^T\mathbf{x}}$ *(Rank 1 matrix)* |
| **2D** | **The Entire Plane** | The whole space $\mathbb{R}^2$ | $\mathbf{I} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$ *(zero loss of info)* |

In 2D, the only non-trivial projection is onto a 1D line. To see how multiple directions work together, we must step up into **3D space**.

---

## 1.4 Projecting a 3D Vector onto a 2D Plane

Imagine a vector $\mathbf{b}$ floating in 3-dimensional space above a flat tabletop (a 2D plane passing through the origin). We want to find its shadow $\mathbf{p}$ on the tabletop.

<div align="center">

![3D Plane Projection](./assets/1_4_fig_plane_projection_3d.png)

*Figure 1.4: Orthogonal projection of 3D vector $\mathbf{b}$ onto a 2D plane spanned by $\mathbf{a}_1$ and $\mathbf{a}_2$.*

👉 **[Open Interactive 3D Visualization in Browser](https://thisispk48.github.io/workshops/20260926_sju_26bda_pca/assets/1_4_fig_plane_projection_3d.html)** *(Rotate, zoom, and inspect in full 3D)*

</div>

### Fact 1: Any vector on the plane is a combination of basis vectors

A 2D plane requires **two linearly independent direction vectors**, $\mathbf{a}_1$ and $\mathbf{a}_2$. We stack them as columns of a matrix $\mathbf{A}$:

$$\mathbf{A} = \begin{bmatrix} \mathbf{a}_1 & \mathbf{a}_2 \end{bmatrix} \quad (\text{shape: } 3 \times 2)$$

Because the projection $\mathbf{p}$ lives on the plane, it must be some linear combination of the columns of $\mathbf{A}$:

$$\mathbf{p} = \hat{x}_1 \mathbf{a}_1 + \hat{x}_2 \mathbf{a}_2 = \mathbf{A} \mathbf{\hat{x}}$$

where $\mathbf{\hat{x}} = \begin{bmatrix} \hat{x}_1 \\ \hat{x}_2 \end{bmatrix}$ is the coordinate vector of weights we must determine.

---

### Fact 2: The drop line (error vector) must hit at 90 degrees

The connection line from the tip of $\mathbf{b}$ down to the projection $\mathbf{p}$ is the **error vector** $\mathbf{e}$:

$$\mathbf{e} = \mathbf{b} - \mathbf{p} = \mathbf{b} - \mathbf{A} \mathbf{\hat{x}}$$

For $\mathbf{p}$ to be the closest point on the plane to $\mathbf{b}$, the drop line $\mathbf{e}$ must hit perpendicular ($90^\circ$) to the **entire plane**.

That means $\mathbf{e}$ must be orthogonal to **both** direction vectors spanning the plane:

$$\mathbf{a}_1 \cdot \mathbf{e} = 0 \implies \mathbf{a}_1^T \mathbf{e} = 0$$

$$\mathbf{a}_2 \cdot \mathbf{e} = 0 \implies \mathbf{a}_2^T \mathbf{e} = 0$$

Stack these two equations together:

$$\begin{bmatrix} \mathbf{a}_1^T \\ \mathbf{a}_2^T \end{bmatrix} \mathbf{e} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$$

Notice that the stacked matrix is simply $\mathbf{A}^T$! This yields the **fundamental orthogonality condition**:

$$\mathbf{A}^T \mathbf{e} = \mathbf{0}$$

---

### Fact 3: Solving for the weights $\mathbf{\hat{x}}$ (The Normal Equations)

Substitute $\mathbf{e} = \mathbf{b} - \mathbf{A} \mathbf{\hat{x}}$ into the orthogonality condition:

$$\mathbf{A}^T (\mathbf{b} - \mathbf{A} \mathbf{\hat{x}}) = \mathbf{0}$$

$$\mathbf{A}^T \mathbf{b} - \mathbf{A}^T \mathbf{A} \mathbf{\hat{x}} = \mathbf{0}$$

$$(\mathbf{A}^T \mathbf{A}) \mathbf{\hat{x}} = \mathbf{A}^T \mathbf{b}$$

Because the columns of $\mathbf{A}$ are linearly independent, the symmetric square matrix $(\mathbf{A}^T \mathbf{A})$ (size $2 \times 2$) is invertible. Multiply both sides by $(\mathbf{A}^T \mathbf{A})^{-1}$:

$$\mathbf{\hat{x}} = (\mathbf{A}^T \mathbf{A})^{-1} \mathbf{A}^T \mathbf{b}$$

---

### Fact 4: Extracting the Master Projection Matrix $\mathbf{P}$

Recall that the projection vector is $\mathbf{p} = \mathbf{A} \mathbf{\hat{x}}$. Substituting our solution for $\mathbf{\hat{x}}$:

$$\mathbf{p} = \mathbf{A} \left[ (\mathbf{A}^T \mathbf{A})^{-1} \mathbf{A}^T \mathbf{b} \right]$$

Grouping the matrices together:

$$\mathbf{p} = \left[ \mathbf{A} (\mathbf{A}^T \mathbf{A})^{-1} \mathbf{A}^T \right] \mathbf{b}$$

This reveals the **Master Projection Matrix Formula**:

$$\mathbf{P} = \mathbf{A} (\mathbf{A}^T \mathbf{A})^{-1} \mathbf{A}^T$$

#### Dimension Verification (in 3D):
$$\mathbf{P} = \underbrace{\mathbf{A}}_{3 \times 2} \, \underbrace{(\mathbf{A}^T \mathbf{A})^{-1}}_{2 \times 2} \, \underbrace{\mathbf{A}^T}_{2 \times 3} = (3 \times 3) \text{ Matrix}$$

Multiplying $(3 \times 3) \mathbf{P}$ by $(3 \times 1) \mathbf{b}$ yields the $(3 \times 1)$ projected vector $\mathbf{p}$.

---

### Special Case: Orthonormal Basis Vectors

If the directions spanning the subspace are chosen to be **mutually perpendicular and unit length** ($\mathbf{q}_1, \mathbf{q}_2$, forming matrix $\mathbf{Q}$), then:

$$\mathbf{Q}^T \mathbf{Q} = \mathbf{I}$$

The inverse term $(\mathbf{Q}^T \mathbf{Q})^{-1}$ disappears entirely, leaving:

$$\mathbf{P} = \mathbf{Q} \mathbf{Q}^T = \mathbf{q}_1 \mathbf{q}_1^T + \mathbf{q}_2 \mathbf{q}_2^T$$

> **Key Takeaway:** Projecting onto an orthonormal subspace is simply the **sum of individual 1D projections** onto each basis vector!

---

## 1.5 Master Taxonomy: All Projections in 2D & 3D Vector Spaces

Here is the complete taxonomy of all possible linear subspace projections in 2D and 3D:

| Vector Space | Subspace Dimension | Geometric Subspace | Basis Matrix $\mathbf{A}$ | Projection Matrix $\mathbf{P}$ | Rank of $\mathbf{P}$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **2D ($\mathbb{R}^2$)** | **0D** | Origin $(0, 0)$ | None | $\mathbf{0}_{2 \times 2}$ | 0 |
| | **1D** | Line through origin | Column $\mathbf{x} \in \mathbb{R}^{2 \times 1}$ | $\frac{\mathbf{x}\mathbf{x}^T}{\mathbf{x}^T\mathbf{x}}$ | 1 |
| | **2D** | Entire 2D space | $\mathbf{I}_{2 \times 2}$ | $\mathbf{I}_{2 \times 2}$ | 2 |
| **3D ($\mathbb{R}^3$)** | **0D** | Origin $(0, 0, 0)$ | None | $\mathbf{0}_{3 \times 3}$ | 0 |
| | **1D** | Line through origin | Column $\mathbf{a} \in \mathbb{R}^{3 \times 1}$ | $\frac{\mathbf{a}\mathbf{a}^T}{\mathbf{a}^T\mathbf{a}}$ | 1 |
| | **2D** | Plane through origin | $\mathbf{A} = [\mathbf{a}_1, \mathbf{a}_2] \in \mathbb{R}^{3 \times 2}$ | $\mathbf{A}(\mathbf{A}^T\mathbf{A})^{-1}\mathbf{A}^T$ | 2 |
| | **3D** | Entire 3D space | $\mathbf{I}_{3 \times 3}$ | $\mathbf{I}_{3 \times 3}$ | 3 |

---

## 1.6 The Three Universal Properties of Any Projection Matrix

Regardless of whether you project in 2D, 3D, or 100D, every orthogonal projection matrix $\mathbf{P}$ satisfies three immutable laws:

### 1. Symmetry
$$\mathbf{P}^T = \mathbf{P}$$
*(The matrix is equal to its own transpose).*

### 2. Idempotency (Repeat Projections Do Nothing)
$$\mathbf{P}^2 = \mathbf{P} \mathbf{P} = \mathbf{P}$$
*Intuition: Once you drop the shadow onto the floor, shining the light on the shadow a second time leaves it in the exact same spot.*

### 3. The Complement Projector (The Error Vector)
$$(\mathbf{I} - \mathbf{P})$$
*Intuition: If $\mathbf{P}$ projects onto the subspace, then $(\mathbf{I} - \mathbf{P})$ is also a projection matrix that projects onto the **perpendicular (orthogonal) complement**.*

$$\mathbf{p} = \mathbf{P} \mathbf{b} \quad (\text{the shadow})$$

$$\mathbf{e} = (\mathbf{I} - \mathbf{P}) \mathbf{b} = \mathbf{b} - \mathbf{P}\mathbf{b} \quad (\text{the perpendicular drop line})$$

$$\text{Total Vector} = \mathbf{p} + \mathbf{e} = \mathbf{P}\mathbf{b} + (\mathbf{I} - \mathbf{P})\mathbf{b} = \mathbf{b}$$

---

# Part 2: The Geometry of Eigenvalues and Eigenvectors

In Part 1, we learned how to project vectors onto a subspace once the direction was already given to us. But in real-world data, **who chooses the direction?**

To find the natural axes of our data, we must understand how matrices deform space.

---

## 2.1 What is a Linear Transformation? (The Axiomatic View)

For absolute visual clarity, we focus on **$2 \times 2$ matrices** acting on 2-dimensional space ($\mathbb{R}^2 \to \mathbb{R}^2$).

A matrix $\mathbf{M}$ is not just a table of numbers—it is a **transformation machine**. You feed it an input vector $\mathbf{v} \in \mathbb{R}^2$, and it outputs a transformed vector $\mathbf{M}\mathbf{v} \in \mathbb{R}^2$.

To be a **linear transformation**, the operation must satisfy two strict axioms:

1. **Additivity:**
   $$T(\mathbf{u} + \mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v})$$
   *(Transforming the sum of two vectors is the same as transforming them individually and then adding).*

2. **Homogeneity (Scaling):**
   $$T(c\mathbf{v}) = cT(\mathbf{v})$$
   *(Scaling a vector by $c$ scales its output by $c$).*

### The Axiomatic Consequence: $T(\mathbf{0}) = \mathbf{0}$
From homogeneity, setting scalar $c = 0$:

$$T(\mathbf{0}) = T(0 \cdot \mathbf{v}) = 0 \cdot T(\mathbf{v}) = \mathbf{0}$$

> **Key Geometric Rule:** Under any linear transformation, **the origin is permanently anchored**. It can never move, shift, or translate!

- **Specific ($\mathbb{R}^2 \to \mathbb{R}^2, 2 \times 2$):**  
  For complete visual intuition, we explore $2 \times 2$ matrices transforming points in the 2D plane:
  $$\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix}$$
  The 2D origin $(0, 0)$ remains anchored at $(0, 0)$. Grid lines remain straight and parallel.

- **Generic ($\mathbb{R}^n \to \mathbb{R}^n, n \times n$):**  
  Any square matrix $\mathbf{M} \in \mathbb{R}^{n \times n}$ defines an operator $T: \mathbb{R}^n \to \mathbb{R}^n$ via matrix-vector multiplication $\mathbf{y} = \mathbf{M}\mathbf{x}$. The $n$-dimensional zero vector is permanently anchored:
  $$T(\mathbf{0}_n) = \mathbf{M}\mathbf{0}_n = \mathbf{0}_n$$
  Lines, planes, and flat hyperplanes in $\mathbb{R}^n$ remain straight and evenly spaced under any linear transformation; space is never bent or curved.

---

## 2.2 Visualizing Transformations: The 4-Quadrant Benchmark Grid in $\mathbb{R}^2$

To observe how different matrices deform space, we establish a **standard benchmark**: a symmetric lattice of 25 points spanning **all 4 quadrants**:

$$(x, y) \in \{-2, -1, 0, 1, 2\} \times \{-2, -1, 0, 1, 2\}$$

This forms a neat $2 \times 2$ cluster in each of the 4 quadrants, plus the axes and the origin.

### The Side-by-Side Visual Setup:
Every transformation figure below is laid out as two matching panels:
- **Left Panel (Input Space $\mathbb{R}^2$):** Shows the original benchmark grid and 5 specifically tracked test vectors.
- **Right Panel (Output Space $\mathbb{R}^2$):** Shows the deformed grid and where those exact 5 vectors land after transformation $\mathbf{M}\mathbf{v}$.

### The 5 Specifically Tracked Vectors:
In every chart, we track the exact same 5 vectors using **identical colors** on both the Left and Right panels so you can visually verify which vectors changed direction and which vectors maintained their span:

1. 🔵 **$\mathbf{e}_1 = [1, 0]^T$ (Medium Blue):** Standard basis vector along the X-axis.
2. 🔷 **$\mathbf{e}_2 = [0, 1]^T$ (Light Blue):** Standard basis vector along the Y-axis.
3. 🟦 **$\mathbf{d} = [1, 1]^T$ (Dark Navy Blue):** Diagonal benchmark vector.
4. 🔴 **Eigenvector 1 (Red):** The first invariant vector (corresponding to $\lambda_1$).
5. 🟢 **Eigenvector 2 (Green):** The second invariant vector (corresponding to $\lambda_2$).

---

## 2.3 The Origin of "Eigen": Invariant Lines and Eigenspaces

Consider the simplest transformation: the **diagonal matrix** $\mathbf{D}$:

$$\mathbf{D} = \begin{bmatrix} 3 & 0 \\ 0 & 2 \end{bmatrix}$$

Multiplying any point $\begin{bmatrix} x \\ y \end{bmatrix}$ by $\mathbf{D}$ scales the horizontal coordinate by $3\times$ and the vertical coordinate by $2\times$:

$$\mathbf{D} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 3x \\ 2y \end{bmatrix}$$

<div align="center">

![Figure 2.3 Diagonal Transformation](./assets/2_3_fig_diagonal_transform.png)

*Figure 2.3: Side-by-side transformation by diagonal matrix $\mathbf{D} = \begin{bmatrix} 3 & 0 \\ 0 & 2 \end{bmatrix}$. Left: Input Space. Right: Transformed Output Space. Both panels feature the neutral grey benchmark grid and tick intervals of 1. Notice how $\mathbf{e}_1$ (Medium Blue) and $\mathbf{e}_2$ (Light Blue) maintain their direction along the red and green eigenspaces, while the diagonal vector $\mathbf{d}$ (Dark Navy Blue) tilts.*

👉 **[Open Interactive Figure 2.3 in Browser](https://thisispk48.github.io/workshops/20260926_sju_26bda_pca/assets/2_3_fig_diagonal_transform.html)**

</div>

### Tracking our 5 vectors under $\mathbf{D}$:
1. 🔵 $\mathbf{e}_1 = [1, 0]^T$ (Medium Blue) $\to \mathbf{D}\mathbf{e}_1 = [3, 0]^T$: **Direction strictly preserved!** Stretched by $3\times$ along the X-axis (Eigenspace 1 line $y = 0$, $\lambda_1 = 3$).
2. 🔷 $\mathbf{e}_2 = [0, 1]^T$ (Light Blue) $\to \mathbf{D}\mathbf{e}_2 = [0, 2]^T$: **Direction strictly preserved!** Stretched by $2\times$ along the Y-axis (Eigenspace 2 line $x = 0$, $\lambda_2 = 2$).
3. 🟦 $\mathbf{d} = [1, 1]^T$ (Dark Navy Blue) $\to \mathbf{D}\mathbf{d} = [3, 2]^T$: **Direction changed!** Slope changed from $1$ to $\frac{2}{3}$.

### The Big Lesson:
> An **Eigenvector** is a vector that **retains its directional span (line of action)** under a linear transformation:
> 
> $$\mathbf{M} \mathbf{v} = \lambda \mathbf{v}$$
> 
> When transformed by $\mathbf{M}$, the vector **does not change its direction**—it is purely scaled by the scalar factor $\lambda$ (the **Eigenvalue**).

- **Specific ($\mathbb{R}^2 \to \mathbb{R}^2, 2 \times 2$):**  
  An eigenvector defines an invariant 1-dimensional straight line through the origin ($y = mx$). Every point on that line stays on that line, simply scaled by $\lambda$. In our $2 \times 2$ diagonal example, the two eigenspaces are the X-axis ($y = 0$, $\lambda_1 = 3$) and the Y-axis ($x = 0$, $\lambda_2 = 2$).

- **Generic ($\mathbb{R}^n \to \mathbb{R}^n, n \times n$):**  
  For any operator $\mathbf{M} \in \mathbb{R}^{n \times n}$, an eigenvalue $\lambda$ corresponds to an entire **Eigenspace** $E_\lambda$, defined as the null space of $(\mathbf{M} - \lambda\mathbf{I})$:
  $$E_\lambda = \text{null}(\mathbf{M} - \lambda\mathbf{I}) = \{\mathbf{v} \in \mathbb{R}^n : \mathbf{M}\mathbf{v} = \lambda\mathbf{v}\}$$
  This is a linear subspace of dimension $1 \le k \le n$ (the geometric multiplicity). In $\mathbb{R}^3$, an eigenspace can be an invariant line or an invariant plane; in $\mathbb{R}^n$, it is an invariant $k$-dimensional hyperplane. Every vector in $E_\lambda$ scales by the exact same factor $\lambda$.

---

## 2.4 Tilted Eigenvectors: The Non-Diagonal Matrix

In the diagonal matrix above, the eigenvectors conveniently coincided with the familiar X and Y axes. But what happens in a general **non-diagonal matrix**?

To explore this, consider the matrix $\mathbf{A}$:

$$\mathbf{A} = \begin{bmatrix} 1 & 1 \\ -2 & 4 \end{bmatrix}$$

Here, the eigenvalues and eigenvectors are not obvious just by looking at the numbers. We need a general method to discover them.

---

### Step 1: Setting up the Equation (The "How")

By definition, we are searching for a non-zero vector $\mathbf{v}$ and a scalar $\lambda$ such that:

$$\mathbf{A}\mathbf{v} = \lambda\mathbf{v}$$

Move everything to the left side:

$$\mathbf{A}\mathbf{v} - \lambda\mathbf{v} = \mathbf{0}$$

We want to factor out vector $\mathbf{v}$. However, we cannot directly subtract a scalar number $\lambda$ from a matrix $\mathbf{A}$. To fix this, we insert the Identity matrix $\mathbf{I}$ (since $\lambda\mathbf{v} = \lambda\mathbf{I}\mathbf{v}$):

$$(\mathbf{A} - \lambda\mathbf{I})\mathbf{v} = \mathbf{0}$$

---

### Step 2: Why Must the Determinant Equal Zero? (The "Why")

Let $\mathbf{B} = (\mathbf{A} - \lambda\mathbf{I})$. Our equation is now:

$$\mathbf{B}\mathbf{v} = \mathbf{0}$$

Notice the fundamental dilemma:
- If $\mathbf{v} = \mathbf{0}$, the equation is trivially true ($\mathbf{B}\mathbf{0} = \mathbf{0}$). But the zero vector has no direction—it tells us nothing about space (the **trivial solution**).
- We demand a **real, non-zero vector** ($\mathbf{v} \ne \mathbf{0}$) that satisfies the equation.

**What does it mean geometrically when a matrix squashes a non-zero vector down into $(0, 0)$?**
It means the matrix **collapses space!** It squashes 2-dimensional area down into a 1-dimensional line (or point).

- The **determinant** measures how much a matrix scales area. If 2D space is crushed into a 1D line, its 2D area becomes **zero**!
- If $\det(\mathbf{B}) \ne 0$, the matrix $\mathbf{B}$ would be invertible, which would force $\mathbf{v} = \mathbf{B}^{-1}\mathbf{0} = \mathbf{0}$ (only the useless zero solution would exist).
- Therefore, for a non-zero eigenvector to exist, the matrix **must collapse space**:

$$\det(\mathbf{A} - \lambda\mathbf{I}) = 0 \quad \text{(The Characteristic Equation)}$$

---

### Step 3: The Characteristic Equation

- **Specific ($\mathbb{R}^2 \to \mathbb{R}^2, 2 \times 2$):**  
  For any general $2 \times 2$ matrix $\mathbf{A} = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$:
  $$\det\begin{bmatrix} a - \lambda & b \\ c & d - \lambda \end{bmatrix} = (a - \lambda)(d - \lambda) - bc = 0$$
  $$\lambda^2 - (a + d)\lambda + (ad - bc) = 0$$
  Notice the two fundamental matrix invariants that appear naturally:
  1. **The Trace:** $\text{Tr}(\mathbf{A}) = a + d$ (sum of diagonal entries)
  2. **The Determinant:** $\det(\mathbf{A}) = ad - bc$
  
  This yields the universal $2 \times 2$ characteristic formula:
  $$\lambda^2 - \text{Tr}(\mathbf{A})\lambda + \det(\mathbf{A}) = 0$$
  where $\lambda_1 + \lambda_2 = \text{Tr}(\mathbf{A})$ and $\lambda_1 \lambda_2 = \det(\mathbf{A})$.

- **Generic ($\mathbb{R}^n \to \mathbb{R}^n, n \times n$):**  
  For any $n \times n$ matrix $\mathbf{A} \in \mathbb{R}^{n \times n}$, expanding $\det(\mathbf{A} - \lambda\mathbf{I}) = 0$ yields an **$n$-th degree characteristic polynomial** in $\lambda$:
  $$p(\lambda) = (-1)^n \lambda^n + (-1)^{n-1}\text{Tr}(\mathbf{A})\lambda^{n-1} + \dots + \det(\mathbf{A}) = 0$$
  By the Fundamental Theorem of Algebra, it has exactly $n$ roots (eigenvalues $\lambda_1, \lambda_2, \dots, \lambda_n$, counted with algebraic multiplicity). The trace and determinant invariant identities generalize universally to $\mathbb{R}^n$:
  $$\sum_{i=1}^n \lambda_i = \text{Tr}(\mathbf{A}) = \sum_{i=1}^n A_{ii}, \qquad \prod_{i=1}^n \lambda_i = \det(\mathbf{A})$$

---

### Step 4: Applying the Machinery to Our Example

Now we can solve our non-diagonal matrix $\mathbf{A} = \begin{bmatrix} 1 & 1 \\ -2 & 4 \end{bmatrix}$:

1. **Calculate Trace & Determinant:**
   - $\text{Tr}(\mathbf{A}) = 1 + 4 = 5$
   - $\det(\mathbf{A}) = (1)(4) - (1)(-2) = 4 + 2 = 6$

2. **Characteristic Equation:**
   $$\lambda^2 - 5\lambda + 6 = 0$$
   $$(\lambda - 3)(\lambda - 2) = 0 \implies \lambda_1 = 3, \quad \lambda_2 = 2$$

3. **Finding the Direction Lines (Eigenvectors):**  
   Substitute each $\lambda$ back into $(\mathbf{A} - \lambda\mathbf{I})\mathbf{v} = \mathbf{0}$. Because the matrix collapsed space, the two row equations are redundant multiples of each other—they reduce to a single invariant line:

   - **For $\lambda_1 = 3$:**
     $$\begin{bmatrix} 1 - 3 & 1 \\ -2 & 4 - 3 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} -2 & 1 \\ -2 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$$
     Both rows state: $-2x + y = 0 \implies y = 2x$.  
     Any vector along the line $y = 2x$ is an eigenvector! We choose the simple integer representative:
     $$\mathbf{v}_1 = \begin{bmatrix} 1 \\ 2 \end{bmatrix} \quad (\text{Eigenvalue } \lambda_1 = 3)$$

   - **For $\lambda_2 = 2$:**
     $$\begin{bmatrix} 1 - 2 & 1 \\ -2 & 4 - 2 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} -1 & 1 \\ -2 & 2 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$$
     Both rows state: $-x + y = 0 \implies y = x$.  
     Any vector along the line $y = x$ is an eigenvector:
     $$\mathbf{v}_2 = \begin{bmatrix} 1 \\ 1 \end{bmatrix} \quad (\text{Eigenvalue } \lambda_2 = 2)$$

<div align="center">

![Figure 2.4 Non-Diagonal Transformation](./assets/2_4_fig_nondiagonal_transform.png)

*Figure 2.4: Side-by-side transformation by non-diagonal matrix $\mathbf{A} = \begin{bmatrix} 1 & 1 \\ -2 & 4 \end{bmatrix}$. Notice where each of the 5 vectors land. Eigenvectors $\mathbf{v}_1$ (Red) and $\mathbf{v}_2$ (Green) strictly preserve their directional lines, but are NOT perpendicular ($\theta \approx 18.4^\circ$).*

👉 **[Open Interactive Figure 2.4 in Browser](https://thisispk48.github.io/workshops/20260926_sju_26bda_pca/assets/2_4_fig_nondiagonal_transform.html)**

</div>

### Tracking our 5 vectors under $\mathbf{A}$:
1. 🔵 $\mathbf{e}_1 = [1, 0]^T$ (Medium Blue) $\to \mathbf{A}\mathbf{e}_1 = [1, -2]^T$: **Direction changed!**
2. 🔷 $\mathbf{e}_2 = [0, 1]^T$ (Light Blue) $\to \mathbf{A}\mathbf{e}_2 = [1, 4]^T$: **Direction changed!**
3. 🟦 $\mathbf{d} = [1, 1]^T$ (Dark Navy Blue) $\to \mathbf{A}\mathbf{d} = [2, 2]^T$: Lands on line $y = x$ (coincides with $\mathbf{v}_2$).
4. 🔴 $\mathbf{v}_1 = [1, 2]^T$ (Red) $\to \mathbf{A}\mathbf{v}_1 = [3, 6]^T$: **Direction strictly preserved on line $y = 2x$!** Stretched by $\lambda_1 = 3\times$.
5. 🟢 $\mathbf{v}_2 = [1, 1]^T$ (Green) $\to \mathbf{A}\mathbf{v}_2 = [2, 2]^T$: **Direction strictly preserved on line $y = x$!** Stretched by $\lambda_2 = 2\times$.

### The Critical Eye-Opener:
Look at the angle between the two eigenvectors:

$$\mathbf{v}_1 \cdot \mathbf{v}_2 = (1)(1) + (2)(1) = 3 \ne 0$$

$$\cos(\theta) = \frac{\mathbf{v}_1 \cdot \mathbf{v}_2}{\|\mathbf{v}_1\| \|\mathbf{v}_2\|} = \frac{3}{\sqrt{5}\sqrt{2}} = \frac{3}{\sqrt{10}} \approx 0.9487 \implies \theta \approx 18.4^\circ$$

> **Key Insight:** In general non-diagonal matrices, eigenvectors are **tilted** away from the standard axes, but they are **NOT orthogonal ($90^\circ$)**. The transformation shears space along non-perpendicular directions.

---

## 2.5 The Power of Symmetry: Strictly Orthogonal Eigenvectors

Now consider a **symmetric matrix** $\mathbf{S}$ (where $\mathbf{S}^T = \mathbf{S}$):

$$\mathbf{S} = \begin{bmatrix} 3 & 1 \\ 1 & 3 \end{bmatrix}$$

### Step 1: Characteristic Equation (Using Trace & Determinant)
For $\mathbf{S} = \begin{bmatrix} 3 & 1 \\ 1 & 3 \end{bmatrix}$:
- $\text{Tr}(\mathbf{S}) = 3 + 3 = 6$
- $\det(\mathbf{S}) = (3)(3) - (1)(1) = 8$

Using our formula $\lambda^2 - \text{Tr}(\mathbf{S})\lambda + \det(\mathbf{S}) = 0$:

$$\lambda^2 - 6\lambda + 8 = 0 \implies (\lambda - 4)(\lambda - 2) = 0 \implies \lambda_1 = 4, \quad \lambda_2 = 2$$

### Step 2: Finding the Eigenvectors
- **For $\lambda_1 = 4$:**
  $$(\mathbf{S} - 4\mathbf{I})\mathbf{q}_1 = \begin{bmatrix} -1 & 1 \\ 1 & -1 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix} \implies y = x \implies \mathbf{q}_1 = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$$

- **For $\lambda_2 = 2$:**
  $$(\mathbf{S} - 2\mathbf{I})\mathbf{q}_2 = \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix} \implies y = -x \implies \mathbf{q}_2 = \begin{bmatrix} -1 \\ 1 \end{bmatrix}$$

<div align="center">

![Figure 2.5 Symmetric Transformation](./assets/2_5_fig_symmetric_transform.png)

*Figure 2.5: Side-by-side transformation by symmetric matrix $\mathbf{S} = \begin{bmatrix} 3 & 1 \\ 1 & 3 \end{bmatrix}$. Notice the $90^\circ$ right-angle marker in both panels: Eigenvectors $\mathbf{q}_1$ (Red) and $\mathbf{q}_2$ (Green) are STRICTLY PERPENDICULAR ($\mathbf{q}_1 \cdot \mathbf{q}_2 = 0$).*

👉 **[Open Interactive Figure 2.5 in Browser](https://thisispk48.github.io/workshops/20260926_sju_26bda_pca/assets/2_5_fig_symmetric_transform.html)**

</div>

### Tracking our 5 vectors under $\mathbf{S}$:
1. 🔵 $\mathbf{e}_1 = [1, 0]^T$ (Medium Blue) $\to \mathbf{S}\mathbf{e}_1 = [3, 1]^T$: **Direction changed!**
2. 🔷 $\mathbf{e}_2 = [0, 1]^T$ (Light Blue) $\to \mathbf{S}\mathbf{e}_2 = [1, 3]^T$: **Direction changed!**
3. 🟦 $\mathbf{d} = [1, 1]^T$ (Dark Navy Blue) $\to \mathbf{S}\mathbf{d} = [4, 4]^T$: Diagonal benchmark vector (coincides with $\mathbf{q}_1$).
4. 🔴 $\mathbf{q}_1 = [1, 1]^T$ (Red) $\to \mathbf{S}\mathbf{q}_1 = [4, 4]^T$: **Direction strictly preserved on line $y = x$!** Stretched by $\lambda_1 = 4\times$.
5. 🟢 $\mathbf{q}_2 = [-1, 1]^T$ (Green) $\to \mathbf{S}\mathbf{q}_2 = [-2, 2]^T$: **Direction strictly preserved on line $y = -x$!** Stretched by $\lambda_2 = 2\times$.

### The Miracle of Symmetry:
Look at the dot product between the eigenvectors:

$$\mathbf{q}_1 \cdot \mathbf{q}_2 = (1)(-1) + (1)(1) = 0$$

The angle between them is **exactly $90^\circ$** on both the input and output sides!

> **The Fundamental Discovery:**  
> While non-diagonal matrices have skewed eigenvectors, a **symmetric matrix always stretches space along mutually perpendicular ($90^\circ$) axes**. It produces a rigid, rotated orthogonal coordinate frame.

---

## 2.6 Special Properties of Symmetric Matrices

Symmetric matrices ($\mathbf{S}^T = \mathbf{S}$) possess fundamental mathematical properties that set them apart from all other square matrices:

### 1. All Eigenvalues are Real Numbers
- **Specific ($\mathbb{R}^2 \to \mathbb{R}^2, 2 \times 2$):**  
  For any $2 \times 2$ symmetric matrix $\mathbf{S} = \begin{bmatrix} a & b \\ b & c \end{bmatrix}$, the characteristic equation is $\lambda^2 - (a + c)\lambda + (ac - b^2) = 0$. Its discriminant is:
  $$\Delta = (a + c)^2 - 4(ac - b^2) = (a - c)^2 + 4b^2 \ge 0$$
  Because $\Delta$ is the sum of two squares, it is never negative. A $2 \times 2$ symmetric matrix can never yield complex or imaginary eigenvalues.
- **Generic ($\mathbb{R}^n \to \mathbb{R}^n, n \times n$):**  
  For any real symmetric matrix $\mathbf{S} \in \mathbb{R}^{n \times n}$, every eigenvalue is guaranteed to be a real number:
  $$\lambda_i \in \mathbb{R} \quad \forall i \in \{1, 2, \dots, n\}$$

---

### 2. Eigenvectors are Strictly Orthogonal
- **Specific ($\mathbb{R}^2 \to \mathbb{R}^2, 2 \times 2$):**  
  The two eigenvectors $\mathbf{q}_1$ and $\mathbf{q}_2$ are strictly perpendicular at $90^\circ$:
  $$\mathbf{q}_1 \cdot \mathbf{q}_2 = 0 \quad (\mathbf{q}_1 \perp \mathbf{q}_2)$$
  As demonstrated in Figure 2.5, the symmetric matrix stretches space along this rigid $90^\circ$ coordinate frame.
- **Generic ($\mathbb{R}^n \to \mathbb{R}^n, n \times n$):**  
  By the **Spectral Theorem**, eigenvectors corresponding to distinct eigenvalues of any symmetric matrix are always mutually orthogonal. Furthermore, even if eigenvalues repeat, one can always construct a complete orthonormal basis $\{\mathbf{q}_1, \mathbf{q}_2, \dots, \mathbf{q}_n\}$ spanning $\mathbb{R}^n$:
  $$\mathbf{q}_i \cdot \mathbf{q}_j = \delta_{ij} = \begin{cases} 1 & \text{if } i = j \\ 0 & \text{if } i \ne j \end{cases}$$

> **Side Note on Repeated Eigenvalues & Multiplicity:**  
> What happens if an eigenvalue repeats (e.g., $(\lambda - 3)^2 = 0$)?
> - **Algebraic Multiplicity (AM):** How many times a root $\lambda$ repeats in the characteristic polynomial.
> - **Geometric Multiplicity (GM):** The dimension of the eigenspace $\dim(\text{null}(\mathbf{S} - \lambda\mathbf{I}))$.
> - While general non-symmetric matrices can be "defective" ($\text{GM} < \text{AM}$, lacking enough independent eigenvectors), **symmetric matrices always satisfy $\mathbf{GM = AM}$**.
> - If an eigenvalue repeats $k$ times ($\text{AM} = k$), its eigenspace is guaranteed to be a full **$k$-dimensional subspace** where every single vector scales by $\lambda$. Within that $k$-dimensional subspace, one can always pick $k$ mutually perpendicular unit vectors (e.g., via Gram-Schmidt) to construct a full orthonormal basis spanning $\mathbb{R}^n$.

---

### 3. Rank of a Symmetric Matrix
Is the rank of a symmetric matrix guaranteed to equal its dimension? **No.**

- **Specific ($\mathbb{R}^2 \to \mathbb{R}^2, 2 \times 2$):**  
  For a $2 \times 2$ symmetric matrix:
  - **Rank 2 (Full Rank):** Both $\lambda_1 \ne 0$ and $\lambda_2 \ne 0$ (e.g., $\begin{bmatrix} 3 & 1 \\ 1 & 3 \end{bmatrix}$, $\lambda_1 = 4, \lambda_2 = 2$). The matrix is invertible and spans all of $\mathbb{R}^2$.
  - **Rank 1:** Exactly one eigenvalue is 0 (e.g., $\begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}$, $\lambda_1 = 2, \lambda_2 = 0$). Space collapses completely from 2D onto a 1D line.
  - **Rank 0:** Both eigenvalues are 0 (only the zero matrix $\mathbf{S} = \mathbf{0}$).
- **Generic ($\mathbb{R}^n \to \mathbb{R}^n, n \times n$):**  
  The rank of any symmetric matrix $\mathbf{S}$ is **strictly equal to the number of non-zero eigenvalues**:
  $$\text{rank}(\mathbf{S}) = r = \text{Count of } \{\lambda_i \ne 0\} \le n$$
  An $n \times n$ symmetric matrix is full rank ($r = n$) if and only if zero is not an eigenvalue.

---

### 4. Spectral Decomposition (Sum of Rank-1 Projections)
Because the eigenvectors form an orthonormal basis ($\mathbf{Q}^T \mathbf{Q} = \mathbf{I}$), any symmetric matrix $\mathbf{S}$ can be factored as $\mathbf{S} = \mathbf{Q} \mathbf{\Lambda} \mathbf{Q}^T$:

- **Specific ($\mathbb{R}^2 \to \mathbb{R}^2, 2 \times 2$):**  
  $$\mathbf{S} = \lambda_1 (\mathbf{q}_1 \mathbf{q}_1^T) + \lambda_2 (\mathbf{q}_2 \mathbf{q}_2^T)$$
  Each outer product $(\mathbf{q}_i \mathbf{q}_i^T)$ is an $n \times n$ matrix of **rank 1**—the exact 1D orthogonal projection matrix onto line $\text{span}(\mathbf{q}_i)$ from Section 1.2!
  - If $\mathbf{S}$ is **Full Rank** ($\text{rank} = 2$), $\mathbf{S}$ is a weighted sum of **two active rank-1 projection matrices**.
  - If $\mathbf{S}$ is **Rank 1** ($\lambda_2 = 0$), the second term vanishes, leaving $\mathbf{S} = \lambda_1 (\mathbf{q}_1 \mathbf{q}_1^T)$ as a single active rank-1 projection matrix.

- **Generic ($\mathbb{R}^n \to \mathbb{R}^n, n \times n$):**  
  For any symmetric $\mathbf{S} \in \mathbb{R}^{n \times n}$ with rank $r \le n$:
  $$\mathbf{S} = \sum_{i=1}^n \lambda_i (\mathbf{q}_i \mathbf{q}_i^T) = \sum_{i=1}^r \lambda_i (\mathbf{q}_i \mathbf{q}_i^T)$$
  where each $\mathbf{P}_i = \mathbf{q}_i \mathbf{q}_i^T$ is a **rank-1** orthogonal projector, satisfying $\mathbf{P}_i^2 = \mathbf{P}_i$ and $\mathbf{P}_i \mathbf{P}_j = \mathbf{0}$ for $i \ne j$.
  
  > **Key Geometric Takeaway:**  
  > Any symmetric matrix is nothing more than a **weighted linear combination of $r$ orthogonal rank-1 projection matrices**, where the weights are its non-zero eigenvalues!

---

### 5. Always Orthogonally Diagonalizable
- **Specific ($\mathbb{R}^2 \to \mathbb{R}^2, 2 \times 2$):**  
  $\mathbf{S} = \mathbf{Q}\mathbf{\Lambda}\mathbf{Q}^T$, where $\mathbf{Q}$ is a $2 \times 2$ rotation/reflection matrix.
- **Generic ($\mathbb{R}^n \to \mathbb{R}^n, n \times n$):**  
  Every symmetric matrix in $\mathbb{R}^{n \times n}$ is orthogonally diagonalizable ($\mathbf{Q}^T \mathbf{S} \mathbf{Q} = \mathbf{\Lambda}$). Unlike general matrices (which may lack enough eigenvectors or produce skewed, sheared axes), a symmetric matrix **never shears space**—it purely rotates the coordinate frame to line up with its eigenvectors and scales each perpendicular axis by $\lambda_i$.

