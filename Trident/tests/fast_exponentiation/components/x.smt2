(declare-const rvalue_x (_ BitVec 32))
(declare-fun rvalue_x () (_ BitVec 32))
(declare-const lvalue_x (_ BitVec 32))
(declare-const rreturn (_ BitVec 32))
(declare-const lreturn (_ BitVec 32))
(assert (and (= rreturn rvalue_x) (= lreturn lvalue_x)))