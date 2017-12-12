import random, string
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
from django.http import HttpResponse, Http404
import os
import logging
from django.conf import settings

# Get an instance of a logger
logger = logging.getLogger('icetus.shopcart')

# 字体路径
path_font = os.path.join(settings.BASE_DIR,'shopcart/static/admin/default/fonts/Arial.ttf')
# 随机生成字符
def getRandomChar():
    # string模块包含各种字符串，以下为小写字母加数字
    ran = string.ascii_lowercase + string.digits
    char = ''
    for i in range(4):
        char += random.choice(ran)
    return char


# 返回一个随机的RGB颜色
def getRandomColor():
    return (random.randint(0, 0), random.randint(0, 0), random.randint(0, 0))


def create_code():
    logger.info('构建图片')
    # 构建图片，模式，大小，背景色
    img = Image.new('RGB', (120, 30), (255, 255, 255))
    # 创建画布
    draw = ImageDraw.Draw(img)
    # 设置字体
    font = ImageFont.truetype(path_font, 25)
    code = getRandomChar()

    # 将生成的字符画在画布上
    for t in range(4):
        draw.text((30 * t + 5, 0), code[t], getRandomColor(), font)

    # 生成干扰点
    for _ in range(random.randint(0, 50)):
        # 位置，颜色
        draw.point((random.randint(0, 120), random.randint(0, 30)), fill=getRandomColor())
    # 使用模糊滤镜使图片模糊
    img = img.filter(ImageFilter.FIND_EDGES)
    # 保存
    logger.info(code)
    # img.save(''.join(code) + '.jpg', 'jpeg')
    return img, code



# 在内存中开辟空间用以生成临时的图片
def create_code_img(request):
    f = BytesIO()
    img, code = create_code()
    request.session['check_code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())


from django.shortcuts import render_to_response, render


def test_code(request):
    # GET方法返回表单
    if request.method == 'GET':
        logger.info('进入页面')
        return render(request, 'client/cassie/test_code.html')
    # post方法验证提交的验证码是否正确
    else:
        code = request.POST.get('code', '')
        if code == request.session.get('check_code', 'error'):
            return HttpResponse('Yes')
        return HttpResponse('No')
