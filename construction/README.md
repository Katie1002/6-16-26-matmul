# A 1,527-product algorithm for rectangular matrix multiplication

The `NewAlgorithm.lean` file is a standalone exact certificate for the
matrix multiplication tensor ⟨6,16,26⟩ over `Int`. It lists 1,527
sparse triples of coefficient vectors `(U,V,W)`. The `brent_identity`
theorem proves that their sum equals every coefficient of the ordinary
matrix multiplication tensor, and `product_count` proves the rank bound.
Thus the same algorithm works over any commutative ring. By tensor symmetry,
every permutation of the format, e.g. ⟨6,26,16⟩, also has rank at most 1,527.

The comparison snapshot from the `solven-eu/matmulcatalog` Git repository
(commit `1bf0df393a56b97d0f5398d24430d1f3f754285a`, 2026-09-26)
records 1,528 for ⟨6,16,26⟩; the older FMM Lille bound is 1,554.
Recursive tensor powers therefore use at most `1527^t` products where
the recorded construction used `1528^t`. The volume-normalized exponent
`3 log(rank) / log(6·16·26)` drops from approximately 2.811799 to 2.811548.
This is a rank upper-bound improvement, not a claim that 1,527 is optimal.

## Construction

An 84-term ⟨2,4,13⟩ scheme has common-U classes of sizes
`3×1 + 2×2 + 19×3 + 5×4`. Substitute certified small-format schemes
of ranks 20, 38, 54, and 73 for ⟨3,4,2⟩, ⟨3,4,4⟩,
⟨3,4,6⟩, and ⟨3,4,8⟩ respectively. The count is

`3·20 + 2·38 + 19·54 + 5·73 = 1,527`.

`build_new.py` constructs the coefficient vectors from the five source
JSON files and checks every Brent equation in Python. `generate_new_lean.py`
emits the standalone Lean proof from those vectors. The Lean proof checks
the final 1,527-term scheme independently; its truth does not rely on the
generator or Python verification.

## Check

Using Lean 4.36.0-pre or a compatible recent Lean 4 installation:

```sh
lean NewAlgorithm.lean
```

The `rank_1527_correct` proof uses `native_decide` on all 6,230,016 tensor
coefficients, so compilation can take several minutes. There are no
`sorry` declarations or custom axioms.

Source schemes: Andrew Perminov's
[FastMatrixMultiplication repository](https://github.com/dronperminov/FastMatrixMultiplication),
with the corresponding files copied into `perminov/schemes` here for
reproducibility. The source construction is the serendipitous product
described in [Perminov (2026)](https://arxiv.org/abs/2606.02480).
