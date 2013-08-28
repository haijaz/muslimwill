def calcSpouse(new):
    print new.relatives.filter(Relations.relationType==getRelationshipIDByName("spouse")).first()
    # if new.spouseAlive == False:
        # spShare = 0
    # else:
        # if new.eds==0:
            # if new.gender=="Female":
                # spShare = 1/2
            # else:
                # spShare=1/4
        # else:
            # if new.gender=="Female":
                # spShare = 1/4
            # else:
                # spShare = 1/8
    return 5