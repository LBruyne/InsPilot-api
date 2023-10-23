prompt_convergence_0 = (
    '接下来我会给你若干个关于设计某个产品的方案描述（整体用<>符号包围，描述之间用#隔开，一个描述可能由多个短句组成，短句之间用逗号隔开），请你挑选出三个最具新颖性和实用性的方案。'
    '其中，新颖性指的是一个产品想法与已有产品相比出现的创新和不寻常的特性，如果一个产品是常见的，则它是不新颖的；实用性是由 重要程度、使用普及程度、使用频率 '
    '三个指标共同确定的，重要程度是指该产品在提升运动的体验或安全性方面的不可或缺程度，使用普及程度是指该产品在某一类运动爱好者中普及的广泛程度，即有多少比例的运动爱好者会使用该产品，使用频率是指使用该产品的频繁程度）'
    '例如，在以下方案中，2,5,6是新颖性和实用性最高的：'
    '可折叠收纳的跑步机#可以拉伸缩放、容易固定的瑜伽垫#充气式游泳浮漂#带海绵结构的跳舞杆#拉伸时的娱乐装置，让拉伸变得有趣#智能运动镜，可以识别运动姿态、实时反馈矫正'
    '根据我的例子，在下面的<>中的方案选择三个最新颖，实用的方案。输出格式：方案之间用#隔开，不要有序号或任何其他的文字！'
    '设计方案：<{input}>'
)

prompt_convergence_1 = (
    '我将告诉你{num}个产品的设计方案（用<>括起来的，方案之间用#隔开），请你为我生成{num}个相应的使用场景。'
    '场景需要满足以下要求：'
    '（1）不超过8个字。'
    '（2）需要是一个具体的地点，且不同产品的使用场景不能相同。'
    '例如，当设计方案是跑步机时，可能场景是：健身房。'
    '输出要求：只需要输出场景内容，场景之间用#隔开，不要有序号或任何其他的文字！'
    '产品：<{input}>'
)

prompt_convergence_2 = (
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
    '(photorealistic:1.5),bestquality,ultradetailed,masterpiece,realistic,finely detailed,purism,minimalism,4k'
)

sd_negative_0 = (
    '(worst quality:1.4),people,man,woman,flame,Cloud,(low quality:1.4),(normal quality:1.5),lowres,((monochrome)),((grayscale)),cropped,text,jpeg,artifacts,signature,watermark,username,sketch,cartoon,drawing,anime,duplicate,blurry,semi-realistic,out of frame,ugly,deformed,weird colors,EasyNegative,flame'
)

sd_options_0 = {
    
}

prompt_convergence_3 = (
    '我将告诉你{num}个产品设计方案（用<>括起来的，产品之间用#隔开），请你为我生成{num}个相应的产品功能表述。'
    '每个产品功能需要满足以下要求：'
    '（1）字数在20-50个字之间。'
    '（2）需要包含产品的功能细节和结构，至少包含3个及以上的功能点，内容尽量丰富。'
    '例如，当设计方案是跳绳时，可能的提示是：一个无绳跳绳，跳绳长度可自由调节，手柄上的球体可以增加负重，以加强燃脂效果。具有计时、计数等功能，可记录每次运动数据。'
    '输出要求：只需要输出产品功能表述的内容，每个内容之间用#隔开，不要有序号或任何其他的文字，包括对于提示词的解释内容！'
    '设计方案：<{input}>'
)

prompt_convergence_4 = (
    '我将告诉你{num}个产品设计方案（用<>括起来的，产品之间用#隔开），请你为我生成{num}个相应的用于stable diffusion的prompt。stable '
    'diffusion是一款利用深度学习的文生图模型，支持通过使用提示词来产生新的图像，描述要包含或省略的元素。我在这里引入stable diffusion算法中的prompt概念，又被称为提示符。'
    '下面我将说明prompt的生成要求：'
    '（1）这里的prompt主要用于描述一个场景，首先需要将场景的内容翻译成英文，作为prompt的一部分。'
    '（2）prompt需要包括对物品外观、材质、形状、结构、光线的描述，细节越多越好。'
    '（3）用英语短句来描述。'
    '（4）使用英文半角,做分隔符分隔提示词，每个提示词不要带引号。'
    '（5）prompt中不能带有-和，单词不能重复。'
    '例如，当产品是跑步机时，可能的提示词是：treadmill, technical sense, metal material, dark color, touch screen, soft light'
    '输出要求：只需要输出提示词的内容，一组提示词之间用#隔开，不要有其他任何的文本，包括对于提示词的解释内容'
    '设计方案：<{input}>'
)

sd_positive_1 = (
    '((({input}))),'
    '(white background:1.5),Actual product pictures,(Product Design:1.3),intelligent,industrial products,Creative,Industrial Products,sense of future,complete view,High Quality,minimalistic futuristic design,emauromin style,finely detailed,64k,blender,purism,ue 5,minimalism,photorealistic'
)

sd_negative_1 = (
    '(worst quality:1.4),Nothing in the background,people, man, woman, flame,Cloud,(low quality:1.4),(normal quality:1.5),lowres,((monochrome)),((grayscale)),cropped,text,jpeg,artifacts,signature,watermark,username,sketch,cartoon,drawing,anime,duplicate,blurry,semi-realistic,out of frame,ugly,deformed,weird colors,EasyNegative,flame,'
)

sd_options_1 = {
    
}
