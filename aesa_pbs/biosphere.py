import bw2data as bd

def get_biosphere_database():
    ERROR = "AESA methods work with ecoinvent biosphere flows only. Install base ecoinvent data."
    assert "biosphere3" in bd.databases, ERROR
    return list(bd.Database("biosphere3"))