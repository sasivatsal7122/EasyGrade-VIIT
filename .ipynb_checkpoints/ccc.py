# def minSwaps(s: str):
#     counter = 0
#     ans = 0
#     for i in s:
#         if i == ')':
#             if counter == 0:
#                 ans += 1
#                 counter += 1
#             else:
#                 counter -= 1
#         else:
#             counter += 1
#     return ans

# s = ')()(())('
# print(minSwaps(s))


# def getmaxdeletions(move):
#     l = len(move)
#     c_up, c_down = 0, 0
#     c_left, c_right = 0, 0
#     for i in range(l):
#         if (move[i] == 'U'):
#             c_up += 1

#         elif(move[i] == 'D'):
#             c_down += 1

#         elif(move[i] == 'L'):
#             c_left += 1

#         elif(move[i] == 'R'):
#             c_right += 1
    
#     return abs(c_right) - abs(c_left) + abs(c_up) - abs(c_down)

# move = 'RRR'
# x = getmaxdeletions(move)
# print(len(move)-x)


# def getTime(s):
#     sec = 0
#     for i in range(0,len(s)-1):
#         if ord(s[i])-ord(s[i+1]) <= 0:
#             sec += ((ord(s[i])-ord(s[i+1]))+26) 
#         else:
#             if (ord(s[i])-ord(s[i+1]))>=13:
#                 sec+= abs(ord(s[i])-ord(s[i+1])-26)
#             else:    
#                 sec+= (ord(s[i])-ord(s[i+1]))
#     return sec

# s = 'AZGB'
# print(getTime(s))


# def minimumSwaps(brackets):
#     counter = 0
#     ans = 0
#     for i in s:
#         if i == ')':
#             if counter == 0:
#                 ans+=1
#                 counter+=1
#             else:
#                 counter-=1
#         else:
#             counter+=1
#     return ans
                

# if __name__ == '__main__':
#     s = str(input())
#     print(minimumSwaps(s))


def getTime(s):
    if s[0]!='A':
        s='A'+s[:]
    sec=0;ls = []
    for i in s:
        ls.append(ord(i)-64)
    for i in range(len(ls)-1):
        x = ls[i+1]-ls[i]
        if x>0 :
            sec+=x-26
        elif x<0 :
            sec+=x+26
        else:
            sec+=x
    return ls,sec
s = 'AZGB'
print(getTime(s))