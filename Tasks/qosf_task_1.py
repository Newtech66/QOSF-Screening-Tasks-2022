import pennylane as qml
import numpy as np

def qft(wires): #in order an,an-1,an-2,...,a1
    n = len(wires)
    for i in range(n):
        qml.Hadamard(wires[i])
        for j in range(2,n+1-i):
            qml.CRZ(2*np.pi/(2**j),wires=[wires[i+j-1],wires[i]])

def multiplier(a,b):
    bin_a = np.binary_repr(a)
    bin_b = np.binary_repr(b)
    len_com = max(len(bin_a),len(bin_b))
    bin_a = np.binary_repr(a,width=len_com)
    bin_b = np.binary_repr(b,width=len_com)
    wires_b=list(range(len_com))
    wires_a=list(range(len_com,2*len_com))
    wires_res=list(range(2*len_com,4*len_com))
    all_wires=wires_b+wires_a+wires_res
    dev = qml.device('default.qubit',wires=all_wires,shots=1)
    @qml.qnode(dev)
    def mult():
        qml.BasisStatePreparation([int(x) for x in bin_b],wires=wires_b)
        qml.BasisStatePreparation([int(x) for x in bin_a],wires=wires_a)
        qft(wires_res)
        for i in range(len_com):
            for j in range(len_com):
                for s in range(2*len_com):
                    qml.ctrl(qml.RZ,control=[wires_b[i],wires_a[j]],control_values=[1,1])(2*np.pi/(2**(i+j-s+2)),wires=wires_res[s])
        qml.adjoint(qft)(wires_res)
        return qml.sample(wires=wires_res)
    print(qml.draw(mult)())
    return bin_to_dec(mult())

def bin_to_dec(bin_r):
    res = 0
    for i in range(len(bin_r)):
        res += bin_r[i]*(2**(len(bin_r)-1-i))
    return res

print(multiplier(5,6))        
    
