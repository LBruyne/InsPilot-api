prompt_deep_divergence_0 = (
    '我将告诉你一些关于设计某个产品时用户的描述文本（用<>括起来的，两个文本间用逗号隔开），请你为我生成{num}个相关的产品。'
    '每个产品需要满足以下要求：'
    '（1）字数不超过8个字。'
    '（2）不同产品之间尽量有较大的差异性'
    '例如，当设计任务是设计一个运动辅助产品时，可能的产品是：跑步机。'
    '输出要求：产品之间用#隔开，不要有序号或任何其他的文字！' 
    '设计方案：<{input}>'
)

prompt_deep_divergence_1 = (
    '我将告诉你{num}个产品（用<>括起来的，产品之间用#隔开），请你为我生成{num}个相应的使用场景。'
    '场景需要满足以下要求：'
    '（1）不超过8个字。'
    '（2）需要是一个具体的地点，且不同产品的使用场景不能相同。'
    '例如，当设计方案是跑步机时，可能场景是：健身房。'
    '输出要求：只需要输出场景内容，场景之间用#隔开，不要有序号或任何其他的文字！'
    '产品：<{input}>'
)

prompt_deep_divergence_2 = (
    '我将告诉你{num}个场景（用<>括起来的，场景之间用#隔开），请你为我生成{num}个相应的用于stable diffusion的prompt。'
    'stable diffusion是一款利用深度学习的文生图模型，支持通过使用提示词来产生新的图像，描述要包含或省略的元素。'
    '下面我将说明prompt的生成要求：'
    '（1）这里的prompt主要用于描述一个场景，首先需要将场景的内容翻译成英文，作为prompt的一部分。'
    '（2）prompt还需要包括对场景中的细节、场景光线、视角的描述，细节越多越好。'
    '（3）用英语短句来描述。'
    '（4）使用英文半角,做分隔符分隔提示词，每个提示词不要带引号。'
    '（5）prompt中不能带有-和，单词不能重复。'
    '例如，当场景是森林时，可能的提示词是：forest, grass, trees, moss, sunlight, distant, morning, quietness '
    '输出要求：只需要输出提示词的内容，一组提示词之间用#隔开，不要有其他任何的文本，包括对于提示词的解释内容'
    '场景：<{input}>'
)

sd_positive_0 = (
    '((({input}))),'
    'bestquality, ultradetailed, masterpiece, realistic, whitebackground, futuristic, finely detailed, purism, ue 5, a computer rendering, minimalism, octane render, 4k'
)

sd_negative_0 = (
    '(((human, man, girl, boy, hand, people, person))), (worst quality:2), (low quality:2), (normal quality:2), lowres, ((monochrome)), ((grayscale)), cropped, text, jpeg artifacts, signature, watermark, username, sketch, cartoon, drawing, anime, duplicate, blurry, semi-realistic, out of frame, ugly, deformed'
)

sd_options_0 = {
    
}

prompt_deep_divergence_3 = (
    '我将告诉你{num}个产品（用<>括起来的，产品之间用#隔开），请你为我生成{num}个相应的设计提示的概念文本。'
    '每个概念文本需要满足以下要求：'
    '（1）字数在6-15个字之间。'
    '（2）描述的是产品的工作原理和背后的机制，提示应该尽量抽象，不应该包含具体的功能，也不要包含具体的产品类型。'
    '例如，当产品是跑步机时，可能的提示是：通过设备的动力带动人的运动。'
    '输出要求：只需要输出提示的内容，每个概念文本之间用#隔开，不要有序号或任何其他的文字，包括对于提示词的解释内容！'
    '设计方案：<{input}>'
)

prompt_deep_divergence_4 = (
    '我将告诉你{num}个产品（用<>括起来的，产品之间用#隔开），请你为我生成{num}个相应的产品功能表述。'
    '每个产品功能需要满足以下要求：'
    '（1）字数在20-50个字之间。'
    '（2）需要包含产品的功能细节和结构，至少包含3个及以上的功能点，内容尽量丰富。'
    '例如，当设计方案是跳绳时，可能的提示是：一个无绳跳绳，跳绳长度可自由调节，手柄上的球体可以增加负重，以加强燃脂效果。具有计时、计数等功能，可记录每次运动数据。'
    '输出要求：只需要输出产品功能表述的内容，每个内容之间用#隔开，不要有序号或任何其他的文字，包括对于提示词的解释内容！'
    '设计方案：<{input}>'
)