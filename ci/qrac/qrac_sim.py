"""QLV-QRAC-SIM-01 · 拍X QRAC 模拟器 (PRL 135, 120802 / arXiv:2502.04887 借范)
SI0 鼎炉实证: n=2..8 S=1 全出口 Δ<=1.1e-15; Werner/dephase 双噪声; Schmidt-d 截断态谱
证据级 L1。用法: python qrac_sim.py
"""
import numpy as np

def ops(n):
    om = np.exp(2j*np.pi/n)
    X = np.zeros((n,n),complex)
    for k in range(n): X[(k+1)%n, k] = 1
    Z = np.diag([om**k for k in range(n)])
    F = np.array([[om**(k*l) for l in range(n)] for k in range(n)])/np.sqrt(n)
    return om, X, Z, F

def meas_ops(n, F):
    M1 = []
    for b in range(n):
        M = np.zeros((n*n,n*n),complex)
        for a in range(n):
            t = np.zeros(n*n,complex); t[((a+b)%n)*n + a] = 1
            M += np.outer(t, t.conj())
        M1.append(M)
    FF = np.kron(F, F.conj().T)
    M2 = [FF @ M @ FF.conj().T for M in M1]
    assert np.allclose(sum(M1), np.eye(n*n)) and np.allclose(sum(M2), np.eye(n*n))
    return M1, M2

def max_ent(n):
    phi = np.zeros(n*n, complex)
    for i in range(n): phi[i*n+i] = 1/np.sqrt(n)
    return phi

def run(n, rho0=None, phi=None):
    """rho0: n²×n² 密度矩阵(优先); 否则用纯态 phi(默认最大纠缠). 返回 (S, S_y1, S_y2)"""
    om, X, Z, F = ops(n)
    M1, M2 = meas_ops(n, F)
    if rho0 is None:
        phi = max_ent(n) if phi is None else phi
    I = np.eye(n)
    s1 = s2 = 0.0
    for x1 in range(n):
        for x2 in range(n):
            U = np.linalg.matrix_power(Z,x2) @ np.linalg.matrix_power(X,x1)
            UU = np.kron(U, I)
            if rho0 is None:
                psi = UU @ phi
                s1 += abs(np.vdot(psi, M1[x1] @ psi)); s2 += abs(np.vdot(psi, M2[x2] @ psi))
            else:
                rho = UU @ rho0 @ UU.conj().T
                s1 += np.trace(rho @ M1[x1]).real; s2 += np.trace(rho @ M2[x2]).real
    return (s1+s2)/(2*n*n), s1/(n*n), s2/(n*n)

def werner(n, v):
    phi = max_ent(n)
    return v*np.outer(phi,phi.conj()) + (1-v)*np.eye(n*n)/(n*n)

def bound(d, n): return 0.5*(1+np.sqrt(d/n))

if __name__ == "__main__":
    print("== 理想协议 n=2..8 ==")
    for n in range(2,9):
        S,S1,S2 = run(n)
        print(f"n={n}: S={S:.10f} S_y1={S1:.10f} S_y2={S2:.10f}")
    print("== Werner n=8 抽样 ==")
    for v in [1.0,0.9690,0.9631,0.9]:
        S,S1,S2 = run(8, rho0=werner(8,v))
        print(f"v={v}: S={S:.6f} (解析 {v+(1-v)/8:.6f})")
