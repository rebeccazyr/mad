# Jupyter Notebook 使用指南

## 什么是Jupyter Notebook？

Jupyter Notebook是一个交互式的开发环境，特别适合：
- 数据科学和机器学习
- 代码实验和原型开发
- 文档编写和分享
- 教学和学习

## 安装Jupyter Notebook

```bash
# 安装Jupyter Notebook
pip install jupyter notebook

# 或者使用conda
conda install jupyter notebook
```

## 启动Jupyter Notebook

```bash
# 在项目目录下启动
jupyter notebook

# 或者指定端口
jupyter notebook --port=8888
```

启动后会在浏览器中打开Jupyter界面。

## 使用我们创建的Notebook

我已经为你创建了一个完整的notebook文件：`claim_verification_pipeline.ipynb`

### 主要功能：

1. **Evidence检索**：使用ChromaDB检索与claim相关的evidence
2. **Single Agent验证**：快速验证claim
3. **Multi Agent验证**：通过辩论方式进行深度验证
4. **结果可视化**：清晰展示验证结果

### 使用步骤：

1. **启动Jupyter**：
   ```bash
   jupyter notebook
   ```

2. **打开notebook**：
   - 在Jupyter界面中点击 `claim_verification_pipeline.ipynb`

3. **运行代码**：
   - 按顺序运行每个代码单元格（Shift + Enter）
   - 或者点击"Cell" → "Run All"

4. **测试验证**：
   - 在"示例：测试验证流程"单元格中修改test_claim
   - 运行该单元格查看结果

### Notebook结构：

```
1. 导入库和初始化
2. Evidence检索函数
3. Single Agent验证函数
4. Multi Agent验证函数
5. 完整验证流程
6. 示例测试
7. 结果显示
8. 交互式界面
9. 批量验证功能
10. 结果保存功能
```

## 常用操作

### 运行代码单元格：
- `Shift + Enter`：运行当前单元格并移动到下一个
- `Ctrl + Enter`：运行当前单元格但不移动
- `Alt + Enter`：运行当前单元格并在下方插入新单元格

### 编辑模式：
- `Enter`：进入编辑模式
- `Esc`：进入命令模式

### 快捷键：
- `A`：在当前单元格上方插入新单元格
- `B`：在当前单元格下方插入新单元格
- `DD`：删除当前单元格
- `Z`：撤销删除

## 示例使用

```python
# 1. 单个claim验证
claim = "Climate change is a hoax."
result = complete_verification_pipeline(claim)

# 2. 查看结果
print("Single Agent结果:", result["single_agent_result"])
print("Multi Agent最终判决:", result["multi_agent_result"]["final_verdict"])

# 3. 保存结果
save_results(result, "my_verification_result.json")
```

## 故障排除

### 常见问题：

1. **导入错误**：
   - 确保所有依赖包已安装
   - 检查Python路径

2. **ChromaDB连接错误**：
   - 确保ChromaDB服务正在运行
   - 检查vector_name是否正确

3. **Agent模块错误**：
   - 确保agents目录存在
   - 检查模型文件路径

### 调试技巧：

1. 使用print语句调试
2. 检查变量类型和内容
3. 逐步运行代码单元格
4. 查看错误信息

## 扩展功能

你可以根据需要扩展notebook：

1. **添加新的验证方法**
2. **改进结果可视化**
3. **添加更多交互功能**
4. **集成其他数据源**

## 保存和分享

- **保存**：Ctrl + S
- **导出为PDF**：File → Download as → PDF
- **分享**：可以分享.ipynb文件或导出的HTML/PDF

## 最佳实践

1. **定期保存**：经常保存你的工作
2. **清理输出**：删除不必要的输出以保持整洁
3. **添加注释**：为代码添加清晰的注释
4. **模块化**：将复杂功能拆分为函数
5. **错误处理**：添加适当的异常处理

现在你可以开始使用Jupyter Notebook进行claim验证了！ 