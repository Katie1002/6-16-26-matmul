<6,16,26> bilinear scheme of rank 1527 over Z (coefficients in {-3,...,3})

Scheme files (same content, three formats, written with the Scheme class from
github.com/dronperminov/FastMatrixMultiplication):
  6x16x26_m1527_Z.m     Maple-style list of 1527 triples {U (6x16), V (16x26), W (26x6)}
  6x16x26_m1527_Z.json  Perminov JSON: u/v/w vectors, explicit m_i products and c_ij formulas
  6x16x26_m1527_Z.txt   "n1 n2 n3 m" header, then flattened u, v, w

Convention (cyclic / Brent form):
  sum_r U_r[i][j] * V_r[j][k] * W_r[k][i] = 1 for all i,j,k, and 0 for every other index triple.
  So C = A*B is recovered as C[i][k] = sum_r W_r[k][i] * <U_r,A> * <V_r,B>
  (W is stored transposed, 26x6).

construction/  build_new.py (builds the scheme from the five source schemes and
               checks every Brent equation), generate_new_lean.py, the source
               schemes under perminov/schemes/, their README.md, and
               NewAlgorithm.lean (standalone Lean 4 certificate: `lean NewAlgorithm.lean`)

All 6,230,016 Brent equations verified exactly over Z.
SHA-256 checksums for every file: MANIFEST.sha256

Construction: Perminov's serendipitous product. A rank-84 <2,4,13> base
(serendipitous_base/2x4x13_m84_0037b2c7..._ZT.json, from Perminov's repo)
has common-U classes of sizes 3x1 + 2x2 + 19x3 + 5x4. Each class is
replaced by a <3,4,2k> scheme of rank 20 / 38 / 54 / 73:
  3*20 + 2*38 + 19*54 + 5*73 = 1527
Previous best known: 1528 (Perminov 2026, arXiv:2606.02480); 1554 in the FMM catalogue.
