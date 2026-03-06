---
name: xhs-douyin-social-manager
description: Manage Xiaohongshu (小红书) and Douyin (抖音) social publishing workflows end-to-end: content planning, cross-platform rewrite, title/hashtag generation, cover ideas, posting SOP, QA checks, and post-publish tracking. Use when asked to create, optimize, schedule, or operate Xiaohongshu/Douyin posts (图文/短视频), including browser-based publishing assistance.
---

# XHS + Douyin Social Manager

## Output Contract

For every request, produce sections in this order unless user asks otherwise:
1. Goal & audience (1-2 lines)
2. Platform strategy split (XHS vs Douyin)
3. Ready-to-post assets
4. Publish checklist
5. Metrics to track at T+1 / T+3 / T+7

Keep Chinese-first unless user requests another language.

## Platform Baseline (Always Apply)

### 小红书（XHS）
- Style: 真实体验、可执行建议、生活方式表达
- Structure: 强标题 + 痛点/场景开头 + 分点干货 + 结尾互动
- Hashtags: 5-10 个，垂类+场景+人群混合
- Visual: 首图必须单独设计（信息密度高，字少而狠）

### 抖音（Douyin）
- Style: 强钩子、快节奏、口语化
- Structure: 3 秒钩子 -> 冲突/收益 -> 步骤 -> CTA
- Captions: 简短直给，避免长段说明
- Video rhythm: 每 2-4 秒一个信息点或镜头变化

## Rewriting Rules (Cross-platform)

When user gives one source draft and asks both platforms:
- Do not duplicate verbatim.
- Keep same core claim, but adapt tone/structure per platform.
- XHS version should be more searchable and note-like.
- Douyin version should be more spoken and punchy.

Return this bundle:
- XHS: 3 title options + note body + hashtag set + cover text (<=16 chars)
- Douyin: 3 hook options + spoken script + on-screen text beats + caption + topic tags

## Publishing SOP (Browser-assisted)

Use this deterministic checklist whenever helping with manual/browser posting:
1. Confirm account and platform (XHS/Douyin)
2. Confirm asset set is complete (title/script/media/hashtags)
3. Open publish page and verify logged-in state
4. Upload media first, then text, then tags/topic
5. Re-check sensitive words / prohibited claims
6. Preview on mobile-style layout if available
7. Publish or save draft (as user requests)
8. Return a post log summary

Post log format:
- Platform:
- Account:
- Mode: Publish / Draft
- Asset used:
- Publish time:
- URL (if available):
- Notes/issues:

## Compliance & Risk Guardrails

Always avoid:
- Absolute claims ("最", "第一", "保证有效") without evidence
- Medical/financial/legal deterministic advice
- Copyright-risk media with unclear ownership
- Misleading before/after transformations

If content is risky, provide a safer rewrite instead of refusing with no alternative.

## Analytics Mini-Loop

After publishing, suggest one optimization loop:
- T+1 day: CTR/3秒留存/互动率 quick check
- T+3 day: 评论关键词聚类（需求、质疑、价格、效果）
- T+7 day: Decide continue / revise angle / stop

Return 1-2 next experiments (title, hook, cover, CTA, posting time).