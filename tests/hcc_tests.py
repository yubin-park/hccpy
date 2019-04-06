from hccpy.hcc import HCCEngine

he = HCCEngine()

cc_lst = he._get_cc(["A01.03", "A227", "a391", "J42"], age=17)
print(cc_lst)
cc_lst = he._get_cc(["A01.03", "A227", "a391", "J42"], age=19)
print(cc_lst)

cc_lst = he._get_cc(["c169", "c180"], age=17)
print(cc_lst)



