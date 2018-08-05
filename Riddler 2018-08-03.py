import collections
import itertools
import numpy as np
import fractions

####################################################################
## Part 1: Look for patterns
##
## I brute-forced the results for 23 coins and looked at what I did.
####################################################################

def judge(coins, head):
    """Returns coins truncated to the part where you win or ''."""
    target = 1
    heads_run = 0
    for i, c in enumerate(coins, start=1):
        if c == head:
            heads_run += 1
            if heads_run == target:
                return ''.join(coins[:i])
        else:
            heads_run = 0
            target += 1
    return ''

def raw_results(num_coins, coin_chars='h+'):
    """coin_chars[0] will be considered "heads".
    Returns a Counter of the winning strings and how often they occurred.
    E.g., results['+hh'] will be 2**(num_coins-3)."""

    results = collections.Counter() # results will be strings
    for coins in itertools.product(coin_chars, repeat=num_coins):
        results[judge(coins, coin_chars[0])] += 1
    return results

def summarize_brute_force():
    results = raw_results(23)

    wins_by_len = collections.Counter()

    # This was the key to "solving" the problem.
    # This sequence is oeis.org/A186426 and based on Mahonian numbers.
    # More on that later.
    win_types_by_len = collections.Counter()

    for k in results.keys():
        wins_by_len[len(k)] += results[k]
        win_types_by_len[len(k)] += 1

    for x in wins_by_len.most_common():
        print(x)
    print()
    for x in sorted(win_types_by_len.keys()):
        print(x, win_types_by_len[x])

####################################################################
## Part 2: Get the result exactly and quickly
##
## A186426 (from above) is the sum of the antidiagonals of A177517.
## A177517 contains the Mahonian numbers in columns, which are
## the coefficients of 1(1+x)(1+x+x^2)...(1+x+...+x^i). I put those
## numbers into rows, added up the diagonals, did some math, and
## spat out the answer.
##
## The main diagonal of the Mahonian matrix is all 1's.
## Everything below that is all 0's.
## Row 0 of the triangle is [1,0,0,0,...].
## Row r, column c is the sum of the last r cells of row r-1.
## E.g. mahonian[5,10] the sum of mahonian[4, 5 thru 9] =
##      3+5+6+5+3 = 22
## (Since this is Python and everything's semi-open, we'd use
## mahonian[4,5:10] to get this sum.)
####################################################################


def build_mahonian(size):
    """(Not the full Mahonian; just the part that we need.)"""

    # These are objects because the values will overflow numpy types.
    mahonian = np.zeros((size, size), dtype=object)
    mahonian[0, 0] = 1
    # This will be a transposition of A177517. Since we want the anti-
    # diagonal values, that's okay.
    for r in range(1, size):
        # We only care about values above the main antidiagonal.
        # Also, the values below the main diagonal are all 0.
        for c in range(r, size-r):
            mahonian[r, c] = sum(mahonian[r-1, c-r:c])
    return mahonian

def winning_prob(max_flips=250):
    """Returns the precise probability of winning within max_flips."""

    mahonian = build_mahonian(max_flips)

    # Eventually, this will have A186426's values.
    coin_wins = collections.Counter()
    # This counts along each antidiagonal to count our winning ways.
    for r in range(max_flips + 1):
        for c in range(max_flips - r):
            coin_wins[r+c+1] += mahonian[r,c]
    wins = 0
    for k in coin_wins.keys():
        # The shorter it takes to win, the more times we'll win that way.
        wins += coin_wins[k] * 2**(max_flips-k)
    return fractions.Fraction(wins, 2**max_flips)
    # If max_flips > 165, the value of this as a Python float freezes at
    # 0.7112119049133976.

####################################################################
## Part 3: Really precise results
##
## Googling the results gives one hit in English; someone on Reddit
## asks how to get a precise result for that number. Someone much
## smarter than I says that that value is just:
##
##     1 - (1/2; 1/2)_infinity
##
## which they say is the q-Pochhammer symbol. Looking that up, it's
## defined as (a; q)_n = product_{k=0 to n-1}(1-aq^k). There's a
## special case named after Euler: phi(q) = (q; q)_infinity. (That's
## not the totient function, as it turns out.)
##
## Wolfram's QPochhammer function has default values like:
##     QPochhammer[a, q=a, n=Infinity]
## so we can get our precise answer by inputting
##     1 - QPochhammer[1/2]
## It has no exact value, but Wolfram Alpha will give you thousands
## of digits of it. Fortunately for me, it starts with what I got.
####################################################################

one_minus_qPoch_half = """0.7112119049133975787211002780707692199110
88095159314215885258933815097759093152987429757156806651921793245662
30666076088281248638791783415398478213747484584295377114030095393147
69605634942658878000833450140902225959747183756477315328387004243986
01802021719071343624128724612772715597958901738078013743142113331342
33221001559559703738492296252251054858373679744333751451397789358660
20603314236789643537603732666880641606987102871333586922928982157481
46164408652890061929122841741013673620106716102485729135535258992608
36054626668318041113677591259120158055767505194968527106365568258888
41933759083995392369423098171542174122243983876598684403963080262859
27089749005284039298085233612158349800694982532250622500841054180861
18026021253275186435101855576853392484939236307909760700558899433058
21921205258836992720287667574225138018300366042590619226195573069331
24124712595077804168998878865284726856859087356430377283281060824030
84574908643037563487349701125750936978510502140203134135622951827053
80556300293587984159704986380351213667256807905634236482804965522720
62783952713006407005716395396132108478152259028452836174283732472946
07870949083363525295051566091807688432755695636796589962522494222149
63649587678058569578246480885940054333197355439580069078858733019940
26964397972442468145366040440601669250087218548473441663047317273610
22074454511308797573127607636590147412011815971670836769015890060243
58400855489563856054157748701045846137196707718995807411323102495910
56053066502893795169312567548801616668551288651432702502152407041506
33962519146985017722040226409024914005513786334345111896726069172043
45908470284626925691084165401935637953062104993907188406406747792998
82650616438411156963661911887959515437047106711464918781470966332539
06816875336822151037197950818841926607510375006423256026582780945485
38740580096624454308485356374920794555922635997295302740909893351536
70618032464220336456149744629407223243225380153318749896197121403205
22498924353175488834725992920398641804845298961580517467477155411622
52320451634072590785069977813743354039617247394973916702148883870640
83484393637764386360036227093559655908456148062611300831976420425070
48359686430769971803232049253310241737631834909292661950085487105902
16982469672833562555877606400294041302050410086587792690753749071137
98905051868451079981796688367886108217786919841422557472902879587034
73987890764280135665773113679474977835533312382283713734374566220757
26313704879568640844596757164242004760394207376745024038989124504825
91098693127180794146599890606120839512188533736378399624399365710403
50955953111890898131334721579256307880550729837344407969317948937456
68225733848198225396283965400650725799141119139773279554198927848117
07960897452378466182891392958407608135615343901526203601716907454229
06796211359659383585504484233126502648000217698148181048075379542280
35652823571292451118483165519217115395439084358748515400653675751862
14754510677737482668588530258899705183626575249943212873478102663424
04489880354833101768612754057046610134945910711782299560428584987165
34876340409411370315854873508756238703521042259219879864539950626693
85286937366756814889543275747137667171887594385104793475879192979577
25901882567313137348408556048190500914283388836702525384215266316575
32868091528558018084559967814027619160369050118144243840738013206433
46444025423862474135241559731777148402982882354647436031064609170533
38897184629501613935562306367585965645619111081287557408831420923840
57481990645875684543948226061320955564015574475986034483934145387730
82124855976512356537885521323542448915368095622970576964985481757984
67777788347186952083306585295924633905655919292176303916416891631470
437"""

# This removes the whitespace in the above.
one_minus_qPoch_half = ''.join(one_minus_qPoch_half.split())

wp = winning_prob()
print(wp)
print(float(wp))
