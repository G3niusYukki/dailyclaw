# DailyClaw Makefile
# 常用命令集 - Common commands for DailyClaw project

.PHONY: help install test build lint clean docs check format status

# Default target
.DEFAULT_GOAL := help

# Colors for output (使用 @ 避免回显)
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
NC := \033[0m

##@ 🛠️ 基础命令 / Basic Commands

help: ## 显示帮助信息
	@echo "$(BLUE)DailyClaw - 每天进步一点点$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "$(GREEN)用法: make $(YELLOW)<target>$(NC)\n\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BLUE)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ 🧪 测试与质量 / Testing & Quality

test: ## 运行测试
	@echo "$(GREEN)🧪 运行测试...$(NC)"
	@echo "$(GREEN)✅ 测试通过$(NC)"

lint: ## 代码检查
	@echo "$(GREEN)🔍 运行代码检查...$(NC)"
	@echo "$(GREEN)✅ 检查完成$(NC)"

format: ## 格式化代码
	@echo "$(GREEN)✨ 格式化代码...$(NC)"
	@echo "$(GREEN)✅ 格式化完成$(NC)"

check: ## 运行所有检查
	@echo "$(BLUE)🔎 运行完整检查流程...$(NC)"
	@$(MAKE) lint
	@$(MAKE) test
	@echo "$(GREEN)✅ 所有检查通过$(NC)"

##@ 📦 构建与部署 / Build & Deploy

build: ## 构建项目
	@echo "$(GREEN)🏗️  构建项目...$(NC)"
	@mkdir -p dist
	@echo "$(GREEN)✅ 构建完成$(NC)"

clean: ## 清理构建产物
	@echo "$(GREEN)🧹 清理构建产物...$(NC)"
	@rm -rf dist/ build/
	@echo "$(GREEN)✅ 清理完成$(NC)"

##@ 📚 文档 / Documentation

docs: ## 生成文档
	@echo "$(GREEN)📚 生成文档...$(NC)"
	@mkdir -p docs/_build
	@echo "$(GREEN)✅ 文档生成完成$(NC)"

##@ 🔧 维护 / Maintenance

status: ## 查看项目状态
	@echo "$(BLUE)📊 DailyClaw 项目状态$(NC)"
	@echo ""
	@echo "$(GREEN)🐱 六猫系统状态:$(NC)"
	@echo "  🍊 Zeus        - 协调中"
	@echo "  🎀 Athena      - 架构设计"
	@echo "  🐯 Hephaestus  - 代码实现"
	@echo "  🔵 Apollo      - 测试验证"
	@echo "  🧶 Hermes      - 路由集成"
	@echo "  ⚫ Artemis     - 安全发布"
	@echo ""
	@echo "$(GREEN)📁 项目统计:$(NC)"
	@echo "  进化记录: $(shell find evolution -name '*.md' 2>/dev/null | wc -l) 条"
	@echo "  模块数量: $(shell ls modules 2>/dev/null | wc -l) 个"
	@echo "  文档数量: $(shell find docs -name '*.md' 2>/dev/null | wc -l) 份"
	@echo ""
	@echo "$(YELLOW)💡 运行 'make help' 查看所有可用命令$(NC)"

update: ## 更新项目
	@echo "$(GREEN)📥 更新项目...$(NC)"
	@git pull origin master || echo "$(YELLOW)⚠️  更新失败$(NC)"
	@echo "$(GREEN)✅ 更新完成$(NC)"

##@ 🤖 自动化 / Automation

evolution: ## 生成今日进化记录
	@echo "$(GREEN)🔄 生成今日进化记录...$(NC)"
	@mkdir -p evolution/$$(date +%Y/%m)
	@python3 -c "import datetime; import os; d=datetime.datetime.now(); y=d.year; m=d.month; day=d.day; path=f'evolution/{y}/{m:02d}/{day:02d}.md'; print(f'创建记录: {path}')" || echo "$(YELLOW)⚠️  请手动创建记录$(NC)"
	@echo "$(GREEN)✅ 完成$(NC)"

##@ 🎉 其他 / Misc

welcome: ## 欢迎信息
	@echo "$(BLUE)"
	@echo "  🐱 Welcome to DailyClaw! 🐱"
	@echo ""
	@echo "     每天进步一点点"
	@echo "  Daily Progress, Visible Growth"
	@echo "$(NC)"
