def accumulated_return(assets_return):
    accumulated = []
    compound = 1
    for r in assets_return:
        compound *= (1+r)
        accumulated.append(compound)
    return accumulated

def accumulated_return_dict(asset_return): # oldest version
    asset_accumulated_return = {}
    for asset in asset_return:
        accumulated = []
        initial = 1
        for r in asset_return[asset]:
            initial *= (1 + r)
            accumulated.append(initial)
        asset_accumulated_return[asset] = accumulated
    return asset_accumulated_return