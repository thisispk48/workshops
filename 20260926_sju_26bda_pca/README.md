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
