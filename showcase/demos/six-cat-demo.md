# 🐱 六猫协作系统演示

## 演示场景：用户请求开发新功能

### 用户输入
> "帮我做一个自动抓取网页数据的工具"

### 六猫协作流程

```
🍊 Zeus (橘猫 - 主协调)
└── 拆解任务：架构设计 → 代码实现 → 测试验证
    ├── > 🎀 Athena (布偶猫) 设计架构
    ├── > 🐯 Hephaestus (狸花猫) 编写代码
    └── > 🔵 Apollo (暹罗猫) 测试验证
```

### 步骤 1: Athena 架构设计

<!-- 在 #🎀-architecture-雅典娜 频道 -->

🎀 **Athena** · 布偶猫

**架构建议**：
- 使用 Playwright 进行浏览器自动化
- 设计配置驱动的抓取规则
- 输出 JSON/CSV 格式

**接口设计**：
```typescript
interface ScraperConfig {
  url: string;
  selectors: Record<string, string>;
  output: 'json' | 'csv';
}
```

---

### 步骤 2: Hephaestus 代码实现

<!-- 在 #🐯-coding-赫菲斯托斯 频道 -->

🐯 **Hephaestus** · 狸花猫

**实现代码**：
```python
from playwright.sync_api import sync_playwright
import json
import csv

class WebScraper:
    def __init__(self, config):
        self.config = config
    
    def scrape(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(self.config['url'])
            
            results = {}
            for key, selector in self.config['selectors'].items():
                results[key] = page.query_selector(selector).inner_text()
            
            browser.close()
            return results
```

---

### 步骤 3: Apollo 测试验证

<!-- 在 #🔵-testing-阿波罗 频道 -->

🔵 **Apollo** · 暹罗猫

**测试用例**：
```python
def test_scraper():
    config = {
        'url': 'https://example.com',
        'selectors': {'title': 'h1'}
    }
    scraper = WebScraper(config)
    result = scraper.scrape()
    assert 'title' in result
```

✅ **测试通过** - 功能正常

---

### 步骤 4: Zeus 汇总汇报

🍊 **Zeus** · 橘猫

**任务完成**！

已交付：
- ✅ 架构设计文档
- ✅ 可运行代码
- ✅ 测试用例

使用方法：
```bash
python scraper.py --config config.json
```

---

## 协作效率数据

| 阶段 | 耗时 | 负责猫 |
|------|------|--------|
| 架构设计 | 2 min | 🎀 Athena |
| 代码实现 | 5 min | 🐯 Hephaestus |
| 测试验证 | 2 min | 🔵 Apollo |
| **总计** | **9 min** | 六猫协作 |

---

*这是 DailyClaw 六猫协作系统的真实演示案例*
