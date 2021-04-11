# TODO: diagram (auto?)
class Material:
    """A physical material, as described by its properties and appearance"""
    def __init__(self, name, abbr, elasticity, density, color='', opacity=1, ior=0, softness=1, explosiveness=0, volatility=1):
        """Create a new material; this can be reused over multiple objects"""

        self.name: str = name
        """The name of the material; 'Gold'"""
        self.abbr: str = abbr
        """An abbreviated name for the material; 'Au'"""

        self.elasticity = elasticity
        self.stiffness = self.elasticity
        self.density = density

        self.color = color
        self.opacity = opacity
        self.ior = ior

        self.softness = softness
        self.malleability = self.softness

        self.explosiveness = explosiveness
        """Energy released when the material combusts (based on volatility threshold)"""
        self.volatility = volatility
        """Sensitivity of material to external forces; if this is exceeded, explosion will occur"""
        self.tempThreshold = tempThreshold
