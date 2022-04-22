partial translation of
> Cramer, R., Boneh, D., Boyen, X., & Eu-Jin Goh. (2005). Hierarchical Identity Based Encryption with Constant Size Ciphertext. In Advances in Cryptology - EUROCRYPT 2005 (pp. 440–456). https://eprint.iacr.org/2005/015.pdf
</br>

* Github에서 LaTeX 지원이 안되는 관계로 수식 보기가 힘듦. 다운로드 받아서 Visual Studio Code로 읽으면 한결 읽기 편하다.(Markdown 파일 열어서 Ctrl+Shift+v 시 미리보기 화면 열림)  
</br>

# Hierarchical Identity Based Encryption with Constant Size Ciphertext  
</br>

## 이 논문에서 다루고 있는 HIBE system의 특징  
* 암호문 사이즈와 복호화 비용이 hierarchy depth($l$)과 독립적  
* 암호문이 항상 세 개의 그룹원소로 이루어지고, 복호화는 단 두번의 bilinear map 연산을 필요로 함  
* private key는 $l$개의 group element를 포함  
</br>

## Forward secure encryption system은 다음과 같다  
* 어느 기간(주기?) T=$2^t$에 대해서나 암호문은 세 개의 그룹 원소로만 이루어져있다. 또, private key의 size는 $O(t^2)$다. 단, section 4에서 다루는 hybrid system은 private key size가 $O(t^{3/2})$, 암호문 사이즈가 $O(\sqrt t)$ 이고, CHK 같은 업데이트 가능한 public 저장소를 사용할 경우 private key size가 $O(t)$나 $O(\sqrt t)$ 까지도 작아질 수 있다.  
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
multiplicative : ~증가하는~ 여기서는 곱셈군 이라는 의미인듯  
cyclic group : 순환군. 순환군의 모든 원소는 어떤 고정된 원소의 거듭제곱이다. 즉, 군의 원소 $g$가 생성하는 순환군은 ${...,g^{-2}, g^{-1}, 1, g, g^2,...}$ 이다.  
order: 원소의 수  
group of prime order: 원소의 수가 소수(prime number)인 그룹  
즉, multiplicative cyclic group of prime order  = 원소의 수가 소수인, 순환군인 곱셈군  
2. $g$는 $G$의 생성자이다. (위에 설명에서 나온 것처럼 $g$의 거듭제곱인 수들로 $G$가 이뤄졌다는 의미)  
3. $e$는 다음과 같은 bilinear map이다. $e$: $G$ x $G$ -> $G_1$.  
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
따라서, $l$-$BDHI$ 문제의 사례 $(w, w_1, ... , w_l)$이 주어졌을 때, $l$-$BDHI^*$의 사례 $(w_l, h, w_{l-1}, ..., w_1, w)$를 정의한다. ($h=w_l^\gamma$, $\gamma$는 $Z_p^*$의 원소)  

$T'$를 이 $l$-$wBDHI^*$문제의 solution이라고 할 때, $T=(T')^{1/\gamma}$가 원래 $l$-$BDHI$의 solution이다.  
</br>

이제 정확하게 computational 하고 decisional한 $l$-$wBDHI$ 가정을 정의하자. 편의를 위해 $l$-$wBDHI^*$에 관해 정의한다. $y_i=g^{(a^i)} \in G^*$ 라고 하자. $Pr[A(g,h,y_1,...,y_l)=e(g,h)^{\alpha^{l+1}}] \geq \epsilon$ 일 때, Algorithm A는 $l$-$wBDHI*$ 문제를 해결함으로써 $\epsilon$ 만큼의 이득을 본다. 이 확률은 $G^*$의 생성자 랜덤선택($g,h$)과 $Z_p$에 속하는 $\alpha$ 선택, 그리고 A에 사용되는 랜덤 비트들에 달렸다(?). $G$에서의 $l$-$wBDHI^*$ problem의 decisional 버전은 다음과 같이 정의된다.  
>$\vec{y_{g, \alpha, l}}=(y_1,...,y_l)$  

$b \in {0,1}$를 output으로 하는 알고리즘 $\beta$는 다음이 성립할 때 Decision $l$-$wBDHI^*$를 풀어서 $\epsilon$ 만큼의 이득을 얻는다. $|Pr[\beta(g,h,\vec{y_{g,\alpha,l}},e(g,h)^{(\alpha^{l+1})})=0]-Pr[\beta(g,h,\vec{y_{g,\alpha,l}},T)=0]|\geq\epsilon$  
이 확률은 $G^*$의 생성자 $g,h$ 선택, $Z_p$에 속하는 $\alpha$ 선택, $T \in G_1^*$ 선택, 그리고 $\beta$에 의 해 소모된 랜덤 비트들에 의해 결정된다.(?) 왼쪽을 $P_{wBDHI^*}$라고 하고, 오른쪽을 $R{wBDHI^*}$라고 부른다.  
</br>

G의 (Decision)$l$-$wBDHI^*$ problem을 해결함으로써 $\epsilon$ 이상의 이득을 얻는 t-time 알고리즘이 존재하지 않을 때, (Decision) $(t, \epsilon, l)$-$wBDHI$ 가정이 성립한다고 한다.  
정확성을 위해 간간히 t와 $\epsilon$ 을 drop하여 (Decision) $l$-$wBDHI$ 가정에 적용한다(?). 위에서 언급된 바와 같이, $G$에서의 computational 하고 decisional한 $l$-$BDHI$ 가정은 각각 computational 하고 decisional한 $l$-$wBDHI$ 가정을 내포한다.  
</br>

## A HIBE System with Constant Size Ciphertext  
여기서부터는 프로젝트에 필요한 만큼만 이해하고 정리함! depth2_HIBE_algorithm.md와 내용 동일  
</br>

예상 시나리오: 최대 깊이가 2인 HIBE system 설계-parent HIBE key가 depth 1, child HIBE key가 depth 2  
</br>

1. Setup:  
다음을 임의로 정해야 한다.  
* $G$(=원소의 개수가 소수 $p$개인 증가하는 순환군)의 원소인 **$g, g_2, g_3, h_1, h_2$**  
* $Z_p$(=modulo $p$ 연산의 결과로 나올 수 있는 수들. 즉 0부터 p-1까지)의 원소인 **$a, r, t, s$**  
* $g_1$은 $g^a$와 같다.  
* $r$은 NFT mint할 때마다(또는 소유자 바뀔 때마다), $t$는 열람권 요청 들어올 때마다 새로 생성  
* $s$는 암호화 과정에서 사용  
* 공개키 $ID$는 $(I_1,..,I_k)$로 이루어지며, 각 원소는 $Z_p$에 속한다.  
</br>

2. KeyGen:  
Level 0 (system): public parameter는 $(g, g_1, g_2, g_3, h_1 ,h_2)$. master key는 $g_2^a$ (이하 $K$)  
Level 1 (parent): $ID$는 $I_1$, private key $d$는 $((K*h_1^{I_1}*g_3)^r, g^r, h_2^r)$  
Level 2 (child): $ID$는 $(I_1, I_2)$, private key $d$는 $((K*h_1^{I_1}*h_2^{I_2}*g_3)^{r+t}, g^{r+t})$  
* 단, parent의 $I_1$과 child의 $I_1$은 다른 값이다!! 같아도 상관은 없겠지만?  
</br>

3. Encrypt:  
우리는 HIBE child key로 암호화 할 것이므로, k=2를 기준으로 기술. $M$은 평문  
$CT = (e(g_1, g_2)^s*M, g^s, (h_1^{I_1}*h_2^{I_2}*g_3)^s)$  
* 여기서 e는 bilinear map($G$ x $G$->$G_1$) 이다.
</br>

4. Decrypt:  
우리는 HIBE child key로 복호화 할것이므로, k=2를 기준으로 기술.  
$CT=(A,B,C)$라고 할 때, private key $d=(a_0,a_1)$를 이용하여 $A*e(a1,C)/e(B,a0) = M$을 계산한다.  
이 때 $e(a_1, C)/e(B, a_0)$는 $1/e(g_1,g_2)^s$와 같다.  
따라서 결국 $M=A/e(g_1,g_2)^s$.  
</br>
