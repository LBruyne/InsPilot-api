class DesignCreative:
    RapidAbstract = 0
    RapidConcrete = 1
    Deep = 2
    ConvergenceGroupOne = 3
    ConvergenceGroupTwo = 4

    Sequence = "sequence"
    Direct = "direct"

    def __init__(self, creative_type, display_type):
        self.creative_type = creative_type
        self.display_type = display_type
        self.items = []

    @classmethod
    def from_rapid_divergence(cls, images: [], texts: []):
        creatives = []
        for i in range(len(images)):
            creative = cls(cls.RapidAbstract, cls.Sequence)
            creative.items.append(DesignCreativeItem(item_type=DesignCreativeItem.AbstractImage, image=images[i]))
            creative.items.append(DesignCreativeItem(item_type=DesignCreativeItem.AbstractText, text=texts[i]))
            creatives.append(creative)
        return creatives

    @classmethod
    def from_deep_divergence(cls, images: [], a_texts: [], c_texts: []):
        creatives = []
        for i in range(len(images)):
            creative = cls(cls.Deep, cls.Sequence)
            creative.items.append(DesignCreativeItem(item_type=DesignCreativeItem.AbstractImage, image=images[i]))
            creative.items.append(DesignCreativeItem(item_type=DesignCreativeItem.AbstractText, text=a_texts[i]))
            creative.items.append(DesignCreativeItem(item_type=DesignCreativeItem.ConcreteText, text=c_texts[i]))
            creatives.append(creative)
        return creatives

    # @classmethod
    # def from_convergence_1(cls, c_images: [], a_images: [], c_texts: []):
    #     creative = cls(cls.ConvergenceGroupOne, cls.Direct)
    #     for i in range(len(c_images)):
    #         creative.items.append(
    #             DesignCreativeItem(
    #                 item_type=DesignCreativeItem.GroupTypeOne,
    #                 combinations=[
    #                     DesignCreativeItem(item_type=DesignCreativeItem.AbstractImage, image=a_images[i]),
    #                     DesignCreativeItem(item_type=DesignCreativeItem.ConcreteImage, image=c_images[i]),
    #                     DesignCreativeItem(item_type=DesignCreativeItem.ConcreteText, text=c_texts[i]),
    #                 ]
    #             )
    #         )
    #     return creative

    @classmethod
    def from_convergence_2(cls, c_images: [], a_images: [], c_texts: []):
        creatives = []
        for i in range(len(c_images)):
            creative = cls(cls.ConvergenceGroupTwo, cls.Direct)
            creative.items.append(DesignCreativeItem(
                item_type=DesignCreativeItem.GroupTypeTwo,
                combinations=[
                    DesignCreativeItem(item_type=DesignCreativeItem.AbstractImage, image=a_images[i]),
                    DesignCreativeItem(item_type=DesignCreativeItem.ConcreteImage, image=c_images[i]),
                    DesignCreativeItem(item_type=DesignCreativeItem.ConcreteText, text=c_texts[i]),
                ]
            ))
            creatives.append(creative)
        return creatives

    @staticmethod
    def array_to_dict(creatives):
        return [creative.to_dict() for creative in creatives]

    def to_dict(self):
        return {
            'type': self.creative_type,
            'displayType': self.display_type,
            'items': [item.to_dict() for item in self.items],
        }


class DesignCreativeItem:
    AbstractText = "abstractText"
    ConcreteText = "concreteText"
    AbstractImage = "abstractImage"
    ConcreteImage = "concreteImage"
    GroupTypeOne = "groupTypeOne"
    GroupTypeTwo = "groupTypeTwo"

    def __init__(self, item_type=None, text=None, image=None, combinations=None):
        self.item_type = item_type
        self.text = text
        self.image = image
        self.combinations = combinations

    def to_dict(self):
        return {
            'type': self.item_type,
            'text': self.text,
            'image': self.image,
            'combinations': [combo.to_dict() for combo in self.combinations] if self.combinations else None,
        }
