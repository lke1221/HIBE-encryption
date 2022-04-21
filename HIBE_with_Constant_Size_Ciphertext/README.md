# Hierarchical Identity Based Encryption with Constant Size Ciphertext  

## 이 논문에서 다루고 있는 HIBE system의 특징  
* 암호문 사이즈와 복호화 비용이 hierarchy depth($l$)과 독립적  
* 암호문이 항상 세 개의 그룹원소로 이루어지고, 복호화는 단 두번의 bilinear map 연산을 필요로 함  
* private key는 $l$개의 group element를 포함  
</br>

## Forward secure encryption system은 다음과 같다  
* 어느 기간(주기?) T=$$[2^t]$$에 대해서나 암호문은 세 개의 그룹 원소로만 이루어져있다. 또, private key의 size는 $O(t^2)$다. 단, section 4에서 다루는 hybrid system은 private key size가 $O(t^{3/2})$, 암호문 사이즈가 $O(\sqrt t)$ 이고, CHK 같은 업데이트 가능한 public 저장소를 사용할 경우 private key size가 $O(t)$나 $O(\sqrt t)$ 까지도 작아질 수 있다.  
</br>

## 서두? 서론? (preliminaries)  
### Fully Secure HIBE Systems  
* HIBE에서 identity는 벡터. 깊이 k의 identity는 k차원의 벡터이다.  
* Setup, KeyGen, Encrypt, Decrypt의 네 가지 알고리즘으로 구성되어 있다.  
    * Setup: 시스템 매개변수(params)와 master key(master-key)를 생성. master key는 깊이 0에서의 private key  
    * KeyGen: Identitiy $ID_k = (I_1,...,I_k)$와 부모 identity의 private key인 $d_{k-1}$을 입력값으로 받아서, $ID_k$ 에 해당하는 private key $d_k$ 를 출력.  
    * Encryption: params를 이용해서 메시지를 암호화한다  
    * Decryption: private key를 이용해서 암호문을 복호화한다  
HIBE에 대한 선택 암호문 공격(Chosen ciphertext attack)은 chosen identity attack으로 정의된다.  
(Chosen identity attack: 공격자가 공격할 public key를 선택할 수 있음)  
</br>

더 정확히는, HIBE security(IND-ID-CCA)는 다음과 같은 공격자 A와 도전자(?) C의 게임으로 정의할 수 있다.  

>Setup: 도전자 C는 Setup알고리즘을 돌리고, 결과로 나온 params를 A에게 넘겨준다. 단, masterkey는 넘겨주지 않는다.  

>1단계: A는 쿼리 $(q_1,...q_m)$을 만든다. 이 때 쿼리 $q_i$는 다음 두 가지 중 하나이다.  
    * 비밀키 쿼리 <$ID_i$> : C는 KeyGen알고리즘으로 공개키 $ID_i$에 해당하는 비밀키 $d_i$를 만들어 A에게 알려준다.  
    * 복호화 쿼리 <$ID_i, C_i$> : C는 KeyGen 알고리즘으로 $ID_i$에 해당하는 비밀키 $d$를 만든다. 그리고 Decrypt 알고리즘과 $d$로 $C_i$를 복호화 하고, 결과로 나온 평문을 A에게 준다.  

>Challenge: A는 1단계가 끝나면 idnetity $ID^*$와, 시험해 보고 싶은 같은 길이의 평문 두 개 M0, M1를 output으로 내보낸다. 이 때 A는 $ID^*$나 $ID^*$의 prefix에 대한 비밀키 쿼리를 한 적이 없어야 한다. 그럼 C는 랜덤 비트(0또는 1)를 선택하여 challenge ciphertext CT를 만든다. CT=Encrypt(params, $ID^*, M_b$). 그리고 이걸 A에게 보낸다.  

>2단계: A는 쿼리 $(q_{m+1},...,q_n)$을 추가로 생성한다. 이 때 쿼리 $q_i$는 다음 두 가지 중 하나이다.  
    * 비밀키 쿼리 <$ID_i$>: $ID_i$는 $ID^*$나 $ID^*$의 prefix가 아니다.  
    * 복호화 쿼리 <$C_i$>: $ID^*$의 복호화 쿼리나 $ID^*$의 prefix의 복호화 쿼리와 다르다.  
    C는 1단계와 같이 답한다.  

Guess: 마지막으로, A는 b(앞에서 나왔던 랜덤비트)가 (0과 1중)무엇인지 추측해서 성공하면 이긴다.  
</br>

이러한 공격자 A를 IND-ID-CCA 공격자라고 한다. 그리고 A가 scheme $\epsilon$를 공격했을 때 얻는 이득 $Adv_{\epsilon, A}$를 A가 랜덤비트 b 추측에 성공할 확률에서 0.5를 뺀 것의 절댓값 ($|Pr[b=b']-0.5|)$로 한다 (아예 확실히 틀린다고 가정할 경우 오히려 반대로 말하면 성공하는거니까 0.5를 빼고 절대값). 좀 더 약한 개념인 selective identity chosen ciphertext secure HIBE(IND-sID-CCA)는 A가 C에게 Setup 단계 이전에 ID*를 공개한다는 것만 빼면 IND-ID-CCA와 동일하다.  
</br>

HIBE 시스템 $\epsilon$은 $(t, q_{ID}, q_C, e)$-IND-ID-CCA secure하다. (=최대 $q_ID$개의 비밀키 쿼리와 $q_C$개의 복호화 쿼리를 만드는 공격자 A와 임의의 $t$에 대해서 $Adv(\epsilon, A)<e$ 이다)  
</br>

Semantic Security: 앞서 나왔던 게임에서와 동일하게 HIBE system의 선택 평문 공격을 정의한다 (이번에는 선택 '평문' 공격이라서 공격자가 아무 복호화 쿼리나 선택할 수 없다). 비밀키 쿼리는 여전히 자유롭게 선택 가능하다. 이 보안 개념은 IND-ID-CPA라고 한다 (selective identity adversary의 경우 IND-sID-CPA)  
HIBE 시스템 $\epsilon$는 $(t, q_{ID}, q_C, e)$-IND-ID-CCA secure할 경우, $(t, q_{ID}, q_C, e)$-IND-ID-CPA secure하다.  
</br>

### Bilinear Groups  
1. $G$와 $G_1$은 두 개의 multiplicative cyclic group of prime order 이다.  
>(논문 읽다가 때려칠 뻔 했던 첫번째 위기)  
multiplicative : 증가하는  
cyclic group : 순환군. 순환군의 모든 원소는 어떤 고정된 원소의 거듭제곱이다. 즉, 군의 원소 $g$가 생성하는 순환군은 ${...,g^{-2}, g^{-1}, 1, g, g^2,...}$ 이다.  
order: 원소의 수  
group of prime order: 원소의 수가 소수(prime number)인 그룹  
즉, multiplicative cyclic group of prime order  = 원소의 수가 소수인 증가하는 순환군  
2. $g$는 $G$의 생성자이다. (위에 설명에서 나온 것처럼 $g$의 거듭제곱인 수들로 $G$가 이뤄졌다는 의미)  
3. $e$는 다음과 같은 bilinear map이다. $e: GxG->G_1$.  
</br>

$e$는 다음과 같은 특징을 갖는다.  
1. Bilinearity(이선형성): $G$에 속하는 모든 $u,v$와 $Z$에 속하는 $a,b$에 대해 $e(u^a, v^b) = e(u,v)^{ab}$  
2. Non-degeneracy: $e(g,g)$는 1이 아니다.  
</br>
$G$의 group action이 효율적으로 계산될 수 있고(efficiently computed), $G_1$과 effciently computable한 $e$가 있으면 $G$를 bilinear group이라고 한다.  
</br>

### Bilinear Diffie-Hellman Inversion Assumption  
$G$가 $p$(prime number)개의 원소를 갖는 bilinear group이라고 하자. $G$의 원소인 $w$를 generator로 하고 $\beta$가 $Z_p^*$에 속할 때, l번째 Bilinear Diffie Hellman Inversion Problem(이하 $l-BDHI$)는 다음과 같이 정의된다.  
> $l$-$BDHI$: $w$, $w^{\beta}$, $w^{\beta^2}$, ... , $w^{\beta^l}$ 이 주어졌을 때, $e(w,w)^{1/{\beta}}$ 를 계산하라  

$G$의 $l$-$BDHI$ assumption: 그 어떤 효율적인 알고리즘도 $G$의 $l$-$BDHI$를 non-neligible probability(무시할 수 없을만큼 큰 확률)로 해결할 수 없다.=그냥 풀기 힘들다는 소리겠지?  
</br>

### Weak BDHI Assumption:  
이 논문에서의 보안 이론은 일반 BDHI 보다 좀 더 약한 가정으로 설명할 수 있다. 이를 Weak BDHI($l$-$wBDHI$)라고 한다.  
$g$와 $h$를 $G$의 두 개의 랜덤 생성자라고 하자. $\alpha$를 $Z_p^*$ 의 랜덤 수라고 할 때, $l$-$wBDHI$와 $l$-$wBDHI^*$를 다음과 같이 정의한다.  
> $l$-$wBDHI$: $g, h, g^a, g^{a^2},...,g^{a^l}$이 주어졌을 때, $e(g,h)^{1/a}$를 계산하라  
> $l$-$wBDHI^*$: $g, h, g^a, g^{a^2},...,g{a^l}$이 주여젔을 때, $e(g,h)^{a^{l+1}}$을 계산하라  

두 문제는 linear time reduction 아래 동일하다. $wBDHI$가 $BDHI$ 문제 쪽에 더 자연스럽게(?) 연관되어 있는 것처럼 보이지만, 더 간편하게 표현하기 위해 $wBDHI^*$ problem을 증명에 사용한다.  
</br>

G의 $l$-$wBDHI$ 또는 $l$-$wBDHI^*$를 위한 알고리즘이 $l$-$BDHI$를 위한 알고리즘을 준다는 것을 확인하기는 쉽다  
>(논문 읽다가 때려칠 뻔한 두 번째 위기. 뭐가 쉽다는건데..)  
따라서, 주어진 $l$-$BDHI$ 문제는 
