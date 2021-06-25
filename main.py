company = "mailto:lesley@abbottpa.com"
if company.upper().startswith("PO"):
    print("yes")
rem = company.replace("mailto:","")
print(rem)