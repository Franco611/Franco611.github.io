# GTF File Processor

This tool processes GTF (Gene Transfer Format) files by extracting the `gene_id` value from column 9 and appending a `gene_name` attribute with the same value to the end of column 9.

## 问题描述 (Problem Description)

对于GTF文件，需要把整个文件中第九列的 `gene_id "evm.TU.Chr01.1";` 复制到这一行的末尾，并且把 `gene_id` 改成 `gene_name`。

For GTF files, we need to copy the `gene_id "evm.TU.Chr01.1";` from column 9 to the end of that line, and change `gene_id` to `gene_name`.

## 使用方法 (Usage)

### 基本用法 (Basic Usage)

```bash
python3 process_gtf.py input.gtf output.gtf
```

### 选项 (Options)

```bash
# 跳过已有 gene_name 的行 (Skip lines that already have gene_name)
python3 process_gtf.py input.gtf output.gtf --skip-if-exists
```

### 参数说明 (Parameters)

- `input.gtf`: 输入的GTF文件路径 (Input GTF file path)
- `output.gtf`: 输出的GTF文件路径 (Output GTF file path)
- `--skip-if-exists`: 可选参数，如果属性中已存在 gene_name，则跳过该行 (Optional flag to skip adding gene_name if it already exists)

### 示例 (Example)

```bash
# 处理示例文件
python3 process_gtf.py sample_input.gtf sample_output.gtf
```

## 输入示例 (Input Example)

```
Chr01	EVM	gene	215447	215758	.	-	.	gene_id "evm.TU.Chr01.1"; ID "evm.TU.Chr01.1";
Chr01	EVM	mRNA	215447	215758	.	-	.	gene_id "evm.TU.Chr01.1"; transcript_id "evm.model.Chr01.1";
```

## 输出示例 (Output Example)

```
Chr01	EVM	gene	215447	215758	.	-	.	gene_id "evm.TU.Chr01.1"; ID "evm.TU.Chr01.1"; gene_name "evm.TU.Chr01.1";
Chr01	EVM	mRNA	215447	215758	.	-	.	gene_id "evm.TU.Chr01.1"; transcript_id "evm.model.Chr01.1"; gene_name "evm.TU.Chr01.1";
```

## 功能特点 (Features)

1. 自动提取每行第9列中的 `gene_id` 值 (Automatically extracts `gene_id` value from column 9)
2. 在第9列末尾添加 `gene_name` 属性 (Appends `gene_name` attribute to the end of column 9)
3. 支持跳过已有 `gene_name` 的行 (Supports skipping lines that already have `gene_name`)
4. 保持GTF文件格式完整性 (Maintains GTF file format integrity)
5. 处理空行和注释行 (Handles empty lines and comments)

## 要求 (Requirements)

- Python 3.x
- 无需额外依赖包 (No additional packages required)

## 文件说明 (File Description)

- `process_gtf.py`: 主处理脚本 (Main processing script)
- `sample_input.gtf`: 示例输入文件 (Sample input file)
- `sample_output.gtf`: 示例输出文件 (Sample output file)

## 注意事项 (Notes)

- 该脚本会读取整个输入文件并创建新的输出文件 (The script reads the entire input file and creates a new output file)
- 原始文件不会被修改 (The original file will not be modified)
- 如果输出文件已存在，将被覆盖 (If the output file exists, it will be overwritten)
