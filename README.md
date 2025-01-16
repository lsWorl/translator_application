# 日语实时翻译器

这是一个基于Python的实时日语翻译工具，可以捕获屏幕指定区域的日文文本，进行OCR识别并翻译成中文。

## 功能特点

- 实时捕获屏幕指定区域
- 支持图像预处理以提高OCR识别率
- 使用Tesseract-OCR进行日文文本识别
- 使用DeepSeek API进行日译中翻译
- 界面始终置顶，方便使用
- 支持图像预处理开关
- 支持清除文本功能

## 安装要求

1. Python 3.7+
2. Tesseract-OCR（需要安装日语语言包）
3. 所需Python包（见requirements.txt）

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/japanese-translator.git
cd japanese-translator
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 安装Tesseract-OCR：
   - Windows: 从[GitHub](https://github.com/UB-Mannheim/tesseract/wiki)下载安装程序
   - 确保安装日语语言包

4. 配置：
   - 复制`config.example.py`为`config.py`
   - 在`config.py`中设置：
     - Tesseract-OCR路径
     - DeepSeek API密钥

## 使用方法

1. 运行程序：
```bash
python translator_app.py
```

2. 使用步骤：
   - 从下拉列表选择目标窗口
   - 点击"选择翻译区域"按钮
   - 使用鼠标框选要翻译的区域
   - 程序会自动开始监控该区域并进行翻译

3. 其他功能：
   - 可以通过复选框开启/关闭图像预处理
   - 使用"清除文本"按钮清空显示区域
   - 使用"刷新窗口列表"更新可选窗口

## 配置说明

在`config.py`中可以配置以下参数：

- `TESSERACT_CMD`: Tesseract-OCR可执行文件路径
- `DEEPSEEK_API_KEY`: DeepSeek API密钥
- OCR相关配置
- 图像处理参数
- UI显示参数

## 注意事项

- 确保有稳定的网络连接以使用翻译API
- 建议使用较新版本的Tesseract-OCR以获得更好的识别效果
- 图像预处理功能可能会影响OCR识别效果，可根据实际情况开启或关闭

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。 