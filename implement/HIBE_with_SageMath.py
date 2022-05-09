def setup(lbd, lbd2):
    p = random_prime(2^lbd, lbound =2^(lbd -1))
    sd_p = 6* randint(2^(lbd2 - lbd -1), 2^(lbd2 - lbd))*p -1
    while not sd_p.is_pseudoprime(): #p가 pseudoprime인지 확인하고, 아닐 경우 pseudoprime이 될 때까지 다시 배정
        p = random_prime(2^lbd, lbound =2^(lbd -1))
        sd_p = 6* randint(2^(lbd2 - lbd -1), 2^(lbd2 - lbd))*p -1
    K = GF(sd_p)
    R.<y > = K[]
    K = K.extension(R.irreducible_element(2), 'x')
    E = EllipticCurve(K,[0, 1])

    return(K, E, p, R) #sd_p는 결론적으로 EllipticCurve 만들기 위해서만 사용하고 반환은 하지 않음

def keygen(parms):
    K = parms[0]
    E = parms[1]
    p = parms[2]
    R = parms[3]

    P = None
    while P is None:
        try:
            a = K(R.random_element(1))
            tmp = a^3 + 1
            while(not tmp.is_square()): #a^3+1이 제곱수가 아닐 경우 sqrt에서 오류터짐. 방지용
                a = K(R.random_element(1))
                tmp = a^3 + 1
            P = E([a, sqrt(a^3 + 1) ])
        except Exception as e:
            print(e)
            pass
        P =((K.characteristic() +1) // p) * P
        while P == E(0):
            P = None
            while P is None:
                try:
                    a = K(R.random_element(1))
                    P = E([a, sqrt(a^3 + 1) ])
                except:
                    pass
            P =((K.characteristic() +1) // p) *P
        g = randint(1 ,p-1) * P
        g2 = randint(1 ,p-1) * P
        g3 = randint(1 ,p-1) * P
        h1 = randint(1 ,p-1) * P
        h2 = randint(1 ,p-1) * P
        # P도, g~h2도 타원 곡선 위의 점

        # 논문대로면 0 ~ p-1이 맞지만 보안상
        a = randint(1, p-1)
        r = randint(1, p-1)

        # a 값이 필요한 system key들 생성
        g1 = g*a
        master_key = g2*a

        # 공개키 생성. parent는 원소가 하나
        parent_id = randint(1, p-1)

        # 비밀키 생성.
        a0 = master_key+((h1*parent_id)+g3)*r
        a1 = g*r
        b2 = h2*r
        parent_d = (a0, a1, b2)

        return((g, g1, g2, g3, h1, h2, p), (parent_id, parent_d))

def keygen_child_public(sys_parms):
    p = sys_parms[6]
    
    child_id1 = randint(1, p-1)
    child_id2 = randint(1, p-1)
    
    return (child_id1, child_id2)

def keygen_child_private(sys_parms, child_public_key, parent_key):
    g = sys_parms[0]
    g3 = sys_parms[3]
    h1 = sys_parms[4]
    h2 = sys_parms[5]
    p = sys_parms[6]
    
    parent_d = parent_key[1]
    a0 = parent_d[0]
    a1 = parent_d[1]
    b2 = parent_d[2]
    
    # 논문대로면 0 ~ p-1이 맞지만 보안상
    t = randint(1, p-1)
    
    # 공개키 생성. child는 원소가 두 개
    child_id1 = parent_key[0]
    child_id2 = child_public_key[1]
    
    # 비밀키 생성
    child_d = (a0+(b2*child_id2)+((h1*child_id1)+(h2*child_id2)+g3)*t, a1+(g*t))
    return ((child_id1, child_id2), child_d)
    
def encrypt(sys_parms, setup_parms, child_id, plaintext):
    # s는 여기서 생성해서 사용
    g = sys_parms[0]
    g1 = sys_parms[1]
    g2 = sys_parms[2]
    g3 = sys_parms[3]
    h1 = sys_parms[4]
    h2 = sys_parms[5]
    p = sys_parms[6]
    
    K = setup_parms[0]
    E = setup_parms[1]

    s = randint(1, p-1)
    g2 = E([g2[0]^K.characteristic(), g2[1]^K.characteristic()])
    
    A = ((g1).weil_pairing(g2,p))^s*plaintext
    B = g*s
    C = (h1*child_id[0]+h2*child_id[1]+g3)*s
    ciphertext = (A, B, C)
    
    return ciphertext

def decrypt(secret_key, setup_parms, ciphertext):

    A, B, C = ciphertext
    
    K = setup_parms[0]
    E = setup_parms[1]
    p = setup_parms[2]
    
    d1 = secret_key[0]
    d2 = secret_key[1]
    
    C = E([C[0]^K.characteristic(), C[1]^K.characteristic()])
    d1 = E([d1[0]^K.characteristic(), d1[1]^K.characteristic()])
    
    plaintext = A*(d2).weil_pairing(C,p)/(B).weil_pairing(d1,p)

    return plaintext

lbd = 160 # log_2 q
lbd2 = 512 # log_2 p

plaintext = 123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789

setup_parms = setup(lbd, lbd2)
sys_parms, parent_key = keygen(setup_parms)
child_public_key = keygen_child_public(sys_parms)
child_key = keygen_child_private(sys_parms, child_public_key, parent_key)
child_key2 = keygen_child_private(sys_parms, child_public_key, parent_key)

ciphertext = encrypt(sys_parms, setup_parms, child_key[0], plaintext)
result = decrypt(child_key[1], setup_parms, ciphertext)
result_two = decrypt(child_key2[1], setup_parms, ciphertext)

print("decrypted1: ", result)
print("decrypted2: ", result_two)