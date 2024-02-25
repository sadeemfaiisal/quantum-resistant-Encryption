import hashlib
import ecdsa
import random
import qiskit as q
import oqs
#self._sig.contents.length_public_key line 351 oqs

def generate_keypair():
    # Generate a new private key
    private_key = ecdsa.SigningKey.generate()

    # Derive the corresponding public key from the private key
    public_key = private_key.verifying_key

    return private_key, public_key

def generate_qresistant_keypair():
    kemalg = "Dilithium2"
    person = oqs.Signature(kemalg)
    
    # Generate a new public key using Crystal Kyber
    private_key = person.generate_keypair()

    # Export the private key 
    public_key = person.export_secret_key()

    return public_key, private_key, person

def transfer_nft(sender_private_key, sender_public_key, recipient_public_key, token_id):

    # Create a message to be signed (concatenation of token ID and recipient's public key)
    message = f"{token_id}:{recipient_public_key}"
    print("Transferring ",token_id,"...")
    message = hashlib.sha256(message.encode()).digest()
    # Sign the hashed message using the sender's private key
    signature = sender_private_key.sign(message)

    # Verify the signature using the sender's public key
    if sender_public_key.verify(signature, message):
        print("Normal Transfer successful.")
    else:
        print("Transfer failed due to invalid signature.")


def transfer_qresistant_nft(sender, sender_public_key, token_id):
    # Create a message to be signed (concatenation of token ID and recipient's public key)
    message = token_id
    print("Transferring ",token_id,"...")

    message = hashlib.sha256(message.encode()).digest()
    # Sign the hashed message using the sender's private key
    signature = sender.sign(message)

    # Verify the signature using the sender's public key
    if sender.verify(message, signature, sender_public_key):
        print("Quantum Resistant Transfer successful.")
    else:
        print("Transfer failed due to invalid signature.")

def qgenerate_token():

    token = ''
    for i in range(36):
        if(len(token)==36):
            continue
        qc = q.QuantumCircuit(7,7)
        qc.h(range(7))
        qc.measure(range(7), range(7))
        output = list(q.execute(qc,q.Aer.get_backend('qasm_simulator'),shots = 1).result().get_counts())[0]
        token+=(hex(int(output, 2))[2:].lower())

    return token

def generate_token():

    token = ''
    for i in range(36):
        h1=''
        h1+=(''.join([str(random.randint(0,1)) for i in range(7)]))
        token += hex(int(h1, 2))[2:].lower()

    return token



# Generate private and public keys for the sender
sender_private_key, sender_public_key = generate_keypair()

# Generate private and public keys for the recipient
recipient_private_key, recipient_public_key = generate_keypair()

# Generate a random token ID (for demonstration purposes)
token_1 = generate_token()

# Simulate transfer of the NFT to the recipient
transfer_nft(sender_private_key, sender_public_key, recipient_public_key, token_1)



#Simulation of Qresistant NFT
sender_private_key, sender_public_key, sender = generate_qresistant_keypair()

recipient_private_key, recipient_public_key, recipient = generate_qresistant_keypair()

token_2 = generate_token()

transfer_qresistant_nft(sender, sender_public_key, token_2)
