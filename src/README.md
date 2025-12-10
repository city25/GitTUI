# 关于 `tests/src/`

原先测试仓库内维护了一份 `src` 的副本，用于示例或测试。项目已迁移至更标准的测试布局：

- `tests/unit/` — 单元测试（快速、非交互）
- `tests/integration/` — 集成测试（包含交互流，通常跳过或使用 mock）
- `tests/fixtures/cli_app/` — 集成测试使用的示例实现或 fixture

建议逐步迁移或删除 `tests/src/` 中的重复代码，直接从项目根目录的 `src/` 导入实现以避免重复。
