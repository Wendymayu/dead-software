# 单体架构进阶：WordPress

## 软件简介

WordPress 是全球使用最广泛的 CMS（内容管理系统），驱动着超过 40% 的网站。它从诞生之初就是典型的单体应用——所有功能（路由、数据库、认证、模板、内容管理）在一个代码库中。但它通过独特的钩子(Hook)机制实现了单体内部的扩展性，使得庞大的插件生态得以繁荣。

## 该软件的架构

WordPress 的单体架构与钩子系统：

1. **单体结构**：所有核心功能在同一个代码库
   - `wp-includes/`：核心函数库（数据库、HTTP、模板等）
   - `wp-admin/`：后台管理界面
   - `wp-content/`：用户可扩展区域（插件、主题）
   - 入口文件 `wp-load.php` 加载整个系统

2. **钩子(Hook)机制**：单体内部的扩展点
   - **Action（动作钩子）**：在特定事件发生时执行额外逻辑
     - `do_action('init')` — 系统初始化时
     - `do_action('publish_post')` — 文章发布时
     - `add_action('publish_post', 'notify_author')` — 注册回调
   - **Filter（过滤器钩子）**：修改数据流转中的值
     - `apply_filters('the_content', $content)` — 修改文章内容
     - `add_filter('the_content', 'add_seo_meta')` — 注册修改函数
   - 钩子是 WordPress 插件系统的根基

3. **插件(Plugin)**：通过钩子扩展的单体组件
   - 每个插件注册自己需要的 Action 和 Filter
   - 插件不修改核心代码，只通过钩子"挂入"
   - 数万个插件构成 WordPress 的生态优势

4. **为什么单体仍然成功**：
   - 大多数 WordPress 站点流量不高，单体性能足够
   - 钩子机制让扩展不需要改核心代码
   - 简单部署：一个 `wp-content/` 目录就能迁移整个站点

## 简化实现思路

我们的简化代码模拟了 WordPress 的单体+钩子机制：

- `WordPressApp` → 模拟 WordPress 核心：路由+认证+内容+模板+钩子 全在一个类
- `add_action()` / `add_filter()` → 模拟 WordPress 的 `add_action()` / `add_filter()`
- `_do_action()` → 模拟 `do_action()`，触发动作钩子
- `_apply_filters()` → 模拟 `apply_filters()`，依次应用过滤器
- 插件函数 → 模拟 WordPress 插件：注册钩子回调来扩展功能

关键对比：单体内部没有服务边界，但钩子系统提供了"柔性边界"——不改核心代码就能扩展。

## 与真实实现的对照

| 简化代码 | 真实 WordPress | 说明 |
|---------|---------------|------|
| `WordPressApp` 单个类 | WordPress核心代码库 | 真实WP核心是数千文件，但逻辑确实在同一个代码库中 |
| `add_action / add_filter` | WP的 `add_action / add_filter` | 机制完全一致：注册钩子回调 |
| `_do_action / _apply_filters` | WP的 `do_action / apply_filters` | 机制完全一致：触发钩子并执行回调 |
| 函数作为插件 | Plugin PHP文件 | 真实插件是独立PHP文件，通过钩子注册函数 |
| 字典模拟数据库 | MySQL + wpdb | 真实WP用MySQL，通过 `$wpdb` 全局对象操作 |
| `_authenticate()` | WP的 `wp_authenticate()` | 真实认证涉及cookie、session、nonce等复杂机制 |
| `_render()` 模板 | WP Template Hierarchy | 真实WP有完整的模板层级系统（single.php、archive.php等） |
| `route()` | WP的 `wp-parse-request` | 真实WP的URL路由基于重写规则(rewrite rules) |

## 学习建议

1. **理解"钩子=柔性边界"**：单体没有硬性服务边界，但钩子系统提供了扩展的"接口"——这是 WordPress 生态繁荣的根本原因
2. **对比 Action vs Filter**：Action 是"做额外的事"（通知、日志），Filter 是"修改数据"（内容、配置）——理解两者的语义差异
3. **思考单体的代价**：所有代码在一起 → 部署简单但扩展受限 → WordPress 的高流量场景需要缓存层（Varnish、Redis）来弥补
4. **动手实践**：安装 WordPress，写一个最简单的插件（注册 `add_action` 或 `add_filter`），观察钩子如何工作
5. **架构反思**：WordPress 证明"单体 + 好的扩展机制"可以成功——不是所有系统都需要微服务，关键看业务需求
