## Hierarchical Identity Based Encryption with Constant Size Ciphertext  

### 이 논문에서 다루고 있는 HIBE system의 특징  
* 암호문 사이즈와 복호화 비용이 hierarchy depth(l)과 독립적  
* 암호문이 항상 세 개의 그룹원소로 이루어지고, 복호화는 단 두번의 bilinear map 연산을 필요로 함  
* private key는 l개의 group element를 포함  
</br>

### Forward secure encryption system은 다음과 같다  
* 어느 기간(주기?) T=2^t에 대해서나 암호문은 세 개의 그룹 원소로만 이루어져있다. 또, private key의 size는 O(t^2)다. 단, section 4에서 다루는 hybrid system은 private key size가 (O^t^(3/2)), 암호문 사이즈가 O(t^(1/2))이고, CHK 같은 업데이트 가능한 public 저장소를 사용할 경우 private key size가 O(t)나 O(t^(1/2))까지도 작아질 수 있다.  
</br>

### 서두? 서론? (preliminaries)  
* HIBE에서 identity는 벡터. 깊이 k의 identity는 k차원의 벡터이다.  
* Setup, KeyGen, Encrypt, Decrypt의 네 가지 알고리즘으로 구성되어 있다.  
    * Setup: 시스템 매개변수(params)와 master key(master-key)를 생성. master key는 깊이 0에서의 private key  
    * KeyGen: Identitiy IDk=(I1,...,Ik)와 부모 identity의 private key인 d(k-1)을 입력값으로 받아서, IDk에 해당하는 private key dk를 출력.  
    * Encryption: params를 이용해서 메시지를 암호화한다  
    * Decryption: private key를 이용해서 암호문을 복호화한다  
HIBE에 대한 선택 암호문 공격(Chosen ciphertext attack)은 chosen identity attack으로 정의된다.  
(Chosen identity attack: 공격자가 공격할 public key를 선택할 수 있음)  
</br>

더 정확히는, HIBE security(IND-ID-CCA)는 다음과 같은 공격자 A와 도전자(?) C의 게임으로 정의할 수 있다.  
```
Setup: 도전자 C는 Setup알고리즘을 돌리고, 결과로 나온 params를 A에게 넘겨준다. 단, masterkey는 넘겨주지 않는다.  

1단계: A는 쿼리 (q1,...qm)을 만든다. 이 때 쿼리 qi는 다음 두 가지 중 하나이다.  
    * 비밀키 쿼리 <IDi> : C는 KeyGen알고리즘으로 공개키 IDi에 해당하는 비밀키 di를 만들어 A에게 알려준다.  
    * 복호화 쿼리 <IDi, Ci> : C는 KeyGen 알고리즘으로 IDi에 해당하는 비밀키 d를 만든다. 그리고 Decrypt 알고리즘과 d로 Ci를 복호화 하고, 결과로 나온 평문을 A에게 준다.  

Challenge: A는 1단계가 끝나면 idnetity ID*와, 시험해 보고 싶은 같은 길이의 평문 두 개 M0, M1를 output으로 내보낸다. 이 때 A는 ID*나 ID*의 prefix에 대한 비밀키 쿼리를 한 적이 없어야 한다. 그럼 C는 랜덤 비트(0또는 1)를 선택하여 challenge ciphertext CT를 만든다. CT=Encrypt(params, ID*, Mb). 그리고 이걸 A에게 보낸다.  

2단계: A는 쿼리 (q(m+1),...,qn)을 추가로 생성한다. 이 때 쿼리 qi는 다음 두 가지 중 하나이다.  
    * 비밀키 쿼리 <IDi>: IDi는 ID*나 ID*의 prefix가 아니다.  
    * 복호화 쿼리 <Ci>: ID*의 복호화 쿼리나 ID*의 prefix의 복호화 쿼리와 다르다.  
    C는 1단계와 같이 답한다.  

Guess: 마지막으로, A는 b(앞에서 나왔던 랜덤비트)가 (0과 1중)무엇인지 추측해서 성공하면 이긴다.  
```
이러한 공격자 A를 IND-ID-CCA 공격자라고 한다. 그리고 A가 scheme E(엡실론이지만 E로 표기하겠음) 공격했을 때 얻는 이득 Adv(E, A)를 A가 랜덤비트 b 추측에 성공할 확률에서 0.5를 뺀 것의 절댓값 (|Pr[b=b']-0.5)|로 한다 (아예 확실히 틀린다고 가정할 경우 오히려 반대로 말하면 성공하는거니까 0.5를 빼고 절대값). 좀 더 약한 개념인 selective identity chosen ciphertext secure HIBE(IND-sID-CCA)는 A가 C에게 Setup 단계 이전에 ID*를 공개한다는 것만 빼면 IND-ID-CCA와 동일하다.  
</br>

