import pennylane as qml
import numpy as np

n_bits, query_reg, aux = None, None, None

def oracle(numbers):
    """This oracle creates a multi-controlled X gate for each number
    in the list.
    """
    for number in numbers:
        qml.MultiControlledX(wires=query_reg+aux,control_values=np.binary_repr(number,width=n_bits))

def diffusion():
    """This implements the Grover diffusion operator
    """
    qml.broadcast(qml.Hadamard,wires=query_reg,pattern='single')
    qml.MultiControlledX(wires=query_reg+aux,control_values='0'*n_bits)
    qml.broadcast(qml.Hadamard,wires=query_reg,pattern='single')

def missing_number(numbers):
    """Assuming that numbers is a list of 2^n-1 distinct numbers
    from [0,2^n). Otherwise, it wouldn't make sense to ask for a
    missing number.
    """
    #setting up stuff
    global n_bits, query_reg, aux
    n_bits = len(np.binary_repr(len(numbers)))
    query_reg = list(range(n_bits))
    aux = [n_bits]
    #grover search quantum circuit
    dev = qml.device('default.qubit',wires=query_reg+aux,shots=1)
    @qml.qnode(dev)
    def grover_search():
        """Implementation of Grover search to find the missing number
        in O(sqrt(N))=O(2^(n/2)) time.
        """
        #apply Hadamard transform on query register
        qml.broadcast(qml.Hadamard,wires=query_reg,pattern='single')
        #apply Pauli X, then Hadamard to send auxiliary qubit from |0> to |->
        qml.PauliX(wires=aux)
        qml.Hadamard(wires=aux)
        #apply Grover iterations grover_iter number of times (approximated as floor(pi/4*sqrt(N)))
        grover_iter = int(np.floor((np.pi/4)*np.sqrt(1+len(numbers))))
        for i in range(grover_iter):
            oracle(numbers)
            diffusion()
        #measure and get result
        return qml.sample(wires=query_reg)
    #draw circuit
    circuit_draw = qml.draw(grover_search)
    print(circuit_draw())
    #run circuit and get result
    bin_A = grover_search()
    A = 0
    for i in range(len(bin_A)):
        A += bin_A[-1-i]*(2**i)
    return A


A = missing_number([0,3,5,1,7,2,4])
print(A)
