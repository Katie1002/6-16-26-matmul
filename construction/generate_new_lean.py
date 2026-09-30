"""Emit a standalone Lean checker for the explicit 1,527-product scheme."""
from build_new import terms

def sparse(d):
    return '#[' + ','.join(f'({i},{v})' for i,v in sorted(d.items())) + ']'

with open('NewAlgorithm.lean','w') as f:
    f.write('''import Lean
set_option maxHeartbeats 0
set_option maxRecDepth 4096

/-!
An explicit integer bilinear scheme for (6,16,26) using 1,527 products.
Each triple below is the sparse coefficient vectors of one product:
  (Σ U[a] A[a]) * (Σ V[b] B[b]), then add W[c] times that product
to the output coordinate c.  The theorem checks all Brent equations,
not sampled matrix products.

Source inputs for construction (independently checked over Int):
Perminov 2x4x13 rank 84, with U classes 3×1, 2×2, 19×3, 5×4;
3x4x2 rank 20, 3x4x4 rank 38, 3x4x6 rank 54, 3x4x8 rank 73.
The composition count is 3*20 + 2*38 + 19*54 + 5*73 = 1527.
-/
namespace NewAlgorithm

structure Term where
  U : Array (Nat × Int)
  V : Array (Nat × Int)
  W : Array (Nat × Int)

''')
    # Break up elaboration into groups of 50 literals.
    batches=[terms[i:i+50] for i in range(0,len(terms),50)]
    for j,batch in enumerate(batches):
        f.write(f'def batch{j} : Array Term := #[\n')
        f.write(',\n'.join(f'  ⟨{sparse(u)},\n   {sparse(v)},\n   {sparse(w)}⟩'
                          for u,v,w in batch))
        f.write('\n]\n\n')
    f.write('def terms : Array Term :=\n  '+ ' ++\n  '.join(f'batch{j}' for j in range(len(batches)))+'\n\n')
    f.write('''def addVW (out : Array Int) (v w : Array (Nat × Int)) (u : Int) : Array Int :=
  v.foldl (fun out (b,vb) =>
    w.foldl (fun out (c,wc) =>
      let ix := b * 156 + c
      out.set! ix (out.getD ix 0 + u * vb * wc)) out) out

def coefficientSlice (a : Nat) : Array Int :=
  terms.foldl (fun out t =>
    t.U.foldl (fun out (index,u) =>
      if index == a then addVW out t.V t.W u else out) out)
    (Array.replicate (416 * 156) (0 : Int))

def expected (a b c : Nat) : Int :=
  if b / 26 == a % 16 && c / 6 == b % 26 && c % 6 == a / 16 then 1 else 0

def checkSlice (a : Nat) : Bool := Id.run do
  let coefficients := coefficientSlice a
  return (List.range (416 * 156)).all fun index =>
    decide (coefficients.getD index 0 = expected a (index / 156) (index % 156))

def certificate : Bool :=
  terms.size == 1527 &&
    terms.all (fun t => t.U.all (fun (i,_) => i < 96) &&
      t.V.all (fun (i,_) => i < 416) && t.W.all (fun (i,_) => i < 156)) &&
    (List.range 96).all checkSlice

/-- All 6,230,016 tensor coefficients satisfy the exact integer Brent equations. -/
theorem rank_1527_correct : certificate = true := by native_decide

/-- The certificate contains exactly 1,527 scalar products. -/
theorem product_count : terms.size = 1527 := by
  have hv := rank_1527_correct
  simp only [certificate, Bool.and_eq_true] at hv
  simpa using hv.1.1

/-- The coefficient of A[a] B[b] in output C[c] is exactly the matrix
    multiplication tensor coefficient for every valid index. -/
theorem brent_identity (a b c : Nat)
    (ha : a < 96) (hb : b < 416) (hc : c < 156) :
    (coefficientSlice a).getD (b * 156 + c) 0 = expected a b c := by
  have hv := rank_1527_correct
  simp only [certificate, Bool.and_eq_true] at hv
  have hs := (List.all_eq_true.mp hv.2) a (List.mem_range.mpr ha)
  dsimp only [checkSlice, Id.run] at hs
  have hi : b * 156 + c < 416 * 156 := by omega
  have he := (List.all_eq_true.mp hs) (b * 156 + c) (List.mem_range.mpr hi)
  have hd : (b * 156 + c) / 156 = b := by omega
  have hm : (b * 156 + c) % 156 = c := by omega
  simpa only [decide_eq_true_eq, hd, hm] using he

/-- The same bound for the ordered format (6,26,16). This is the
    cyclically transposed coefficient tensor:
    swap the old U and W factors and transpose the old V factor. -/
def orderedCoefficient (a b c : Nat) : Int :=
  (coefficientSlice ((c % 6) * 16 + c / 6)).getD
    (((b % 16) * 26 + b / 16) * 156 + ((a % 26) * 6 + a / 26)) 0

def orderedExpected (a b c : Nat) : Int :=
  if b / 16 == a % 26 && c / 6 == b % 16 && c % 6 == a / 26 then 1 else 0

theorem ordered_brent_identity (a b c : Nat)
    (ha : a < 6 * 26) (hb : b < 26 * 16) (hc : c < 16 * 6) :
    orderedCoefficient a b c = orderedExpected a b c := by
  have h1 : ((c % 6) * 16 + c / 6) < 96 := by omega
  have h2 : ((b % 16) * 26 + b / 16) < 416 := by omega
  have h3 : ((a % 26) * 6 + a / 26) < 156 := by omega
  have h := brent_identity ((c % 6) * 16 + c / 6)
    ((b % 16) * 26 + b / 16) ((a % 26) * 6 + a / 26) h1 h2 h3
  have e1 : ((c%6)*16+c/6)%16 = c/6 := by omega
  have e2 : ((c%6)*16+c/6)/16 = c%6 := by omega
  have e3 : ((b%16)*26+b/16)/26 = b%16 := by omega
  have e4 : ((b%16)*26+b/16)%26 = b/16 := by omega
  have e5 : ((a%26)*6+a/26)/6 = a%26 := by omega
  have e6 : ((a%26)*6+a/26)%6 = a/26 := by omega
  simp only [orderedCoefficient, expected, orderedExpected,
    e1,e2,e3,e4,e5,e6] at *
  grind

theorem improvement : 1527 < 1528 := by decide

theorem recursive_improvement (depth : Nat) (positive : depth ≠ 0) :
    1527 ^ depth < 1528 ^ depth :=
  Nat.pow_lt_pow_left improvement positive

end NewAlgorithm
''')
print('generated NewAlgorithm.lean')
