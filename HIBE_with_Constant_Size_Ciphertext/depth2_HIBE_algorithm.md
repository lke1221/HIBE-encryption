최대 깊이가 2인 HIBE system 설계-parent HIBE key가 depth 1, child HIBE key가 depth 2  
</br>

1. Setup:  
다음을 임의로 정해야 한다.  
* G(=원소의 개수가 소수 p개인 증가하는 순환군)의 원소인 **g, g2, g3, h1, h2**  
* Zp(=modulo p 연산의 결과로 나올 수 있는 수들. 즉 0부터 p-1까지)의 원소인 **a, r, t, s**  
* g1은 g^a와 같다.  
* r은 NFT mint할 때마다(또는 소유자 바뀔 때마다), t는 열람권 요청 들어올 때마다 새로 생성  
* s는 암호화 과정에서 사용  
* 공개키 ID는 (I1,..,Ik)로 이루어지며, 각 원소는 Zp*에 속한다.  
</br>

2. KeyGen:  
Level 0 (system): public parameter는 (g, g1, g2, g3, h1 ,h2). master key는 (g2)^a (이하 K)  
Level 1 (parent): ID는 I1, private key d는 ({K\*(h1^I1)\*(g3)}^r, g^r, h2^r)  
Level 2 (child): ID는 (I1, I2), private key d는 ({K\*(h1^I1)\*(h2^I2)\*(g3)}^(r+t), g^(r+t))  
* 단, parent의 I1과 child의 I1은 다른 값이다!! 같아도 상관은 없겠지만?  
</br>

3. Encrypt:  
우리는 HIBE child key로 암호화 할 것이므로, k=2를 기준으로 기술. M은 평문  
CT = ((e(g1, g2)^s)M, g^s, ((h1^I1)\*(h2^I2)\*g3})^s)  
* 여기서 e는 bilinear map(GxG->G1) 이다.
</br>

4. Decrypt:  
우리는 HIBE child key로 복호화 할것이므로, k=2를 기준으로 기술.  
CT=(A,B,C)라고 할 때, private key d=(a0,a1)를 이용하여 A\*e(a1,C)/e(B,a0) = M을 계산한다.  
이 때 e(a1, C)/e(B, a0)는 1/{e(g1,g2)^s}와 같다.  
따라서 결국 M=A/{e(g1,g2)^s}.  
</br>
