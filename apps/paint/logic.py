from apps.utils import BusinessException, BUSINESS_FAIL
from apps.paint.creatives import DesignCreative
from agent.sd import sd_pool
from agent.gpt import gpt_pool

from settings import rapid_divergence, deep_divergence, convergence_1, convergence_2

from concurrent.futures import ThreadPoolExecutor

from pymongo import MongoClient
import config

mongo_client = MongoClient(config.MONGO_HOST)
mongo_db = mongo_client[config.MONGO_DB]
mongo_users_collection = mongo_db['users']

def parse_generated(generated_text):
    return generated_text.strip().split('#')

def generate_prompts(template: str, **input): 
    return template.format(**input)

def rapid_divergence_stimulus(prompts):
    try:
        task = prompts.get('task')
        if not task:
            raise BusinessException(BUSINESS_FAIL, '设计任务缺失')
        num = prompts.get('num')
        if not num:
            raise BusinessException(BUSINESS_FAIL, '设计数量缺失')

        # Step 1: 产品
        gpt_task = {"messages": generate_prompts(rapid_divergence.prompt_rapid_divergence_0, input=task, num=num)}
        products = gpt_pool.chat(gpt_task)['text']
        print(products)

        # Step 2: 场景
        gpt_task = {"messages": generate_prompts(rapid_divergence.prompt_rapid_divergence_1, input=products, num=num)}
        scenes = gpt_pool.chat(gpt_task)['text']
        print(scenes)

        # Step 3: SD 提示
        gpt_task = {"messages": generate_prompts(rapid_divergence.prompt_rapid_divergence_2, input=scenes, num=num)}
        sd_prompts = gpt_pool.chat(gpt_task)['text']

        # Step 4: 并行生成 SD 图片
        sd_tasks = []
        for idx, prompt in enumerate(parse_generated(sd_prompts)):
            if prompt == '':
                continue

            task = {'index': idx, 'prompt': generate_prompts(rapid_divergence.sd_positive_0, input=prompt),
                    'task_type': "abstract_image",
                    'negative_prompt': rapid_divergence.sd_negative_0, 'options': rapid_divergence.sd_options_0}
            sd_tasks.append(task)
            
            # dall-e-3的调用
            # task = {'index': idx, 'prompt': generate_prompts(rapid_divergence.sd_positive_0, input=prompt),
            #         'task_type': "abstract_image"}
            # sd_tasks.append(task)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(sd_pool.text2Image, task) for task in sd_tasks]
            images = [future.result() for future in futures]
            
            # dall-e-3的调用
            # futures = [executor.submit(gpt_pool.text2Image, task) for task in sd_tasks]
            # images = [future.result() for future in futures]          

        # Step 5: 抽象文本
        gpt_task = {"messages": generate_prompts(rapid_divergence.prompt_rapid_divergence_3, input=products, num=num)}
        abstracts = gpt_pool.chat(gpt_task)['text']
        print(abstracts)
        abstract_texts = parse_generated(abstracts)

        if len(images) != len(abstract_texts):
            raise BusinessException(BUSINESS_FAIL, '生成目标数量不一致')

        result = DesignCreative.array_to_dict(DesignCreative.from_rapid_divergence(images=[images[i]['image'] for i in range(len(images))], texts=abstract_texts))

        return {
            "count": len(result),
            "result": result
        }
    except BusinessException as be:
        raise be
    except Exception as e:
        raise e


def deep_divergence_stimulus(prompts):
    generate_num = 3
    try:
        texts = prompts.get('designTexts')
        if not texts or not isinstance(texts, list) or len(texts) == 0:
            raise BusinessException(BUSINESS_FAIL, '设计文本缺失')
        scheme_id = prompts.get('schemeId')
        if scheme_id is None:
            raise BusinessException(BUSINESS_FAIL, '关联方案缺失')
        image = prompts.get('designImage')
        if image is None:
            raise BusinessException(BUSINESS_FAIL, '设计图片缺失')

        texts = ','.join(texts)
        # Step 1: 产品
        gpt_task = {"messages": generate_prompts(deep_divergence.prompt_deep_divergence_0, input=texts, num=generate_num)}
        products = gpt_pool.chat(gpt_task)['text']
        print(products)

        # Step 2: 场景
        gpt_task = {"messages": generate_prompts(deep_divergence.prompt_deep_divergence_1, input=products, num=generate_num)}
        scenes = gpt_pool.chat(gpt_task)['text']
        print(scenes)

        # Step 3: SD 提示
        gpt_task = {"messages": generate_prompts(deep_divergence.prompt_deep_divergence_2, input=scenes, num=generate_num)}
        sd_prompts = gpt_pool.chat(gpt_task)['text']

        # Step 4: 图片
        sd_tasks = []
        for idx, prompt in enumerate(parse_generated(sd_prompts)):
            if prompt == '':
                continue

            task = {'index': idx, 'prompt': generate_prompts(deep_divergence.sd_positive_0, input=prompt),
                    'task_type': "abstract_image",
                    'negative_prompt': deep_divergence.sd_negative_0, 'options': deep_divergence.sd_options_0}
            sd_tasks.append(task)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(sd_pool.text2Image, task) for task in sd_tasks]
            images = [future.result() for future in futures]

        # Step 5: 抽象文本
        gpt_task = {"messages": generate_prompts(deep_divergence.prompt_deep_divergence_3, input=products, num=generate_num)}
        abstracts = gpt_pool.chat(gpt_task)['text']
        print(abstracts)
        abstract_texts = parse_generated(abstracts)

        # Step 6: 具体文本
        gpt_task = {"messages": generate_prompts(deep_divergence.prompt_deep_divergence_4, input=products, num=generate_num)}
        concretes = gpt_pool.chat(gpt_task)['text']
        print(concretes)
        concrete_texts = parse_generated(concretes)

        if len(images) != len(abstract_texts) or len(abstract_texts) != len(concrete_texts):
            raise BusinessException(BUSINESS_FAIL, '生成目标数量不一致')

        result = DesignCreative.array_to_dict(
            DesignCreative.from_deep_divergence(images=[images[i]['image'] for i in range(len(images))], a_texts=abstract_texts, c_texts=concrete_texts))

        return {
            "schemeId": scheme_id,
            "count": len(result),
            "result": result
        }
    except BusinessException as be:
        raise be
    except Exception as e:
        raise e


def convergence_1_stimulus(prompts):
    try:
        designTask = prompts.get('designTask')
        if not designTask:
            raise BusinessException(BUSINESS_FAIL, '方案描述缺失')
        
        schemes = prompts.get('schemes')
        if not schemes or not isinstance(schemes, list) or len(schemes) == 0:
            raise BusinessException(BUSINESS_FAIL, '设计方案缺失')

        schemes_design_texts = [",".join(scheme.get('designTexts')) for scheme in schemes]
        schemes_images = [scheme.get('designImage') for scheme in schemes]
        # 一共方案数
        schemes_num = len(schemes_design_texts)
        # 选择数
        select_num = int(prompts.get('selectNum'))
        
        # Step 1: 方案名
        def generate_description(input):
            res = ""
            for i, text in enumerate(input, start=1):
                res += f"第{i}张图：{text}"
                if i != len(input):
                    res += "，"
            return res
        description = generate_description(schemes_design_texts)
        gpt_task = {"prompt": generate_prompts(convergence_1.prompt_convergence_0, task=designTask, input=description),
                    "images": schemes_images}
        names = gpt_pool.ask_image(gpt_task)['text']
        print(names)
        parsed_names = parse_generated(names)
        
        if len(parsed_names) != len(schemes_design_texts):
            raise BusinessException(BUSINESS_FAIL, '生成目标数量不一致')

        packed_schemes = [name + ":" + texts for (name, texts) in zip(parsed_names, schemes_design_texts)]
        packed_schemes_as_input = "#".join(packed_schemes)

        if schemes_num < select_num:
            select_num = schemes_num

        # Step 2: 最佳方案
        gpt_task = {"messages": generate_prompts(convergence_1.prompt_convergence_1, input=packed_schemes_as_input, select_num=select_num, num=schemes_num)}
        selected = gpt_pool.chat(gpt_task)['text']
        print(selected)
        parsed_selected = parse_generated(selected)
        
        return {
            "names": parsed_names,
            "selected": parsed_selected
        }
    except BusinessException as be:
        raise be
    except Exception as e:
        raise e


def convergence_2_stimulus(prompts):
    try:
        schemes = prompts.get('selectedSchemes')
        if not schemes or not isinstance(schemes, list) or len(schemes) == 0:
            raise BusinessException(BUSINESS_FAIL, '设计方案缺失')

        schemes_design_texts = [",".join(scheme.get('designTexts')) for scheme in schemes]
        generate_num = int(prompts.get('num'))
        product_generate_num = len(schemes_design_texts) * generate_num

        # Step 1: 场景
        gpt_task = {"messages": generate_prompts(convergence_2.prompt_convergence_0, input_num=len(schemes_design_texts), num=generate_num, input=schemes_design_texts, total_num=product_generate_num)}
        scenes = gpt_pool.chat(gpt_task)['text']
        print(scenes)

        # Step 2: 场景提示
        gpt_task = {"messages": generate_prompts(convergence_2.prompt_convergence_1, input=scenes, num=product_generate_num)}
        sd_prompts = gpt_pool.chat(gpt_task)['text']
        
        # Step 3: 具体文本
        gpt_task = {"messages": generate_prompts(convergence_2.prompt_convergence_2, input_num=len(schemes_design_texts), num=generate_num, input=schemes_design_texts, total_num=product_generate_num)}
        concretes = gpt_pool.chat(gpt_task)['text']
        print(concretes)
        concrete_texts = parse_generated(concretes)

        # Step 4: 产品图提示
        gpt_task = {"messages": generate_prompts(convergence_2.prompt_convergence_3, input=concretes, num=product_generate_num)}
        sd_prompts_2 = gpt_pool.chat(gpt_task)['text']
    
        # Step 5: 场景和产品图
        all_tasks = []
        for idx, prompt in enumerate(parse_generated(sd_prompts)):
            if prompt == '':
                continue

            task = {
                'index': idx, 
                'prompt': generate_prompts(convergence_2.sd_positive_0, input=prompt),
                'negative_prompt': convergence_2.sd_negative_0, 
                'options': convergence_2.sd_options_0, 
                'task_type': 'abstract_image'
            }
            all_tasks.append(task)
            
        for idx, prompt in enumerate(parse_generated(sd_prompts_2)):
            if prompt == '':
                continue
            task = {
                'index': idx,
                'prompt': generate_prompts(convergence_2.sd_positive_1, input=prompt),
                'negative_prompt': convergence_2.sd_negative_1,
                'options': convergence_2.sd_options_1,
                'task_type': 'concrete_image'
            }
            all_tasks.append(task)

        # 一次性提交所有任务
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(sd_pool.text2Image, task) for task in all_tasks]
            results = [future.result() for future in futures]

        abstract_images = [None] * (len(results) // 2)
        concrete_images = [None] * (len(results) // 2)
        for result in results:
            if result["type"] == "abstract_image":
                abstract_images[result["index"]] = result["image"]
            elif result["type"] == "concrete_image":
                concrete_images[result["index"]] = result["image"]

        if len(concrete_images) != len(abstract_images) or len(abstract_images) != len(concrete_texts):
            raise BusinessException(BUSINESS_FAIL, '生成目标数量不一致')

        result = DesignCreative.array_to_dict(
            DesignCreative.from_convergence_2(a_images=abstract_images, c_images=concrete_images,
                                              c_texts=concrete_texts))

        return {
            "result": result
        }
    except BusinessException as be:
        raise be
    except Exception as e:
        raise e


def start(username: str):
    try:
        if username == '':
            raise BusinessException(BUSINESS_FAIL, '用户名字为空')
        user = mongo_users_collection.find_one({"username": username})
        if user is None:
            # 用户不存在，创建新文档
            user_data = {
                "username": username,
                "currentStage": "准备",
                "designTask": "",
                "rapidDivergenceSchemes": [],
                "deepDivergenceSchemes": [],
                "convergenceSchemes": []
            }
            mongo_users_collection.insert_one(user_data)
            return {**user_data, "_id": str(user_data["_id"])}
        else:
            return {**user, "_id": str(user["_id"])}
    except BusinessException as be:
        raise be
    except Exception as e:
        raise e

def save(username: str, data):
    try:
        if username is None or data is None:
            raise BusinessException(BUSINESS_FAIL, '用户名字或数据为空')
        
        to_update = {
            "rapidDivergenceSchemes": data['designSchemes']['快速发散'],
            "deepDivergenceSchemes": data['designSchemes']['深入发散'],
            "convergenceSchemes": data['designSchemes']['收敛'],
            "designTask": data['designTask'],
            "currentStage": data['currentStage']
        }
        
        update_result = mongo_users_collection.update_one(
            {"username": username},
            {"$set": to_update}
        )
        
        print(update_result.matched_count)

        if update_result.matched_count == 0:
            raise BusinessException(BUSINESS_FAIL, '用户不存在')
    except BusinessException as be:
        raise be
    except Exception as e:
        raise e
