# Worked example: a Module deep-dive (Multi-Head Self-Attention)

Useful shape for a method subsection: architecture / data flow (when there is more than one moving part), then input/output, core formula, code, and design analysis. Use `<h4>` for deep-dive headings and bold paragraphs for named formula blocks.

Use either the paper's architecture figure or a Mermaid schematic. If the paper has a clean architecture figure, hoist it here with `anchor_section: "architecture"`. Use Mermaid when the paper has no usable figure, or when a simpler schematic teaches faster. The example below shows the Mermaid path.

```html
<h4>Architecture / data flow</h4>
<figure class="mermaid-figure">
  <pre class="mermaid">
flowchart LR
    X["Input X (n x d_model)"] --> QKV["Linear projection<br/>Q, K, V"]
    QKV --> H1["head 1<br/>scaled dot-product"]
    QKV --> H2["head 2"]
    QKV --> HH["head h"]
    H1 --> CAT["Concat heads"]
    H2 --> CAT
    HH --> CAT
    CAT --> WO["Output projection W_O"]
    WO --> Y["Output Y (n x d_model)"]
    classDef accent fill:#fff,stroke:#b8462e,stroke-width:2px
    class H1,H2,HH accent
  </pre>
  <figcaption>One input is projected into h independent head subspaces, each running scaled dot-product attention in parallel; their outputs are concatenated and mixed back to model width by W<sup>O</sup>.</figcaption>
</figure>
<p>Each head attends in its own subspace; the output projection recombines them. Because the h heads run in parallel and share the same total width, the module costs about the same as one full-width attention.</p>

<h4>Input / Output</h4>
<ul>
  <li>Input: \( X \in \mathbb{R}^{n \times d_\text{model}} \), a length-\(n\) sequence of \(d_\text{model}\)-dimensional tokens.</li>
  <li>Output: \( Y \in \mathbb{R}^{n \times d_\text{model}} \), same shape as the input.</li>
  <li>\(h\) heads, each of width \( d_k = d_v = d_\text{model} / h \), so total width is preserved.</li>
</ul>

<h4>Core formula</h4>

<p><strong>Per-head attention.</strong> Each head projects X into its own query/key/value subspace and runs scaled dot-product attention:</p>

\[ \text{head}_i = \text{softmax}\!\left(\frac{(X W_i^Q)(X W_i^K)^\top}{\sqrt{d_k}}\right)(X W_i^V) \]

<p>where:</p>
<ul>
  <li>\( W_i^Q, W_i^K \in \mathbb{R}^{d_\text{model} \times d_k} \), \( W_i^V \in \mathbb{R}^{d_\text{model} \times d_v} \): the per-head projection matrices that pick out head i's subspace.</li>
  <li>\( \sqrt{d_k} \): scaling that holds the dot-product variance near 1 (see the Why callout).</li>
</ul>
<p>Key point: heads are independent, so different heads can specialize (one tracks position, another tracks a syntactic relation), and they run in parallel.</p>

<p><strong>Concatenation and output projection.</strong> The h head outputs are concatenated and mixed back to model width:</p>

\[ \text{MultiHead}(X) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h)\, W^O \]

<p>where \( W^O \in \mathbb{R}^{h d_v \times d_\text{model}} \) recombines the per-head subspaces. Key point: because \( h \cdot d_k = d_\text{model} \), the whole module costs about the same as one full-width attention, so multiple heads are nearly free.</p>

<h4>Code implementation</h4>
<pre><code>import torch, torch.nn as nn, torch.nn.functional as F, math

class MultiHeadSelfAttention(nn.Module):
    def __init__(self, d_model, h):
        super().__init__()
        assert d_model % h == 0
        self.h, self.d_k = h, d_model // h
        self.qkv  = nn.Linear(d_model, 3 * d_model)   # W^Q, W^K, W^V stacked
        self.proj = nn.Linear(d_model, d_model)       # W^O

    def forward(self, x):                             # x: (B, n, d_model)
        B, n, _ = x.shape
        q, k, v = self.qkv(x).chunk(3, dim=-1)
        # (B, n, d_model) -> (B, h, n, d_k)
        q, k, v = (t.view(B, n, self.h, self.d_k).transpose(1, 2) for t in (q, k, v))
        scores = q @ k.transpose(-2, -1) / math.sqrt(self.d_k)   # (B, h, n, n)
        out = F.softmax(scores, dim=-1) @ v                      # (B, h, n, d_k)
        out = out.transpose(1, 2).reshape(B, n, -1)              # concat heads
        return self.proj(out)                                    # (B, n, d_model)

x = torch.randn(2, 16, 64)
assert MultiHeadSelfAttention(d_model=64, h=8)(x).shape == (2, 16, 64)
</code></pre>

<h4>Design analysis</h4>
<p><strong>Why h small heads instead of one full-width attention?</strong> The obvious alternative is a single d_model-wide head, which has the same parameter count. But one head produces one set of attention weights, so it must average all the relations it cares about into a single distribution. Splitting into h heads lets each attend in a different subspace at the same total cost (\( h \cdot d_k = d_\text{model} \)); the tradeoff is that each head sees a narrower d_k-dimensional view, so individual heads are weaker and the model leans on having several.</p>
<p><strong>Why divide by \( \sqrt{d_k} \)?</strong> Without scaling, \( q \cdot k \) is a sum of \( d_k \) unit-variance products, so its variance grows with \( d_k \). At \( d_k = 64 \) that pushes softmax into a near one-hot regime where the gradient vanishes. Dividing by \( \sqrt{d_k} \) holds the variance at about 1 regardless of \( d_k \), keeping softmax in its useful range and training stable.</p>
```
