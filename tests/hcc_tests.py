from hccpy.hcc import HCCEngine

he = HCCEngine()

print(he.profile(["A01.03", "A227", "a391", "J42"], age=89))
print(he.profile(["A01.03", "A227", "a391", "J42"], age=79))
print(he.profile(["c169", "c180", "I5040", "E0801"], age=67))



