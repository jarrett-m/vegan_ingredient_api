import re

x = "DARK CHOCOLATE (SUGAR, CHOCOLATE, COCOA BUTTER, MILK FAT, COCOA PROCESSED WITH ALKALI, LECITHIN (SOY), MILK, SALT, NATURAL VANILLA FLAVOR), SUGAR, CORN SYRUP, MALTODEXTRIN, DEIONIZED APPLE JUICE CONCENTRATE, NATURAL FLAVOR, POMEGRANATE JUICE CONCENTRATE, PECTIN, MALIC ACID, APPLE JUICE CONCENTRATE, RASPBERRY JUICE CONCENTRATE, BLUEBERRY JUICE CONCENTRATE, CANOLA OIL, ACAI PUREE CONCENTRATE, CRANBERRY JUICE CONCENTRATE, LEMON JUICE CONCENTRATE, BAKING SODA, ASCORBIC ACID, SODIUM CITRATE, CITRIC ACID, DEXTROSE, CONFECTIONER'S GLAZE."

def ing_spliter(ingredients):
    pat = re.compile("([^,()]+(?:\(.*\))?)")
    result = pat.findall(ingredients)

    ing = []

    for item in result:
        if '(' in item:
            more = re.findall('\(.*?\)', item)[0]
            if ',' in more:
                new_split = pat.findall(more)
                new_split = [i.strip() for i in new_split]
                ing += new_split
            else:
                ing.append(item.strip())
        else:
            ing.append(item.strip())

    return list(set(ing))

for item in ing_spliter(x):
    print(item)